"""
The `xdmf.py` module provides utilities for creating, writing, and manipulating XDMF files. XDMF (eXtensible
Data Model and Format) is a format that allows for the exchange of scientific data between High Performance Computing
codes and tools for visualization, analysis, and data processing.

The module includes functions for:

- Writing XDMF files for surfaces, such as ROIs (`write_xdmf_surf`).
- Creating XDMF markup files for given HDF5 files, mainly for paraview visualization (`write_xdmf`).
- Creating XDMF markup files for given ROI HDF5 data files with 4D data (`write_temporal_xdmf`).
- Creating one XDMF file that allows paraview plottings of coil position paths (`create_position_path_xdmf`).
- Overlaying data stored in HDF5 files except in regions where data_substitute is found (`data_superimpose`).
- Writing the coordinates to an XDMF file for visualization (`write_xdmf_coordinates`).
- Creating XDMF file to plot fibres in Paraview (`create_fibre_xdmf`).

This module is primarily used for handling and visualizing data related to neuroimaging and brain stimulation studies.
"""
import warnings
import os
import h5py
import numpy as np
import pynibs


def write_xdmf_surf(data_hdf_fn_out, data_names, data_xdmf_fn, geo_hdf_fn, data_dims,
                    data_in_tris=True, data_prefix='/data/tris/'):
    """
    Write XDMF files for surfaces, such as ROIs.

    Parameters
    ----------
    data_hdf_fn_out : str

    data_names : list of str

    data_xdmf_fn : str

    geo_hdf_fn : str

    data_dims : list of int
        The data dimensions.
    data_in_tris : bool, default: True.

    data_prefix : str, default: '/data/tris/'


    Returns
    -------
    <File> : .xdmf file
        Descriptor file pointing to geo and data .hdf5 files
    """
    if not data_in_tris:
        raise NotImplementedError
    # if geo file exists in same folder then data file only use relative path
    if os.path.split(data_hdf_fn_out)[0] == os.path.split(geo_hdf_fn)[0]:
        geo_hdf_fn_xdmf = os.path.basename(geo_hdf_fn)
    else:
        geo_hdf_fn_xdmf = geo_hdf_fn

    with open(data_xdmf_fn, 'w') as xdmf, h5py.File(geo_hdf_fn, 'r') as h5_geo:
        # write xdmf file linking the data to the surfaces in geo_hdf_fn
        xdmf.write('<?xml version="1.0"?>\n')
        xdmf.write('<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>\n')
        xdmf.write('<Xdmf Version="2.0" xmlns:xi="http://www.w3.org/2001/XInclude">\n')
        xdmf.write('<Domain>\n')

        # one collection grid
        xdmf.write('<Grid\nCollectionType="Spatial"\nGridType="Collection"\nName="Collection">\n')

        # read all available surfaces
        surface = []
        lookup_str = 'triangle_number_list_'
        lookup_str_node = 'node_coord_'
        lookup_str_tri = 'tri_tissue_type_'

        keys = list(h5_geo['mesh/elm/'].keys())
        for key in keys:
            idx = key.find(lookup_str)
            if idx >= 0:
                surface.append(key[(idx + len(lookup_str)):])

        if not surface:
            surface = []
            lookup_str = 'triangle_number_list'
            lookup_str_node = 'node_coord'
            lookup_str_tri = 'tri_tissue_type'
            keys = list(h5_geo['mesh/elm/'].keys())
            for key in keys:
                idx = key.find(lookup_str)
                if idx >= 0:
                    surface.append(key[(idx + len(lookup_str)):])

        for surf in surface:
            n_tris = len(h5_geo['/mesh/elm/' + lookup_str + surf][:])
            n_nodes = len(h5_geo['/mesh/nodes/' + lookup_str_node + surf][:])
            assert n_tris, n_nodes

            # one grid for triangles...
            ###########################
            xdmf.write('<Grid Name="tris" GridType="Uniform">\n')
            xdmf.write('<Topology NumberOfElements="' + str(n_tris) +
                       '" TopologyType="Triangle" Name="' + surf + '_Tri">\n')
            xdmf.write('<DataItem Format="HDF" Dimensions="' + str(n_tris) + ' 3">\n')
            xdmf.write(geo_hdf_fn_xdmf + ':' + '/mesh/elm/' + lookup_str + surf + '\n')
            xdmf.write('</DataItem>\n')
            xdmf.write('</Topology>\n')

            # nodes
            xdmf.write('<Geometry GeometryType="XYZ">\n')
            xdmf.write('<DataItem Format="HDF" Dimensions="' + str(n_nodes) + ' 3">\n')
            xdmf.write(geo_hdf_fn_xdmf + ':' + '/mesh/nodes/' + lookup_str_node + surf + '\n')
            xdmf.write('</DataItem>\n')
            xdmf.write('</Geometry>\n')

            # data
            for idx, dat in enumerate(data_dims):
                xdmf.write(f'<Attribute Name="{data_names[idx]}" AttributeType="Scalar" Center="Cell">\n')
                xdmf.write(f'<DataItem Format="HDF" Dimensions="{str(n_tris)} {str(data_dims[idx])}">\n')
                xdmf.write(os.path.basename(data_hdf_fn_out) + ':' + data_prefix + data_names[idx] + '\n')
                xdmf.write('</DataItem>\n')
                xdmf.write('</Attribute>\n')

            # tissue_type
            xdmf.write('<Attribute Name="tissue_type" AttributeType="Scalar" Center="Node">\n')
            xdmf.write('<DataItem Format="HDF" Dimensions="' + str(n_nodes) + ' 1">\n')
            xdmf.write(geo_hdf_fn_xdmf + ':' + '/mesh/elm/' + lookup_str_tri + surf + '\n')
            xdmf.write('</DataItem>\n')
            xdmf.write('</Attribute>\n')
            xdmf.write('</Grid>\n')

        xdmf.write('</Grid>\n')
        xdmf.write('</Domain>\n')
        xdmf.write('</Xdmf>\n')


