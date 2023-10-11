import time

from utils.base_util import BaseUtil
from dsimage import DSImage
from logger import logger
from cv2 import fastNlMeansDenoisingColored, fastNlMeansDenoising

class NoiseUtil(BaseUtil):
    hint = "This is a utility for working with deep sky object detection, star detection, etc."
    def __init__(self):
        """
        NoiseUtil
        
        A utility for working with deep sky object detection, star detection, etc.
        """
        super().__init__()
        self.funcs = {
            "denoise_saltnpepper": self.denoise_saltnpepper, # TODO: Add function hints
            "denoise_color": self.denoise_color
        }
        logger.debug(f"[{__name__}] {self.id} registered as NoiseUtil")
        
    def denoise_saltnpepper(self, image: DSImage):
        """
        Use PIL to remove salt-and-pepper noise from an image.
        """
        tic = time.time()
        cv2_image = image.get_cv2()
        cv2_image = fastNlMeansDenoising(cv2_image, None, 10, 7, 21) # TODO: Make these parameters configurable
        image.set_data_from_cv2(cv2_image)
        toc = time.time()
        logger.debug(f"[{__name__}] Denoised image {image.id} in {toc-tic} seconds")
        return image
    
    def denoise_color(self, image: DSImage):
        """
        Use PIL to remove color noise from an image.
        """
        tic = time.time()
        cv2_image = image.get_cv2()
        cv2_image = fastNlMeansDenoisingColored(cv2_image, None, 10, 10, 7, 21) # TODO: Make these parameters configurable
        image.set_data_from_cv2(cv2_image)
        toc = time.time()
        logger.debug(f"[{__name__}] Denoised image {image.id} in {toc-tic} seconds")
        return image
        
EXPORT_UTIL = NoiseUtil