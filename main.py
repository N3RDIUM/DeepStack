with open('DeepStacker.log', 'w') as f:
    f.write("")
# TODO: Create an image list handler ('DSSequence')

from dsimage import DSImage
from util_loader import utils
import numpy as np

image = DSImage()
image.load_from_pil("./example_images/example.jpg")
image.write_tiff("./example_images/test.tiff")

# saltnpeppered = utils["NoiseUtil"].denoise_saltnpepper(image)
# saltnpeppered.write_tiff("./example_images/test-saltnpepper.tiff")

# colornoised = utils["NoiseUtil"].denoise_color(image)
# colornoised.write_tiff("./example_images/test-colornoise.tiff")

bkgremoved = utils["BackgroundUtil"].extract(image)
subtracted = utils["BackgroundUtil"].subtract(image, bkgremoved)
subtracted.write_tiff("./example_images/test-nobg.tiff")

objects = utils["ObjectDetectorUtil"].detect(image, {"thresh": 1.5}).data