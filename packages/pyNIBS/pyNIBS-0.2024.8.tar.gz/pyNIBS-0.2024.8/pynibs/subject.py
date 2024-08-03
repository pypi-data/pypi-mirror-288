import os
import h5py
import pickle
import warnings
import numpy as np
import pynibs


class Subject:
    """
    Subject containing subject specific information, like mesh, roi, uncertainties, plot settings.

    Attributes
    ----------
    self.id : str
        Subject id.

    Notes
    -----
    **Initialization**

    .. code-block:: python

        sub = pynibs.subject(subject_ID, mesh)

    **Parameters**

    id : str
        Subject id.
    fn_mesh : str
         .msh or .hdf5 file containing the mesh information.

    **Subject.seg, segmentation information dictionary**

    fn_lh_wm : str
        Filename of left hemisphere white matter surface.
    fn_rh_wm : str
        Filename of right hemisphere white matter surface.
    fn_lh_gm : str
        Filename of left hemisphere grey matter surface.
    fn_rh_gm : str
        Filename of right hemisphere grey matter surface.
    fn_lh_curv : str
        Filename of left hemisphere curvature data on grey matter surface.
    fn_rh_curv : str
        Filename of right hemisphere curvature data on grey matter surface.

    **Subject.mri, mri information dictionary**

    fn_mri_T1 : str
        Filename of T1 image.
    fn_mri_T2 : str
        Filename of T2 image.
    fn_mri_DTI : str
        Filename of DTI dataset.
    fn_mri_DTI_bvec : str
        Filename of DTI bvec file.
    fn_mri_DTI_bval : str
        Filename of DTI bval file.
    fn_mri_conform : str
        Filename of conform T1 image resulting from SimNIBS mri2mesh function.

    **Subject.ps, plot settings dictionary**

    see plot functions in para.py for more details

    **Subject.exp, experiment dictionary**

    info : str
        General information about the experiment.
    date : str
        Date of experiment (e.g. 01/01/2018).
    fn_tms_nav : str
        Path to TMS navigator folder.
    fn_data : str
        Path to data folder or files.
    fn_exp_csv : str
        Filename of experimental data .csv file containing the merged experimental data information.
    fn_coil : str
        Filename of .ccd or .nii file of coil used in the experiment (contains ID).
    fn_mri_nii : str
        Filename of MRI .nii file used during the experiment.
    cond : str or list of str
        Conditions in the experiment in the recorded order (e.g. ['PA-45', 'PP-00']).
    experimenter : str
        Name of experimenter who conducted the experiment.
    incidents : str
        Description of special events occurred during the experiment.

    **Subject.mesh, mesh dictionary**

    info : str
        Information about the mesh (e.g. dicretization, etc.).
    fn_mesh_msh : str
        Filename of the .msh file containing the FEM mesh.
    fn_mesh_hdf5 : str
        Filename of the .hdf5 file containing the FEM mesh.
    seg_idx : int
        Index indicating to which segmentation dictionary the mesh belongs.

    **Subject.roi region of interest dictionary**

    type : str
        Specify type of ROI ('surface', 'volume')
    info : str
        Info about the region of interest, e.g. "M1 midlayer from freesurfer mask xyz".
    region : list of str or float
        Filename for freesurfer mask or ``[[X_min, X_max], [Y_min, Y_max], [Z_min, Z_max]]``.
    delta : float
        Distance parameter between WM and GM (0 -> WM, 1 -> GM) (for surfaces only).
    """
    def __init__(self, subject_id, subject_folder):
        self.id = subject_id  # subject id
        self.subject_folder = subject_folder  # folder containing subject information
        self.mri = []  # list containing mri information
        self.mesh = {}  # dict containing mesh information
        self.exp = {}  # dict containing information about conducted experiments
        self.ps = []  # list containing plot settings
        self.roi = {}  # dict containing the roi information

    def __str__(self):
        """ Overload method to allow print(subject_object)"""
        ret = f'{"=" * 64}\n' \
              f'Subject ID : {self.id}\n' \
              f'Folder     : {self.subject_folder}\n' \
              f'Meshes     : {len(self.mesh.items())}\n' \
              f'Experiments: {len(self.exp.items())}\n'
        ret += f'{"=" * 64}\n\n'
        ret += '------------------------------MRI------------------------------\n'
        if not self.mri:
            ret += 'None\n'
        else:
            for idx_mesh, mri in enumerate(self.mri):
                ret += f"|- MRI[{idx_mesh}]\n"
                for k, d in mri.items():
                    if k == list(mri.keys())[-1]:
                        pref = '└-'
                    else:
                        pref = '|-'
                    ret += f'   {pref}  {k: >19}: {d}\n'

        ret += '\n------------------------------MESH------------------------------\n'
        if not self.mesh:
            ret += 'None\n'
        else:
            for idx_mesh, mesh in self.mesh.items():
                ret += f"|- Mesh name: {idx_mesh}\n"

                # plot roi keys
                if idx_mesh in self.roi.keys():
                    for r_idx, roi in self.roi[idx_mesh].items():
                        key_list_roi = []
                        ret += f'  |-- ROI: {r_idx}\n'
                        for k, d in roi.items():
                            if d is not None and k != 'name' and k != 'mesh_name':
                                key_list_roi.append(k)
                        for k in key_list_roi:
                            if k == key_list_roi[-1]:
                                pref = '└-'
                            else:
                                pref = '|-'
                            ret += f'    {pref} {k: >19}: {roi[k]}\n'

                # plot mesh keys
                key_list_mesh = []
                for k, d in mesh.items():
                    if d is not None and k != 'name' and k != 'subject_id':
                        key_list_mesh.append(k)
                for k in key_list_mesh:
                    if k == key_list_mesh[-1]:
                        pref = '└-'
                    else:
                        pref = '|-'
                    ret += f'  {pref} {k: >19}: {mesh[k]}\n'

                ret += "\n"
        ret += '\n----------------------------Experiments-------------------------\n'
        if not self.exp:
            ret += 'None\n'
        else:
            for idx_exp, exp in self.exp.items():
                ret += f"|- Exp name: {idx_exp}\n"
                key_list_exp = []
                for k, d in exp.items():
                    if d is not None and k != 'name' and k != 'subject_id':
                        key_list_exp.append(k)
                for k in key_list_exp:
                    if k == key_list_exp[-1]:
                        pref = '└-'
                    else:
                        pref = '|-'
                    ret += f'  {pref} {k: >19}: {exp[k]}\n'
        return ret

    def add_mesh_info(self, mesh_dict):
        """
        Adding filename information of the mesh to the subject object (multiple filenames possible).

        Parameters
        ----------
        mesh_dict : dict or list of dict
            Dictionary containing the mesh information.

        Notes
        -----
        **Adds Attributes**

        Subject.mesh : list of dict
            Dictionaries containing the mesh information.
        """
        if type(mesh_dict) is list:
            for mesh in mesh_dict:
                self.mesh.append(mesh)

        else:
            self.mesh = mesh_dict

    def add_roi_info(self, roi_dict):
        """
        Adding ROI (surface) information of the mesh with mesh_index to the subject object (multiple ROIs possible).

        Parameters
        ----------
        roi_dict : dict of dict or list of dict
            Dictionary containing the ROI information of the mesh with mesh_index ``[mesh_idx][roi_idx]``.

        Notes
        -----
        **Adds Attributes**

        Subject.mesh[mesh_index].roi : list of dict
            Dictionaries containing ROI information.
        """
        for mesh_idx in roi_dict.keys():
            self.roi[mesh_idx] = dict()

            for roi_idx in roi_dict[mesh_idx].keys():
                self.roi[mesh_idx][roi_idx] = roi_dict[mesh_idx][roi_idx]

    def add_plotsettings(self, ps_dict):
        """
        Adding ROI information to the subject object (multiple ROIs possible).

        Parameters
        ----------
        ps_dict : dict or list of dict
            Dictionary containing plot settings of the subject.

        Notes
        -----
        **Adds Attributes**

        Subject.ps : list of dict
            Dictionary containing plot settings of the subject.
        """
        if type(ps_dict) is not list:
            ps_dict = [ps_dict]

        for ps in ps_dict:
            self.ps.append(ps)

    def add_mri_info(self, mri_dict):
        """
        Adding MRI information to the subject object (multiple MRIs possible).

        Parameters
        ----------
        mri_dict : dict or list of dict
            Dictionary containing the MRI information of the subject.

        Notes
        -----
        **Adds Attributes**

        Subject.mri : list of dict
            Dictionary containing the MRI information of the subject.
        """
        if type(mri_dict) is not list:
            mri_dict = [mri_dict]

        for mri in mri_dict:
            self.mri.append(mri)

    @staticmethod
    def _prep_fn(val):
        if type(val) is dict:
            pass
        elif type(val) is not list:
            val = [val]
            for j in range(len(val)):
                _ = check_file_and_format(val[j])
        return val

    def add_experiment_info(self, exp_dict):
        """
        Adding information about a particular experiment.

        Parameters
        ----------
        exp_dict : dict of dict or list of dict
            Dictionary containing information about the experiment.

        Notes
        -----
        **Adds Attributes**

        exp : list of dict
            Dictionary containing information about the experiment.
        """
        fns = ['fn_data', 'fn_coil', 'fn_mri_nii']
        if exp_dict is None:
            return

        # if type(exp_dict) is not list:
        #     exp_dict = [exp_dict
        # check if files and folder exist and convert to list
        for i in exp_dict.keys():

            # # fn_tms_nav
            # if type(exp_dict[i]['fn_tms_nav']) is not list:
            #     exp_dict[i]['fn_tms_nav'] = [exp_dict[i]['fn_tms_nav']]
            # for j in range(len(exp_dict[i]['fn_tms_nav'])):
            #     _ = check_file_and_format(exp_dict[i]['fn_tms_nav'][j])

            # fn_data
            for fn in fns:
                try:
                    exp_dict[i][fn] = self._prep_fn(exp_dict[i][fn])
                except KeyError:
                    pass

            # new subject files have 'cond' as dictionary
            if 'cond' in exp_dict[i].keys():
                if isinstance(exp_dict[i]['cond'], dict):
                    for cond_name in exp_dict[i]['cond'].keys():
                        for fn in fns:
                            try:
                                exp_dict[i]['cond'][cond_name][fn] = self._prep_fn(exp_dict[i]['cond'][cond_name][fn])
                            except KeyError:
                                pass
            else:
                exp_dict[i]['cond'] = [[""]]

        for exp in exp_dict:
            self.exp[exp] = exp_dict[exp]


