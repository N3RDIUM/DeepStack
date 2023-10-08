from fitsutils import load_fits, save_fits, convert2fits
from background import remove_background
import numpy as np

convert2fits('example_images/1.dng', 'example_images/something.fits')
data = load_fits('example_images/something.fits')
data = np.reshape(data, (data.shape[0], data.shape[1], 3))

# Split into R, G, B channels (3 separate image arrays)
red = np.ascontiguousarray(data[:,:,0], dtype=np.float32)
green = np.ascontiguousarray(data[:,:,1], dtype=np.float32)
blue = np.ascontiguousarray(data[:,:,2], dtype=np.float32)
nobackground_red = remove_background(red, 64, 64, 3, 3)
nobackground_green = remove_background(green, 64, 64, 3, 3)
nobackground_blue = remove_background(blue, 64, 64, 3, 3)

# Save the background-subtracted images
save_fits(nobackground_red, 'example_images/nobackground_red.fits')
save_fits(nobackground_green, 'example_images/nobackground_green.fits')
save_fits(nobackground_blue, 'example_images/nobackground_blue.fits')