def write_xdmf(hdf5_fn, hdf5_geo_fn=None, overwrite_xdmf=False, overwrite_array=False, verbose=False, mode="r+"):
    """
    Creates .xdmf markup file for given hdf5 file, mainly for paraview visualization. Checks if triangles and
    tetrahedra already exists as distinct arrays in ``hdf5_fn``. If not, these are added to the .hdf5 file and
    rebased to 0 (from 1). If only ``hdf5_fn`` is provided, spatial information has to be present as arrays for tris
    and tets in this dataset.

    Parameters
    ----------
    hdf5_fn : str
        Filename of hdf5 file containing the data
    hdf5_geo_fn : str, optional
        Filename of hdf5 file containing the geometry
    overwrite_xdmf : bool, default: False
        Overwrite existing xdmf file if present.
    overwrite_array : bool, default: False
        Overwrite existing arrays if present
    verbose : bool
        Print output.
    mode : str, default: "r+"
        Mode to open hdf5_geo file. If hdf5_geo is already separated in tets and tris etc., nothing has to be written,
        use "r" to avoid IOErrors in case of parallel computing.

    Returns
    -------
    fn_xml : str
        Filename of the created .xml file
    <File> : .xdmf file
        hdf5_fn[-4].xdmf (only data if hdf5Geo_fn provided)
    <File> : .hdf5 file
        hdf5_fn changed if neccessary
    <File> : .hdf5 file
        hdf5geo_fn containing spatial data
    """

    if os.path.splitext(hdf5_fn)[1] not in ['.hdf5', '.h5', '.hdf']:
        print("Provide .hdf5 filename for existing file.")
        return

    xdmf_fn = os.path.splitext(hdf5_fn)[0] + '.xdmf'
    try:
        hdf5 = h5py.File(hdf5_fn, mode)
        hdf5_geo = h5py.File(hdf5_fn, mode)
    except IOError:
        print(f"Error opening file: {hdf5_fn} ... Quitting")
        raise IOError

    hdf5_fn = os.path.basename(hdf5_fn)

    if verbose:
        print("Creating " + xdmf_fn)

    if hdf5_geo_fn is not None:

        try:
            hdf5_geo = h5py.File(hdf5_geo_fn, mode)
        except IOError:
            print(f"Error opening file: {hdf5_geo_fn} ... Quitting")
            hdf5.close()
            hdf5_geo.close()
            raise IOError
    else:
        hdf5_geo_fn = os.path.basename(hdf5_fn)

    if os.path.isfile(xdmf_fn) and not overwrite_xdmf:
        hdf5.close()
        hdf5_geo.close()
        raise FileExistsError(f'{xdmf_fn} already exists. Remove or set overwrite_xdmf=True. Quitting.')

    # check if triangle and tetra data is already in 2 dataframes in hdf5
    # /mesh/elm or /elm/?
    if "/elm/" in hdf5_geo:
        path_elm = '/elm'
    else:
        path_elm = '/mesh/elm'

    if "/nodes/" in hdf5_geo:
        node_path = '/nodes'
    else:
        node_path = '/mesh/nodes'

    if path_elm not in hdf5_geo:
        print(f"Not elements (triangles or tetrahedra) present in {hdf5_geo_fn}")
        triangles, tetrahedra = None, None

    elif path_elm + "/triangle_number_list" not in hdf5_geo:
        if verbose:
            print(("triangle_number_list and tetrahedra_number_list do not exist. Adding to " + hdf5_geo_fn + "."))

        # get tris and tets from node_number list ... take the triangle ones
        triangles = (hdf5_geo[path_elm + '/node_number_list'][:][hdf5_geo[path_elm + '/elm_type'][:] == 2][:, 0:3])
        tetrahedra = (hdf5_geo[path_elm + '/node_number_list'][:][hdf5_geo[path_elm + '/elm_type'][:] == 4])

        # add to hdf5_fn and rebase to 0
        hdf5_geo.create_dataset(path_elm + '/triangle_number_list', data=triangles - 1)
        hdf5_geo.create_dataset(path_elm + '/tetrahedra_number_list', data=tetrahedra - 1)

    else:
        triangles = hdf5_geo[path_elm + '/triangle_number_list']
        try:
            tetrahedra = hdf5_geo[path_elm + '/tetrahedra_number_list']
        except KeyError:
            tetrahedra = None

    # check if data is divided into tets and tris

    # get information for .xdmf
    n_nodes = len(hdf5_geo[node_path + '/node_coord'])
    try:
        n_tets = len(tetrahedra)
    except TypeError:
        n_tets = -1

    try:
        n_tris = len(triangles)
    except TypeError:
        n_tris = -1

    if not path_elm + "/tri_tissue_type" in hdf5_geo:
        if (n_tris > -1 or n_tets > -1):
            if verbose:
                print("elm data is not divided into tris and tets. Doing that now")
            if 'tag1' in hdf5_geo[path_elm + '/']:
                hdf5_geo.create_dataset(path_elm + '/tri_tissue_type',
                                        data=hdf5_geo[path_elm + '/tag1'][:][hdf5_geo[path_elm + '/elm_type'][:] == 2])
                hdf5_geo.create_dataset(path_elm + '/tet_tissue_type',
                                        data=hdf5_geo[path_elm + '/tag1'][:][hdf5_geo[path_elm + '/elm_type'][:] == 4])

            hdf5_geo.create_dataset(path_elm + '/tri_elm_type',
                                    data=hdf5_geo[path_elm + '/elm_type'][:][hdf5_geo[path_elm + '/elm_type'][:] == 2])
            hdf5_geo.create_dataset(path_elm + '/tet_elm_type',
                                    data=hdf5_geo[path_elm + '/elm_type'][:][hdf5_geo[path_elm + '/elm_type'][:] == 4])

    if "data" in hdf5:
        for data in hdf5['/data/']:
            value = ""  # remove .value structure and save data directly in /data/dataname array
            try:
                if 'value' in list(hdf5['/data/' + data].keys()):
                    value = '/value'
            except (KeyError, AttributeError):
                pass
            if verbose:
                print(('Processing ' + data))
            if len(hdf5['/data/' + data + value]) == n_tris:
                if not "data/tris/" + data in hdf5:
                    if verbose:
                        print(('Writing /data/tris/' + data))
                    hdf5.create_dataset('/data/tris/' + data, data=hdf5['/data/' + data + value + value][:])

            elif len(hdf5['/data/' + data + value]) == n_tets:
                if not "data/tets/" + data in hdf5:
                    if verbose:
                        print(('Writing /data/tets/' + data))
                    hdf5.create_dataset('/data/tets/' + data, data=hdf5['/data/' + data + value + value][:])

            elif len(hdf5['/data/' + data + value]) == n_tris + n_tets and n_tets > 0:
                if not "data/tris" + data in hdf5:
                    if verbose:
                        print(('Writing /data/tris/' + data))
                    hdf5.create_dataset('/data/tris/' + data,
                                        data=hdf5['/data/' + data + value][:][hdf5_geo[path_elm + '/elm_type'][:] == 2])

                if not "data/tets/" + data in hdf5:
                    if verbose:
                        print(('Writing /data/tets/' + data))
                    hdf5.create_dataset('/data/tets/' + data,
                                        data=hdf5['/data/' + data + value][:][hdf5_geo[path_elm + '/elm_type'][:] == 4])

            elif len(hdf5['/data/' + data + value]) == n_nodes:
                if not "data/nodes" + data in hdf5:
                    if verbose:
                        print(("Writing /data/nodes/" + data))
                    if overwrite_array:
                        try:
                            del hdf5[f'/data/nodes/{data}']
                        except KeyError:
                            pass
                    try:
                        hdf5.create_dataset('/data/nodes/' + data, data=hdf5['/data/' + data + value][:])
                    except RuntimeError:
                        print(('/data/nodes/' + data + " already exists"))
            elif verbose:
                print((data + " not fitting to triangle or tetrahedra or total number. Ignoring."))

    if '/mesh/fields' in hdf5:
        for field in hdf5['/mesh/fields']:
            if verbose:
                print(('Processing ' + field))
            if '/data/tris/' + field not in hdf5:
                hdf5.create_dataset('/data/tris/' + field,
                                    data=hdf5['/mesh/fields/' + field + '/value'][:][
                                        hdf5_geo[path_elm + '/elm_type'][:] == 2])
            if '/data/tets/' + field not in hdf5:
                hdf5.create_dataset('/data/tets/' + field,
                                    data=hdf5['/mesh/fields/' + field + '/value'][:][
                                        hdf5_geo[path_elm + '/elm_type'][:] == 4])

    if '/elmdata/' in hdf5:
        for field in hdf5['/elmdata']:
            if verbose:
                print(('Processing ' + field))
            if '/data/tris/' + field not in hdf5:
                # sometimes data is stored in a 'value' subfolder
                try:
                    subfolder = '/value'
                    _ = hdf5['/elmdata/' + field + subfolder][0]
                # ... sometimes not
                except KeyError:
                    subfolder = ''
                hdf5.create_dataset('/data/tris/' + field,
                                    data=hdf5[f'/elmdata/{field}{subfolder}'][:][
                                        hdf5_geo[f'{path_elm}/elm_type'][:] == 2])
            if '/data/tets/' + field not in hdf5:
                try:
                    subfolder = '/value'
                    _ = hdf5[f'/elmdata/{field}{subfolder}'][0]
                except KeyError:
                    subfolder = ''
                hdf5.create_dataset(f'/data/tets/{field}',
                                    data=hdf5[f'/elmdata/{field}{subfolder}'][:][
                                        hdf5_geo[f'{path_elm}/elm_type'][:] == 4])

    # create .xdmf file
    f = open(xdmf_fn, 'w')
    space = '\t'

    # header
    f.write('<?xml version="1.0"?>\n')
    # f.write('<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>\n')
    f.write('<!DOCTYPE Xdmf>\n')
    f.write('<Xdmf Version="2.0" xmlns:xi="http://www.w3.org/2001/XInclude">\n')
    f.write('<Domain>\n')

    # one collection grid
    f.write('<Grid CollectionType="Spatial" GridType="Collection" Name="Collection">\n')

    # one grid for triangles...
    ###########################
    f.write(f'{space}<Grid Name="tris" GridType="Uniform">\n')
    space += '\t'
    f.write(f'{space}<Topology NumberOfElements="{n_tris}" TopologyType="Triangle" Name="Tri">\n')
    space += '\t'
    f.write(f'{space}<DataItem Format="HDF" Dimensions="{n_tris} 3">\n')
    f.write(f'{space}{hdf5_geo_fn}:{path_elm}/triangle_number_list\n')
    f.write(f'{space}</DataItem>\n')
    space = space[:-1]
    f.write(f'{space}</Topology>\n\n')

    # nodes
    f.write(f'{space}<Geometry GeometryType="XYZ">\n')
    space += '\t'
    f.write(f'{space}<DataItem Format="HDF" Dimensions="{n_nodes} 3">\n')
    f.write(f'{space}{hdf5_geo_fn}:{node_path}/node_coord\n')
    f.write(f'{space}</DataItem>\n')
    space = space[:-1]
    f.write(f'{space}</Geometry>\n\n')

    # link tissue type to tris geometry for visualization
    if n_tris > -1 and 'tri_tissue_type' in hdf5_geo[path_elm + '/']:
        f.write(f'{space}<Attribute Name="tissue_type" AttributeType="Scalar" Center="Cell">\n')
        space += '\t'
        f.write(f'{space}<DataItem Format="HDF" Dimensions="{n_tris} 1">\n')
        f.write(f'{space}{hdf5_geo_fn}:{path_elm}/tri_tissue_type\n')
        f.write(f'{space}</DataItem>\n')
        space = space[:-1]
        f.write(f'{space}</Attribute>\n\n')
    # link data in tris to geometry
    if '/data/tris' in hdf5:

        # elm type
        if 'tri_elm_type' in hdf5_geo[path_elm + '/']:
            f.write(f'{space}<Attribute Name="elm_type" AttributeType="Scalar" Center="Cell">\n')
            space += '\t'
            f.write(f'{space}<DataItem Format="HDF" Dimensions="{n_tris} 1">\n')
            f.write(f'{space}{hdf5_geo_fn}:{path_elm}/tri_elm_type\n')
            f.write(f'{space}</DataItem>\n')
            space = space[:-1]
            f.write(f'{space}</Attribute>\n')

        for key, data in hdf5['/data/tris'].items():

            value = ""
            try:
                if 'value' in list(data.keys()):
                    data = data['value']
                    value = '/value'
            except (KeyError, AttributeError):
                pass
            if hasattr(data, 'shape') and len(data.shape) > 1:
                if data.shape[1] == 3:
                    attr_type = "Vector"
                    dim = 3
                elif data.shape[1] == 1:
                    attr_type = "Scalar"
                    dim = 1
                else:
                    print(("Data shape unknown: " + str(data.shape[1])))
                    attr_type, dim = None, None  # just to make compiler happy
                    quit()
            else:
                attr_type = "Scalar"
                dim = 1

            f.write(f'{space}<Attribute Name="{key}" AttributeType="{attr_type}" Center="Cell">\n')
            space += '\t'
            f.write(f'{space}<DataItem Format="HDF" Dimensions="{n_tris} {dim} ">\n')
            f.write(f'{space}{hdf5_fn}:/data/tris/{key}{value}\n')
            f.write(f'{space}</DataItem>\n')
            space = space[:-1]
            f.write(f'{space}</Attribute>\n\n')

    # node data
    if '/data/nodes' in hdf5:
        # data sets (mostly statistics)
        space += '\t'
        for key, data in hdf5['/data/nodes'].items():
            value = ""
            try:
                if 'value' in list(data.keys()):
                    data = data['value']
                    value = '/value'
            except (KeyError, AttributeError):
                pass
            if hasattr(data, 'shape') and len(data.shape) > 1:
                if data.shape[1] == 3:
                    attr_type = "Vector"
                    dim = 3
                elif data.shape[1] == 1:
                    attr_type = "Scalar"
                    dim = 1
                else:
                    print(("Data shape unknown: " + str(data.shape[1])))
                    attr_type, dim = None, None  # just to make compiler happy
                    quit()

            else:
                attr_type = "Scalar"
                dim = 1

            f.write(f'{space}<Attribute Name="{key}" AttributeType="{attr_type}" Center="Node">\n')
            f.write(f'{space}<DataItem Format="HDF" Dimensions="{n_nodes}  {dim}">\n')
            f.write(f'{hdf5_fn}:/data/nodes/{key}{value}\n')

            f.write('</DataItem>\n')
            f.write('</Attribute>\n')
    space = space[:-1]
    f.write(f'{space}</Grid>\n\n')

    # ...one grid for tetrahedra...
    ##################################
    if n_tets > 0:
        f.write(f'{space}<Grid Name="tets" GridType="Uniform">\n')
        space += '\t'
        f.write(f'{space}<Topology NumberOfElements="{n_tets}" TopologyType="Tetrahedron" Name="Tet">\n')
        space += '\t'
        f.write(f'{space}<DataItem Format="HDF" Dimensions="{n_tets} 4">\n')
        f.write(f'{space}{hdf5_geo_fn}:{path_elm}/tetrahedra_number_list\n')
        f.write(f'{space}</DataItem>\n')
        space = space[:-1]
        f.write(f'{space}</Topology>\n\n')

        # nodes
        f.write(f'{space}<Geometry GeometryType="XYZ">\n')
        space += '\t'
        f.write(f'{space}<DataItem Format=\"HDF\" Dimensions=\"{n_nodes} 3">\n')
        f.write(f'{space}{hdf5_geo_fn}:{node_path}/node_coord\n')
        f.write(f'{space}</DataItem>\n')
        space = space[:-1]
        f.write(f'{space}</Geometry>\n')

        # link tissue type to tets geometry for visualization
        if 'tet_tissue_type' in hdf5_geo[path_elm + '/']:
            f.write(f'{space}<Attribute Name="tissue_type" AttributeType="Scalar" Center="Cell">\n')
            space += '\t'
            f.write(f'{space}<DataItem Format=\"HDF\" Dimensions=\"{n_tets} 1\">\n')
            f.write(f'{space}{hdf5_geo_fn}:{path_elm}/tet_tissue_type\n')

            f.write(f'{space}</DataItem>\n')
            space = space[:-1]
            f.write(f'{space}</Attribute>\n')

        # data in tets
        if '/data/tets' in hdf5 or '/data/nodes' in hdf5 or '/mesh/fields' in hdf5:

            # elm type
            if 'tet_elm_type' in hdf5_geo[path_elm + '/']:
                f.write('<Attribute Name="elm_type" AttributeType="Scalar" Center="Cell">\n')
                f.write(f'<DataItem Format=\"HDF\" Dimensions=\"{n_tets} 1\">\n')
                f.write(f'{hdf5_geo_fn}:{path_elm}/tet_elm_type\n')
                f.write(f'</DataItem>\n')
                f.write(f'</Attribute>\n')

            # link tet data to geometry
            if '/data/tets' in hdf5:
                # data sets (mostly statistics)
                for key, data in hdf5['/data/tets'].items():
                    value = ""
                    try:
                        if 'value' in list(data.keys()):
                            data = data['value']
                            value = '/value'
                    except (KeyError, AttributeError):
                        pass
                    if hasattr(data, 'shape') and len(data.shape) > 1:
                        if data.shape[1] == 3:
                            attr_type = "Vector"
                            dim = 3
                        elif data.shape[1] == 1:
                            attr_type = "Scalar"
                            dim = 1
                        else:
                            print(("Data shape unknown: " + str(data.shape[1])))
                            attr_type, dim = None, None  # just to make compiler happy
                            quit()
                    else:
                        attr_type = "Scalar"
                        dim = 1

                    f.write('<Attribute Name="' + key + '" AttributeType="' + attr_type + '" Center="Cell">\n')
                    f.write('<DataItem Format="HDF" Dimensions="' + str(n_tets) + ' ' + str(dim) + '">\n')
                    f.write(hdf5_fn + ':/data/tets/' + key + value + '\n')

                    f.write('</DataItem>\n')
                    f.write('</Attribute>\n')
        space = space[:-1]
        f.write(f'{space}</Grid>\n')
    # end tetrahedra data

    # one grid for coil dipole nodes...store data hdf5.
    #######################################################
    if '/coil' in hdf5:
        f.write('<Grid Name="coil" GridType="Uniform">\n')
        f.write('<Topology NumberOfElements="' + str(len(hdf5['/coil/dipole_position'][:])) +
                '" TopologyType="Polyvertex" Name="Tri">\n')
        f.write('<DataItem Format="XML" Dimensions="' + str(len(hdf5['/coil/dipole_position'][:])) + ' 1">\n')
        # f.write(hdf5_fn + ':' + path + '/triangle_number_list\n')
        np.savetxt(f, list(range(len(hdf5['/coil/dipole_position'][:]))), fmt='%d',
                   delimiter=' ')  # 1 2 3 4 ... N_Points
        f.write('</DataItem>\n')
        f.write('</Topology>\n')

        # nodes
        f.write('<Geometry GeometryType="XYZ">\n')
        f.write('<DataItem Format="HDF" Dimensions="' + str(len(hdf5['/coil/dipole_position'][:])) + ' 3">\n')
        f.write(hdf5_fn + ':' + '/coil/dipole_position\n')
        f.write('</DataItem>\n')
        f.write('</Geometry>\n')

        # data
        if '/coil/dipole_moment_mag' in hdf5:
            # dipole magnitude
            f.write('<Attribute Name="dipole_mag" AttributeType="Scalar" Center="Cell">\n')
            f.write('<DataItem Format="HDF" Dimensions="' + str(len(hdf5['/coil/dipole_moment_mag'][:])) + ' 1">\n')
            f.write(hdf5_fn + ':' + '/coil/dipole_moment_mag\n')

            f.write('</DataItem>\n')
            f.write('</Attribute>\n')

        f.write('</Grid>\n')
        # end coil dipole data

    # footer
    f.write('</Grid>\n')
    f.write('</Domain>\n')
    f.write('</Xdmf>\n')
    f.close()

    return xdmf_fn


