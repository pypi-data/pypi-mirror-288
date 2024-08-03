# WRITER: LauNT # DATE: 05/2024
# FROM: akaOCR Team - QAI

from .detect import BoxEngine
from .recog import TextEngine
from .rotate import RotateEngine

__version__ = 'akaocr-v2.0.13'
__all__ = ['BoxEngine', 'TextEngine', 'RotateEngine']
