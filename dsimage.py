import os
import uuid
import time

from PIL import Image
from astropy.io import fits
import numpy as np
import imageio
import fitsio
import rawpy

from logger import logger

class DSImage:
    def __init__(self):
        """
        DSImage
        
        This is an image class handler thingy for DeepStack.
        """
        self.id = uuid.uuid4()
        self.loaded = False
        self.parent = None
        self.load_details = {
            "file_type": None,
            "file_path": None,
            "converted_path": None
        }
        self.data = None
        logger.debug(f"[{__name__}] Created new DSImage with ID {self.id}")
        
    def load_from_raw(self, filepath: str, output_path: str):
        """
        Load a DeepStack image from a raw file format, like CR2 or DNG.
        """
        tic = time.time()
        details_update = {}
        details_update["file_path"] = filepath
        
        try:
            with rawpy.imread(filepath) as raw:
                rgb = raw.postprocess()
            imageio.imsave(f'{output_path}-temp.tiff', rgb)
            image = Image.open(f"{output_path}-temp.tiff")
            imarray = np.array(image)
            os.remove(f"{output_path}-temp.tiff")
        except Exception as e:
            logger.error(f"[{__name__}] Could not open {filepath}: {e}")
            imarray = None
            
        if imarray is not None:
            hdul = fits.PrimaryHDU()
            hdul.data = imarray
            # TODO: Ask the user if they want to overwrite the file
            # TODO: Make the fits file inherit the exif data (header) from the original file
            hdul.writeto(output_path, overwrite=True)
            self.data = self.read_fits(output_path)
        else:
            raise ValueError(f"Could not open {filepath}.")
        
        toc = time.time()
        logger.debug(f"[{__name__}] Loaded {filepath} in {toc-tic} seconds.")
        return 0
        
    def read_fits(self, input_path: str):
        """
        Read data from a fits file using fitsio.
        """
        try:
            im = fitsio.read(input_path)
        except Exception as e:
            logger.error(f"[{__name__}] Could not open {input_path}: {e}")
            return None # TODO: Check if this is None in other functions that will call this
        return im
    
    def write_fits(self, output_path: str, dtype: str):
        """
        Write the changes made to the image to a fits file.
        """
        try:
            fitsio.write(output_path, self.data.astype(dtype))
        except Exception as e:
            logger.error(f"[{__name__}] Could not save {output_path}: {e}")
            return None
        return 0
    
    def write_tiff(self, output_path: str):
        """
        Write the changes made to the image to a tiff file.
        """
        try:
            imageio.imsave(output_path, self.data)
        except Exception as e:
            logger.error(f"[{__name__}] Could not save {output_path}: {e}")
            return None
        return 0
    
    def inherit_from(self, parent_image: object):
        """
        Inherit data from another DSImage object.
        """
        assert isinstance(parent_image, DSImage)
        self.parent = parent_image
        self.data = parent_image.data
        self.load_details = parent_image.load_details
        self.loaded = True
        logger.debug(f"[{__name__}] {self.id} inherited data from {parent_image.id}")
        