def write_temporal_xdmf(hdf5_fn, data_folder='c', coil_center_folder=None, coil_ori_0_folder=None,
                        coil_ori_1_folder=None, coil_ori_2_folder=None, coil_current_folder=None, hdf5_geo_fn=None,
                        overwrite_xdmf=True, verbose=False, xdmf_fn=None):
    """
    Creates .xdmf markup file for given ROI hdf5 data file with 4D data. This was written to be able to visualize data
    from the permutation analysis of the regression approach
    It expects an .hdf5 with a data group with (many) subarrays. The N subarrays name should be named from 0 to N-1
    Each subarray has shape ``(N_elemns, 1)``

    Not tested for whole brain.

    .. code-block:: sh

        hdf5:/data_folder/0
                         /1
                         /2
                         /3
                         /4
                         ...

    Parameters
    ----------
    hdf5_fn : str
        Filename of hdf5 file containing the data.
    data_folder : str or list of str
        Path within hdf5 to group of dataframes.
    hdf5_geo_fn : str, optional
        Filename of hdf5 file containing the geometry.
    overwrite_xdmf : bool, default: False
        Overwrite existing .xdmf file if present.
    coil_center_folder :  str, optional
    coil_ori_0_folder : str, optional
    coil_ori_1_folder : str, optional
    coil_ori_2_folder : str, optional
    coil_current_folder : str, optional
    xdmf_fn : str, optional
        Filename of the temporal xdmf file. If not given, created from hdf5 hdf5_fn.
    verbose : bool, default: False
        Print output or not.

    Returns
    -------
    <File> : .xdmf file
        hdf5_fn[-4].xdmf
    """
    hdf5_fn_full = hdf5_fn

    if os.path.splitext(hdf5_fn)[1] not in ['.hdf5', '.h5', '.hdf']:
        raise ValueError("Provide .hdf5 filename for existing file.")

    if xdmf_fn is None:
        xdmf_fn = os.path.splitext(hdf5_fn)[0] + '.xdmf'
    else:
        if not os.path.isabs(xdmf_fn):
            xdmf_fn = os.path.join(os.path.split(hdf5_fn_full)[0], xdmf_fn)

    if hdf5_geo_fn is None:
        hdf5_geo_fn = hdf5_fn

    with h5py.File(hdf5_fn, 'r+') as hdf5, h5py.File(hdf5_geo_fn, 'r+') as hdf5_geo:
        # hdf5 = h5py.File(hdf5_fn, 'r+')
        # hdf5_geo = h5py.File(hdf5_geo_fn, 'r+')

        if os.path.split(hdf5_fn)[0] == os.path.split(hdf5_geo_fn)[0]:
            hdf5_geo_fn = os.path.basename(hdf5_geo_fn)

        hdf5_fn = os.path.basename(hdf5_fn)
        if os.path.isfile(xdmf_fn) and not overwrite_xdmf:
            print((xdmf_fn + ' already exists. Remove or set overwriteXDMF. Quitting.'))
            return

        # check if triangle and tetra data is already in 2 dataframes in hdf5
        # /mesh/elm or /elm/?
        if "/elm/" in hdf5_geo:
            path = '/elm'
        else:
            path = '/mesh/elm'

        if "/nodes/" in hdf5_geo:
            node_path = '/nodes'
        else:
            node_path = '/mesh/nodes'

        if path + "/triangle_number_list" not in hdf5_geo:

            # if not, create
            if verbose:
                print(("triangle_number_list and tetrahedra_number_list do not exist. Adding to " + hdf5_geo_fn + "."))

            # get tris and tets
            triangles = (hdf5_geo[path + '/node_number_list'][:]  # from node_number list...
                         [hdf5_geo[path + '/elm_type'][:] == 2]  # ... take the triangle ones...
            [:, 0:3])
            tetrahedra = (hdf5_geo[path + '/node_number_list'][:]  # same with tetrahedra nodelist
            [hdf5_geo[path + '/elm_type'][:] == 4])

            # add to hdf5_fn and rebase to 0
            hdf5_geo.create_dataset(f'{path}/triangle_number_list', data=triangles - 1)
            hdf5_geo.create_dataset(f'{path}/tetrahedra_number_list', data=tetrahedra - 1)
            n_tets = len(tetrahedra)

        else:
            triangles = hdf5_geo[f'{path}/triangle_number_list']
            try:
                tetrahedra = hdf5_geo[path + '/tetrahedra_number_list']
                n_tets = len(tetrahedra)
            except KeyError:
                tetrahedra = None
                n_tets = 0

        # check if data is divided into tets and tris

        # get information for .xdmf
        n_nodes = len(hdf5_geo[f'{node_path}/node_coord'])
        n_tris = len(triangles)

        # get shape of temporal information
        dimensions = dict()
        if data_folder is not None:
            if isinstance(data_folder, list):
                allkeys = [set(hdf5[dat_folder].keys()) for dat_folder in data_folder]
                data_keys = set.intersection(*allkeys)
                allkeys = set.union(*allkeys)
                dif = allkeys.difference(data_keys)
                if len(dif) != 0:
                    warnings.warn(f"Unequal sets of keys found. Missing keys: {dif}")

                # get first value from dict to get shape of data array
                for dat_folder in data_folder:
                    dimensions[dat_folder] = next(iter(hdf5[dat_folder].values())).shape[0]

            else:
                data_keys = hdf5[data_folder].keys()
                dimensions[data_folder] = next(iter(hdf5[data_folder].values())).shape[0]
        else:
            data_keys = hdf5[coil_center_folder].keys()
            dimensions[data_folder] = next(iter(hdf5[coil_center_folder].values())).shape[0]

        # create .xdmf file
        f = open(xdmf_fn, 'w')
        space = '\t'
        # header
        f.write('<?xml version="1.0"?>\n')
        f.write('<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>\n')
        f.write('<Xdmf Version="2.0" xmlns:xi="http://www.w3.org/2001/XInclude">\n')
        f.write('<Domain>\n')

        # one collection grid
        # f.write('<Grid\nCollectionType="Spatial"\nGridType="Collection"\nName="Collection">\n')
        f.write(f'{space}<Grid Name="GridTime" GridType="Collection" CollectionType="Temporal">\n')
        space += '\t'
        for i in data_keys:
            f.write("\n<!-- " + '#' * 20 + f" Timestep {i:0>3}/{len(data_keys): >3} " + '#' * 20 + ' -->\n')
            if data_folder is not None:
                # one grid for triangles...
                ###########################
                f.write(f'{space}<Grid Name="tris" GridType="Uniform">\n')
                space += '\t'
                f.write(f'{space}<Time Value="{i}" />	\n')
                f.write(f'{space}<Topology NumberOfElements="{n_tris}" TopologyType="Triangle" Name="Tri">\n')
                space += '\t'
                f.write(f'{space}<DataItem Format="HDF" Dimensions="{n_tris} 3">\n')
                space += '\t'
                f.write(f'{space}{hdf5_geo_fn}:{path}/triangle_number_list\n')
                space = space[:-1]
                f.write(f'{space}</DataItem>\n')
                space = space[:-1]
                f.write(f'{space}</Topology>\n\n')

                # nodes
                f.write(f'{space}<Geometry GeometryType="XYZ">\n')
                space += '\t'
                f.write(f'{space}<DataItem Format="HDF" Dimensions="{n_nodes} 3">\n')
                f.write(f'{space}{hdf5_geo_fn}:{node_path}/node_coord\n')
                f.write(f'{space}</DataItem>\n')
                space = space[:-1]
                f.write(f'{space}</Geometry>\n\n')

                # data
                if isinstance(data_folder, list):
                    for dat_folder in data_folder:
                        attribute_name = dat_folder.replace('/', '_').replace('\\', '_')
                        # scalar or vector
                        if len(next(iter(hdf5[dat_folder].values())).shape) > 1:
                            attrtype = 'Vector'
                            data_dims = 3
                        else:
                            attrtype = 'Scalar'
                            data_dims = 1

                        f.write(f'{space}<Attribute Name="{attribute_name}" AttributeType="{attrtype}" Center="Cell">\n')
                        space += '\t'
                        f.write(f'{space}<DataItem Format="HDF" Dimensions="{dimensions[dat_folder]} {data_dims}">\n')
                        f.write(f'{space}{hdf5_fn}:{dat_folder}/{i}\n')
                        f.write(f'{space}</DataItem>\n')
                        space = space[:-1]
                        f.write(f'{space}</Attribute>\n\n')
                else:
                    attribute_name = data_folder.replace('/', '_').replace('\\', '_')
                    # scalar or vector
                    if len(np.squeeze(next(iter(hdf5[data_folder].values()))).shape) > 1:
                        attrtype = 'Vector'
                        data_dims = 3
                    else:
                        attrtype = 'Scalar'
                        data_dims = 1
                    f.write(f'{space}<Attribute Name="{attribute_name}" AttributeType="{attrtype}" Center="Cell">\n')
                    space += '\t'
                    f.write(f'{space}<DataItem Format="HDF" Dimensions="{dimensions[data_folder]} {data_dims}">\n')
                    f.write(f'{space}{hdf5_fn}:{data_folder}/{i}\n')
                    f.write(f'{space}</DataItem>\n')

                    space = space[:-1]
                    f.write(f'{space}</Attribute>\n\n')

                #     for key, data in hdf5['/data/tris'].items():
                #
                #         value = ""
                #         try:
                #             if 'value' in list(data.keys()):
                #                 data = data['value']
                #                 value = '/value'
                #         except (KeyError, AttributeError):
                #             pass
                #         if hasattr(data, 'shape') and len(data.shape) > 1:
                #             if data.shape[1] == 3:
                #                 attr_type = "Vector"
                #                 dim = 3
                #             elif data.shape[1] == 1:
                #                 attr_type = "Scalar"
                #                 dim = 1
                #             else:
                #                 print(("Data shape unknown: " + str(data.shape[1])))
                #                 quit()
                #         else:
                #             attr_type = "Scalar"
                #             dim = 1
                #         assert attr_type
                #         assert dim
                #         # except IndexError or AttributeError:
                #         #                 AttrType = "Scalar"
                #         #                 dim = 1
                #
                #         f.write('<Attribute Name="' + key + '" AttributeType="' + attr_type + '" Center="Cell">\n')
                #         f.write('<DataItem Format="HDF" Dimensions="' + str(n_tris) + ' ' + str(dim) + '">\n')
                #         f.write(hdf5_fn + ':/data/tris/' + key + value + '\n')
                #         f.write('</DataItem>\n')
                #         f.write('</Attribute>\n')
                #         # node data
                # if '/data/nodes' in hdf5:
                #     # data sets (mostly statistics)
                #     for key, data in hdf5['/data/nodes'].items():
                #         value = ""
                #         try:
                #             if 'value' in list(data.keys()):
                #                 data = data['value']
                #                 value = '/value'
                #         except (KeyError, AttributeError):
                #             pass
                #         if hasattr(data, 'shape') and len(data.shape) > 1:
                #             if data.shape[1] == 3:
                #                 attr_type = "Vector"
                #                 dim = 3
                #             elif data.shape[1] == 1:
                #                 attr_type = "Scalar"
                #                 dim = 1
                #             else:
                #                 print(("Data shape unknown: " + str(data.shape[1])))
                #                 quit()
                #
                #                 #                 except IndexError or AttributeError:
                #         else:
                #             attr_type = "Scalar"
                #             dim = 1
                #
                #         f.write('<Attribute Name="' + key + '" AttributeType="' + attr_type + '" Center="Node">\n')
                #         f.write('<DataItem Format="HDF" Dimensions="' + str(n_nodes) + ' ' + str(dim) + '">\n')
                #         f.write(hdf5_fn + ':/data/nodes/' + key + value + '\n')
                #
                #         f.write('</DataItem>\n')
                #         f.write('</Attribute>\n')
                # f.write('</Grid>\n')

                # # ...one grid for tetrahedra...
                # ##################################
                # f.write('<Grid Name="tets" GridType="Uniform">\n')
                # f.write('<Topology NumberOfElements="' + str(n_tris) + '" TopologyType="Tetrahedron" Name="Tet">\n')
                # f.write('<DataItem Format="HDF" Dimensions="' + str(n_tets) + ' 4">\n')
                # f.write(hdf5_geo_fn + ':' + path + '/tetrahedra_number_list\n')
                # f.write('</DataItem>\n')
                # f.write('</Topology>\n')

                # nodes
                f.write(f'{space}<Geometry GeometryType="XYZ">\n')
                space += '\t'
                f.write(f'{space}<DataItem Format="HDF" Dimensions="{n_nodes} 3">\n')
                f.write(f'{space}{hdf5_geo_fn}:{node_path}/node_coord\n')
                f.write(f'{space}</DataItem>\n')
                space = space[:-1]
                f.write(f'{space}</Geometry>\n')

                # link tissue type to tets geometry for visualization
                # if 'tet_tissue_type' in hdf5_geo[path + '/']:
                #     f.write(f'{space}<Attribute Name="tissue_type" AttributeType="Scalar" Center="Cell">\n')
                #     space += '\t'
                #     f.write(f'{space}<DataItem Format=\"HDF\" Dimensions=\"{n_tets} 1\">\n')
                #     f.write(f'{space}{hdf5_geo_fn}:{path}/tet_tissue_type\n')
                #     f.write(f'{space}</DataItem>\n')
                #     space = space[:-1]
                #     f.write(f'{space}</Attribute>\n')
                #     space = space[:-1]
                # if 'tet_tissue_type' in hdf5_geo[path + '/']:
                if 'tri_tissue_type' in hdf5_geo[path].keys():
                    f.write(f'{space}<Attribute Name="tissue_type" AttributeType="Scalar" Center="Cell">\n')
                    space += '\t'
                    f.write(f'{space}<DataItem Format=\"HDF\" Dimensions=\"{n_tris} 1\">\n')
                    f.write(f'{space}{hdf5_geo_fn}:{path}/tri_tissue_type\n')
                    f.write(f'{space}</DataItem>\n')
                    space = space[:-1]
                    f.write(f'{space}</Attribute>\n')
                space = space[:-1]

                # data in tets
                if '/data/tets' in hdf5 or '/data/nodes' in hdf5 or '/mesh/fields' in hdf5:

                    # elm type
                    if 'tet_elm_type' in hdf5_geo[path + '/']:
                        f.write('<Attribute Name="elm_type" AttributeType="Scalar" Center="Cell">\n')
                        f.write(f'<DataItem Format=\"HDF\" Dimensions=\"{str(n_tets)} 1\">\n')
                        f.write(hdf5_geo_fn + ':' + path + '/tet_elm_type\n')
                        f.write('</DataItem>\n')
                        f.write('</Attribute>\n\n')

                    # link tet data to geometry
                    if '/data/tets' in hdf5:
                        # data sets (mostly statistics)
                        for key, data in hdf5['/data/tets'].items():
                            value = ""
                            try:
                                if 'value' in list(data.keys()):
                                    data = data['value']
                                    value = '/value'
                            except (KeyError, AttributeError):
                                pass
                            if hasattr(data, 'shape') and len(data.shape) > 1:
                                if data.shape[1] == 3:
                                    attr_type = "Vector"
                                    dim = 3
                                elif data.shape[1] == 1:
                                    attr_type = "Scalar"
                                    dim = 1
                                else:
                                    print(("Data shape unknown: " + str(data.shape[1])))
                                    attr_type, dim = 0, 0
                                    quit()
                            else:
                                attr_type = "Scalar"
                                dim = 1

                            f.write('<Attribute Name="' + key + '" AttributeType="' + attr_type + '" Center="Cell">\n')
                            f.write(f'<DataItem Format=\"HDF\" Dimensions=\"{n_tets} {dim}\">\n')
                            f.write(hdf5_fn + ':/data/tets/' + key + value + '\n')

                            f.write('</DataItem>\n')
                            f.write('</Attribute>\n')

                f.write(f'{space}</Grid>\n\n')
                # end tetrahedra data

        # footer
        space = space[:-1]
        f.write(f'{space}</Grid>\n\n')

        # one grid for coil dipole nodes...store data hdf5.
        #######################################################
        if '/coil' in hdf5:
            for i in data_keys:
                f.write(f'{space}<Grid Name="GridTime" GridType="Collection" CollectionType="Temporal">\n')

                f.write(f'{space}<Grid Name="coil" GridType="Uniform">\n')
                space += '\t'
                f.write(f'{space}<Time Value="{i}" />	\n')
                f.write(f'{space}<Topology NumberOfElements="' + str(len(hdf5[f'/coil/dipole_position/{i}'][:])) +
                        '" TopologyType="Polyvertex" Name="Tri">\n')
                space += '\t'
                f.write(
                        f'{space}<DataItem Format="XML" Dimensions="' + str(
                                len(hdf5[f'/coil/dipole_position/{i}'][:])) + ' 1">\n')
                # f.write(hdf5_fn + ':' + path + '/triangle_number_list\n')
                np.savetxt(f, list(range(len(hdf5[f'/coil/dipole_position/{i}'][:]))), fmt='%d',
                           delimiter=' ')  # 1 2 3 4 ... N_Points
                f.write(f'{space}</DataItem>\n')
                space = space[:-1]
                f.write(f'{space}</Topology>\n\n')

                # nodes
                f.write(f'{space}<Geometry GeometryType="XYZ">\n')
                space += '\t'
                f.write(
                        f'{space}<DataItem Format="HDF" Dimensions="' + str(
                                len(hdf5[f'/coil/dipole_position/{i}'][:])) + ' 3">\n')

                f.write(space + hdf5_fn + ':' + f'/coil/dipole_position/{i}\n')

                f.write(f'{space}</DataItem>\n')
                space = space[:-1]
                f.write(f'{space}</Geometry>\n\n')
                space = space[:-1]
                # data
                if '/coil/dipole_moment_mag' in hdf5:
                    # dipole magnitude
                    f.write('<Attribute Name="dipole_mag" AttributeType="Scalar" Center="Cell">\n')
                    f.write('<DataItem Format="HDF" Dimensions="' + str(
                            len(hdf5[f'/coil/dipole_moment_mag/{i}'][:])) + ' 1">\n')
                    f.write(hdf5_fn + ':' + f'/coil/dipole_moment_mag/{i}\n')

                    f.write('</DataItem>\n')
                    f.write('</Attribute>\n')

                f.write(f'{space}</Grid>\n')
                # end coil dipole data
                f.write(f'{space}</Grid>\n\n')

        # one grid for coil dipole nodes...store data hdf5.
        #######################################################
        if coil_center_folder is not None:
            f.write(f'{space}<Grid Name="GridTime" GridType="Collection" CollectionType="Temporal">\n')
            for i in data_keys:
                space += '\t'
                with h5py.File(hdf5_fn_full, "r") as g:
                    n_coil_pos = g[f"{coil_center_folder}/{i}"][:].shape[0]
                f.write(f'{space}<Grid Name="stimsites" GridType="Uniform">\n')
                space += '\t'
                f.write(f'{space}<Time Value="{i}" />	\n')

                f.write(
                        f'{space}<Topology NumberOfElements="' + str(
                                n_coil_pos) + '" TopologyType="Polyvertex" Name="Tri">\n')
                space += '\t'
                f.write(f'{space}<DataItem Format="XML" Dimensions="' + str(n_coil_pos) + ' 1">\n')
                space += '\t'
                np.savetxt(f, list(range(n_coil_pos)), fmt='%d', delimiter=' ')  # 1 2 3 4 ... N_Points
                f.write(f'{space}</DataItem>\n')
                space = space[:-1]
                f.write(f'{space}</Topology>\n\n')

                # nodes
                f.write(f'{space}<Geometry GeometryType="XYZ">\n')
                space += '\t'
                f.write(f'{space}<DataItem Format="HDF" Dimensions="' + str(n_coil_pos) + ' 3">\n')
                space += '\t'
                f.write(f'{space}{hdf5_fn}:{coil_center_folder}/{i}\n')
                space = space[:-1]
                f.write(f'{space}</DataItem>\n')
                space = space[:-1]
                f.write(f'{space}</Geometry>\n\n')

                coil_ori_folder = [coil_ori_0_folder, coil_ori_1_folder, coil_ori_2_folder]

                for j in range(3):
                    f.write(f'{space}<Attribute Name="dir_' + str(j) + '" AttributeType="Vector" Center="Cell">\n')
                    space += '\t'
                    f.write(f'{space}<DataItem Format="HDF" Dimensions="' + str(n_coil_pos) + ' 3">\n')
                    space += '\t'
                    f.write(f'{space}{hdf5_fn}:{coil_ori_folder[j]}/{i}\n')
                    space = space[:-1]
                    f.write(f'{space}</DataItem>\n')
                    space = space[:-1]
                    f.write(f'{space}</Attribute>\n\n')

                if coil_current_folder is not None:
                    f.write(f'{space}<Attribute Name="current" AttributeType="Scalar" Center="Cell">\n')
                    space += '\t'
                    f.write(f'{space}<DataItem Format="HDF" Dimensions="' + str(n_coil_pos) + ' 1">\n')
                    space += '\t'
                    f.write(f'{space}{hdf5_fn}:{coil_current_folder}/{i}\n')
                    space = space[:-1]
                    f.write(f'{space}</DataItem>\n')
                    space = space[:-1]
                    f.write(f'{space}</Attribute>\n\n')

                space = space[:-1]
                f.write(f'{space}</Grid>\n\n')
            space = space[:-1]
            f.write(f'{space}</Grid>\n\n')

        f.write('</Domain>\n')
        f.write('</Xdmf>\n')
        f.close()

        hdf5.close()
        hdf5_geo.close()


