from collections import OrderedDict
import onnxruntime
import numpy as np
import math
from skimage import measure
from skimage.segmentation import watershed
import cv2
import matplotlib.patheffects as patheffects
from functools import reduce
import operator
from itertools import groupby
from matplotlib.patches import Rectangle
from matplotlib import pyplot as plt
import requests
from tqdm import tqdm

INTER = cv2.INTER_LINEAR


def download_model(url, filepath):
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024
        with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
            with open(filepath, "wb") as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)

        if total_size != 0 and progress_bar.n != total_size:
            raise RuntimeError("Could not download file")
    except:
        raise RuntimeError("Could not download file")

def load_vocab(vocab_file):
    vocab = OrderedDict()
    with open(vocab_file, "r", encoding="utf-8") as reader:
        pairs = reader.readlines()

    for index, pair in enumerate(pairs):
        pair = pair.rstrip("\n")
        vocab[pair] = index
    return vocab

class OnnxModel:
    def __init__(self, model_path, force_onnx_cpu=False):
        opts = onnxruntime.SessionOptions()
        #opts.inter_op_num_threads = 1
        #opts.intra_op_num_threads = 1

        if force_onnx_cpu and 'CPUExecutionProvider' in onnxruntime.get_available_providers():
            self.ort_session = onnxruntime.InferenceSession(model_path, providers=['CPUExecutionProvider'], sess_options=opts)
        else:
            self.ort_session = onnxruntime.InferenceSession(model_path, sess_options=opts)

    def __call__(self, input):
        if isinstance(input, dict):
            ort_inputs = {i: x for i, x in input.items()}
        else:
            ort_inputs = {'input': input}
        output = self.ort_session.run(None, ort_inputs)

        if len(output) > 1:
            output = [x for x in output]
        else:
            output = output[0]

        return output
    

class GreedyCTCDecoder():
    def __init__(self, labels, blank=0):
        super().__init__()
        self.labels = labels
        self.blank = blank

    def __call__(self, emission, drop_duplicates=True) -> str:
        batch = len(emission.shape) == 3
        if batch:
            emission = emission.transpose((1, 0, 2))
        else:
            emission = emission[None, :, :]

        indices = np.argmax(emission, axis=-1)  # [num_seq,]        
        result = []
        for ind in range(len(indices)):
            if drop_duplicates:
                row_indices = [k for k,_ in groupby(indices[ind])]
            else:
                row_indices = indices[ind].tolist()
            result.append("".join([self.labels[i] for i in row_indices if i != self.blank]))

        return result if batch else result[0]


def run_craft(img, model, ths=0.2):

    img_tensor, shape = prepare_image_for_model(img)
    out = model(img_tensor)
    score_text, score_link = out[0, :, :, 0], out[0, :, :, 1]  # starnge indexing, sorry :(
    score_text = score_text[:shape[0], :shape[1]]
    score_link = score_link[:shape[0], :shape[1]]

    # scores below 0.2 look like noisy clouds, drop them
    score_text[score_text < ths] = 0
    score_link[score_link < ths] = 0

    orig_h, orig_w = img.shape[:2]
    score_link = cv2.resize(score_link, (orig_w, orig_h), interpolation = INTER)
    score_text = cv2.resize(score_text, (orig_w, orig_h), interpolation = INTER)
    return score_text, score_link, img_tensor


def resize_to_32(img):
    height, width, channel = img.shape

    new_height, new_width = height, width
    if new_height % 32 != 0:
        new_height = new_height + (32 - new_height % 32)
    if new_width % 32 != 0:
        new_width = new_width + (32 - new_width % 32)

    resized = np.zeros((new_height, new_width, channel), dtype=np.float32)
    resized[:height, :width, :] = img

    return resized


def normalize(x, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]):
    mean = [x * 255 for x in mean]
    std = [x * 255 for x in std]
    return ((x - mean) / (std)).astype('float32')


def prepare_image_for_model(x):
    # preparation for craft model
    extreme = 960
    max_shape = max(x.shape)
    if max_shape > extreme:  # maximum image size craft can process
        factor = extreme / max_shape
        w, h = [int(x * factor) for x in x.shape[:2]]
        x = cv2.resize(x, (h, w), interpolation = INTER)

    shape = x.shape
    x = resize_to_32(x)
    x = normalize(x)
    x = x.transpose((2, 0, 1))[None, :, :, :]
    return x, shape


