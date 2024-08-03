import sys
import h5py
import os.path
import numpy as np


def render_coil_positions(
        coil_conf_set_1_positions,
        coil_conf_set_1_orientations,
        coil_conf_set_2_positions=None,
        coil_conf_set_2_orientations=None,
        coil_conf_set_3_positions=None,
        coil_conf_set_3_orientations=None,
        fn_mesh=None,
        surf_type="skin",
        viewport_dim=(1280, 720),
        camera_polar_coords=(-175, 66, 110),
        screenshot_fn=None,
        interactive=False):
    """
    Plots coil positions (and their orientation) in space,
    optionally also display a second set of coil positions,
    optionally also display a surface (e.g. gray matter or skin)

    Parameters:
    -----------
    coil_conf_set_1_positions : np.ndarray
        The "center" coordinates of the primary coil configurations
    coil_conf_set_1_orientations : np.ndarray
         Either the "m0", "m1" or "m2" orientation vector of the primary coil position.
    coil_conf_set_2_positions : np.ndarray | None, optional
        The "center" coordinates of the secondary coil configurations. Can be omitted.
    coil_conf_set_2_orientations : np.ndarray | None, optional
         Either the "m0", "m1" or "m2" orientation vector of the secondary coil position. Can be omitted.
    fn_mesh : str, optional
        Path to the mesh hdf5-file containing the geometry information of a head model. Can be omitted.
    surf_type : str, optional
        Name of the surface to display. Currently supported: "skin", "skull", "csf", "gm", "wm"
        Only valid if 'fn_mesh' has been provided.

    Returns:
    --------
    True if successful, False in case of a fatal error.
    """
    try:
        import mayavi.mlab
    except ModuleNotFoundError:
        print("[render_3D.py] Error: Cannot import module mayavi. Most rendering functions will not work.")
    if "mayavi" in sys.modules:
        if not interactive:
            mayavi.mlab.options.offscreen = True
        else:
            mayavi.mlab.options.offscreen = False

        if not isinstance(viewport_dim, tuple) or len(viewport_dim) != 2:
            viewport_dim = (1280, 720)
            print(
                "[render_coil_positions] Error: Provided viewport dimensions are not in the required format: (x,y),"
                "expected 2 integer representing x,y coordinates of the viewport. Will use default dimensions instead:"
                "(1280,720)")

        random_figure_id = int(np.random.default_rng().random(1)[0] * 1e9)
        fig = mayavi.mlab.figure(figure=random_figure_id, bgcolor=(1, 1, 1), engine=None, fgcolor=(0., 0., 0.),
                                 size=viewport_dim)

        if fn_mesh is not None and os.path.exists(fn_mesh):
            with h5py.File(fn_mesh, 'r') as mesh_h5:

                # tissue tags from SimNIBS v2 - v4
                tissue_tag = 1005  # default to skin

                if surf_type == "wm":
                    tissue_tag = 1001
                elif surf_type == "gm":
                    tissue_tag = 1002
                elif surf_type == "csf":
                    tissue_tag = 1003
                elif surf_type == "skull":
                    tissue_tag = 1007
                elif surf_type == "skin":
                    tissue_tag = 1005
                else:
                    print(f"[render_coil_positions] Error: Unsupported surface type '{surf_type}'. Will "
                          f"render skin surface per default.")

                mesh_tissue_type = np.array(mesh_h5["/mesh/elm/tri_tissue_type"])
                mesh_tris = np.array(mesh_h5["/mesh/elm/node_number_list"][:, :3])
                mesh_pts = np.array(mesh_h5["/mesh/nodes/node_coord"])
                surf_tris_idcs = np.where(mesh_tissue_type == tissue_tag)
                surf_tris = mesh_tris[surf_tris_idcs]

                scalp_surf = mayavi.mlab.triangular_mesh(
                    mesh_pts[:, 0],
                    mesh_pts[:, 1],
                    mesh_pts[:, 2],
                    surf_tris,
                    representation='surface',
                    opacity=1,
                    color=(0.8, 0.8, 0.8)
                )

        if coil_conf_set_2_positions is not None and coil_conf_set_2_orientations is not None:
            mayavi.mlab.points3d(
                coil_conf_set_2_positions[:, 0],
                coil_conf_set_2_positions[:, 1],
                coil_conf_set_2_positions[:, 2],
                scale_factor=0.3,
                color=(.9, .9, .9)
            )

            mayavi.mlab.quiver3d(
                coil_conf_set_2_positions[:, 0],
                coil_conf_set_2_positions[:, 1],
                coil_conf_set_2_positions[:, 2],
                coil_conf_set_2_orientations[:, 0],
                coil_conf_set_2_orientations[:, 1],
                coil_conf_set_2_orientations[:, 2],
                mode="arrow",
                scale_factor=1,
                color=(.9, .9, .9)
            )
        mayavi.mlab.points3d(
            coil_conf_set_1_positions[:, 0],
            coil_conf_set_1_positions[:, 1],
            coil_conf_set_1_positions[:, 2],
            scale_factor=0.5,
            color=(1., .0, .0)
        )

        mayavi.mlab.quiver3d(
            coil_conf_set_1_positions[:, 0],
            coil_conf_set_1_positions[:, 1],
            coil_conf_set_1_positions[:, 2],
            coil_conf_set_1_orientations[:, 0],
            coil_conf_set_1_orientations[:, 1],
            coil_conf_set_1_orientations[:, 2],
            mode="arrow",
            scale_factor=2,
            color=(1., .0, .0)
        )

        if coil_conf_set_3_positions is not None and coil_conf_set_3_orientations is not None:
            mayavi.mlab.points3d(
                coil_conf_set_3_positions[:, 0],
                coil_conf_set_3_positions[:, 1],
                coil_conf_set_3_positions[:, 2],
                scale_factor=2,
                color=(0.161, 0.812, 0.247)
            )

            mayavi.mlab.quiver3d(
                coil_conf_set_3_positions[:, 0],
                coil_conf_set_3_positions[:, 1],
                coil_conf_set_3_positions[:, 2],
                coil_conf_set_3_orientations[:, 0],
                coil_conf_set_3_orientations[:, 1],
                coil_conf_set_3_orientations[:, 2],
                mode="arrow",
                scale_factor=4,
                color=(0.161, 0.812, 0.247)
            )


        if not isinstance(camera_polar_coords, tuple) or len(camera_polar_coords) != 3:
            print(
                "[render_coil_positions] Error: Provided camera coordinates are not in the required format: (a,p,r), "
                "3 floats "
                "representing azimuthal angle, polar angle and radius. Will use default coordinates instead:"
                "(-175, 66, 110)")
            camera_polar_coords = (-175, 66, 110)

        mean_pts = np.mean(coil_conf_set_1_positions, axis=0)
        mayavi.mlab.view(
            azimuth=camera_polar_coords[0],
            elevation=camera_polar_coords[1],
            distance=camera_polar_coords[2],
            focalpoint=np.array(mean_pts),
            roll=None, reset_roll=None, figure=None
        )

        if screenshot_fn is not None:
            # Bug? Must execute the command twice to generate an output screenshot of the requested dimensions.
            # Otherwise its dimensions will be always (300,300).
            mayavi.mlab.savefig(filename=screenshot_fn, figure=fig)
            mayavi.mlab.savefig(filename=screenshot_fn, figure=fig)

        if interactive:
            mayavi.mlab.show()

        # In theory, passing a reference of the to-be closed figure should be
        # sufficient as well. In practice, it did not work reliably yielding
        # error after too many calls to that function because of too many open
        # figures. Introducing a (random) figure-ID and using this ID to refer
        # to the figure seemed to have solved the isse.
        mayavi.mlab.close(random_figure_id)
        mayavi.mlab.close(all=True)

        return True

    else:
        print("[render_coil_positions] Error: Required module 'mayavi' could be not successfully imported."
              "Is it installed? Cannot execute 'render_data_on_surface'.")

    return False


