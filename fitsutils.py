from PIL import Image, UnidentifiedImageError
from astropy.io import fits
import numpy as np
import imageio
import fitsio
import rawpy
import os
    
def convert2fits(infile, outfile):
    """
    Converts any other image format to fits format
    """
    # TODO: This format test is dirty, find a better way (like looking at the extension)
    try:
        im = Image.open(infile)
        imarray = np.array(im)
    except UnidentifiedImageError:
        # Assume that it is a raw image
        with rawpy.imread(infile) as raw:
            rgb = raw.postprocess()
        imageio.imsave(f'{outfile}-temp.tiff', rgb)
        im = Image.open(f"{outfile}-temp.tiff")
        imarray = np.array(im)
        os.remove(f"{outfile}-temp.tiff")
    except:
        raise ValueError(f"Could not open {infile}")
    
    hdul = fits.PrimaryHDU()
    hdul.data = imarray
    # TODO: Ask the user if they want to overwrite the file
    # TODO: Make the fits file inherit the exif data (header) from the original file
    hdul.writeto(outfile, overwrite=True) 
    
    return load_fits(outfile)

def load_fits(infile):
    """
    Load a fits file using fitsio
    """
    try:
        im = fitsio.read(infile)
    except:
        raise ValueError(f"Could not open {infile}")
    return im

def save_fits(sep_fitsdata, outfile):
    """
    Save a fits file using fitsio
    """
    try:
        fitsio.write(outfile, sep_fitsdata)
    except:
        raise ValueError(f"Could not save {outfile}")
    return load_fits(outfile)

def save_tiff(imarray, outfile):
    """
    Save a tiff file using imageio
    """
    try:
        imageio.imsave(outfile, imarray)
    except:
        raise ValueError(f"Could not save {outfile}")
    return load_fits(outfile)