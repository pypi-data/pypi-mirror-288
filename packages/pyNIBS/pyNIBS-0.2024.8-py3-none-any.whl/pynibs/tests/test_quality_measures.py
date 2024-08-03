import gdist
import pynibs
import unittest
import numpy as np


class TestGeodesicDist(unittest.TestCase):
    """
    Test pynibs.quality_measures.geodesic_dist()
    """
    nodes1 = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
    tris1 = np.array([[0, 1, 2]])
    nodes2 = np.array([[0, 0, 0], [1, 1, 1], [5, 2, 0], [5, 3, 5]])
    tris2 = np.array([[0, 1, 2], [1, 2, 3]])
    source_node = np.array([0])
    source_tri = 1
    source_is_node_node = True
    source_is_node_tri = False

    def test_geodesic_dist_node(self):
        # Test case 1: source is a node
        nodes_dist, tris_dist = pynibs.geodesic_dist(self.nodes1, self.tris1, self.source_node,
                                                     self.source_is_node_node)

        assert isinstance(nodes_dist, np.ndarray)
        assert isinstance(tris_dist, np.ndarray)
        assert np.allclose(nodes_dist, [0, np.sqrt(3), 2 * np.sqrt(3)])
        assert np.allclose(tris_dist, [np.sqrt(3)])

    '''
    # doesn't work yet:
    def test_geodesic_dist_tri(self):  
        # Test case 2: source is a triangle
        nodes_dist, tris_dist = pynibs.geodesic_dist(self.nodes2, self.tris2, self.source_tri, self.source_is_node_tri)

        assert isinstance(nodes_dist, np.ndarray)
        assert isinstance(tris_dist, np.ndarray)
        assert np.allclose(nodes_dist, ?)
        assert np.allclose(tris_dist, ?)
    '''


class TestEuclideanDist(unittest.TestCase):
    """
    Test pynibs.quality_measures.euclidean_dist()
    """
    nodes = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3]])
    tris = np.array([[0, 1, 2], [1, 2, 3]])
    source_node = np.array([0])
    source_tri = np.array([0])
    source_is_node_node = True
    source_is_node_tri = False

    def test_euclidean_dist_node(self):
        # Test case 1: source is a node
        nodes_dist, tris_dist = pynibs.euclidean_dist(self.nodes[:-1], self.tris[:-1], self.source_node,
                                                      self.source_is_node_node)

        assert isinstance(nodes_dist, np.ndarray)
        assert isinstance(tris_dist, np.ndarray)
        assert np.allclose(nodes_dist, [0, np.sqrt(3), 2 * np.sqrt(3)])
        assert np.allclose(tris_dist, [np.sqrt(3)])

    '''
    doesnt work yet:
    def test_euclidean_dist_tri(self):
        # Test case 2: source is a triangle
        nodes_dist, tris_dist = pynibs.euclidean_dist(self.nodes, self.tris, self.source_tri, self.source_is_node_tri)

        assert isinstance(nodes_dist, np.ndarray)
        assert isinstance(tris_dist, np.ndarray)
        assert np.allclose(nodes_dist, [0, np.sqrt(3), 2 * np.sqrt(3), 3 * np.sqrt(3)])
        assert np.allclose(tris_dist, [0, np.sqrt(3)])
    '''


class TestIntersectionVecPlan(unittest.TestCase):

    def test_direct_intersection(self):
        ray_dir = np.array([0, 0, -1])
        ray_origin = np.array([0, 0, 10])
        plane_n = np.array([0, 0, 1])
        plane_p = np.array([0, 0, 0])
        expected_intersection = np.array([0, 0, 0])
        intersec = pynibs.intersection_vec_plan(ray_dir, ray_origin, plane_n, plane_p)
        np.testing.assert_array_almost_equal(intersec, expected_intersection)

    def test_parallel_no_intersection(self):
        ray_dir = np.array([0, 1, 0])
        ray_origin = np.array([0, 0, 10])
        plane_n = np.array([0, 0, 1])
        plane_p = np.array([0, 0, 0])
        intersec = pynibs.intersection_vec_plan(ray_dir, ray_origin, plane_n, plane_p)
        assert (intersec == [np.inf, np.inf, np.inf]).all()

    def test_origin_within_plane(self):
        ray_dir = np.array([0, 0, 1])
        ray_origin = np.array([0, 0, 0])
        plane_n = np.array([0, 0, 1])
        plane_p = np.array([0, 0, 0])
        expected_intersection = np.array([0, 0, 0])
        intersec = pynibs.intersection_vec_plan(ray_dir, ray_origin, plane_n, plane_p)
        np.testing.assert_array_almost_equal(intersec, expected_intersection)

    def test_edge_case_near_parallel(self):
        ray_dir = np.array([0.001, 0.001, -1])
        ray_origin = np.array([0, 0, 10])
        plane_n = np.array([0, 0, 1])
        plane_p = np.array([0, 0, 0])
        # Expected intersection is approximate due to near parallel direction
        expected_intersection = np.array([0.01, 0.01, 0])
        intersec = pynibs.intersection_vec_plan(ray_dir, ray_origin, plane_n, plane_p)
        np.testing.assert_array_almost_equal(intersec, expected_intersection, decimal=2)


if __name__ == '__main__':
    unittest.main()
