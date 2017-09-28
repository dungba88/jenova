"""IO utility for image"""

import base64
from io import BytesIO
from PIL import Image
import cv2
import numpy as np

def read_base64(base64_string):
    """read an image from base64 string"""
    sbuf = BytesIO()
    sbuf.write(base64.b64decode(base64_string))
    pimg = Image.open(sbuf)
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
