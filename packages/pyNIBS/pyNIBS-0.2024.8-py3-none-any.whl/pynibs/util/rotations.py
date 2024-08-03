"""Some helper functions to take care of geometric rotations"""
import math
import numpy as np
from scipy.spatial.transform import Rotation


def normalize_rot(rot):
    """
    Normalize rotation matrix.

    Parameters
    ----------
    rot : np.ndarray of float
        (3, 3) Rotation matrix.

    Returns
    -------
    rot_norm : np.ndarray of float
        (3, 3) Normalized rotation matrix.
    """
    q = rot_to_quat(rot)
    q /= np.sqrt(np.sum(q ** 2))
    return quat_to_rot(q)


def quat_rotation_angle(q):
    """
    Computes the rotation angle from the quaternion in rad.

    Parameters
    ----------
    q : np.ndarray of float
        Quaternion, either only the imaginary part (length=3) [qx, qy, qz]
        or the full quaternion (length=4) [qw, qx, qy, qz].

    Returns
    -------
    alpha : float
        Rotation angle of quaternion in rad.
    """

    if len(q) == 3:
        return 2 * np.arcsin(np.linalg.norm(q))
    elif len(q) == 4:
        return q[0]
    else:
        raise ValueError('Please check size of quaternion')


def quat_to_rot(q):
    """
    Computes the rotation matrix from quaternions.

    Parameters
    ----------
    q : np.ndarray of float
        Quaternion, either only the imaginary part (length=3) or the full quaternion (length=4).

    Returns
    -------
    rot : np.ndarray of float
        (3, 3) Rotation matrix, containing the x, y, z axis in the columns.
    """
    if q.size == 3:
        q = np.hstack([np.sqrt(1 - np.sum(q ** 2)), q])
    rot = np.array([[q[0] ** 2 + q[1] ** 2 - q[2] ** 2 - q[3] ** 2, 2 * (q[1] * q[2] - q[0] * q[3]),
                     2 * (q[1] * q[3] + q[0] * q[2])],
                    [2 * (q[2] * q[1] + q[0] * q[3]), q[0] ** 2 - q[1] ** 2 + q[2] ** 2 - q[3] ** 2,
                     2 * (q[2] * q[3] - q[0] * q[1])],
                    [2 * (q[3] * q[1] - q[0] * q[2]), 2 * (q[3] * q[2] + q[0] * q[1]),
                     q[0] ** 2 - q[1] ** 2 - q[2] ** 2 + q[3] ** 2]])
    return rot


def rot_to_quat(rot):
    """
    Computes the quaternions from rotation matrix
    (see e.g. https://www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToQuaternion/).

    Parameters
    ----------
    rot : np.ndarray of float
        (3, 3) Rotation matrix, containing the x, y, z axis in the columns.

    Returns
    -------
    q : np.ndarray of float
        Quaternion, full (length=4).
    """

    rot = rot.flatten()
    t = 1. + rot[0] + rot[4] + rot[8]
    if t > np.finfo(rot.dtype).eps:
        s = np.sqrt(t) * 2.
        qx = (rot[7] - rot[5]) / s
        qy = (rot[2] - rot[6]) / s
        qz = (rot[3] - rot[1]) / s
        qw = 0.25 * s
    elif rot[0] > rot[4] and rot[0] > rot[8]:
        s = np.sqrt(1. + rot[0] - rot[4] - rot[8]) * 2.
        qx = 0.25 * s
        qy = (rot[1] + rot[3]) / s
        qz = (rot[2] + rot[6]) / s
        qw = (rot[7] - rot[5]) / s
    elif rot[4] > rot[8]:
        s = np.sqrt(1. - rot[0] + rot[4] - rot[8]) * 2
        qx = (rot[1] + rot[3]) / s
        qy = 0.25 * s
        qz = (rot[5] + rot[7]) / s
        qw = (rot[2] - rot[6]) / s
    else:
        s = np.sqrt(1. - rot[0] - rot[4] + rot[8]) * 2.
        qx = (rot[2] + rot[6]) / s
        qy = (rot[5] + rot[7]) / s
        qz = 0.25 * s
        qw = (rot[3] - rot[1]) / s
    return np.array((qw, qx, qy, qz))


def quaternion_conjugate(q):
    """
    https://stackoverflow.com/questions/15425313/inverse-quaternion

    :param q:
    :type q:
    :return:
    :rtype:
    """
    return np.array((-q[0], -q[1], -q[2]))


def quaternion_inverse(q):
    """
    Compute the inverse of a quaternion.

    The inverse of a quaternion is computed by taking the conjugate of the quaternion and dividing it by the norm of
    the quaternion.
    https://stackoverflow.com/questions/15425313/inverse-quaternion

    Parameters
    ----------
    q : np.ndarray
        Input quaternion.

    Returns
    -------
    np.ndarray
        Inverse of the input quaternion.
    """
    return quaternion_conjugate(q) / np.linalg.norm(q)