def fill_from_dict(obj, d):
    """
    Set all attributes from d in obj.

    Parameters
    ----------
    obj : pynibs.Mesh or pynibs.roi.ROI
        Object to fill with ``d``.
    d : dict
        Dictionary containing the attributes to set.

    Returns
    -------
    obj : pynibs.Mesh or pynibs.ROI
        Object with attributes set from ``d``.
    """
    for key, value in d.items():
        if not hasattr(obj, f"{key}"):
            warnings.warn(f"{key} not existing.")
        setattr(obj, key, value)

    return obj


def save_subject(subject_id, subject_folder, fname, mri_dict=None, mesh_dict=None, roi_dict=None,
                 exp_dict=None, ps_dict=None, **kwargs):
    """
    Saves subject information in .pkl or .hdf5 format (preferred)

    Parameters
    ----------
    subject_id : str
        ID of subject.
    subject_folder : str
        Subject folder
    fname : str
        Filename with .hdf5 or .pkl extension (incl. path).
    mri_dict : list of dict, optional
        MRI info.
    mesh_dict : list of dict, optional
        Mesh info.
    roi_dict : list of list of dict, optional
        Mesh info.
    exp_dict : list of dict, optional
        Experiment info.
    ps_dict : list of dict, optional
        Plot-settings info.
    kwargs : str or np.ndarray
        Additional information saved in the parent folder of the .hdf5 file.

    Returns
    -------
    <File> : .hdf5 file
        Subject information
    """
    filetype = os.path.splitext(fname)[1]

    if filetype == ".hdf5":
        if os.path.exists(fname):
            os.remove(fname)

        save_subject_hdf5(subject_id=subject_id,
                          subject_folder=subject_folder,
                          fname=fname,
                          mri_dict=mri_dict,
                          mesh_dict=mesh_dict,
                          roi_dict=roi_dict,
                          exp_dict=exp_dict,
                          ps_dict=ps_dict,
                          **kwargs)

    elif filetype == ".pkl":
        raise NotImplementedError
        #
        # # create and initialize subject
        # subject = Subject(subject_id=subject_id)
        #
        # # add mri information
        # subject.add_mri_info(mri_dict=mri_dict)
        #
        # # add mesh information
        # subject.add_mesh_info(mesh_dict=mesh_dict)
        #
        # # add roi info to mesh
        # subject.add_roi_info(roi_dict=roi_dict)
        #
        # # add experiment info
        # subject.add_experiment_info(exp_dict=exp_dict)
        #
        # # add plotsettings
        # subject.add_plotsettings(ps_dict=ps_dict)
        #
        # save_subject_pkl(sobj=subject, fname=fname)