def create_position_path_xdmf(sorted_fn, coil_pos_fn, output_xdmf, stim_intens=None,
                              coil_sorted='/0/0/coil_seq'):
    """
    Creates one .xdmf file that allows paraview plottings of coil position paths.

    .. figure:: ../../doc/images/create_position_path_xdmf.png
       :scale: 50 %
       :alt: A set of coil positions plotted to show the path of coil movement.

    Paraview can be used to visualize the order of realized stimulation positions.

    Parameters
    ----------
    sorted_fn : str
        .hdf5 filename with position indices, values, intensities from ``pynibs.sort_opt_coil_positions()``.
    coil_pos_fn : str
        .hdf5 filename with original set of coil positions. Indices from sorted_fn are mapped to this.
        Either '/matsimnibs' or 'm1' and 'm2' datasets.
    output_xdmf : str
    stim_intens : int, optional
        Intensities are multiplied by this factor.

    Returns
    -------
    output_xdmf : <file>

    Other Parameters
    ----------------
    coil_sorted : str
        Path to coil positions in sorted_fn
    """
    # get datasets for nodes used in path, goal value, intensity
    sorted_data = h5py.File(sorted_fn, 'r')[coil_sorted][:]
    nodes_idx, goal_val, intens = sorted_data[:, 0].astype(int), sorted_data[:, 1], sorted_data[:, 2]

    # get direction vectors (for all positions)
    with h5py.File(coil_pos_fn, 'r') as f:
        m0 = f['/m0'][:]
        m1 = f['/m1'][:]
        m2 = f['/m2'][:]

    if stim_intens is not None and stim_intens != 0:
        intens *= stim_intens
    write_coil_sequence_xdmf(coil_pos_fn, intens, m0, m1, m2, output_xdmf)


