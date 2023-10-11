from uuid import uuid4
import time

import sep
from utils.base_util import BaseUtil
from dsimage import DSImage
from logger import logger

class DSObjects:
    def __init__(self, id: (uuid4, str), data):
        """
        DSObjects
        
        This stores the output of sep's object detection function (sep.extract())
        Currently this does not do anything, but its importance as a separate class will be revealed later.
        """
        self.id = id
        self.data = data

class ObjectDetectorUtil(BaseUtil):
    hint = "This is a utility for working with deep sky object detection, star detection, etc."
    def __init__(self):
        """
        ObjectDetectorUtil
        
        A utility for working with deep sky object detection, star detection, etc.
        """
        super().__init__()
        self.funcs = {
            "detect": self.detect
        }
        logger.debug(f"[{__name__}] {self.id} registered as ObjectDetectorUtil")
        
    def detect(self, image: DSImage, sep_params: dict):
        """
        Extract the background from an image.
        """
        tic = time.time()
        objects = DSObjects(image.id, sep.extract(image.data, **sep_params))
        toc = time.time()
        logger.debug(f"[{__name__}] Detected {len(objects)} objects in {image.id} in {toc-tic} seconds.")
        return objects

EXPORT_UTIL = ObjectDetectorUtil