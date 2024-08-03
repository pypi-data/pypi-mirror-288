from importlib.metadata import version
try:
    __version__ = version(__name__)
except:
    pass

from silero_ocr.model import load_silero_ocr
from silero_ocr.utils import draw_boxes