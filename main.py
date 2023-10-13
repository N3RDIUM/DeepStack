with open('DeepStacker.log', 'w') as f:
    f.write("")
# TODO: Create an image list handler ('DSSequence')

from dsimage import DSImage
from util_loader import utils
import numpy as np

image = DSImage()
image.load_from_pil("./example_images/example.jpg")
image.write_tiff("./example_images/test.tiff")

saltnpeppered = utils["NoiseUtil"].denoise_saltnpepper(image)
colornoised = utils["NoiseUtil"].denoise_color(image)
bkgremoved = utils["BackgroundUtil"].extract(image)
subtracted = utils["BackgroundUtil"].subtract(image, bkgremoved)
objects = utils["StarfinderUtil"].detect(image, {"thresh": 4}).data
obj_coords = np.array([objects['x'], objects['y'], objects['a'], objects['b']]).T

# Mark the objects
from PIL import Image, ImageDraw
im = Image.open('./example_images/example.jpg')
draw = ImageDraw.Draw(im)
fct = 2
for obj in obj_coords:
    draw.rectangle([obj[0]-obj[2]*fct, obj[1]-obj[3]*fct, obj[0]+obj[2]*fct, obj[1]+obj[3]*fct], outline="red")
im.save("./example_images/test-nobg-marked.tiff")
im.save("./example_images/result.jpg")