with open('DeepStacker.log', 'w') as f:
    f.write("")
# TODO: Create an image list handler ('DSSequence')

from PIL import Image, ImageDraw
from util_loader import utils
from dsimage import DSImage
import numpy as np


def load_and_get_objs(path):
    image = DSImage()
    image.load_from_pil(path)
    bkgremoved = utils["BackgroundUtil"].extract(image)
    subtracted = utils["BackgroundUtil"].subtract(image, bkgremoved)
    objects = utils["StarfinderUtil"].detect(subtracted, {"thresh": 128})

    # obj_coords = np.array([objects.data['x'], objects.data['y'], objects.data['a'], objects.data['b']])

    # # Mark the objects
    # im = Image.open('./example_images/example.jpg')
    # draw = ImageDraw.Draw(im)
    # fct = 3
    # for obj in obj_coords.T:
    #     draw.rectangle([obj[0]-obj[2]*fct, obj[1]-obj[3]*fct, obj[0]+obj[2]*fct, obj[1]+obj[3]*fct], outline="red", width=2)
    # im.save("./example_images/result.jpg")

    n_objs = len(list(objects.data['x']))
    obj_coords = np.zeros((n_objs, 3))
    for i in range(n_objs):
        obj_coords[i, 0] = objects.data['x'][i]
        obj_coords[i, 1] = objects.data['y'][i]
    return obj_coords

# TODO: Make this process configurable
# TODO: Make this a function

src = load_and_get_objs("./example_images/1.png")
tgt = load_and_get_objs("./example_images/2.png")
offset = utils["AlignerUtil"].get_transform(src, tgt)
print(offset)
dx = offset[1][0]
dy = offset[1][1]
roll = offset[0][0]

# Now we have the offset, we can add the pixels to the image
# Calculate the size of the new image
src_shape = Image.open("./example_images/1.png").size
tgt_shape = Image.open("./example_images/2.png").size
size = [int(max(src_shape[0], tgt_shape[0]) + abs(dx)), int(max(src_shape[1], tgt_shape[1]) + abs(dy))]
# Create the new image
new_image = Image.new("RGB", size)
# Load the images
src_image = Image.open("./example_images/1.png")
tgt_image = Image.open("./example_images/2.png")
# Paste the images
new_image.paste(src_image, (100, 100))
new_image.paste(tgt_image, (int(dx)+100, int(dy)+100))
# Save the image
new_image.save("./example_images/result-stack.jpg")