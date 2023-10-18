from utils.base_util import BaseUtil
from scipy.spatial import cKDTree
from logger import logger
import numpy as np

def icp(point_cloud_src, point_cloud_tgt, max_iterations=50, tolerance=1e-6):
    """
    Perform Iterative Closest Point (ICP) to find the rotation and translation between two point clouds.

    :param point_cloud_src: Source point cloud as an N x 3 numpy array.
    :param point_cloud_tgt: Target point cloud as an N x 3 numpy array.
    :param max_iterations: Maximum number of iterations.
    :param tolerance: Convergence tolerance.
    :return: R (3x3 rotation matrix), t (3x1 translation vector), transformed_src (transformed source point cloud).
    """

    assert point_cloud_src.shape[1] == 3 and point_cloud_tgt.shape[1] == 3, "Point clouds must be Nx3 arrays."

    # Initialize the transformation
    R = np.eye(3)  # Identity rotation matrix
    t = np.zeros((3, 1))  # Zero translation vector

    for iteration in range(max_iterations):
        # Step 1: Find the correspondences using a KD-tree
        tree = cKDTree(point_cloud_tgt)
        distances, indices = tree.query(point_cloud_src)

        # Step 2: Calculate the transformation matrix using SVD
        src_correspondences = point_cloud_src
        tgt_correspondences = point_cloud_tgt[indices]

        src_mean = np.mean(src_correspondences, axis=0)
        tgt_mean = np.mean(tgt_correspondences, axis=0)

        H = np.dot((src_correspondences - src_mean).T, tgt_correspondences - tgt_mean)
        U, _, Vt = np.linalg.svd(H)
        R_candidate = np.dot(Vt.T, U.T)
        t_candidate = tgt_mean.reshape(3, 1) - np.dot(R_candidate, src_mean.reshape(3, 1))

        # Step 3: Update the transformation
        delta_R = R_candidate
        delta_t = t_candidate

        R = np.dot(delta_R, R)
        t = np.dot(delta_R, t) + delta_t

        # Check for convergence
        if np.linalg.norm(delta_R - np.eye(3)) < tolerance:
            break

    # Transform the source point cloud using the found transformation
    transformed_src = np.dot(R, point_cloud_src.T).T + t.T

    return R, t, transformed_src

def rotation_matrix_to_euler_angles(R):
    """
    Convert a 3x3 rotation matrix to Euler angles (roll, pitch, yaw) in degrees.

    :param R: 3x3 rotation matrix.
    :return: Euler angles (roll, pitch, yaw) in degrees.
    """
    # Extract individual rotation elements from the rotation matrix
    r11, r12, r13 = R[0, 0], R[0, 1], R[0, 2]
    r21, r22, r23 = R[1, 0], R[1, 1], R[1, 2]
    r31, r32, r33 = R[2, 0], R[2, 1], R[2, 2]

    # Calculate pitch (y-axis rotation)
    pitch = np.arcsin(-r31)
    
    # Calculate yaw (z-axis rotation)
    yaw = np.arctan2(r21 / np.cos(pitch), r11 / np.cos(pitch))
    
    # Calculate roll (x-axis rotation)
    roll = np.arctan2(r32 / np.cos(pitch), r33 / np.cos(pitch))

    # Convert angles from radians to degrees
    pitch = np.degrees(pitch)
    yaw = np.degrees(yaw)
    roll = np.degrees(roll)

    return roll, pitch, yaw

class AlignerUtil(BaseUtil):
    hint = "This is a utility for working with image alignment."
    def __init__(self):
        """
        AlignerUtil
        
        A utility for working with image alignment.
        """
        super().__init__()
        self.funcs = {
            "get_transform": self.get_transform
        }
        logger.debug(f"[{__name__}] {self.id} registered as AlignerUtil")
        
    def get_transform(self, src, tgt, max_iterations=50, tolerance=1e-6):
        """
        Get the transformation matrix between two images.
        """
        R, t, transformed_src = icp(src, tgt, max_iterations, tolerance)
        return rotation_matrix_to_euler_angles(R), t
    
EXPORT_UTIL = AlignerUtil