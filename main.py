with open('DeepStacker.log', 'w') as f:
    f.write("")
# TODO: Create an image list handler ('DSSequence')

from dsimage import DSImage
from util_loader import utils

image = DSImage()
image.load_from_raw("./example_images/1.dng", "./example_images/test.fits")
image.write_tiff("./example_images/test.tiff")