def save_subject_pkl(sobj, fname):
    """
    Saving subject object as pickle file.

    Parameters
    ----------
    sobj: object
        Subject object to save
    fname: str
        Filename with .pkl extension

    Returns
    -------
    <File> : .pkl file
        Subject object instance
    """

    if type(fname) is list:
        fname = fname[0]

    with open(fname, 'wb') as output:
        pickle.dump(sobj, output, -1)


def save_subject_hdf5(subject_id, subject_folder, fname, mri_dict=None, mesh_dict=None, roi_dict=None,
                      exp_dict=None, ps_dict=None, overwrite=True, check_file_exist=False, verbose=False, **kwargs):
    """
    Saving subject information in hdf5 file.

    Parameters
    ----------
    subject_id : str
        ID of subject.
    subject_folder : str
        Subject folder.
    fname : str
        Filename with .hdf5 extension (incl. path).
    mri_dict : list of dict, optional
        MRI info.
    mesh_dict : list of dict, optional
        Mesh info.
    roi_dict : list of list of dict, optional
        Mesh info.
    exp_dict : list of dict or dict of dict, optional
        Experiment info.
    ps_dict : list of dict, optional, default:None
        Plot-settings info.
    overwrite : bool
        Overwrites existing .hdf5 file.
    check_file_exist : bool
        Hide warnings.
    verbose : bool
        Print information about meshes and ROIs.
    kwargs : str or np.ndarray
        Additional information saved in the parent folder of the .hdf5 file.

    Returns
    -------
    <File> : .hdf5 file
        Subject information.
    """
    assert fname.endswith('.hdf5')

    if overwrite and os.path.exists(fname):
        os.remove(fname)

    with h5py.File(fname, 'a') as f:
        f["subject_id"] = np.array(subject_id).astype("|S")
        f["subject_folder"] = np.array(subject_folder).astype("|S")

    if mri_dict is not None:
        if isinstance(mri_dict, list):
            mri_dict = {i: mri_dict[i] for i in range(len(mri_dict))}

        for i in mri_dict.keys():
            pynibs.write_dict_to_hdf5(fn_hdf5=fname, data=mri_dict[i], folder=f"mri/{i}", check_file_exist=True)

    if mesh_dict is not None:
        if isinstance(mesh_dict, list):
            mesh_dict = {i: mesh_dict[i] for i in range(len(mesh_dict))}

        for mesh_name, mesh_dict in mesh_dict.items():
            mesh = pynibs.Mesh(mesh_name=mesh_name, subject_id=subject_id, subject_folder=subject_folder)
            mesh.fill_defaults(mesh_dict['approach'])
            mesh = fill_from_dict(mesh, mesh_dict)
            mesh.write_to_hdf5(fn_hdf5=fname, check_file_exist=check_file_exist, verbose=verbose)

    if roi_dict is not None:
        for mesh_name in roi_dict.keys():
            for roi_name, roi_dict_i in roi_dict[mesh_name].items():
                roi = pynibs.ROI(subject_id=subject_id, roi_name=roi_name, mesh_name=mesh_name)
                roi = fill_from_dict(roi, roi_dict_i)
                roi.write_to_hdf5(fn_hdf5=fname, check_file_exist=check_file_exist, verbose=verbose)

    if exp_dict is not None:
        if isinstance(exp_dict, list):
            exp_dict = {i: exp_dict[i] for i in range(len(exp_dict))}
        for i in exp_dict.keys():
            pynibs.write_dict_to_hdf5(fn_hdf5=fname, data=exp_dict[i], folder=f"exp/{i}",
                                      check_file_exist=check_file_exist)

    if ps_dict is not None:
        for i in range(len(ps_dict)):
            pynibs.write_dict_to_hdf5(fn_hdf5=fname, data=ps_dict[i], folder=f"ps/{i}",
                                      check_file_exist=check_file_exist)

    with h5py.File(fname, 'a') as f:
        for key, value in kwargs.items():
            try:
                del f[key]
            except KeyError:
                pass
            f.create_dataset(name=key, data=value)


