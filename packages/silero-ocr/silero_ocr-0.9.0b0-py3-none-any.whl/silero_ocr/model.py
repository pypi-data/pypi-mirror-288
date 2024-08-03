from .utils import SileroOCR, download_model
import os

def load_silero_ocr(force_onnx_cpu=True):
    txt_name = 'word_symbols_vocab.txt'
    package_path = "silero_ocr.data"
    
    try:
        import importlib_resources as impresources
        word_vocab_path = str(impresources.files(package_path).joinpath(txt_name))
    except:
        from importlib import resources as impresources
        try:
            with impresources.path(package_path, txt_name) as f:
                word_vocab_path = f
        except:
            word_vocab_path = str(impresources.files(package_path).joinpath(txt_name))

    word_vocab_path = str(word_vocab_path)
    craft_model_path = word_vocab_path.replace(txt_name, 'craft_model.onnx')
    if not os.path.exists(craft_model_path):
        download_model('https://models.silero.ai/ocr-models/craft_vgg_13_v10_newlink.onnx', craft_model_path)

    word_model_path = word_vocab_path.replace(txt_name, 'word_model.onnx')
    if not os.path.exists(word_model_path):
        download_model('https://models.silero.ai/ocr-models/word_model.onnx', word_model_path)

    model = SileroOCR(craft_model_path=craft_model_path,
                      word_model_path=word_model_path,
                      word_vocab_path=word_vocab_path,
                      force_onnx_cpu=force_onnx_cpu)
    return model
