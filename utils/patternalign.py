from utils.base_util import BaseUtil
from logger import logger
import numpy as np
import cv2

def get_transform_and_rotation(image1, image2):
    """
    Get the transformation (translation, rotation, and scale) and rotation between two images based on pattern matching.

    :param image1: First input image.
    :param image2: Second input image.
    :return: transformation matrix, rotation angle (degrees).
    """
    
    # Load images and convert them to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    # Initialize the SIFT detector
    sift = cv2.SIFT_create()
    
    # Find the key points and descriptors in both images
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)
    
    # Create a Brute Force Matcher
    bf = cv2.BFMatcher()
    
    # Match the descriptors
    matches = bf.knnMatch(des1, des2, k=2)
    
    # Apply a ratio test to select good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)
    
    if len(good_matches) < 4:
        return None, None
    
    # Extract the matched key points
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    
    # Estimate the transformation matrix using RANSAC
    transformation_matrix, mask = cv2.estimateAffinePartial2D(src_pts, dst_pts)
    
    if transformation_matrix is None:
        return None, None
    
    # Extract the rotation angle from the transformation matrix
    rotation_angle = -np.degrees(np.arctan2(transformation_matrix[0, 1], transformation_matrix[0, 0]))
    
    return transformation_matrix, rotation_angle


def transform_matrix_to_xy(matrix):
    """
    Convert a 2D transformation matrix into XY translation values.

    :param matrix: 3x3 transformation matrix.
    :return: x and y translation values as a tuple (x, y).
    """
    
    if matrix.shape != (3, 3):
        raise ValueError("Input matrix should be a 3x3 transformation matrix.")
    
    x_translation = matrix[0, 2]
    y_translation = matrix[1, 2]
    
    return x_translation, y_translation

class PatternAlignerUtil(BaseUtil):
    hint = "This is a utility for working with image pattern alignment."
    def __init__(self):
        """
        PatternAlignerUtil
        
        A utility for working with image pattern alignment.
        """
        super().__init__()
        self.funcs = {
            "get_transform": self.get_transform
        }
        logger.debug(f"[{__name__}] {self.id} registered as PatternAlignerUtil")
        
    def get_transform(self, src, tgt):
        """
        Get the transformation matrix between two images based on patterns.
        """
        transformation_matrix, rotation_angle = get_transform_and_rotation(src, tgt)
        x_translation, y_translation = transform_matrix_to_xy(transformation_matrix)
        return x_translation, y_translation, rotation_angle
    
EXPORT_UTIL = PatternAlignerUtil