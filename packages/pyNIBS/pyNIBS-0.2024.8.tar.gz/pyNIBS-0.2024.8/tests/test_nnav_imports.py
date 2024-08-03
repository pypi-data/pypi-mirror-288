import unittest
import numpy as np
import pynibs

class TestPyNIBSLocalite(unittest.TestCase):
    def setUp(self):
        # Set up any necessary paths to your .xml files here
        self.valid_im_path = f"{pynibs.__testdatadir__}/InstrumentMarker20200225163611937.xml"
        self.valid_tm_path = f"{pynibs.__testdatadir__}/TriggerMarkers_Coil1_20200225170337572.xml"
        self.im_test = np.array([[[  0.9013614 ,   0.29839201,  -0.3138959 , -71.18429093],
                                  [  0.38530408,  -0.8834528 ,   0.26659466, -79.95375675],
                                  [ -0.19776044,  -0.36123975,  -0.91127244,  38.69342634],
                                  [  0.        ,   0.        ,   0.        ,   1.        ]]])
        self.self_tm_0 = np.array([[  0.89563849,   0.37653939,  -0.2367116 , -71.16214655],
                                   [  0.42635749,  -0.87839562,   0.21592364, -75.74648256],
                                   [ -0.12662378,  -0.29431584,  -0.94727356,  38.65814855],
                                   [  0.        ,   0.        ,   0.        ,   1.        ]])

    # def test_get_instrument_marker_valid(self):
    #     # Test get_instrument_marker with valid input
    #     final_arr, marker_description = pynibs.localite.get_instrument_marker(self.valid_im_path)
    #     # Assert expected result here
    #     assert np.isclose(final_arr, self.im_test).all()
    #     assert np.array(marker_description) == np.array(['test'])
    #
    # def test_get_instrument_marker_list(self):
    #     # Test get_instrument_marker with a list of valid paths
    #     final_arr, marker_description = pynibs.localite.get_instrument_marker([self.valid_im_path, self.valid_im_path])
    #     # Assert expected result here
    #     assert len(final_arr) == len(marker_description) == 2
    #     assert np.isclose(final_arr[0], self.im_test).all()
    #     assert np.isclose(final_arr[1], self.im_test).all()
    #     assert np.array(marker_description[0]) == np.array(['test'])
    #     assert np.array(marker_description[1]) == np.array(['test'])

    def test_get_marker_valid(self):
        # Test get_marker with valid parameters
        final_arr, marker_description, times = pynibs.localite.get_marker(self.valid_im_path, 'InstrumentMarker')
        # Assert expected result here
        assert np.isclose(final_arr, self.im_test).all()
        assert np.array(marker_description) == np.array(['test'])
        assert times == []

    def test_read_triggermarker_localite_valid(self):
        # Test read_triggermarker_localite with valid input
        m_nnav, didt, mso, descr, rec_time = pynibs.localite.read_triggermarker_localite(self.valid_tm_path)

        assert m_nnav.shape == (4,4,400)
        assert np.isclose(self.self_tm_0, m_nnav[:,:,0]).all()

        assert len(didt) == 400
        assert (didt[:2] == np.array([1,4])).all()

        assert len(mso) == 400
        assert (mso[:2] == np.array([3, 6])).all()

        assert len(descr) == 400

        assert len(rec_time) == 400
        assert rec_time[:3] == ['475056', '475251', '475450']


class TestReadTargetsBrainsight(unittest.TestCase):
    def setUp(self):
        # Prepare a valid test file
        self.valid_file = f"{pynibs.__testdatadir__}/brainsight_niiImage_nifticoord.txt"
        self.target0 = np.array([[-9.9700e-01,  5.3000e-02,  5.9000e-02,  1.5020e+01],
                                 [-5.6000e-02, -9.9700e-01, -4.4000e-02,  5.3062e+01],
                                 [ 5.6000e-02, -4.8000e-02,  9.9700e-01,  8.7219e+01],
                                 [ 0.0000e+00,  0.0000e+00,  0.0000e+00,  1.0000e+00]])

        self.sample0 = np.array([[ 7.1200e-01,  3.2100e-01, -6.2400e-01, -4.4198e+01],
                                 [ 1.3000e-02,  8.8300e-01,  4.6900e-01,  7.5810e+01],
                                 [ 7.0200e-01, -3.4200e-01,  6.2400e-01,  6.5742e+01],
                                 [ 0.0000e+00,  0.0000e+00,  0.0000e+00,  1.0000e+00]])

    def test_read_targets_brainsight(self):
        # Test reading from a valid file
        result = pynibs.brainsight.read_targets_brainsight(self.valid_file)
        assert len(result) == 4
        assert np.isclose(self.target0, result[:,:,0]).all()
        self.assertEqual(result.shape, (4, 4, 7))  # Expecting one target with a 4x4 matrix


    def test_get_marker_targets(self):
        # Test reading from a valid file
        matsimnibs, description, timings = pynibs.brainsight.get_marker(self.valid_file, markertype='Targets')
        assert matsimnibs.shape == (7,4,4)
        assert np.isclose(self.target0, matsimnibs[0,:,:]).all()


    def test_get_marker_samples(self):
        # Test reading from a valid file
        matsimnibs, description, timings = pynibs.brainsight.get_marker(self.valid_file, markertype='Samples')
        assert matsimnibs.shape == (101,4,4)
        assert matsimnibs.shape[0] == len(description) == len(timings)
        assert np.isclose(self.sample0, matsimnibs[0,:,:]).all()


if __name__ == '__main__':
    unittest.main()