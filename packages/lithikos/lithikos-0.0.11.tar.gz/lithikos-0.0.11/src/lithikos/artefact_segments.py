import enum
import vedo
import numpy as np


class SegmentationMethod(enum.Enum):
    COLLAPSE_TO_PLANE = 1  # Creates a flange artefact on quadrants
    COLLAPSE_TO_POINT = 2  # Creates a set of triangular artefacts on plane faces


class ArtefactSegments:
    def segment_mesh_dorsal(
        self,
        mesh: vedo.Mesh,
        segmentation_method: SegmentationMethod,
    ) -> vedo.Mesh:
        points = np.asarray(mesh.vertices)
        new_points = points.copy()
        match segmentation_method:
            case SegmentationMethod.COLLAPSE_TO_PLANE:
                np.minimum(new_points[:, 2], 0, out=new_points[:, 2])
            case SegmentationMethod.COLLAPSE_TO_POINT:
                new_points[new_points[:, 2] > 0] = 0
        new_mesh = vedo.Mesh((new_points, mesh.cells))
        return new_mesh

    def segment_mesh_ventral(
        self,
        mesh: vedo.Mesh,
        segmentation_method: SegmentationMethod,
    ) -> vedo.Mesh:
        points = np.asarray(mesh.vertices)
        new_points = points.copy()
        match segmentation_method:
            case SegmentationMethod.COLLAPSE_TO_PLANE:
                np.maximum(new_points[:, 2], 0, out=new_points[:, 2])
            case SegmentationMethod.COLLAPSE_TO_POINT:
                new_points[new_points[:, 2] < 0] = 0
        new_mesh = vedo.Mesh((new_points, mesh.cells))
        return new_mesh

    def segment_mesh_left(
        self,
        mesh: vedo.Mesh,
        segmentation_method: SegmentationMethod,
    ) -> vedo.Mesh:
        points = np.asarray(mesh.vertices)
        new_points = points.copy()
        match segmentation_method:
            case SegmentationMethod.COLLAPSE_TO_PLANE:
                np.minimum(new_points[:, 0], 0, out=new_points[:, 0])
            case SegmentationMethod.COLLAPSE_TO_POINT:
                new_points[new_points[:, 0] > 0] = 0
        new_mesh = vedo.Mesh((new_points, mesh.cells))
        return new_mesh

    def segment_mesh_right(
        self,
        mesh: vedo.Mesh,
        segmentation_method: SegmentationMethod,
    ) -> vedo.Mesh:
        points = np.asarray(mesh.vertices)
        new_points = points.copy()
        match segmentation_method:
            case SegmentationMethod.COLLAPSE_TO_PLANE:
                np.maximum(new_points[:, 0], 0, out=new_points[:, 0])
            case SegmentationMethod.COLLAPSE_TO_POINT:
                new_points[new_points[:, 0] < 0] = 0
        new_mesh = vedo.Mesh((new_points, mesh.cells))
        return new_mesh

    def __init__(self, artefact: vedo.Mesh):
        # SEGMENTATION_METHOD = SegmentationMethod.COLLAPSE_TO_POINT
        SEGMENTATION_METHOD = SegmentationMethod.COLLAPSE_TO_PLANE

        self.artefact = artefact

        self.volume = artefact.volume()
        self.points = np.asarray(artefact.vertices)
        self.faces = artefact.cells

        self.dorsal = self.segment_mesh_dorsal(
            mesh=artefact,
            segmentation_method=SEGMENTATION_METHOD,
        )

        self.ventral = self.segment_mesh_ventral(
            mesh=artefact,
            segmentation_method=SEGMENTATION_METHOD,
        )

        self.left = self.segment_mesh_left(
            mesh=artefact,
            segmentation_method=SEGMENTATION_METHOD,
        )

        self.right = self.segment_mesh_right(
            mesh=artefact,
            segmentation_method=SEGMENTATION_METHOD,
        )

        self.dorsal_right = self.segment_mesh_right(
            mesh=self.dorsal,
            segmentation_method=SEGMENTATION_METHOD,
        )

        self.dorsal_left = self.segment_mesh_left(
            mesh=self.dorsal,
            segmentation_method=SEGMENTATION_METHOD,
        )

        self.ventral_right = self.segment_mesh_right(
            mesh=self.ventral,
            segmentation_method=SEGMENTATION_METHOD,
        )

        self.ventral_left = self.segment_mesh_left(
            mesh=self.ventral,
            segmentation_method=SEGMENTATION_METHOD,
        )