def get_width(h, rh, w):
    width = int(math.floor(w * (rh / h)))
    return width + width % 2


def prepare_word_image(image, h):
    w = max(h, get_width(image.shape[0], h, image.shape[1]))
    w = min(w, 2407)  # maximum shape for model
    #image_tensor = A.Resize(h, w)(image=image)['image']
    image_tensor = cv2.resize(image, (w, h), interpolation = INTER)
    image_tensor = normalize(image_tensor)
    image_tensor = image_tensor.transpose((2, 0, 1))
    return image_tensor, w


def word_separation_score_and_distance(score_text, score_link, text_score_ths, link_score_ths):
    """
    score and distance for word separation with watershed
    """
    text_score = (score_text >= text_score_ths) * np.ones_like(score_text)
    link_score = (score_link >= link_score_ths) * np.ones_like(score_text)

    text_score_comb = np.clip(text_score + link_score, 0, 1)
    distance = score_text + score_link

    return text_score_comb, distance


def watershed_separation(score, distance, min_marker_size_px=15, min_label_size_px=30):

    markers, nLabels = measure.label(score, background=0, return_num=True) # connected components
    for k in range(1, nLabels+1):
        size = (markers == k).sum()
        if size < min_marker_size_px:  # drop small islets
            markers[markers == k] = 0
            continue

    labels = watershed(-distance, markers, mask=distance > 0)

    for k in range(1, nLabels+1):
        size = (labels == k).sum()
        if size < min_label_size_px:  # drop small islets after watershed
            labels[labels == k] = 0
            continue

    return markers, labels


def make_warp_images_from_labels(labels, img, dilation_coeff=0.4):
    nLabels = labels.max()
    images = []
    word_boxes = []
    label_boxes = []
    for k in range(1, nLabels+1):
        current_word_mask = (labels == k).astype(np.uint8)

        if not current_word_mask.sum():
            continue

        dilate_by = int(np.ceil(min(np.ptp(np.argwhere(current_word_mask), axis=0)) * dilation_coeff))
        current_word_mask = cv2.dilate(current_word_mask, np.ones(dilate_by, dtype=np.uint8))

        minar = cv2.minAreaRect(np.argwhere(current_word_mask))
        word_box = order_points(cv2.boxPoints(minar)).astype(int)
        word_box[:, 0] = np.clip(word_box[:, 0], 0, img.shape[0])
        word_box[:, 1] = np.clip(word_box[:, 1], 0, img.shape[1])
        word_boxes.append(word_box)

        height = int(np.linalg.norm(word_box[1] - word_box[0]))
        width = int(np.linalg.norm(word_box[0] - word_box[3]))

        input = np.float32(np.roll(word_box, 1, axis=1))
        output = np.float32([[0, 0], [0, height], [width, height], [width, 0]])

        M = cv2.getPerspectiveTransform(input, output)
        warped = cv2.warpPerspective(img, M, (width, height))
        warped_label = cv2.warpPerspective(current_word_mask, M, (width, height))

        images.append(warped)
        label_boxes.append(warped_label)
    return images, word_boxes, label_boxes


def order_points(coords):
    coords = coords.tolist()
    center = tuple(map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), coords), [len(coords)] * 2))
    coords = np.array(sorted(coords, key=lambda coord: -(-135 - math.degrees(math.atan2(*tuple(map(operator.sub, coord, center))[::-1])))))
    # tl, bl, br, tr

    return coords


