import unittest
import pynibs
import numpy as np
from scipy.spatial.transform import Rotation as R


class TestUtilsRotationsbases2rotmat(unittest.TestCase):
    mat = np.array(([1., 0., 0., 0.],
                    [0., 1., 0., 0.],
                    [0., 0., 1., 0.],
                    [10., 20., 30., 1.])).T

    def test_bases2rotmat(self):
        v1 = np.array(([0, 0, 1], [0, 1, 0], [1, 0, 0]))
        v2 = np.array(([1, 0, 0], [0, 1, 0], [0, 0, 1]))
        res = R.from_matrix(pynibs.bases2rotmat(v1, v2)).as_euler('xyz', degrees=True)
        assert (res == np.array([180., 0., 180.])).all()

    def test_roatate_matsimnibs_euler_no_rot(self):
        for axis in ['x', 'y', 'z']:
            assert (self.mat == pynibs.rotate_matsimnibs_euler(axis=axis, angle=0, matsimnibs=self.mat,
                                                               metric='rad')).all()
            assert (self.mat == pynibs.rotate_matsimnibs_euler(axis=axis, angle=0, matsimnibs=self.mat,
                                                               metric='deg')).all()

            assert np.allclose(
                    pynibs.rotate_matsimnibs_euler(axis=axis, angle=2 * np.pi, matsimnibs=self.mat, metric='rad'),
                    self.mat)
            assert np.allclose(pynibs.rotate_matsimnibs_euler(axis=axis, angle=360, matsimnibs=self.mat, metric='deg'),
                               self.mat)

    def test_identity(self):
        # Test if the function returns identity matrix for the same input
        identity = np.eye(3)
        result = pynibs.bases2rotmat(identity, identity)
        np.testing.assert_array_almost_equal(result, identity)

    def test_rotation(self):
        # Test if the function correctly calculates rotation matrix
        rot = R.from_euler('xyz', [80, 0, 0], degrees=True)
        base = np.eye(3)
        target = rot.as_matrix()
        result = pynibs.bases2rotmat(target, base)
        np.testing.assert_array_almost_equal(result, target)

    def test_rotate_matsimnibs_euler_180(self):
        assert np.allclose(pynibs.rotate_matsimnibs_euler(axis='x', angle=np.pi, matsimnibs=self.mat, metric='rad'),
                           np.array([[1., 0., 0., 10.],
                                     [0., -1., -0., 20.],
                                     [0., 0., -1., 30.],
                                     [0., 0., 0., 1.]])
                           )
        assert np.allclose(pynibs.rotate_matsimnibs_euler(axis='y', angle=np.pi, matsimnibs=self.mat, metric='rad'),
                           np.array([[-1., 0., 0., 10.],
                                     [0., 1., 0., 20.],
                                     [-0., 0., -1., 30.],
                                     [0., 0., 0., 1.]]))
        assert np.allclose(pynibs.rotate_matsimnibs_euler(axis='z', angle=np.pi, matsimnibs=self.mat, metric='rad'),
                           np.array([[-1., -0., 0., 10.],
                                     [0., -1., 0., 20.],
                                     [0., 0., 1., 30.],
                                     [0., 0., 0., 1.]]))


class TestUtilsRotationsrotmatfromvecs(unittest.TestCase):
    def test_rotmat_from_vecs(self):
        vec1 = np.array([1, 0, 0])
        vec2 = np.array([0, 1, 0])
        expected_result = R.from_euler('z', 90, degrees=True)
        result = pynibs.rotmat_from_vecs(vec1, vec2)
        np.testing.assert_array_almost_equal(result.as_matrix(), expected_result.as_matrix())


class TestUtilsRotationsrotMattoEulerAngles(unittest.TestCase):
    def test_rotation_matrix_to_euler_angles(self):
        # Define some Euler angles
        euler_angles = np.array([np.pi / 2, np.pi / 3, np.pi / 4])

        # Convert the Euler angles to a rotation matrix
        rotation_matrix = pynibs.euler_angles_to_rotation_matrix(euler_angles)

        # Pass the rotation matrix to the function and get the output Euler angles
        output_euler_angles = pynibs.rotation_matrix_to_euler_angles(rotation_matrix)

        # Check that the output Euler angles match the original Euler angles
        np.testing.assert_array_almost_equal(output_euler_angles, euler_angles)
