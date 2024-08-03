import os
import h5py
import pynibs
import unittest
import tempfile
import numpy as np
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
try:
    import simnibs
except ImportError:
    raise unittest.SkipTest("Cannot import SimNIBS - skipping test_coil.py")


def check_xml(xml_fn):
    """Check well-formedness of xml"""
    parser = make_parser()
    parser.setContentHandler(ContentHandler())
    parser.parse(xml_fn)


class TestCreateStimsiteFromTmslist(unittest.TestCase):
    """
    Test pynibs.coil.create_stimsite_from_tmslist()
    """
    folder = tempfile.TemporaryDirectory()
    pos1 = np.array(([11, 12, 13, 14],
                     [21, 22, 23, 24],
                     [31, 32, 33, 34],
                     [41, 42, 43, 44]))
    pos1 = pos1.transpose()
    pos2 = np.array(([110, 120, 130, 140],
                     [210, 220, 230, 240],
                     [310, 320, 330, 340],
                     [410, 420, 430, 440]))
    pos2 = pos2.transpose()

    def test_create_stimsite_from_tmslist1_pos(self):
        with tempfile.TemporaryDirectory() as folder:
            pos1 = simnibs.sim_struct.POSITION()
            pos1.matsimnibs = self.pos1
            tmslist = simnibs.sim_struct.TMSLIST()
            tmslist.add_position(pos1)
            fn_hdf = os.path.join(folder, "stimsite_from_list.hdf5")
            pynibs.create_stimsite_from_tmslist(fn_hdf, tmslist, datanames=None, data=None, overwrite=False)
            assert os.path.exists(fn_hdf)
            assert os.path.exists(fn_hdf.replace('.hdf5', '.xdmf'))
            check_xml(fn_hdf.replace('.hdf5', '.xdmf'))
            with h5py.File(fn_hdf, 'r')as h:
                for idx, k in enumerate(['m0', 'm1', 'm2', 'centers', 'matsimnibs']):
                    assert k in h.keys(), f"{k} missing in {fn_hdf}"
                    if k != 'matsimnibs':
                        assert h[k][:].shape == (1, 3), f"Wrong shape for {k}: {h[k][:].shape}"
                        assert (h[k][:] == self.pos1[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"

    def test_create_stimsite_from_tmslist1_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            pos1 = simnibs.sim_struct.POSITION()
            pos1.matsimnibs = self.pos1
            tmslist = simnibs.sim_struct.TMSLIST()
            tmslist.add_position(pos1)
            fn_hdf = os.path.join(folder, "stimsite_from_list.hdf5")
            pynibs.create_stimsite_from_tmslist(fn_hdf, tmslist, datanames=None, data=None, overwrite=False)
            assert os.path.exists(fn_hdf)
            assert os.path.exists(fn_hdf.replace('.hdf5', '.xdmf'))

            # raise error if overwrite=False
            with self.assertRaises(OSError):
                pynibs.create_stimsite_from_tmslist(fn_hdf, tmslist, datanames=None, data=None, overwrite=False)

            # let's write a different file to make sure the correct one is written
            pos2 = simnibs.sim_struct.POSITION()
            pos2.matsimnibs = self.pos2
            tmslist = simnibs.sim_struct.TMSLIST()
            tmslist.add_position(pos2)
            pynibs.create_stimsite_from_tmslist(fn_hdf, tmslist, datanames=None, data=None, overwrite=True)
            check_xml(fn_hdf.replace('.hdf5', '.xdmf'))
            with h5py.File(fn_hdf, 'r')as h:
                for idx, k in enumerate(['m0', 'm1', 'm2', 'centers', 'matsimnibs']):
                    assert k in h.keys(), f"{k} missing in {fn_hdf}"
                    if k != 'matsimnibs':
                        assert h[k][:].shape == (1, 3), f"Wrong shape for {k}: {h[k][:].shape}"
                        assert (h[k][:] == self.pos2[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"

    def test_create_stimsite_from_tmslist_2pos(self):
        with tempfile.TemporaryDirectory() as folder:
            pos1 = simnibs.sim_struct.POSITION()
            pos1.matsimnibs = self.pos1
            pos2 = simnibs.sim_struct.POSITION()
            pos2.matsimnibs = self.pos2
            tmslist = simnibs.sim_struct.TMSLIST()
            tmslist.add_position(pos1)
            tmslist.add_position(pos2)

            fn_hdf = os.path.join(folder, "stimsite_from_list.hdf5")
            pynibs.create_stimsite_from_tmslist(fn_hdf, tmslist, datanames=None, data=None, overwrite=False)

            assert os.path.exists(fn_hdf)
            assert os.path.exists(fn_hdf.replace('.hdf5', '.xdmf'))
            check_xml(fn_hdf.replace('.hdf5', '.xdmf'))
            with h5py.File(fn_hdf, 'r')as h:
                for idx, k in enumerate(['m0', 'm1', 'm2', 'centers', 'matsimnibs']):
                    assert k in h.keys(), f"{k} missing in {fn_hdf}"
                    if k != 'matsimnibs':
                        assert h[k][:].shape == (2, 3), f"Wrong shape for {k}: {h[k][:].shape}"
                        assert (h[k][:][0, :] == self.pos1[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"
                        assert (h[k][:][1, :] == self.pos2[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"

    def test_create_stimsite_from_tmslist1_datanames(self):
        with tempfile.TemporaryDirectory() as folder:
            pos1 = simnibs.sim_struct.POSITION()
            pos1.matsimnibs = self.pos1
            tmslist = simnibs.sim_struct.TMSLIST()
            tmslist.add_position(pos1)
            fn_hdf = os.path.join(folder, "stimsite_from_list.hdf5")
            datanames = 'somedata'
            data = np.array(1)
            with self.assertRaises(AssertionError):
                pynibs.create_stimsite_from_tmslist(fn_hdf, tmslist, datanames=['1', '2'], data=data,
                                                    overwrite=False)
            with self.assertRaises(ValueError):
                pynibs.create_stimsite_from_tmslist(fn_hdf, tmslist, datanames=None, data=data, overwrite=False)
            with self.assertRaises(ValueError):
                pynibs.create_stimsite_from_tmslist(fn_hdf, tmslist, datanames=datanames, data=None, overwrite=False)

            pynibs.create_stimsite_from_tmslist(fn_hdf, tmslist, datanames=datanames, data=data, overwrite=False)
            assert os.path.exists(fn_hdf)
            assert os.path.exists(fn_hdf.replace('.hdf5', '.xdmf'))
            check_xml(fn_hdf.replace('.hdf5', '.xdmf'))
            with h5py.File(fn_hdf, 'r')as h:
                for idx, k in enumerate(['m0', 'm1', 'm2', 'centers', 'matsimnibs', 'data']):
                    assert k in h.keys(), f"{k} missing in {fn_hdf}"
                    if k == 'data':
                        assert h[f"{k}/somedata"][:] == np.array([1])
                    elif k != 'matsimnibs':
                        assert h[k][:].shape == (1, 3), f"Wrong shape for {k}: {h[k][:].shape}"
                        assert (h[k][:] == self.pos1[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"

            datanames = ['somedata']
            data = 1
            with self.assertRaises(AssertionError):
                pynibs.create_stimsite_from_tmslist(fn_hdf, tmslist, datanames=datanames, data=data, overwrite=True)
            data = np.array(1)
            pynibs.create_stimsite_from_tmslist(fn_hdf, tmslist, datanames=datanames, data=data, overwrite=True)
            assert os.path.exists(fn_hdf)
            assert os.path.exists(fn_hdf.replace('.hdf5', '.xdmf'))
            check_xml(fn_hdf.replace('.hdf5', '.xdmf'))
            with h5py.File(fn_hdf, 'r')as h:
                for idx, k in enumerate(['m0', 'm1', 'm2', 'centers', 'matsimnibs', 'data']):
                    assert k in h.keys(), f"{k} missing in {fn_hdf}"
                    if k == 'data':
                        assert h[f"{k}/somedata"][:] == np.array([1])
                    elif k != 'matsimnibs':
                        assert h[k][:].shape == (1, 3), f"Wrong shape for {k}: {h[k][:].shape}"
                        assert (h[k][:] == self.pos1[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"

    def test_create_stimsite_from_tmslist_2pos_2datanames(self):
        with tempfile.TemporaryDirectory() as folder:
            pos1 = simnibs.sim_struct.POSITION()
            pos1.matsimnibs = self.pos1
            pos2 = simnibs.sim_struct.POSITION()
            pos2.matsimnibs = self.pos2
            tmslist = simnibs.sim_struct.TMSLIST()
            tmslist.add_position(pos1)
            tmslist.add_position(pos2)
            datanames = ['somedata1', 'somedata2']
            data = np.array(([1, 2], [3, 4])).transpose()
            fn_hdf = os.path.join(folder, "stimsite_from_list.hdf5")
            pynibs.create_stimsite_from_tmslist(fn_hdf, tmslist, datanames=datanames, data=data, overwrite=False)

            assert os.path.exists(fn_hdf)
            assert os.path.exists(fn_hdf.replace('.hdf5', '.xdmf'))
            check_xml(fn_hdf.replace('.hdf5', '.xdmf'))
            with h5py.File(fn_hdf, 'r')as h:
                for idx, k in enumerate(['m0', 'm1', 'm2', 'centers', 'matsimnibs','data']):
                    assert k in h.keys(), f"{k} missing in {fn_hdf}"
                    if k == 'data':
                        h[k].keys()
                        assert (h[f"{k}/somedata1"][:] == np.array([1,2])).all()
                        assert (h[f"{k}/somedata2"][:] == np.array([3,4])).all()
                    elif k != 'matsimnibs':
                        assert h[k][:].shape == (2, 3), f"Wrong shape for {k}: {h[k][:].shape}"
                        assert (h[k][:][0, :] == self.pos1[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"
                        assert (h[k][:][1, :] == self.pos2[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"


class TestCreateStimsiteFromMatsimnibs(unittest.TestCase):
    """
    Test pynibs.coil.create_stimsite_from_matsimnibs()
    """
    folder = tempfile.TemporaryDirectory()
    pos1 = np.array(([11, 12, 13, 14],
                     [21, 22, 23, 24],
                     [31, 32, 33, 34],
                     [41, 42, 43, 44]))
    pos1 = pos1.transpose()
    pos2 = np.array(([110, 120, 130, 140],
                     [210, 220, 230, 240],
                     [310, 320, 330, 340],
                     [410, 420, 430, 440]))
    pos2 = pos2.transpose()

    def test_create_stimsite_from_matsimnibs_1pos(self):
        with tempfile.TemporaryDirectory() as folder:
            pos1 = simnibs.sim_struct.POSITION()
            pos1.matsimnibs = self.pos1
            fn_hdf = os.path.join(folder, "stimsite_from_list.hdf5")
            pynibs.create_stimsite_from_matsimnibs(fn_hdf, self.pos1, datanames=None, data=None, overwrite=False)
            assert os.path.exists(fn_hdf)
            assert os.path.exists(fn_hdf.replace('.hdf5', '.xdmf'))
            check_xml(fn_hdf.replace('.hdf5', '.xdmf'))
            with h5py.File(fn_hdf, 'r')as h:
                for idx, k in enumerate(['m0', 'm1', 'm2', 'centers', 'matsimnibs']):
                    assert k in h.keys(), f"{k} missing in {fn_hdf}"
                    if k != 'matsimnibs':
                        assert h[k][:].shape == (1, 3), f"Wrong shape for {k}: {h[k][:].shape}"
                        assert (h[k][:] == self.pos1[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"

    def test_create_stimsite_from_matsimnibs_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:

            fn_hdf = os.path.join(folder, "stimsite_from_list.hdf5")
            pynibs.create_stimsite_from_matsimnibs(fn_hdf, self.pos1, datanames=None, data=None, overwrite=False)
            assert os.path.exists(fn_hdf)
            assert os.path.exists(fn_hdf.replace('.hdf5', '.xdmf'))

            # raise error if overwrite=False
            with self.assertRaises(OSError):
                pynibs.create_stimsite_from_matsimnibs(fn_hdf, self.pos1, datanames=None, data=None, overwrite=False)

            # let's write a different file to make sure the correct one is written

            pynibs.create_stimsite_from_matsimnibs(fn_hdf, self.pos2, datanames=None, data=None, overwrite=True)
            check_xml(fn_hdf.replace('.hdf5', '.xdmf'))
            with h5py.File(fn_hdf, 'r')as h:
                for idx, k in enumerate(['m0', 'm1', 'm2', 'centers', 'matsimnibs']):
                    assert k in h.keys(), f"{k} missing in {fn_hdf}"
                    if k != 'matsimnibs':
                        assert h[k][:].shape == (1, 3), f"Wrong shape for {k}: {h[k][:].shape}"
                        assert (h[k][:] == self.pos2[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"

    def test_create_stimsite_from_matsimnibs_2pos(self):
        with tempfile.TemporaryDirectory() as folder:

            matsimnibs = np.dstack((self.pos1, self.pos2))
            fn_hdf = os.path.join(folder, "stimsite_from_list.hdf5")
            pynibs.create_stimsite_from_matsimnibs(fn_hdf, matsimnibs, datanames=None, data=None, overwrite=False)

            assert os.path.exists(fn_hdf)
            assert os.path.exists(fn_hdf.replace('.hdf5', '.xdmf'))
            check_xml(fn_hdf.replace('.hdf5', '.xdmf'))
            with h5py.File(fn_hdf, 'r')as h:
                for idx, k in enumerate(['m0', 'm1', 'm2', 'centers', 'matsimnibs']):
                    assert k in h.keys(), f"{k} missing in {fn_hdf}"
                    if k != 'matsimnibs':
                        assert h[k][:].shape == (2, 3), f"Wrong shape for {k}: {h[k][:].shape}"
                        assert (h[k][:][0, :] == self.pos1[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"
                        assert (h[k][:][1, :] == self.pos2[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"

    def test_create_stimsite_from_matsimnibs_datanames(self):
        with tempfile.TemporaryDirectory() as folder:
            fn_hdf = os.path.join(folder, "stimsite_from_list.hdf5")
            datanames = 'somedata'
            data = np.array(1)
            with self.assertRaises(AssertionError):
                pynibs.create_stimsite_from_matsimnibs(fn_hdf, self.pos1, datanames=['1', '2'], data=data,
                                                    overwrite=False)
            with self.assertRaises(ValueError):
                pynibs.create_stimsite_from_matsimnibs(fn_hdf, self.pos1, datanames=None, data=data, overwrite=False)
            with self.assertRaises(ValueError):
                pynibs.create_stimsite_from_matsimnibs(fn_hdf, self.pos1, datanames=datanames, data=None, overwrite=False)

            pynibs.create_stimsite_from_matsimnibs(fn_hdf, self.pos1, datanames=datanames, data=data, overwrite=False)
            assert os.path.exists(fn_hdf)
            assert os.path.exists(fn_hdf.replace('.hdf5', '.xdmf'))
            check_xml(fn_hdf.replace('.hdf5', '.xdmf'))
            with h5py.File(fn_hdf, 'r')as h:
                for idx, k in enumerate(['m0', 'm1', 'm2', 'centers', 'matsimnibs', 'data']):
                    assert k in h.keys(), f"{k} missing in {fn_hdf}"
                    if k == 'data':
                        assert h[f"{k}/somedata"][:] == np.array([1])
                    elif k != 'matsimnibs':
                        assert h[k][:].shape == (1, 3), f"Wrong shape for {k}: {h[k][:].shape}"
                        assert (h[k][:] == self.pos1[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"

            datanames = ['somedata']
            data = 1

            with self.assertRaises(AssertionError):
                pynibs.create_stimsite_from_matsimnibs(fn_hdf, self.pos1, datanames=datanames, data=data, overwrite=True)

            data = np.array(1)
            pynibs.create_stimsite_from_matsimnibs(fn_hdf, self.pos1, datanames=datanames, data=data, overwrite=True)

            assert os.path.exists(fn_hdf)
            assert os.path.exists(fn_hdf.replace('.hdf5', '.xdmf'))
            check_xml(fn_hdf.replace('.hdf5', '.xdmf'))
            with h5py.File(fn_hdf, 'r')as h:
                for idx, k in enumerate(['m0', 'm1', 'm2', 'centers', 'matsimnibs', 'data']):
                    assert k in h.keys(), f"{k} missing in {fn_hdf}"
                    if k == 'data':
                        assert h[f"{k}/somedata"][:] == np.array([1])
                    elif k != 'matsimnibs':
                        assert h[k][:].shape == (1, 3), f"Wrong shape for {k}: {h[k][:].shape}"
                        assert (h[k][:] == self.pos1[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"

    def test_create_stimsite_from_matsimnibs_2pos_2datanames(self):
        with tempfile.TemporaryDirectory() as folder:
            matsimnibs = np.dstack((self.pos1, self.pos2))
            datanames = ['somedata1', 'somedata2']
            data = np.array(([1, 2], [3, 4])).transpose()
            fn_hdf = os.path.join(folder, "stimsite_from_list.hdf5")
            pynibs.create_stimsite_from_matsimnibs(fn_hdf, matsimnibs, datanames=datanames, data=data, overwrite=False)

            assert os.path.exists(fn_hdf)
            assert os.path.exists(fn_hdf.replace('.hdf5', '.xdmf'))
            check_xml(fn_hdf.replace('.hdf5', '.xdmf'))
            with h5py.File(fn_hdf, 'r')as h:
                for idx, k in enumerate(['m0', 'm1', 'm2', 'centers', 'matsimnibs','data']):
                    assert k in h.keys(), f"{k} missing in {fn_hdf}"
                    if k == 'data':
                        h[k].keys()
                        assert (h[f"{k}/somedata1"][:] == np.array([1,2])).all()
                        assert (h[f"{k}/somedata2"][:] == np.array([3,4])).all()
                    elif k != 'matsimnibs':
                        assert h[k][:].shape == (2, 3), f"Wrong shape for {k}: {h[k][:].shape}"
                        assert (h[k][:][0, :] == self.pos1[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"
                        assert (h[k][:][1, :] == self.pos2[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"


class TestCreateStimsiteFromList(unittest.TestCase):
    """
    Test pynibs.coil.create_stimsite_from_list()
    """
    folder = tempfile.TemporaryDirectory()
    pos1 = np.array(([11, 12, 13, 14],
                     [21, 22, 23, 24],
                     [31, 32, 33, 34],
                     [41, 42, 43, 44]))
    pos1 = pos1.transpose()
    pos2 = np.array(([110, 120, 130, 140],
                     [210, 220, 230, 240],
                     [310, 320, 330, 340],
                     [410, 420, 430, 440]))
    pos2 = pos2.transpose()

    def test_create_stimsite_from_list_1pos(self):
        with tempfile.TemporaryDirectory() as folder:
            pos1 = simnibs.sim_struct.POSITION()
            pos1.matsimnibs = self.pos1
            fn_hdf = os.path.join(folder, "stimsite_from_list.hdf5")
            pynibs.create_stimsite_from_list(fn_hdf, [self.pos1], datanames=None, data=None, overwrite=False)
            assert os.path.exists(fn_hdf)
            assert os.path.exists(fn_hdf.replace('.hdf5', '.xdmf'))
            check_xml(fn_hdf.replace('.hdf5', '.xdmf'))
            with h5py.File(fn_hdf, 'r')as h:
                for idx, k in enumerate(['m0', 'm1', 'm2', 'centers', 'matsimnibs']):
                    assert k in h.keys(), f"{k} missing in {fn_hdf}"
                    if k != 'matsimnibs':
                        assert h[k][:].shape == (1, 3), f"Wrong shape for {k}: {h[k][:].shape}"
                        assert (h[k][:] == self.pos1[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"

    def test_create_stimsite_from_list_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:

            fn_hdf = os.path.join(folder, "stimsite_from_list.hdf5")
            pynibs.create_stimsite_from_list(fn_hdf, [self.pos1], datanames=None, data=None, overwrite=False)
            assert os.path.exists(fn_hdf)
            assert os.path.exists(fn_hdf.replace('.hdf5', '.xdmf'))

            # raise error if overwrite=False
            with self.assertRaises(OSError):
                pynibs.create_stimsite_from_list(fn_hdf, [self.pos1], datanames=None, data=None, overwrite=False)

            # let's write a different file to make sure the correct one is written

            pynibs.create_stimsite_from_list(fn_hdf, [self.pos2], datanames=None, data=None, overwrite=True)
            check_xml(fn_hdf.replace('.hdf5', '.xdmf'))
            with h5py.File(fn_hdf, 'r')as h:
                for idx, k in enumerate(['m0', 'm1', 'm2', 'centers', 'matsimnibs']):
                    assert k in h.keys(), f"{k} missing in {fn_hdf}"
                    if k != 'matsimnibs':
                        assert h[k][:].shape == (1, 3), f"Wrong shape for {k}: {h[k][:].shape}"
                        assert (h[k][:] == self.pos2[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"

    def test_create_stimsite_from_list_2pos(self):
        with tempfile.TemporaryDirectory() as folder:

            matsimnibs = [self.pos1, self.pos2]
            fn_hdf = os.path.join(folder, "stimsite_from_list.hdf5")
            pynibs.create_stimsite_from_list(fn_hdf, matsimnibs, datanames=None, data=None, overwrite=False)

            assert os.path.exists(fn_hdf)
            assert os.path.exists(fn_hdf.replace('.hdf5', '.xdmf'))
            check_xml(fn_hdf.replace('.hdf5', '.xdmf'))
            with h5py.File(fn_hdf, 'r')as h:
                for idx, k in enumerate(['m0', 'm1', 'm2', 'centers', 'matsimnibs']):
                    assert k in h.keys(), f"{k} missing in {fn_hdf}"
                    if k != 'matsimnibs':
                        assert h[k][:].shape == (2, 3), f"Wrong shape for {k}: {h[k][:].shape}"
                        assert (h[k][:][0, :] == self.pos1[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"
                        assert (h[k][:][1, :] == self.pos2[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"

    def test_create_stimsite_from_list_datanames(self):
        with tempfile.TemporaryDirectory() as folder:
            fn_hdf = os.path.join(folder, "stimsite_from_list.hdf5")
            datanames = 'somedata'
            data = np.array(1)
            with self.assertRaises(AssertionError):
                pynibs.create_stimsite_from_list(fn_hdf, [self.pos1], datanames=['1', '2'], data=data,
                                                    overwrite=False)
            with self.assertRaises(ValueError):
                pynibs.create_stimsite_from_list(fn_hdf, [self.pos1], datanames=None, data=data, overwrite=False)
            with self.assertRaises(ValueError):
                pynibs.create_stimsite_from_list(fn_hdf, [self.pos1], datanames=datanames, data=None, overwrite=False)

            pynibs.create_stimsite_from_list(fn_hdf, [self.pos1], datanames=datanames, data=data, overwrite=False)
            assert os.path.exists(fn_hdf)
            assert os.path.exists(fn_hdf.replace('.hdf5', '.xdmf'))
            check_xml(fn_hdf.replace('.hdf5', '.xdmf'))
            with h5py.File(fn_hdf, 'r')as h:
                for idx, k in enumerate(['m0', 'm1', 'm2', 'centers', 'matsimnibs', 'data']):
                    assert k in h.keys(), f"{k} missing in {fn_hdf}"
                    if k == 'data':
                        assert h[f"{k}/somedata"][:] == np.array([1])
                    elif k != 'matsimnibs':
                        assert h[k][:].shape == (1, 3), f"Wrong shape for {k}: {h[k][:].shape}"
                        assert (h[k][:] == self.pos1[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"

            datanames = ['somedata']
            data = 1

            with self.assertRaises(AssertionError):
                pynibs.create_stimsite_from_list(fn_hdf, [self.pos1], datanames=datanames, data=data, overwrite=True)
            data = np.array(1)
            pynibs.create_stimsite_from_list(fn_hdf, [self.pos1], datanames=datanames, data=data, overwrite=True)
            assert os.path.exists(fn_hdf)
            assert os.path.exists(fn_hdf.replace('.hdf5', '.xdmf'))
            check_xml(fn_hdf.replace('.hdf5', '.xdmf'))
            with h5py.File(fn_hdf, 'r')as h:
                for idx, k in enumerate(['m0', 'm1', 'm2', 'centers', 'matsimnibs', 'data']):
                    assert k in h.keys(), f"{k} missing in {fn_hdf}"
                    if k == 'data':
                        assert h[f"{k}/somedata"][:] == np.array([1])
                    elif k != 'matsimnibs':
                        assert h[k][:].shape == (1, 3), f"Wrong shape for {k}: {h[k][:].shape}"
                        assert (h[k][:] == self.pos1[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"

    def test_create_stimsite_from_list_2pos_2datanames(self):
        with tempfile.TemporaryDirectory() as folder:
            matsimnibs = [self.pos1, self.pos2]
            datanames = ['somedata1', 'somedata2']
            data = np.array(([1, 2], [3, 4])).transpose()
            fn_hdf = os.path.join(folder, "stimsite_from_list.hdf5")
            pynibs.create_stimsite_from_list(fn_hdf, matsimnibs, datanames=datanames, data=data, overwrite=False)

            assert os.path.exists(fn_hdf)
            assert os.path.exists(fn_hdf.replace('.hdf5', '.xdmf'))
            check_xml(fn_hdf.replace('.hdf5', '.xdmf'))
            with h5py.File(fn_hdf, 'r')as h:
                for idx, k in enumerate(['m0', 'm1', 'm2', 'centers', 'matsimnibs','data']):
                    assert k in h.keys(), f"{k} missing in {fn_hdf}"
                    if k == 'data':
                        h[k].keys()
                        assert (h[f"{k}/somedata1"][:] == np.array([1,2])).all()
                        assert (h[f"{k}/somedata2"][:] == np.array([3,4])).all()
                    elif k != 'matsimnibs':
                        assert h[k][:].shape == (2, 3), f"Wrong shape for {k}: {h[k][:].shape}"
                        assert (h[k][:][0, :] == self.pos1[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"
                        assert (h[k][:][1, :] == self.pos2[:3, idx]).all(), f"Wrong values for {k}: {h[k][:]}"


if __name__ == '__main__':
    unittest.main()