def write_coil_sequence_xdmf(coil_pos_fn, data, vec1, vec2, vec3, output_xdmf):
    # get path from node to node
    n_nodes = vec2.shape[0]
    nodes_path = []
    for i in range(n_nodes - 1):
        nodes_path.append([i, i + 1])
    nodes_path = np.array(nodes_path).astype(int)

    # write .xdmf file
    with open(output_xdmf, 'w') as f:
        # header
        f.writelines('<?xml version="1.0"?>\n'
                     '<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>\n'
                     '<Xdmf Version="2.0" xmlns:xi="http://www.w3.org/2001/XInclude">\n'
                     '<Domain>\n')

        # one collection grid for everything
        f.writelines('  <Grid CollectionType="Spatial" GridType="Collection" Name="Collection">\n')

        # one grid for the lines
        f.writelines('      <Grid Name="path" GridType="Uniform">\n')
        f.writelines('          <Topology NumberOfElements="1764860" TopologyType="Polyline" Name="Tri" '
                     'NodesPerElement="2">\n')
        f.writelines(f'             <DataItem Format="XML" Dimensions="{nodes_path.shape[0]} 2">\n')
        for node_path in nodes_path:
            f.writelines(f"                 {node_path[0]} {node_path[1]}\n")
        f.writelines('             </DataItem>\n')
        f.writelines('          </Topology>\n')
        f.writelines('			<Geometry GeometryType="XYZ">\n')
        f.writelines(f'				<DataItem Format="HDF" Dimensions="{vec2.shape[0]} 3">\n')
        f.writelines(f'				{coil_pos_fn}:/centers\n')
        f.writelines('				</DataItem>\n')
        f.writelines('			</Geometry>\n')

        f.writelines('			<Attribute Name="Stimulation #" AttributeType="Scalar" Center="Cell">\n')
        f.writelines(f'				<DataItem Format="XML" Dimensions="{nodes_path.shape[0]}">\n')
        for i in range(n_nodes - 1):
            f.writelines(f"                 {i + 1}\n")
        f.writelines('				</DataItem>\n')
        f.writelines('			</Attribute>\n')

        f.writelines('			<Attribute Name="line" AttributeType="Scalar" Center="Cell">\n')
        f.writelines(f'				<DataItem Format="XML" Dimensions="{nodes_path.shape[0]}">\n')
        for i in range(n_nodes - 1):
            f.writelines(f"                 {i + 1}\n")
        f.writelines('				</DataItem>\n')
        f.writelines('			</Attribute>\n')

        f.writelines('			<Attribute Name="data" AttributeType="Scalar" Center="Cell">\n')
        f.writelines(f'				<DataItem Format="XML" Dimensions="{nodes_path.shape[0]}">\n')
        for i in data[:-1]:
            f.writelines(f"                 {i}\n")
        f.writelines('				</DataItem>\n')
        f.writelines('			</Attribute>\n')

        f.writelines('		</Grid>\n')

        # one grid for the spheres
        f.writelines('      <Grid Name="nodes" GridType="Uniform">\n')
        f.writelines('          <Topology NumberOfElements="1764860" TopologyType="Polyvertex" Name="nodes" '
                     'NodesPerElement="2">\n')
        f.writelines(f'             <DataItem Format="XML" Dimensions="{nodes_path.shape[0]} 1">\n')
        for i in range(n_nodes):
            f.writelines(f"                 {int(i)}\n")
        f.writelines('             </DataItem>\n\n')
        f.writelines('          </Topology>\n\n')
        f.writelines('			<Geometry GeometryType="XYZ">\n')
        f.writelines(f'				<DataItem Format="HDF" Dimensions="{vec2.shape[0]} 3">\n')
        f.writelines(f'				{coil_pos_fn}:/centers\n')
        f.writelines('				</DataItem>\n')
        f.writelines('			</Geometry>\n')

        # intensity dataset for the spheres
        f.writelines('			<Attribute Name="data" AttributeType="Scalar" Center="Cell">\n')
        f.writelines(f'				<DataItem Format="XML" Dimensions="{n_nodes}">\n')
        for i in data:
            f.writelines(f"                 {i}\n")
        f.writelines('				</DataItem>\n')
        f.writelines('			</Attribute>\n')

        f.writelines('			<Attribute Name="Stimulation #" AttributeType="Scalar" Center="Cell">\n')
        f.writelines(f'				<DataItem Format="XML" Dimensions="{n_nodes}">\n')
        for i in range(n_nodes):
            f.writelines(f"                 {int(i)}\n")
        f.writelines('				</DataItem>\n')
        f.writelines('			</Attribute>\n')

        f.writelines('			<Attribute Name="sphere" AttributeType="Scalar" Center="Cell">\n')
        f.writelines(f'				<DataItem Format="XML" Dimensions="{n_nodes}">\n')
        for i in range(n_nodes):
            f.writelines(f"                 {int(i)}\n")
        f.writelines('				</DataItem>\n')
        f.writelines('			</Attribute>\n')

        # direction dataset for spheres
        for idx, vecs in enumerate([vec1, vec2, vec3]):
            f.writelines(f'          <Attribute Name="dir_{idx}" AttributeType="Vector" Center="Cell">\n')
            f.writelines(f'              <DataItem Format="XML" Dimensions="{n_nodes} 3">\n')
            for i in range(n_nodes):
                f.writelines(f"                 {vecs[i][0]} {vecs[i][1]} {vecs[i][2]} \n")
            f.writelines('              </DataItem>\n')
            f.writelines('          </Attribute>\n')
            f.writelines('          \n')
        f.writelines('\n')
        f.writelines('		</Grid>\n')

        # collection grid close
        f.writelines('	</Grid>\n')
        f.writelines('</Domain>\n</Xdmf>')


