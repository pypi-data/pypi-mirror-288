# Import the Python module first
from .marearts_anpr import marearts_anpr_from_pil, marearts_anpr_from_image_file, marearts_anpr_from_cv2

# Now import the public Cython-compiled modules
from .marearts_anpr_d import ma_anpr_detector
from .marearts_anpr_r import ma_anpr_ocr

__all__ = [
    "marearts_anpr_from_pil",
    "marearts_anpr_from_image_file",
    "marearts_anpr_from_cv2",
    "ma_anpr_detector",
    "ma_anpr_ocr"
]