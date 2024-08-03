import unittest
import tempfile
import pynibs
import sys
import shutil
import os


class TestSubject(unittest.TestCase):
    """
    Test pynibs.subject.* functions.
    """
    subject_id = 'testsub'
    mesh_names = ['charm_refm1_sm', 'headreco', 'headreco_refined_m1']
    create_subject_fn = "create_subject_testsub.py"
    create_subject_fn_org = os.path.join(pynibs.__testdatadir__, create_subject_fn)

    # get temporary folder and move create_subject.py theree
    folder = tempfile.TemporaryDirectory()
    fn_create_subject = os.path.join(folder.name, create_subject_fn)
    fn_subject_object = os.path.join(folder.name, f"{subject_id}.hdf5")
    shutil.copyfile(create_subject_fn_org, fn_create_subject)

    def test_01_create_subject(self):
        cmd = f"{sys.executable} {self.fn_create_subject}"
        assert os.system(cmd) == 0, f"Creating subject failed"

    def test_02_load_subject(self):
        subject = pynibs.load_subject(self.fn_subject_object)
        for mesh_id in self.mesh_names:
            assert mesh_id in subject.mesh.keys(), f"{mesh_id} not found in {self.fn_subject_object}"

    def test_03_load_subject_h5(self):
        no_hdf5_suffix = os.path.join(self.folder.name, 'test.h5')
        shutil.copyfile(self.fn_subject_object, no_hdf5_suffix)
        with self.assertRaises(NotImplementedError):
            pynibs.load_subject(no_hdf5_suffix)
        subject = pynibs.load_subject(no_hdf5_suffix, filetype='hdf5')
        for mesh_id in self.mesh_names:
            assert mesh_id in subject.mesh.keys(), f"{mesh_id} not found in {self.fn_subject_object}"

    def test_04_save_subject(self):
        subject = pynibs.load_subject(self.fn_subject_object)
        fn_new = self.fn_subject_object.replace('.hdf5', '_new.hdf5')
        pynibs.save_subject(subject_id=self.subject_id,
                            subject_folder=self.folder.name,
                            fname=fn_new,
                            mri_dict=subject.mri,
                            mesh_dict=subject.mesh,
                            roi_dict=subject.roi,
                            exp_dict=subject.exp,
                            ps_dict=subject.ps,
                            overwrite=True,
                            check_file_exist=False,
                            verbose=False)
        subject = pynibs.load_subject(fn_new)
        for mesh_id in self.mesh_names:
            assert mesh_id in subject.mesh.keys(), f"{mesh_id} not found in {self.fn_subject_object}"

    # def test_06_add_stuff(self):
    #     subject = pynibs.load_subject(self.fn_subject_object)
    #     mri = subject.mri[0]
    #     subject.add_mri_info(mri)
    #
    #     exp = {'TMS_localite': subject.exp['TMS_localite']}
    #     exp['fn_coil'] = exp['TMS_localite']['fn_coil'][0][0]
    #     subject.add_experiment_info(exp)

    def test_05_print_subject(self):
        subject = pynibs.load_subject(self.fn_subject_object)
        print(subject)