def create_fibre_xdmf(fn_fibre_geo_hdf5, fn_fibre_data_hdf5=None, overwrite=True, fibre_points_path="fibre_points",
                      fibre_con_path="fibre_con", fibre_data_path=""):
    """
    Creates .xdmf file to plot fibres in Paraview

    Parameters
    ----------
    fn_fibre_geo_hdf5 : str
        Path to fibre_geo.hdf5 file containing the geometry (in /plot subfolder created with create_fibre_geo_hdf5())
    fn_fibre_data_hdf5 : str (optional) default: None
        Path to fibre_data.hdf5 file containing the data to plot (in parent folder)
    fibre_points_path : str (optional) default: fibre_points
        Path to fibre point array in .hdf5 file
    fibre_con_path : str (optional) default: fibre_con
        Path to fibre connectivity array in .hdf5 file
    fibre_data_path : str (optional) default: ""
        Path to parent data folder in data.hdf5 file (Default: no parent folder)

    Returns
    -------
    <File> : .xdmf file for Paraview
    """
    if fn_fibre_data_hdf5 is None:
        fn_xdmf = os.path.splitext(fn_fibre_geo_hdf5)[0] + ".xdmf"

    else:
        fn_xdmf = os.path.splitext(fn_fibre_data_hdf5)[0] + ".xdmf"

        data_dict = dict()
        with h5py.File(fn_fibre_data_hdf5, "r") as f:
            for key in f.keys():
                data_dict[key] = f[key][:]

    with h5py.File(fn_fibre_geo_hdf5, "r") as f:
        n_con = f[fibre_con_path][:].shape[0]
        n_points = f[fibre_points_path][:].shape[0]

    if os.path.exists(fn_xdmf) and not overwrite:
        print("Aborting .xdmf file already exists (overwrite=False)")
        return

    with open(fn_xdmf, 'w') as xdmf:
        # Header
        xdmf.write(f'<?xml version="1.0"?>\n')
        xdmf.write(f'<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>\n')
        xdmf.write(f'<Xdmf Version="2.0" xmlns:xi="http://www.w3.org/2001/XInclude">\n')

        # Domain and Grid
        xdmf.write(f'<Domain>\n')
        xdmf.write(f'<Grid\n')
        xdmf.write(f'CollectionType="Spatial"\n')
        xdmf.write(f'GridType="Collection"\n')
        xdmf.write(f'Name="Collection">\n')
        xdmf.write(f'<Grid Name="fibres" GridType="Uniform">\n')

        # Topology (connectivity)
        xdmf.write(f'<Topology NumberOfElements="{n_con}" TopologyType="Polyline" NodesPerElement="2" Name="fibres">\n')
        xdmf.write(f'<DataItem Format="HDF" Dimensions="{n_con} 2">\n')
        xdmf.write(f'{fn_fibre_geo_hdf5}:{fibre_con_path}\n')
        xdmf.write(f'</DataItem>\n')
        xdmf.write(f'</Topology>\n')

        # Geometry (points)
        xdmf.write(f'<Geometry GeometryType="XYZ">\n')
        xdmf.write(f'<DataItem Format="HDF" Dimensions="{n_points} 3">\n')
        xdmf.write(f'{fn_fibre_geo_hdf5}:{fibre_points_path}\n')
        xdmf.write(f'</DataItem>\n')
        xdmf.write(f'</Geometry>\n')

        # Data
        if fn_fibre_data_hdf5 is not None:
            for data_name in data_dict.keys():
                data_shape_0 = data_dict[data_name].shape[0]

                if data_dict[data_name].ndim < 2:
                    data_shape_1 = 1
                else:
                    data_shape_1 = data_dict[data_name].shape[1]

                xdmf.write(f'<Attribute Name="{data_name}" AttributeType="Scalar" Center="Cell">\n')
                xdmf.write(f'<DataItem Format="HDF" Dimensions="{data_shape_0} {data_shape_1}">\n')
                xdmf.write(f'{fn_fibre_data_hdf5}:{fibre_data_path}/{data_name}\n')
                xdmf.write(f'</DataItem>\n')
                xdmf.write(f'</Attribute>\n')

        xdmf.write(f'</Grid>\n')
        xdmf.write(f'</Grid>\n')
        xdmf.write(f'</Domain>\n')
        xdmf.write(f'</Xdmf>\n')


