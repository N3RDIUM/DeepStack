from uuid import uuid4
import time

import sep
from utils.base_util import BaseUtil
from dsimage import DSImage
from logger import logger
import pandas as pd
import tqdm
from scipy.spatial import KDTree
import numpy as np
from scipy.spatial import distance
from math import acos, degrees
import pandas as pd
from uuid import uuid4

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
            "detect": self.detect,
            "group": self.group,
            "analyze": self.analyze
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
        
        tree = objects.data[['x', 'y']].to_numpy()
        _tree = tree.copy()
        kdtree = KDTree(tree)
        neighbours = np.array(kdtree.query(tree, k=3))
        neighbours = np.moveaxis(neighbours, 1, 0)
        neighbours = np.moveaxis(neighbours, 1, -1)
        
        tris = []
        for triplet in neighbours:
            indexes = [int(i[1]) for i in triplet]
            _xz = _tree[indexes[0]], tree[indexes[1]], tree[indexes[2]]
            tris.append(_xz)
        
        return tris
    
    def analyze(self, tris: list):
        """
        Analyze the triangles for their side length ratios and angles and store them in a dataframe
        """
        tris_header = ["uuid", "side_1", "side_2", "side_3", "angle_1", "angle_2", "angle_3"]
        tris_data = []

        for tri in tris:
            # Tri shape: ((x1, y1), (x2, y2), (x3, y3))
            # Get the distances between the points
            distances = [distance.euclidean(tri[0], tri[1]), distance.euclidean(tri[1], tri[2]), distance.euclidean(tri[2], tri[0])]
            # Now convert the distances to ratios
            total = sum(distances)
            distances = [i / total for i in distances]
            
            # Get the angles between the points
            angles = [degrees(acos((distances[0]**2 + distances[2]**2 - distances[1]**2) / (2 * distances[0] * distances[2]))),
                    degrees(acos((distances[0]**2 + distances[1]**2 - distances[2]**2) / (2 * distances[0] * distances[1]))),
                    degrees(acos((distances[1]**2 + distances[2]**2 - distances[0]**2) / (2 * distances[1] * distances[2])))]
            # Store the data
            tris_data.append([uuid4(), distances[0], distances[1], distances[2], angles[0], angles[1], angles[2]])
            
        tris_df = pd.DataFrame(tris_data, columns=tris_header)
        tris_df.set_index("uuid", inplace=True)
        
        return tris_df

EXPORT_UTIL = StarfinderUtil