class SileroOCR:
    def __init__(self,
                 craft_model_path,
                 word_model_path,
                 word_vocab_path,
                 force_onnx_cpu=True):

        self.craft_model = OnnxModel(craft_model_path, force_onnx_cpu)
        self.word_model = OnnxModel(word_model_path, force_onnx_cpu)
        vocab = load_vocab(word_vocab_path)
        self.word_decoder = GreedyCTCDecoder(labels=OrderedDict([(ids, c) for c, ids in vocab.items()]))

        two_way_replace = {'A': 'А', 'H': 'Н', 'E': 'Е', 'C': 'С', 'K': 'К', 'O': 'О', 'P': 'Р', 'X': 'Х', 'Y': 'У', 'M': 'М', 'B': 'В', 'T': 'Т',
                         'a': 'а', 'c': 'с', 'e': 'е', 'o': 'о', 'p': 'р', 'k': 'к', 'x': 'х', 'y': 'у'}
        
        one_way_ru = {'b': 'ь', 'l': '1', 'n': 'п', 't': 'т', 'u': 'и', 'r': 'г'}
        one_way_en = {'З': '3', 'П': 'n', 'Ч': '4', 'Ь': 'b', 'в': 'B', 'з': '3', 'м': 'M', 'н': 'H', 'п': 'n', 'т': 'T', 'ы': 'bI', 'ь': 'b', 'г': 'r'}
        
        self.word_replace_ru = {**two_way_replace, **one_way_ru}
        self.word_replace_en = {**{j: i for i, j in two_way_replace.items()}, **one_way_en}

    def __call__(self, path, language=None, **kwargs):
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        score_text, score_link, new_img = run_craft(img=img,
                                           model=self.craft_model,
                                           ths=0.2)

        score, distance = word_separation_score_and_distance(score_text=score_text,
                                                             score_link=score_link,
                                                             text_score_ths=kwargs.get('text_score_ths', 0.8),
                                                             link_score_ths=kwargs.get('link_score_ths', 0.3))

        markers, labels = watershed_separation(score=score,
                                         distance=distance,
                                         min_marker_size_px=kwargs.get('min_marker_size_px', 15),
                                         min_label_size_px=kwargs.get('min_label_size_px', 15))

        word_images, word_boxes, label_boxes = make_warp_images_from_labels(labels=labels,
                                                               img=img,
                                                               dilation_coeff=kwargs.get('dilation_coeff', 0.4))

        word_boxes, predicts = self.final_word_predicts(word_images,
                                                        word_boxes,
                                                        batch_size=kwargs.get('batch_size', 24),
                                                        decoder_ths=kwargs.get('decoder_ths', 0.6))
        
        if language is not None:
            assert language in ['ru', 'en']
            predicts = [self.to_correct_lang(x, language=language) for x in predicts]

        return word_boxes, predicts, img

    def final_word_predicts(self, word_images, word_boxes, batch_size, decoder_ths):
        predicts = []
        final_boxes = []
        for j in range(0, len(word_images), batch_size):
            chunk_images = word_images[j: j+batch_size]
            chunk_boxes = word_boxes[j: j+batch_size]

            chunk_predicts, chunk_outs = predict_word_batch(self.word_model, self.word_decoder, chunk_images)
            for i in range(0, len(chunk_images), 1):
                values = chunk_outs[:, i, :].max(axis=1)
                indices = chunk_outs[:, i, :].argmax(axis=1)
                confidence = values[indices != 0].mean()

                if confidence > decoder_ths:
                    predicts.append(chunk_predicts[i])
                    final_boxes.append(chunk_boxes[i])

        return final_boxes, predicts
    

    def to_correct_lang(self, x, language):
        out_string = ''
        if language == 'ru':
            dct = self.word_replace_ru
        elif language == 'en':
            dct = self.word_replace_en
        else:
            return x

        for char in x:
            if char in dct:
                out_string += dct[char]
            else:
                out_string += char

        return out_string


def predict_word_batch(model, decoder, images=None, h=32):
    image_tensors = []
    ws = []
    for image in images:
        image_tensor, w = prepare_word_image(image, h)
        image_tensors.append(image_tensor)
        ws.append(w)

    max_w = max(300, max(ws))

    batch_size = len(image_tensors)
    x_batched = np.zeros((batch_size, 3, h, max_w), dtype='float32')

    for i, x in enumerate(image_tensors):
        x_batched[i, :, :h, :x.shape[2]] = x

    output = model(x_batched)
    decoded_ctc = decoder(output[0])

    return decoded_ctc, output[0]


def draw_boxes(img, final_boxes, predicts):
    rects = []
    for box, text in zip(final_boxes, predicts):
        xmin = box[:, 0].min()
        ymin = box[:, 1].min()
        xmax = box[:, 0].max()
        ymax = box[:, 1].max()
        rects.append(Rectangle((ymin, xmin), ymax-ymin, xmax-xmin, linewidth=2,edgecolor='b',facecolor='none'))
        plt.text(ymin - 10, xmin - 10, text, fontsize=10, c='white', path_effects=[patheffects.withStroke(linewidth=2, foreground='black')])
        
    plt.imshow(img)
    ax = plt.gca()
    for i in rects:
        ax.add_patch(i)