def data_superimpose(fn_in_hdf5_data, fn_in_geo_hdf5, fn_out_hdf5_data, data_hdf5_path='/data/tris/',
                     data_substitute=-1, normalize=False):
    """
    Overlaying data stored in .hdf5 files except in regions where data_substitute is found. These points
    are omitted in the analysis and will be replaced by data_substitute instead.

    Parameters
    ----------
    fn_in_hdf5_data: list of str
        Filenames of .hdf5 data files with common geometry, e.g. generated by pynibs.data_sub2avg(...).
    fn_in_geo_hdf5: str
        Geometry .hdf5 file, which corresponds to the .hdf5 data files.
    fn_out_hdf5_data: str
        Filename of .hdf5 data output file containing the superimposed data.
    data_hdf5_path: str
        Path in .hdf5 data file where data is stored (e.g. ``'/data/tris/'``).
    data_substitute: float or np.NaN, default: -1
        Data substitute with this number for all points in the inflated brain, which do not belong to
        the given data set.
    normalize: bool or str, default: False
        Decide if individual datasets are normalized w.r.t. their maximum values before they are superimposed.

        * 'global': global normalization w.r.t. maximum value over all datasets and subjects
        * 'dataset': dataset wise normalization w.r.t. maximum of each dataset individually (over subjects)
        * 'subject': subject wise normalization (over datasets)

    Returns
    -------
    <File>: .hdf5 file
        Overlayed data.
    """

    n_subjects = len(fn_in_hdf5_data)
    data_dic = [dict() for _ in range(n_subjects)]
    labels = [''] * n_subjects
    percentile = [99]

    # load .hdf5 data files and save them in dictionaries
    for i, filename in enumerate(fn_in_hdf5_data):
        with h5py.File(filename, 'r') as f:
            labels[i] = list(f[data_hdf5_path].keys())
            for j, label in enumerate(labels[i]):
                data_dic[i][label] = f[data_hdf5_path + label][:]
                # normalize data if desired

    # find matching labels in all datasets
    cmd = " ".join(['set(labels[' + str(int(i)) + ']) &' for i in range(n_subjects)])[0:-2]
    data_labels = list(eval(cmd))

    # reform data
    data = [np.zeros((data_dic[0][data_labels[i]].shape[0], n_subjects)) for i in range(len(data_labels))]
    for i, label in enumerate(data_labels):
        for j in range(n_subjects):
            data[i][:, j] = data_dic[j][label].flatten()

    del data_dic

    # Normalize each dataset over subjects to 1
    if normalize == 'dataset':
        for i in range(len(data_labels)):
            mask = np.all(data[i] != data_substitute, axis=1)
            data[i][mask, :] = data[i][mask, :] / np.tile(np.percentile(data[i][mask, :],
                                                                        percentile)[0],
                                                          (np.sum(mask), 1))

            # trim values > 1 from percentile to 1
            mask_idx = np.where(mask)[0]
            data[i][mask_idx[data[i][mask, :] > 1], :] = 1
            # np.max(data[i][mask, :], axis=0)

    elif normalize == 'subject':
        # subject - wise
        for i_subj in range(n_subjects):
            sub_data = np.array(())
            mask = np.array(())
            max_val = []

            # dataset - wise
            for i_data in range(len(data_labels)):
                mask = np.append(mask, np.all(data[i_data] != data_substitute, axis=1))
                sub_data = np.append(sub_data, data[i_data][:, i_subj])
                max_val.append(np.percentile(sub_data[mask == 1.], percentile)[0])

            # max(max) over all datasets
            max_val = np.max(max_val)
            for i_data in range(len(data_labels)):
                mask = np.all(data[i_data] != data_substitute, axis=1)
                data[i_data][mask, i_subj] /= max_val

                # trim values > 1 from percentile to 1
                mask_idx = np.where(mask)[0]
                data[i_data][mask_idx[data[i_data][mask, i_subj] > 1], i_subj] = 1

    # Find max of all datasets of all subject and normalize w.r.t. this value
    elif normalize == 'global':
        data_max = []
        # mag, norm, tan
        for i in range(len(data_labels)):
            mask = np.all(data[i] != data_substitute, axis=1)
            # take max(subject-wise 99.9percentile)
            data_max.append(np.max(np.percentile(data[i][mask, :], percentile, axis=0)[0]))

        # find maximum of mag, norm, tan
        data_max = np.max(data_max)

        # normalize
        for i in range(len(data_labels)):
            mask = np.all(data[i] != data_substitute, axis=1)
            # data[i][mask, :] = data[i][mask, :]/np.tile(data_max, (np.sum(mask), 1))
            data[i][mask, :] = data[i][mask, :] / data_max

            # trim values > 1 from percentile to 1
            mask_idx = np.where(mask)[0]
            data[i][mask_idx[data[i][mask, :] > 1], :] = 1

    # average data in regions where values are defined in every dataset
    data_mean = [np.ones(data[i].shape[0]) * data_substitute for i in range(len(data_labels))]

    for i in range(len(data_labels)):
        mask = np.all(data[i] != data_substitute, axis=1)
        data_mean[i][mask] = np.mean(data[i][mask, :], axis=1)

    # create results directory
    if not os.path.exists(os.path.split(fn_out_hdf5_data)[0]):
        os.makedirs(os.path.split(fn_out_hdf5_data)[0])

    # copy .hdf5 geometry file to results folder of .hdf5 data file
    os.system('cp ' + fn_in_geo_hdf5 + ' ' + os.path.split(fn_out_hdf5_data)[0])

    # rename .hdf5 geo file to match with .hdf5 data file
    fn_in_geo_hdf5_new = os.path.splitext(fn_out_hdf5_data)[0] + '_geo.hdf5'
    os.system('mv ' + os.path.join(os.path.split(fn_out_hdf5_data)[0], os.path.split(fn_in_geo_hdf5)[1]) + ' ' +
              fn_in_geo_hdf5_new)

    # write data to .hdf5 data file
    pynibs.write_data_hdf5_surf(data=data_mean,
                                data_names=data_labels,
                                data_hdf_fn_out=fn_out_hdf5_data,
                                geo_hdf_fn=fn_in_geo_hdf5_new,
                                replace=True)


