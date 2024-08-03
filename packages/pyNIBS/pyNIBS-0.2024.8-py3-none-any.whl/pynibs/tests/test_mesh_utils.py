import os
import pynibs
import unittest
import numpy as np


class TestFindNearest(unittest.TestCase):
    monot_arr = np.array([0, 1, 2, 3, 5, 10])
    nonmonot_arr = np.array([10, 0, 1, 2, 3, 5, 10])
    value = 5

    def test_01_find_nearest(self):
        idx = pynibs.find_nearest(array=self.monot_arr, value=self.value)
        assert idx == 4

    def test_02_find_nearest_fail(self):
        idx = pynibs.find_nearest(array=self.nonmonot_arr, value=self.value)
        assert idx == -1


class TestCalcSampleSphere(unittest.TestCase):
    mesh_hdf5_fn = os.path.join(pynibs.__testdatadir__, 'geo.hdf5')
    mesh = pynibs.load_mesh_hdf5(mesh_hdf5_fn)

    def test_01_sample_sphere_even(self):
        with self.assertRaises(AssertionError):
            pynibs.sample_sphere(n_points=10, r=10)

    def test_02_sample_sphere_odd(self):
        points = pynibs.sample_sphere(n_points=11, r=10)
        assert points.shape == (11, 3)


class TestCalcTriSurface(unittest.TestCase):
    mesh_hdf5_fn = os.path.join(pynibs.__testdatadir__, 'geo.hdf5')
    mesh = pynibs.load_mesh_hdf5(mesh_hdf5_fn)

    def test_01_calc_tri_volume(self):
        tri_surf = pynibs.calc_tri_surface(points=self.mesh.points[self.mesh.triangles])
        assert tri_surf.size == self.mesh.triangles.shape[0]
        assert (tri_surf > 0).all()


class TestCalcTetVolume(unittest.TestCase):
    mesh_hdf5_fn = os.path.join(pynibs.__testdatadir__, 'geo.hdf5')
    mesh = pynibs.load_mesh_hdf5(mesh_hdf5_fn)

    def test_01_calc_tet_volume_abs(self):
        tet_vol = pynibs.calc_tet_volume(points=self.mesh.points[self.mesh.tetrahedra])
        assert tet_vol.size == self.mesh.tetrahedra.shape[0]
        assert (tet_vol > 0).all()

    def test_02_calc_tet_volume_no_abs(self):
        tet_vol = pynibs.calc_tet_volume(points=self.mesh.points[self.mesh.tetrahedra],
                                         abs=False)
        assert tet_vol.size == self.mesh.tetrahedra.shape[0]
        assert (tet_vol < 0).any()


class TestGetSphere(unittest.TestCase):
    """
    Test pynibs.mesh.utils.* functions.
    """
    mesh_hdf5_fn = os.path.join(pynibs.__testdatadir__, 'geo.hdf5')
    target_empty = [10, 20, 30]
    target_full_tris = [0., 45.2227265, 71.97155693]
    target_full_tets = [9.51698047, 84.46553784, 0.]
    radius = 3

    def test_01_get_sphere_fails(self):
        # no mesh and no mesh_fn
        with self.assertRaises(AssertionError):
            pynibs.get_sphere(mesh=None,
                              mesh_fn=None,
                              target=self.target_empty,
                              radius=self.radius)

        # no target
        with self.assertRaises(AssertionError):
            pynibs.get_sphere(mesh=None, mesh_fn=self.mesh_hdf5_fn)

        # wrong element type
        with self.assertRaises(ValueError):
            # no radius, return nearest element
            pynibs.get_sphere(mesh=None,
                              mesh_fn=self.mesh_hdf5_fn,
                              target=self.target_empty,
                              elmtype='square')

    def test_02_get_sphere_nearest_tri(self):
        # no radius, return nearest element
        nearest_elm = pynibs.get_sphere(mesh=None,
                                        mesh_fn=self.mesh_hdf5_fn,
                                        target=self.target_empty)
        assert nearest_elm == 681

        nearest_elm = pynibs.get_sphere(mesh=None,
                                        mesh_fn=self.mesh_hdf5_fn,
                                        target=self.target_empty,
                                        elmtype='Triangle')
        assert nearest_elm == 681

    def test_02_get_sphere_nearest_tet(self):
        # no radius, return nearest element
        nearest_elm = pynibs.get_sphere(mesh=None,
                                        mesh_fn=self.mesh_hdf5_fn,
                                        target=self.target_empty,
                                        elmtype='tets')
        assert nearest_elm == 20232

        nearest_elm = pynibs.get_sphere(mesh=None,
                                        mesh_fn=self.mesh_hdf5_fn,
                                        target=self.target_empty,
                                        elmtype='Tetrahedron')
        assert nearest_elm == 20232

        # return sphere, but should be empty
        sphere_empty = pynibs.get_sphere(mesh=None,
                                         mesh_fn=self.mesh_hdf5_fn,
                                         target=self.target_empty,
                                         radius=5)
        assert sphere_empty.size == 0

    def test_02_get_sphere_tris(self):
        # return tri sphere, should not be empty
        sphere_full_tris = pynibs.get_sphere(mesh=None,
                                             mesh_fn=self.mesh_hdf5_fn,
                                             target=self.target_full_tris,
                                             radius=10)
        assert sphere_full_tris.size == 13

    def test_03_get_sphere_tets(self):
        # return tet sphere, should not be empty
        sphere_full_tets = pynibs.get_sphere(mesh=None,
                                             mesh_fn=self.mesh_hdf5_fn,
                                             target=self.target_full_tets,
                                             radius=10,
                                             elmtype='tets')
        assert sphere_full_tets.size == 50


if __name__ == '__main__':
    unittest.main()
