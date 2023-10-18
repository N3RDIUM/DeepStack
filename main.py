with open('DeepStacker.log', 'w') as f:
    f.write("")
# TODO: Create an image list handler ('DSSequence')

from PIL import Image, ImageDraw
from util_loader import utils
from dsimage import DSImage
import numpy as np

image = DSImage()
image.load_from_pil("./example_images/example.jpg")
image.write_tiff("./example_images/test.tiff")

# saltnpeppered = utils["NoiseUtil"].denoise_saltnpepper(image)
# colornoised = utils["NoiseUtil"].denoise_color(image)
bkgremoved = utils["BackgroundUtil"].extract(image)
subtracted = utils["BackgroundUtil"].subtract(image, bkgremoved)
objects = utils["StarfinderUtil"].detect(image, {"thresh": 32})
obj_coords = np.array([objects.data['x'], objects.data['y'], objects.data['a'], objects.data['b']])

# Mark the objects
im = Image.open('./example_images/example.jpg')
draw = ImageDraw.Draw(im)
fct = 2
for obj in obj_coords.T:
    draw.rectangle([obj[0]-obj[2]*fct, obj[1]-obj[3]*fct, obj[0]+obj[2]*fct, obj[1]+obj[3]*fct], outline="red")
im.save("./example_images/result.jpg")

# TODO: Make this process configurable
# TODO: Make this a function