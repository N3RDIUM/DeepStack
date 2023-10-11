from uuid import uuid4
import time

import sep
import numpy as np

from utils.base_util import BaseUtil
from dsimage import DSImage
from logger import logger

# TODO: Make this do bkg extraction for each channel separately
class BackgroundUtil(BaseUtil):
    hint = "This is a utility for working with image background extraction and subtraction."
    def __init__(self):
        """
        BackgroundUtil
        
        A utility for working with image background extraction and subtraction.
        """
        super().__init__()
        self.funcs = {
            "extract": self.extract
        }
        logger.debug(f"[{__name__}] {self.id} registered as BackgroundUtil")
        
    def extract(self, image: DSImage):
        """
        Extract the background from an image.
        """
        tic = time.time()
        # TODO: Make this more dynamic and accept more color channels and schemes (RGB, CMYK, etc.)
        # The lines of code that have this type of work to do are marked with a RGB-TODO comment
        # RGB-TODO
        bkg_r = sep.Background(np.ascontiguousarray(image.channel_data["r"], dtype=np.float32))
        bkg_g = sep.Background(np.ascontiguousarray(image.channel_data["g"], dtype=np.float32))
        bkg_b = sep.Background(np.ascontiguousarray(image.channel_data["b"], dtype=np.float32))
        toc = time.time()
        logger.debug(f"[{__name__}] Extracted background from {image.id} in {toc-tic} seconds.")
        return {
            "r": bkg_r,
            "g": bkg_g,
            "b": bkg_b
        }
    
    def subtract(self, image: DSImage, background: dict):
        """
        Subtract the background from an image.
        """
        # RGB-TODO
        tic = time.time()
        data = np.array(image.data, dtype=np.float32)
        data[:,:,0] = data[:,:,0] - background['r']
        data[:,:,1] = data[:,:,1] - background['g']
        data[:,:,2] = data[:,:,2] - background['b']
        image.set_data(data)
        toc = time.time()
        logger.debug(f"[{__name__}] Subtracted background from {image.id} in {toc-tic} seconds.")
        return image
    
EXPORT_UTIL = BackgroundUtil