def render_data_on_surface(
        points,
        tris,
        data,
        viewport_dim=(1280, 720),
        camera_polar_coords=(-175, 66, 110),
        title=None,
        data_name="Data",
        colormap="jet",
        screenshot_fn=None,
        interactive=False
):
    """
    Plots data on surface:
    - If the number of data points equals the number of vertices in the mesh, the data will be displayed as point data.
    - If the number of data points equals the number of triangles in the mesh, the data will be displayed as cell data.

    Parameters
    ----------
    points : np.darray[float], [n_points x 3]
        Points (vertices) of surface mesh.
    tris : np.array[float], [n_tris x 3]
        Connectivity list of triangles.
    data : np.array[float], [n_tris]
        Data in triangular center
    viewport_dim : Tuple[int, int]
        Size of the viewport. Default: (1280, 720)
    camera_polar_coords : Tuple[float, float, float)
        The coordinate of the camera around the object in polar coordinates: (azimuthal angle, polar angle, radius)
    title : str
        Tile of the rendering window.
    data_name : str
        Name of the visualized data set.
    colormap : str
        Identifier of the desired color map. Available colormaps are:
        'Accent', 'Blues', 'BrBG', 'BuGn', 'BuPu', 'CMRmap', 'Dark2', 'GnBu', 'Greens', 'Greys'
        'OrRd', 'Oranges', 'PRGn', 'Paired', 'Pastel1', 'Pastel2', 'PiYG', 'PuBu', 'PuBuGn', 'PuOr',
        'PuRd', 'Purples', 'RdBu', 'RdGy', 'RdPu', 'RdYlBu', 'RdYlGn', 'Reds', 'Set1', 'Set2', 'Set3'
        'Spectral', 'Vega10', 'Vega20', 'Vega20b', 'Vega20c', 'Wistia', 'YlGn', 'YlGnBu', 'YlOrBr',
        'YlOrRd', 'afmhot', 'autumn', 'binary', 'black-white', 'blue-red', 'bone', 'brg', 'bwr',
        'cool', 'coolwarm', 'copper', 'cubehelix', 'file', 'flag', 'gist_earth', 'gist_gray',
        'gist_heat', 'gist_ncar', 'gist_rainbow', 'gist_stern', 'gist_yarg', 'gnuplot', 'gnuplot2', 'gray',
        'hot', 'hsv', 'inferno', 'jet', 'magma', 'nipy_spectral', 'ocean', 'pink', 'plasma', 'prism',
        'rainbow', 'seismic', 'spectral', 'spring', 'summer', 'terrain', 'viridis', 'winter'
    screenshot_fn : str | None
        If provided a screenshot will be saved to that path.
    interactive : bool
        If true, a blocking window will be spawned.

    Returns
    -------
    True if successful, False in case of a fatal error.
    """
    try:
        import mayavi.mlab
    except ModuleNotFoundError:
        print("[render_3D.py] Error: Cannot import module mayavi. Most rendering functions will not work.")
    if "mayavi" in sys.modules:
        if not interactive:
            mayavi.mlab.options.offscreen = True
        else:
            mayavi.mlab.options.offscreen = False

        if not isinstance(viewport_dim, tuple) or len(viewport_dim) != 2:
            viewport_dim = (1280, 720)
            print(
                "[render_data_on_surface] Error: Provided viewport dimensions are not in the required format: (x,y),"
                "expected 2 integer representing x,y coordinates of the viewport. Will use default dimensions instead:"
                "(1280,720)")

        random_figure_id = int(np.random.default_rng().random(1)[0] * 1e9)
        fig = mayavi.mlab.figure(figure=random_figure_id, bgcolor=(1, 1, 1), engine=None, fgcolor=(0., 0., 0.),
                                 size=viewport_dim)
        mesh = mayavi.mlab.triangular_mesh(points[:, 0], points[:, 1], points[:, 2], tris, representation='wireframe',
                                           opacity=0)

        if data.shape[0] == tris.shape[0]:
            mesh.mlab_source.dataset.cell_data.scalars = data
            mesh.mlab_source.dataset.cell_data.scalars.name = data_name
            mesh.mlab_source.update()
            mesh.parent.update()
            mesh = mayavi.mlab.pipeline.set_active_attribute(mesh, cell_scalars=data_name)
        elif data.shape[0] == points.shape[0]:
            mesh.mlab_source.dataset.point_data.scalars = data
            mesh.mlab_source.dataset.point_data.scalars.name = data_name
            mesh.mlab_source.update()
            mesh.parent.update()
            mesh = mayavi.mlab.pipeline.set_active_attribute(mesh, point_scalars=data_name)
        else:
            print(
                "[render_data_on_surface] Error: Provided data does neither equal the number of ertices nor triangles "
                "of the "
                "surface mesh. Cannot map data onto mesh.")
            return False

        surf = mayavi.mlab.pipeline.surface(mesh, colormap=colormap, vmin=0, vmax=1)

        if not isinstance(camera_polar_coords, tuple) or len(camera_polar_coords) != 3:
            print(
                "[render_data_on_surface] Error: Provided camera coordinates are not in the required format: (a,p,r), "
                "3 floats "
                "representing azimuthal angle, polar angle and radius. Will use default coordinates instead:"
                "(-175, 66, 110)")
            camera_polar_coords = (-175, 66, 110)

        mean_pts = np.mean(points, axis=0)
        mayavi.mlab.view(
            azimuth=camera_polar_coords[0],
            elevation=camera_polar_coords[1],
            distance=camera_polar_coords[2],
            focalpoint=np.array(mean_pts),
            roll=None, reset_roll=None, figure=None
        )

        mayavi.mlab.colorbar(
            surf,
            title=title
        )

        if screenshot_fn is not None:
            # Bug? Must execute the command twice to generate an output screenshot of the requested dimensions.
            # Otherwise its dimensions will be always (300,300).
            mayavi.mlab.savefig(filename=screenshot_fn, figure=fig)
            mayavi.mlab.savefig(filename=screenshot_fn, figure=fig)

        if interactive:
            mayavi.mlab.show()

        # In theory, passing a reference of the to-be closed figure should be
        # sufficient as well. In practice, it did not work reliably yielding
        # error after too many calls to that function because of too many open
        # figures. Introducing a (random) figure-ID and using this ID to refer
        # to the figure seemed to have solved the isse.
        mayavi.mlab.close(random_figure_id)

        return True
    else:
        print("[render_data_on_surface] Error: Required module 'mayavi' could not be successfully imported."
              "Is it installed? Cannot execute 'render_data_on_surface'.")

        return False
