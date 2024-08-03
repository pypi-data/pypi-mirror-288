import silero_ocr
import sys
silero_ocr.__version__


if __name__ == "__main__":
    print(sys.version)
    print(silero_ocr.__version__)
    model = silero_ocr.load_silero_ocr()
    final_boxes, predicts, img = model('test.jpg', language='en')
    silero_ocr.draw_boxes(img, final_boxes, predicts)
    for i in predicts:
        print(i)

    print('reloading model')
    model = silero_ocr.load_silero_ocr()

    final_boxes, predicts, img = model('test.jpg', language='ru')
    silero_ocr.draw_boxes(img, final_boxes, predicts)
    for i in predicts:
        print(i)