def load_subject_hdf5(fname):
    """
    Loading subject information from .hdf5 file and returning subject object.

    Parameters
    ----------
    fname : str
        Filename with .hdf5 extension (incl. path).

    Returns
    -------
    subject : pynibs.subject.Subject
        The Subject object.
    """
    with h5py.File(fname, 'r') as f:
        subject_id = str(f["subject_id"][()].astype(str))
        subject_folder = str(f["subject_folder"][()].astype(str))

        # create and initialize subject
        subject = Subject(subject_id=subject_id, subject_folder=subject_folder)

        # add mri information
        try:
            mri_keys = f["mri"].keys()
            mri = []

            for key in mri_keys:
                mri.append(pynibs.read_dict_from_hdf5(fn_hdf5=fname, folder=f"mri/{key}"))

        except KeyError:
            mri = None

        subject.add_mri_info(mri_dict=mri)

        # add mesh information
        try:
            mesh_keys = f["mesh"].keys()
            mesh = {}

            for key in mesh_keys:
                mesh[key] = pynibs.read_dict_from_hdf5(fn_hdf5=fname, folder=f"mesh/{key}")

        except KeyError:
            mesh = None

        subject.add_mesh_info(mesh_dict=mesh)

        # add roi info
        try:
            mesh_idx_keys = f["roi"].keys()
            roi = dict()

            for mesh_idx in mesh_idx_keys:
                try:
                    roi_idx_keys = f[f"roi/{mesh_idx}"].keys()
                    roi[mesh_idx] = dict()

                    for roi_idx in roi_idx_keys:
                        roi[mesh_idx][roi_idx] = pynibs.read_dict_from_hdf5(fn_hdf5=fname,
                                                                            folder=f"roi/{mesh_idx}/{roi_idx}")

                except KeyError:
                    roi[mesh_idx] = None

            subject.add_roi_info(roi_dict=roi)

        except KeyError:
            pass

        # add experiment information
        try:
            exp_keys = f["exp"].keys()
            exp = {}

            for key in exp_keys:
                exp[key] = pynibs.read_dict_from_hdf5(fn_hdf5=fname, folder=f"exp/{key}")

        except KeyError:
            exp = None

        subject.add_experiment_info(exp_dict=exp)

        # add plotsettings information
        try:
            ps_keys = f["ps"].keys()
            ps = []

            for key in ps_keys:
                ps.append(pynibs.read_dict_from_hdf5(fn_hdf5=fname, folder=f"ps/{key}"))

        except KeyError:
            ps = None

        subject.add_plotsettings(ps_dict=ps)

    return subject


