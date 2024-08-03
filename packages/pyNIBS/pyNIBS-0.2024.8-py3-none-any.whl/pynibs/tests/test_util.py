import pynibs
import unittest
from scipy.spatial.transform import Rotation as rot
import numpy as np


class TestIntersectionVecPlan(unittest.TestCase):
    def test_intersection(self):
        r = rot.from_rotvec([45, 0, 0], degrees=True)

        # Define plane
        plane_n = np.array([0, 0, 1])
        plane_p = np.array([0, 0, 20])  # Any point on the plane

        # Define ray
        ray_dir = r.apply([0, 0, 1])  # np.array([0, -1, -1])
        ray_origin = np.array([0, 0, 0])  # Any point along the ray

        ret = pynibs.intersection_vec_plan(ray_dir, ray_origin, plane_n, plane_p, eps=1e-6)
        assert np.all(np.isclose(np.array([0., -20., 20.]), np.array(ret)))


if __name__ == '__main__':
    unittest.main()