def quaternion_diff(q1, q2):
    """
    https://math.stackexchange.com/questions/2581668/
    error-measure-between-two-rotations-when-one-matrix-might-not-be-a-valid-rotatio

    Parameters
    ----------
    q1 : np.ndarray
        Quaternion 1.
    q2 : np.ndarray
        Quaternion 2.

    Returns
    -------
    float
        Difference between the two quaternions.
    """
    return np.linalg.norm(q1 * quaternion_inverse(q2) - 1)


def euler_angles_to_rotation_matrix(theta):
    """
    Determines the rotation matrix from the three Euler angles theta = [Psi, Theta, Phi] (in rad), which rotate the
    coordinate system in the order z, y', x''.

    Parameters
    ----------
    theta : np.ndarray
        (3) Euler angles in rad.

    Returns
    -------
    r : np.ndarray
        (3) Rotation matrix (z, y', x'').
    """

    # theta in rad
    r_x = np.array([[1., 0., 0.],
                    [0., math.cos(theta[0]), -math.sin(theta[0])],
                    [0., math.sin(theta[0]), math.cos(theta[0])]
                    ])

    r_y = np.array([[math.cos(theta[1]), 0, math.sin(theta[1])],
                    [0., 1., 0.],
                    [-math.sin(theta[1]), 0, math.cos(theta[1])]
                    ])

    r_z = np.array([[math.cos(theta[2]), -math.sin(theta[2]), 0],
                    [math.sin(theta[2]), math.cos(theta[2]), 0],
                    [0., 0., 1.]
                    ])

    r = np.dot(r_z, np.dot(r_y, r_x))

    return r


def rotation_matrix_to_euler_angles(r):
    """
    Calculates the euler angles theta = [Psi, Theta, Phi] (in rad) from the rotation matrix R which, rotate the
    coordinate system in the order z, y', x'' (https://www.learnopencv.com/rotation-matrix-to-euler-angles/).

    Parameters
    ----------
    r : np.ndarray
        (3, 3) Rotation matrix (z, y', x'').

    Returns
    -------
    theta : np.ndarray
        (3) Euler angles in rad.
    """
    sy = math.sqrt(r[0, 0] * r[0, 0] + r[1, 0] * r[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(r[2, 1], r[2, 2])
        y = math.atan2(-r[2, 0], sy)
        z = math.atan2(r[1, 0], r[0, 0])
    else:
        x = math.atan2(-r[1, 2], r[1, 1])
        y = math.atan2(-r[2, 0], sy)
        z = 0

    return np.array([x, y, z])


def bases2rotmat(v1, v2):
    """
    Computes rotation matrix to rotate basis 1 (``v1``) to another basis (``v2``).

    Parameters
    ----------
    v1 : np.ndarray
        (3, 3) original basis.
    v2 : np.ndarray
        (3, 3) rotated basis.

    Returns
    -------
    rot_mat : np.ndarray
        (3, 3) rotation matrix to go from v1 to v2.
    """
    return np.linalg.solve(v1, v2).T


def rotate_matsimnibs_euler(axis, angle, matsimnibs, metric='rad'):
    """
    Rotates a matsimnibs matrix around ``axis`` by ``angle``.

    Parameters
    ----------
    axis : str
        One of ('x','y','z').
    angle : float
        Angle to rotate system around ``axis``.
    matsimnibs : np.ndarray
        (4, 4) SimNIBS matsimnibs coil orientation and position matrix.
    metric : str, default: 'rad'
        One of ('rad', 'deg'). If ``deg``, ``angle`` is transformed to radians.

    Returns
    -------
    rotated_matsimnibs : np.ndarray
        (4, 4) Rotated system.
    """

    if metric.lower().startswith('deg'):
        angle = np.deg2rad(angle)
    elif not metric.lower().startswith('rad'):
        raise Exception(ValueError)

    if axis == 'x':
        # rotate around x
        rotated_system = np.array((
            (1, 0, 0),
            (0, np.cos(angle), -np.sin(angle)),
            (0, np.sin(angle), np.cos(angle)),
        ))

    elif axis == 'y':
        # rotate around y
        rotated_system = np.array((
            (np.cos(angle), 0, np.sin(angle)),
            (0, 1, 0),
            (-np.sin(angle), 0, np.cos(angle)),
        ))
    elif axis == 'z':
        # rotate aroun z
        rotated_system = np.array((
            (np.cos(angle), -np.sin(angle), 0),
            (np.sin(angle), np.cos(angle), 0),
            (0, 0, 1),
        ))
    else:
        raise Exception(ValueError)

    rot_vecs = matsimnibs[0:3, :3].dot(rotated_system)

    return np.vstack((np.hstack((rot_vecs,
                                 matsimnibs[:3, 3, None])),
                      [0, 0, 0, 1]))


def rotmat_from_vecs(vec1, vec2):
    """
    Find the rotation matrix that aligns vec1 to vec2

    Parameters
    ----------
    vec 1: np.ndarray
        A 3D vector ('source').
    vec 2: np.ndarray
        A 3D vector ('destination').

    Returns
    -------
    rot_mat: scipy.Rotation
    A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return Rotation.from_matrix(rotation_matrix)
