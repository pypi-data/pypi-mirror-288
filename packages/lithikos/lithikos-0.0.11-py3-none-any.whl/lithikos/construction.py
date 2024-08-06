"""Code to create meshes from points"""

import numpy as np
from tqdm import tqdm
import vedo

from . import AngularDirection
from . import Quadrant
from . import ConstructedResult
from . import ConstructionData
from ._sample import PointXyzType


def get_point_index(
    points: np.ndarray,
    point: np.ndarray,
) -> int:
    """Finds matching index for entries in points which match the valus in point"""
    match = (points == point).all(axis=1)
    return np.where(match)[0]


def make_segment_faces_np(
    points: np.ndarray,
    slice1: np.ndarray,
    slice2: np.ndarray,
) -> np.ndarray:
    """Builds the faces between the two slices to create a complete ring"""

    faces = []

    quadrant_angles = np.unique(slice1.angle.quadrant_angle)
    quadrant_angles.sort()

    for quadrant_attributes in Quadrant:
        angular_direction = quadrant_attributes.value.angular_direction
        direction = angular_direction == AngularDirection.clockwise
        start_angle = quadrant_attributes.value.start_angle

        quadrant_angle = quadrant_angles[0]

        slice1_point = slice1[
            (slice1.angle.start_angle == start_angle)
            & (slice1.angle.clockwise == direction)
            & (slice1.angle.quadrant_angle == quadrant_angle)
        ]

        actual_slice1_point = slice1_point.point.view(PointXyzType)

        slice1_previous_point_index = get_point_index(
            points=points,
            point=actual_slice1_point,
        )

        slice2_point = slice2[
            (slice2.angle.start_angle == start_angle)
            & (slice2.angle.clockwise == direction)
            & (slice2.angle.quadrant_angle == quadrant_angle)
        ]

        actual_slice2_point = slice2_point.point.view(PointXyzType)

        slice2_previous_point_index = get_point_index(
            points=points,
            point=actual_slice2_point,
        )

        for quadrant_angle in quadrant_angles[1:]:
            slice1_point = slice1[
                (slice1.angle.start_angle == start_angle)
                & (slice1.angle.clockwise == direction)
                & (slice1.angle.quadrant_angle == quadrant_angle)
            ]

            actual_slice1_point = slice1_point.point.view(PointXyzType)

            slice1_point_index = get_point_index(
                points=points,
                point=actual_slice1_point,
            )

            slice2_point = slice2[
                (slice2.angle.start_angle == start_angle)
                & (slice2.angle.clockwise == direction)
                & (slice2.angle.quadrant_angle == quadrant_angle)
            ]

            actual_slice2_point = slice2_point.point.view(PointXyzType)

            slice2_point_index = get_point_index(
                points=points,
                point=actual_slice2_point,
            )

            face1 = np.concatenate(
                (
                    slice1_previous_point_index,
                    slice1_point_index,
                    slice2_previous_point_index,
                )
            )
            faces.append(face1)

            face2 = np.concatenate(
                (
                    slice2_previous_point_index,
                    slice1_point_index,
                    slice2_point_index,
                )
            )
            faces.append(face2)

            slice1_previous_point_index = slice1_point_index
            slice2_previous_point_index = slice2_point_index

    return faces


