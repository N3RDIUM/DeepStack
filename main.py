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
# colornoised = utils["NoiseUtil"].denoise_color(image)
bkgremoved = utils["BackgroundUtil"].extract(image)
subtracted = utils["BackgroundUtil"].subtract(image, bkgremoved)
objects = utils["StarfinderUtil"].detect(image, {"thresh": 16})
obj_coords = np.array([objects.data['x'], objects.data['y'], objects.data['a'], objects.data['b']])

# Mark the objects
from PIL import Image, ImageDraw
im = Image.open('./example_images/example.jpg')
draw = ImageDraw.Draw(im)
fct = 2
for obj in obj_coords.T:
    draw.rectangle([obj[0]-obj[2]*fct, obj[1]-obj[3]*fct, obj[0]+obj[2]*fct, obj[1]+obj[3]*fct], outline="red")
im.save("./example_images/result.jpg")

# Format the objects into a dataframe
import pandas as pd

neighbours, tree = utils["StarfinderUtil"].group(objects, {})
# Plot the neighbours with white lines
from PIL import Image, ImageDraw
im = Image.open('./example_images/result.jpg')
draw = ImageDraw.Draw(im)
fct = 2
# This is the return value of scipy.spatial.KDTree.query()
# Draw the lines
neighbours = np.moveaxis(neighbours, 1, 0)
neighbours = np.moveaxis(neighbours, 1, -1)
for triplet in neighbours:
    indexes = [int(i[1]) for i in triplet]
    coords = tree[indexes[0]], tree[indexes[1]], tree[indexes[2]]
    draw.line([coords[0][0], coords[0][1], coords[1][0], coords[1][1]], fill="white")
    draw.line([coords[1][0], coords[1][1], coords[2][0], coords[2][1]], fill="white")
    draw.line([coords[2][0], coords[2][1], coords[0][0], coords[0][1]], fill="white")
im.save("./example_images/result-trimarked.jpg")