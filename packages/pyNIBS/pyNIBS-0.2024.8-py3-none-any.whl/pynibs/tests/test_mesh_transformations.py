import unittest
import numpy as np
import os
import meshio
import tempfile
from pynibs import (point_data_to_cell_data_vtk,
                    cell_data_to_point_data_vtk,
                    cell_data_to_point_data,
                    data_nodes2elements)


class TestMeshFunctions(unittest.TestCase):
    def setUp(self):
        # Create a simple mesh for testing
        self.points = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
        self.con = np.array([[0, 1, 2]])
        cells = [("triangle", self.con)]

        self.cell_data = {"test": [np.array([[1]])]}
        self.mesh_cell_data_1d = meshio.Mesh(self.points, cells, cell_data=self.cell_data)

        self.cell_data = {"test": [np.array([[1, 2, 3]])]}
        self.mesh_cell_data_3d = meshio.Mesh(self.points, cells, cell_data=self.cell_data)

        cell_data = {"test": [np.array([[1, 2, 3]])],
                     "test2": [np.array([[100, 200, 300]])]}
        self.mesh_cell_datas_3d = meshio.Mesh(self.points, cells, cell_data=cell_data)

        # Create another mesh for testing with point data
        self.point_data = {"test": np.array([[1, 2, 3],
                                             [1, 2, 3],
                                             [1, 2, 3]])}
        self.mesh_point_data_3d = meshio.Mesh(self.points, cells, point_data=self.point_data)

        point_data = {"test": np.array([1, 2, 3])}
        self.mesh_point_data_1d = meshio.Mesh(self.points, cells, point_data=point_data)

        point_data = {"test": np.array([1, 2, 3]),
                      "test2": np.array([100, 200, 300])}
        self.mesh_point_datas_1d = meshio.Mesh(self.points, cells, point_data=point_data)

    def test_point_to_cell_data(self):
        # Test conversion from point data to cell data for both meshes
        for mesh in [self.mesh_point_data_1d, self.mesh_point_data_3d]:
            with tempfile.NamedTemporaryFile(suffix=".vtu") as temp_file:
                cell_data = point_data_to_cell_data_vtk(mesh, fn=temp_file.name)
                self.assertTrue("test" in cell_data)
                self.assertEqual(cell_data["test"].shape[0], mesh.cells[0].data.shape[0])
                self.assertTrue(os.path.exists(temp_file.name))

    def test_cell_to_point_data(self):
        # Test conversion from cell data to point data for both meshes
        for mesh in [self.mesh_cell_data_1d, self.mesh_cell_data_3d]:
            with tempfile.NamedTemporaryFile(suffix=".vtu") as temp_file:
                point_data = cell_data_to_point_data_vtk(mesh, fn=temp_file.name)
                self.assertTrue("test" in point_data)
                self.assertEqual(point_data["test"].shape[0], mesh.points.shape[0])
                self.assertTrue(os.path.exists(temp_file.name))

    def test_point_to_cell_data_from_con(self):
        # Test conversion from point data to cell data for both meshes
        for mesh in [self.mesh_point_data_1d, self.mesh_point_data_3d]:
            with tempfile.NamedTemporaryFile(suffix=".vtu") as temp_file:
                cell_data = point_data_to_cell_data_vtk(nodes=self.points,
                                                        con=self.con,
                                                        point_data=self.point_data, fn=temp_file.name)
                self.assertTrue("test" in cell_data)
                self.assertEqual(cell_data["test"].shape[0], mesh.cells[0].data.shape[0])
                self.assertTrue(os.path.exists(temp_file.name))

    def test_cell_to_point_data_from_con(self):
        # Test conversion from cell data to point data for both meshes
        for mesh in [self.mesh_cell_data_1d, self.mesh_cell_data_3d]:
            with tempfile.NamedTemporaryFile(suffix=".vtu") as temp_file:
                point_data = cell_data_to_point_data_vtk(nodes=self.points,
                                                         con=self.con,
                                                         cell_data=self.cell_data,
                                                         fn=temp_file.name)
                self.assertTrue("test" in point_data)
                self.assertEqual(point_data["test"].shape[0], mesh.points.shape[0])
                self.assertTrue(os.path.exists(temp_file.name))

    def test_point_to_cell_multiple_data(self):
        # Test conversion from point data to cell data for both meshes
        mesh = self.mesh_point_datas_1d
        with tempfile.NamedTemporaryFile(suffix=".vtu") as temp_file:
            cell_data = point_data_to_cell_data_vtk(mesh, fn=temp_file.name)
            self.assertTrue("test" in cell_data)
            self.assertEqual(cell_data["test"].shape[0], mesh.cells[0].data.shape[0])
            self.assertTrue("test2" in cell_data)
            self.assertEqual(cell_data["test2"].shape[0], mesh.cells[0].data.shape[0])
            self.assertTrue(os.path.exists(temp_file.name))

    def test_cell_to_point_multiple_data(self):
        # Test conversion from cell data to point data for both meshes
        mesh = self.mesh_cell_datas_3d
        with tempfile.NamedTemporaryFile(suffix=".vtu") as temp_file:
            point_data = cell_data_to_point_data_vtk(mesh, fn=temp_file.name)
            self.assertTrue("test" in point_data)
            self.assertEqual(point_data["test"].shape[0], mesh.points.shape[0])
            self.assertTrue("test2" in point_data)
            self.assertEqual(point_data["test2"].shape[0], mesh.points.shape[0])
            self.assertTrue(os.path.exists(temp_file.name))

    def test_cell_data_to_point_data(self):
        # Convert the cell data to point data
        data_nodes = cell_data_to_point_data(self.con, self.cell_data['test'][0], self.points)

        # Check the result
        self.assertEqual(data_nodes.shape, self.points.shape)
        self.assertTrue(np.all(data_nodes >= 1) and np.all(data_nodes <= 4))

    def test_data_nodes2elements(self):
        # Convert the node data to element data
        data_tris = data_nodes2elements(self.point_data['test'], self.con)

        # Check the result
        self.assertEqual(data_tris.shape, self.con.shape)
        self.assertTrue(np.all(data_tris >= 1) and np.all(data_tris <= 4))


if __name__ == "__main__":
    unittest.main()