def load_subject(fname, filetype=None):
    """
    Wrapper for pkl and hdf5 subject loader

    Parameters
    ----------
    fname: str
        endswith('.pkl') | endswith('.hdf5').
    filetype: str
        Explicitly set file version.

    Returns
    -------
    subject : pynibs.subject.Subject
        Loaded Subject object.
    """
    # explicit set fname type
    if filetype:
        if filetype.lower().endswith("hdf5"):
            filetype = "hdf5"
        elif filetype.lower().endswith("pkl"):
            filetype = "pkl"
        else:
            raise NotImplementedError(f"{filetype} unknown.")

    # determine fname type from file-ending
    else:
        if fname.lower().endswith("hdf5"):
            filetype = "hdf5"
        elif fname.lower().endswith("pkl"):
            filetype = "pkl"
        else:
            raise NotImplementedError(f"{fname} type unknown.")

    # load file using correct load function
    if filetype == "hdf5":
        return load_subject_hdf5(fname)
    elif filetype == "pkl":
        return load_subject_pkl(fname)


def load_subject_pkl(fname):
    """
    Loading subject object from .pkl file.

    Parameters
    ----------
    fname : str
        Filename with .pkl extension.

    Returns
    -------
    subject : pynibs.subject.Subject
        Loaded Subject object.
    """
    try:
        with open(fname, 'rb') as f:
            return pickle.load(f)

    except UnicodeDecodeError:
        print(".pkl file version does not match python version... recreating subject object")
        fn_scipt = os.path.join(os.path.split(fname)[0],
                                "create_subject_" +
                                os.path.splitext(os.path.split(fname)[1])[0] + ".py")
        pynibs.bash_call("python {}".format(fn_scipt))

        with open(fname, 'rb') as f:
            return pickle.load(f)


