from uuid import uuid4
import time

import sep
from utils.base_util import BaseUtil
from dsimage import DSImage
from logger import logger
import pandas as pd
from uuid import uuid4
import tqdm
from scipy.spatial import KDTree
import numpy as np

class DSObjects:
    def __init__(self, id: (uuid4, str), data):
        """
        DSObjects
        
        This stores the output of sep's object detection function (sep.extract())
        Currently this does not do anything, but its importance as a separate class will be revealed later.
        """
        self.id = id
        self.data = data

class StarfinderUtil(BaseUtil):
    hint = "This is a utility for working with deep sky object detection, star detection, etc."
    def __init__(self):
        """
        StarfinderUtil
        
        A utility for working with deep sky object detection, star detection, alignment preprocessing, etc.
        """
        super().__init__()
        self.funcs = {
            "detect": self.detect
        }
        logger.debug(f"[{__name__}] {self.id} registered as StarfinderUtil")
        
    def detect(self, image: DSImage, sep_params: dict):
        """
        Extract the background from an image.
        """
        tic = time.time()
        objects = DSObjects(image.id, sep.extract(image.mono_data, **sep_params))
        toc = time.time()
        logger.debug(f"[{__name__}] Detected objects in {image.id} in {toc-tic} seconds.")
        return objects
    
    def group(self, objects: DSObjects, group_params: dict):
        """
        Group objects into triangles and spot out the triangle vertex coords, angles formed, and the ratio of the side lengths.
        """
        arr = []
        for i in objects.data:
            arr.append(list(i))
        objects.data = pd.DataFrame(arr[1:], columns=objects.data.dtype.names)
        objects.data['uuid'] = [uuid4() for i in tqdm.trange(len(objects.data))]
        # Now we have a dataframe with the objects and their uuids.
        # Now we can use those UUIDs to group the objects into triangles.
        # Use math.dist, form triplets of nearest neighbors, and then calculate the angles and side lengths.
        tree = objects.data[['x', 'y']].to_numpy()
        _tree = tree.copy()
        kdtree = KDTree(tree)
        nearest_neighbors = np.array(kdtree.query(tree, k=3))
        return nearest_neighbors, _tree
EXPORT_UTIL = StarfinderUtil