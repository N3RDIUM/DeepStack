from uuid import uuid4

import sep
from utils.base_util import BaseUtil
from dsimage import DSImage
from logger import logger

class DSBackground:
    def __init__(self, id: (uuid4, str), data):
        """
        DSBackground
        
        This is a wrapper for sep.Background()
        Currently this does not do anything, but its importance as a separate class will be revealed later.
        """
        self.id = id
        self.data = data

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
        bkg = DSBackground(image.id, sep.Background(image.data))
        return bkg
    
    def subtract(self, image: DSImage, background: DSBackground):
        """
        Subtract the background from an image.
        """
        image = DSImage()
        image.inherit_from(image)
        image.data = image.data - background.data
        return image
    
EXPORT_UTIL = BackgroundUtil