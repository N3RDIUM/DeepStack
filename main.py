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

# Format the objects into a dataframe
tris = utils["StarfinderUtil"].group(objects)

# TODO: Do the same processes with different thresholds for the object detector to get more variety in structure (size of groups of objects)
# TODO: Higher thresholds give larger triangle structures, lower thresholds give smaller triangle structures
# TODO: Make this process configurable
# TODO: Make this a function

# Now analyze the triangles for their side length ratios and angles and store them in a dataframe
analyzed = utils["StarfinderUtil"].analyze(tris)
print(analyzed.head())
print(analyzed.iloc[0])

# Now find similar triangles
similar = utils["StarfinderUtil"].find_matches(analyzed.iloc[0], analyzed, 8)
print(similar.head(8))