def check_file_and_format(fname):
    """
    Checking existence of file and transforming to list if necessary.

    Parameters
    ----------
    fname: str or list of str
        Filename(s) to check.

    Returns
    -------
    fname: list of str
        Checked filename(s) as list.
    """
    if type(fname) is not list:
        fname = [fname]

    for fn in fname:
        if not (os.path.exists(fn)):
            Exception('File/Folder {} does not exist!'.format(fn))

    return fname


def create_plot_settings_dict(plotfunction_type):
    """
    Creates a dictionary with default plotsettings.

    Parameters
    ----------
    plotfunction_type : str
        Plot function the dictionary is generated for:

        * 'surface_vector_plot'
        * 'surface_vector_plot_vtu'
        * 'volume_plot'
        * 'volume_plot_vtu'

    Returns
    -------
    ps : dict
        Dictionary containing the plotsettings.
    axes : bool
        Show orientation axes.
    background_color : nparray
         (1m 3) Set background color of exported image RGB (0...1).
    calculator : str
        Format string with placeholder of the calculator expression the quantity to plot is modified with,
        e.g.: "{}^5".
    clip_coords : nparray of float
        (N_clips, 3) Coordinates of clip surface origins (x,y,z).
    clip_normals : nparray of float
        (N_clips, 3) Surface normals of clip surfaces pointing in the direction where the volume is kept for
        clip_type = ['clip' ...] (x,y,z).
    clip_type : list of str
        Type of clipping:

        * 'clip':  cut geometry but keep volume behind
        * 'slice': cut geometry and keep only the slice
    coil_dipole_scaling : list [1 x 2]
        Specify the scaling type of the dipoles (2 entries):
        ``coil_dipole_scaling[0]``:

        * 'uniform': uniform scaling, i.e. all dipoles have the same size
        + 'scaled': size scaled according to dipole magnitude

        ``coil_dipole_scaling[1]``:

        * scalar scale parameter of dipole size
    coil_dipole_color : str or list
        Color of the dipoles; either str to specify colormap (e.g. 'jet') or list of RGB values [1 x 3] (0...1).
    coil_axes : bool, default: True
        Plot coil axes visualizing the principle direction and orientation of the coil.
    colorbar_label : str
        Label of plotted data close to colorbar.
    colorbar_position : list of float
        (1, 2) Position of colorbar (lower left corner) 0...1 [x_pos, y_pos].
    colorbar_orientation : str
        Orientation of colorbar (``'Vertical'``, ``'Horizontal'``).
    colorbar_aspectratio : int
        Aspectratio of colorbar (higher values make it thicker).
    colorbar_titlefontsize : float
        Fontsize of colorbar title.
    colorbar_labelfontsize : float
        Fontsize of colorbar labels (numbers).
    colorbar_labelformat : str
        Format of colorbar labels (e.g.: '%-#6.3g').
    colorbar_numberoflabels : int
        maximum number of colorbar labels.
    colorbar_labelcolor : list of float
        (1, 3) Color of colorbar labels in RGB (0...1).
    colormap : str or nparray
        If nparray [1 x 4*N]: custom colormap providing data and corresponding RGB values

        .. math::
            \\begin{bmatrix}
              data_{1} & R_1 & G_1 & B_1  \\\\
              data_{2} & R_2 & G_2 & B_2  \\\\
              ...      & ... & ... & ...  \\\\
              data_{N} & R_N & G_N & B_N  \\\\
             \\end{bmatrix}

        if str: colormap of plotted data chosen from included presets:

        * 'Cool to Warm',
        * 'Cool to Warm (Extended)',
        * 'Blue to Red Rainbow',
        * 'X Ray',
        * 'Grayscale',
        * 'jet',
        * 'hsv',
        * 'erdc_iceFire_L',
        * 'Plasma (matplotlib)',
        * 'Viridis (matplotlib)',
        * 'gray_Matlab',
        * 'Spectral_lowBlue',
        + 'BuRd'
        * 'Rainbow Blended White'
        * 'b2rcw'
    colormap_categories : bool
        Use categorized (discrete) colormap.
    datarange : list
        (1, 2) Minimum and Maximum of plotted datarange [MIN, MAX] (default: automatic).
    domain_IDs : int or list of int
        Domain IDs
        surface plot: Index of surface where the data is plotted on (Default: 0)
        volume plot: Specify the domains IDs to show in plot (default: all) Attention! Has to be included in the
        dataset under the name 'tissue'! e.g. for SimNIBS:

        * 1 -> white matter (WM)
        * 2 -> grey matter (GM)
        * 3 -> cerebrospinal fluid (CSF)
        * 4 -> skull
        * 5 -> skin
    domain_label : str
        Label of the dataset which contains the domain IDs (default: 'tissue_type').
    edges : BOOL
        Show edges of mesh.
    fname_in : str or list of str
        Filenames of input files, 2 possibilities:

        * .xdmf-file: filename of .xmdf (needs the corresponding .hdf5 file(s) in the same folder)
        * .hdf5-file(s): filename(s) of .hdf5 file(s) containing the data and the geometry. The data can be provided
          in the first hdf5 file and the geometry can be provided in the second file. However, both can be also
          provided in a single hdf5 file.
    fname_png : str
        Name of output .png file (incl. path).
    fname_vtu_volume : str
        Name of .vtu volume file containing volume data (incl. path).
    fname_vtu_surface : str
        Name of .vtu surface file containing surface data (incl. path) (to distinguish tissues).
    fname_vtu_coil : str, optional
        Name of coil .vtu file (incl. path).
    info : str
        Information about the plot the settings belong to.
    interpolate : bool
        Interpolate data for visual smoothness.
    NanColor : list of float
        (3) RGB color values for "Not a Number" values (range 0 ... 1).
    opacitymap : np.ndarray
        Points defining the piecewise linear opacity transfer function (transparency) (default: no transparency)
        connecting data values with opacity (alpha) values ranging from 0 (max. transparency) to 1 (no transparency).

        .. math::
           \\begin{bmatrix}
            data_{1} & opac_1 & 0.5 & 0  \\\\
            data_{2} & opac_2 & 0.5 & 0  \\\\
            ...      & ...   & ... & ...\\\\
            data_{N} & opac_N & 0.5 & 0  \\\\
           \\end{bmatrix}
    plot_function : str
        Function the plot is generated with:

        - 'surface_vector_plot'
        - 'surface_vector_plot_vtu'
        - 'volume_plot'
        - 'volume_plot_vtu'
    png_resolution : float
        Resolution parameter of output image (1...5).
    quantity : str
        Label of magnitude dataset to plot.
    surface_color : np.ndarray
        (1, 3) Color of brain surface in RGB (0...1) for better visibility of tissue borders.
    surface_smoothing : bool
        Smooth the plotted surface (True/False).
    show_coil : bool, default: True
        show coil if present in dataset as block termed 'coil'.
    vcolor : np.ndarray of float
        (N_vecs, 3) Array containing the RGB values between 0...1 of the vector groups in dataset to plot.
    vector_mode : dict
        Key determines the type how many vectors are shown:

        - 'All Points'
        - 'Every Nth Point'
        - 'Uniform Spatial Distribution'

        Value (int) is the corresponding number of vectors:

        - 'All Points' (not set)
        - 'Every Nth Point' (every Nth vector is shown in the grid)
        - 'Uniform Spatial Distribution' (not set)
    view : list
        Camera position and angle in 3D space:
        ``[[3 x CameraPosition], [3 x CameraFocalPoint], [3 x CameraViewUp], 1 x CameraParallelScale]``.
    viewsize : nparray [1 x 2]
        Set size of exported image in pixel [width x height] will be extra scaled by parameter png_resolution.
    vlabels : list of str
        Labels of vector datasets to plot (other present datasets are ignored).
    vscales : list of float
        Scale parameters of vector groups to plot.
    vscale_mode : list of str [N_vecs x 1]
        List containing the type of vector scaling:

        - 'off': all vectors are normalized
        - 'vector': vectors are scaled according to their magnitudeeee
    """
    if plotfunction_type not in ['surface_vector_plot', 'surface_vector_plot_vtu', 'volume_plot', 'volume_plot_vtu']:
        raise Exception('plotfunction_type not set correctly, specify either [\'surface_vector_plot\', \
                            \'surface_vector_plot_vtu\', \'volume_plot\', \'volume_plot_vtu\']')

    ps = dict()
    ps['info'] = []
    ps['plot_function'] = plotfunction_type
    ps['fname_png'] = []
    ps['png_resolution'] = 1
    ps['quantity'] = None
    ps['datarange'] = None
    ps['colorbar_label'] = ''
    ps['colorbar_position'] = []
    ps['colorbar_orientation'] = 'Vertical'
    ps['colorbar_aspectratio'] = 20
    ps['colorbar_titlefontsize'] = 7
    ps['colorbar_labelfontsize'] = 7
    ps['colorbar_labelformat'] = '%-#6.3g'
    ps['colorbar_numberoflabels'] = 5
    ps['colorbar_labelcolor'] = [0, 0, 0]
    ps['colorbar_font'] = 'Arial'
    ps['view'] = 0
    ps['interpolate'] = False
    ps['edges'] = False
    ps['axes'] = True
    ps['colormap'] = "jet"
    ps['colormap_categories'] = False
    ps['opacitymap'] = None
    ps['background_color'] = [1, 1, 1]
    ps['viewsize'] = [800, 800]
    ps['NanColor'] = [1, 1, 1]
    ps["surface_smoothing"] = True
    ps["calculator"] = None

    # filename of input files
    if plotfunction_type in ['surface_vector_plot', 'surface_vector_plot_vtu', 'volume_plot']:
        ps['fname_in'] = []

    elif plotfunction_type in ['volume_plot_vtu']:
        ps['fname_vtu_volume'] = []
        ps['fname_vtu_surface'] = []
        ps['fname_vtu_coil'] = []

    # new features in .xdmf plot functions
    if plotfunction_type in ['surface_vector_plot', 'volume_plot', 'volume_plot_vtu']:
        ps['domain_label'] = 'tissue_type'
        ps['domain_IDs'] = 0
        ps['show_coil'] = True
        ps['coil_dipole_scaling'] = ['uniform', 1]
        ps['coil_dipole_color'] = 'jet'
        ps['coil_axes'] = True

    # surface specific properties
    if plotfunction_type in ['surface_vector_plot', 'surface_vector_plot_vtu']:
        ps['vlabels'] = ''
        ps['vscales'] = np.array([1])
        ps['vscale_mode'] = 'vector'
        ps['vector_mode'] = {'All Points': 0}
        ps['vcolor'] = np.array([1.0, 0.0, 0.0])

    # volume specific properties
    if plotfunction_type in ['volume_plot', 'volume_plot_vtu']:
        ps['clip_coords'] = np.array([])
        ps['clip_normals'] = np.array([])
        ps['clip_type'] = []
        ps['surface_color'] = [1, 1, 1]

    return ps
