from utils.base_util import BaseUtil
from scipy.spatial import distance
from scipy.spatial import KDTree
from math import acos, degrees
from dsimage import DSImage
from logger import logger
from uuid import uuid4
import pandas as pd
import numpy as np
import time
import tqdm
import sep

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
    
    def group(self, objects: DSObjects):
        """
        Group objects into triangles and spot out the triangle vertex coords, angles formed, and the ratio of the side lengths.
        """
        arr = []
        for i in objects.data:
            arr.append(list(i))
        objects.data = pd.DataFrame(arr[1:], columns=objects.data.dtype.names)
        
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
        tris_header = ["id", "side1", "side2", "side3", "angle1", "angle2", "angle3", "absolute_distances"]
        tris_data = []

        for tri in tris:
            # Tri shape: ((x1, y1), (x2, y2), (x3, y3))
            # Get the distances between the points
            distances = [distance.euclidean(tri[0], tri[1]), distance.euclidean(tri[1], tri[2]), distance.euclidean(tri[2], tri[0])]
            # Now convert the distances to ratios
            total = sum(distances)
            distance_ratio = [i / total for i in distances]
            
            # Get the angles between the points
            angles = [degrees(acos((distances[0]**2 + distances[2]**2 - distances[1]**2) / (2 * distances[0] * distances[2]))),
                    degrees(acos((distances[0]**2 + distances[1]**2 - distances[2]**2) / (2 * distances[0] * distances[1]))),
                    degrees(acos((distances[1]**2 + distances[2]**2 - distances[0]**2) / (2 * distances[1] * distances[2])))]
            # Store the data
            tris_data.append([len(tris_data), distance_ratio[0], distance_ratio[1], distance_ratio[2], angles[0], angles[1], angles[2], distances])
            
        tris_df = pd.DataFrame(tris_data, columns=tris_header)
        tris_df.set_index("id", inplace=True)
        
        return tris_df
    
    def _similarity (self, tri1, tri2):
        """
        Returns a similarity score between two triangles, between 0 and 1.
        """
        return (
            (
                abs(tri1['side1'] - tri2['side1']) +
                abs(tri1['side2'] - tri2['side2']) +
                abs(tri1['side3'] - tri2['side3'])
            ) + 
            (
                abs(tri1['angle1'] - tri2['angle1']) + 
                abs(tri1['angle2'] - tri2['angle2']) + 
                abs(tri1['angle3'] - tri2['angle3'])
            ) / (180 * 3)
        ) / 6
    
    def find_matches(self, tri, tris_df: pd.DataFrame, n_matches: int):
        """
        Analyze a triangle and find the closest match in the tris_df dataframe.
        """
        similarities = {}
        for _tri in tqdm.trange(len(tris_df), desc="Finding matches for tri"):
            similarities[_tri] = self._similarity(tri, tris_df.iloc[_tri])
        ret = sorted(similarities, key=similarities.get)[:n_matches]
        # Return in a df
        return tris_df.iloc[ret]

EXPORT_UTIL = StarfinderUtil