def write_xdmf_coordinates(fn_xdmf, coords_center):
    """
    Writes the coordinates to an XDMF file for visualization.

    Parameters
    ----------
    fn_xdmf : str
        The filename of the XDMF file to be written.
    coords_center : np.ndarray
        The coordinates to be written to the XDMF file.
        This should be a 2D array where each row represents a point in 3D space.
    """
    with open(fn_xdmf, 'w') as f:
        # header
        f.write('<?xml version="1.0"?>\n')
        f.write('<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>\n')
        f.write('<Xdmf Version="2.0" xmlns:xi="http://www.w3.org/2001/XInclude">\n')
        f.write('<Domain>\n')
        f.write('<Grid CollectionType="Spatial" GridType="Collection" Name="Collection">\n')

        # one grid for coil dipole nodes...store data hdf5.
        #######################################################
        f.write('<Grid Name="stimsites" GridType="Uniform">\n')
        f.write(f'<Topology NumberOfElements="{coords_center.shape[0]}" TopologyType="Polyvertex" Name="Tri">\n')
        f.write(f'\t<DataItem Format="XML" Dimensions="{coords_center.shape[0]} 1">\n')
        np.savetxt(f, list(range(coords_center.shape[0])), fmt='\t%d', delimiter=' ')  # 1 2 3 4 ... N_Points
        f.write('\t</DataItem>\n')
        f.write('</Topology>\n\n')

        # nodes
        f.write('<Geometry GeometryType="XYZ">\n')
        f.write(f'\t<DataItem Format="XML" Dimensions="{coords_center.shape[0]} 3">\n')
        np.savetxt(f, coords_center, fmt='\t%d', delimiter=' ')  # 1 2 3 4 ... N_Points
        f.write('\t</DataItem>\n')
        f.write('</Geometry>\n\n')

        # data
        # dipole magnitude
        # the 4 vectors
        f.write(f'\t\t<Attribute Name="id" AttributeType="Scalar" Center="Cell">\n')
        f.write('\t\t\t<DataItem Format="XML" Dimensions="' + str(coords_center.shape[0]) + ' 1">\n')
        for i in range(coords_center.shape[0]):
            f.write(f'\t\t\t{i}\n')
        f.write('\t\t\t</DataItem>\n')
        f.write('\t\t</Attribute>\n\n')

        f.write('</Grid>\n')
        # end coil dipole data

        # footer
        f.write('</Grid>\n')
        f.write('</Domain>\n')
        f.write('</Xdmf>\n')