def make_end_faces_np(
    points: np.ndarray,
    end_point: np.ndarray,
    artefact_slice: np.ndarray,
) -> np.ndarray:
    """Builds faces from the last slice to the end point"""

    faces = []

    end_index = get_point_index(points=points, point=end_point)

    quadrant_angles = np.unique(artefact_slice.angle.quadrant_angle)
    quadrant_angles.sort()

    for quadrant_attributes in Quadrant:
        angular_direction = quadrant_attributes.value.angular_direction
        direction = angular_direction == AngularDirection.clockwise
        start_angle = quadrant_attributes.value.start_angle

        quadrant_angle = quadrant_angles[0]

        point = artefact_slice[
            (artefact_slice.angle.start_angle == start_angle)
            & (artefact_slice.angle.clockwise == direction)
            & (artefact_slice.angle.quadrant_angle == quadrant_angle)
        ]

        actual_point = point.point.view(PointXyzType)

        previous_point_index = get_point_index(
            points=points,
            point=actual_point,
        )

        for quadrant_angle in quadrant_angles[1:]:
            point = artefact_slice[
                (artefact_slice.angle.start_angle == start_angle)
                & (artefact_slice.angle.clockwise == direction)
                & (artefact_slice.angle.quadrant_angle == quadrant_angle)
            ]

            actual_point = point.point.view(PointXyzType)

            point_index = get_point_index(
                points=points,
                point=actual_point,
            )
            face = np.concatenate((end_index, point_index, previous_point_index))
            faces.append(face)
            previous_point_index = point_index

    return faces


def create_mesh_from_point_data(
    construction_data: ConstructionData,
) -> ConstructedResult:
    """Creates a mesh from the point data provided"""

    analysis_method = construction_data.analysis_method
    sample_data = construction_data.sample_data

    tip_mean, butt_mean = construction_data.end_points

    sample_points = sample_data.point.view(PointXyzType)

    sample_lengths = np.unique(sample_data.point.length)

    sample_lengths[::-1].sort()

    # add a point for the tip to points
    sample_points = np.concatenate((sample_points, np.asarray((tip_mean,))))

    # add a point for the butt to points
    sample_points = np.concatenate((sample_points, np.asarray((butt_mean,))))

    # there are duplicated points at the edges of the quadrants
    sample_points = np.unique(sample_points, axis=0)  # remove duplicate points

    # make the faces from the tip to the first slice
    sample_artefact_slice = sample_data[sample_data.point.length == sample_lengths[0]]

    sample_tip_faces = make_end_faces_np(
        points=sample_points,
        end_point=tip_mean,
        artefact_slice=sample_artefact_slice,
    )

    sample_faces = sample_tip_faces

    # make faces for all the slices
    previous_sample_slice = sample_data[sample_data.point.length == sample_lengths[0]]

    desc = f"     Synthesising {analysis_method.text}"
    for i in tqdm(range(1, len(sample_lengths)), desc=desc):
        sample_artefact_slice = (
            sample_points[sample_points[:, 1] == sample_lengths[i]],
        )
        sample_artefact_slice = sample_data[
            sample_data.point.length == sample_lengths[i]
        ]

        # make faces between two slices

        sample_segment_faces = make_segment_faces_np(
            points=sample_points,
            slice1=previous_sample_slice,
            slice2=sample_artefact_slice,
        )

        previous_sample_slice = sample_artefact_slice

        sample_faces = np.concatenate((sample_faces, sample_segment_faces))

    # make faces from last slice to butt

    sample_artefact_slice = sample_data[sample_data.point.length == sample_lengths[-1]]

    sample_butt_faces = make_end_faces_np(
        points=sample_points,
        end_point=butt_mean,
        artefact_slice=sample_artefact_slice,
    )

    sample_faces = np.concatenate((sample_faces, sample_butt_faces))

    sample_faces = np.unique(sample_faces, axis=0)  # remove duplicate faces

    sample_points_vedo = vedo.Points(sample_points)
    sample_mesh = vedo.Mesh([sample_points, sample_faces]).compute_normals()

    if False:
        # The following can be used to create a mesh when pasted into a python
        # script and added to a numpy ndarray print(points)
        for point in sample_points_vedo.vertics:
            print(f"[{point[0]}, {point[1]}, {point[2]}],")
        # print(sample_faces)
        for face in sample_faces:
            print(f"[{face[0]}, {face[1]}, {face[2]}],")

    if False:
        artefact_axes = vedo.Axes(sample_mesh)

        vedo.Plotter().show(
            artefact_axes,
            sample_points_vedo,
            sample_mesh.alpha(0.5),
        )

    sample_constructed_result = ConstructedResult(
        points=sample_points_vedo.clean(),
        mesh=sample_mesh.clean(),
    )

    return sample_constructed_result
