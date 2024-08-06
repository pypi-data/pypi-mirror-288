"""Sample points from a 3d scanned mesh organised in quadrants"""

from tqdm import tqdm

import numpy as np
from numpy.lib.recfunctions import stack_arrays

import vedo

from ._sample import SampleType

from . import AngularDirection
from . import ArtefactInfo
from . import MeasurementData
from .measurement_data import MeasurementAttributes
from . import Quadrant
from . import SliceData
from . import SampleParameters

from . import logger


def get_artefact_y_intersect(
    artefact: vedo.Mesh,
) -> tuple[np.ndarray]:
    """Get the points where the y axis intersects the artefact"""
    (
        _,  # breadth_min,
        _,  # breadth_max,
        length_min,
        length_max,
        _,  # thickness_min,
        _,  # thickness_max,
    ) = artefact.bounds()

    artefact_length = abs(length_max - length_min)

    extention = artefact_length * 0.05

    p0 = (0, length_max + extention, 0)
    p1 = (0, length_min - extention, 0)
    axis_line = vedo.Line(p0=p0, p1=p1)

    if False:
        plt = vedo.Plotter()
        plt.show(artefact.clone().alpha(0.3), axis_line, axes=True)

    points = artefact.intersect_with_line(axis_line)
    points_sorted = points[points[:, 1].argsort()][::-1]

    # TODO: choose which method to use if multiple points are identified at the
    # y intersects

    # this will use external points
    tip_intersect = points_sorted[0]
    butt_intersect = points_sorted[-1]

    # this will use innermost points tip_intersect =
    # points_sorted[points_sorted[:,1] > 0][-1] butt_intersect =
    # points_sorted[points_sorted[:,1] < 0][0]

    return tip_intersect, butt_intersect


def get_intersection_at_angle(
    artefact: vedo.Mesh,
    angle: float,
    magnitude: float,
    origin: tuple[int],
) -> np.ndarray:
    """
    Get the points at the intersection of a line perpendicular to the y axis at
    the angle an origin given
    """

    offset_breadth, offset_length, offset_thickness = origin

    calculated_thickness = np.sin(angle * np.pi / 180) * magnitude
    calculated_breadth = np.cos(angle * np.pi / 180) * magnitude
    p0 = (offset_breadth, offset_length, offset_thickness)
    p1 = (
        offset_breadth + calculated_breadth,
        offset_length,
        offset_thickness + calculated_thickness,
    )
    line = vedo.Line(p0=p0, p1=p1)

    if False:
        plt = vedo.Plotter()
        plt.show(artefact.c("green").alpha(0.1), line.c("red"))

    points = artefact.intersect_with_line(line)

    # TODO add check for multiple or no points being available We only want one
    # point returned from the intersection
    if len(points) == 1:
        point_to_return = points[-1]
    elif len(points) > 1:
        logger.warning(
            "intersect with line at angle: %f origin: %s found %i points",
            angle,
            origin,
            len(points),
        )
        for point in points:
            logger.warning("%s", point)

        if True:  # Use the first point encountered
            point_to_return = points[0]
            logger.warning("using first point as point %s", point_to_return)
        else:  # Use the mean of all points
            point_to_return = np.asanyarray(points).mean(axis=0)
            logger.warning("using mean as point %s", point_to_return)

    else:
        logger.warning(
            "intersect with line at angle: %f origin: %s found %i points",
            angle,
            origin,
            len(points),
        )
        point_to_return = origin
        logger.warning("using slice origin as point %s", point_to_return)

        if False:
            (
                breadth_min,
                breadth_max,
                length_min,
                length_max,
                thickness_min,
                thickness_max,
            ) = artefact.bounds()

            breadth = abs(breadth_max - breadth_min)
            # length = abs(length_max - length_min)
            thickness = abs(thickness_max - thickness_min)

            slice_plane = vedo.Plane(
                pos=origin,
                normal=(0, 1, 0),
                s=(breadth, thickness),
                c="yellow",
                alpha=0.5,
            )
            axis_line = vedo.Line(p0=(0, -200, 0), p1=(0, 200, 0))
            plt = vedo.Plotter()
            plt.show(
                artefact, slice_plane, line.c("red"), axis_line.c("green"), axes=True
            )

    return line, point_to_return


def get_slice_points(
    artefact: vedo.Mesh,
    slice_location: float,
    point_count: int,
    normalise_axis: bool = False,  # see comment below regarding this method
) -> tuple[SliceData, np.ndarray]:
    """Get a list of points for all the angles of a slice"""

    slice_data = SliceData()

    slice_samples = np.empty(0, dtype=SampleType).view(np.recarray)

    (
        breadth_min,
        breadth_max,
        _,  # length_min,
        _,  # length_max,
        thickness_min,
        thickness_max,
    ) = artefact.bounds()

    breadth_limits = abs(
        breadth_max - breadth_min
    )  # make the line length much longer than it needs to be

    slice_origin = (0, slice_location, 0)

    # TODO: consider whether this makes sense This method shifts the centre of
    # each slice before processing Note: this will lose a certain amount of
    # information regarding bi-facial and bi-lateral symmetry
    if normalise_axis:
        slice_data.this_slice = artefact.clone().slice(
            origin=slice_origin, normal=(0, 1, 0)
        )
        slice_data.origin = slice_data.this_slice.center_of_mass()
    else:
        slice_data.this_slice = None
        slice_data.origin = slice_origin

    points_per_quadrant = point_count // 4
    segment_count = points_per_quadrant - 1

    plot_points = []

    entry_list: list[MeasurementAttributes] = []

    for q in Quadrant:
        for entry in MeasurementData(quadrant=q, segment_count=segment_count):
            entry_list.append(entry)

    measurement_angles: list[float] = sorted({m.measurement_angle for m in entry_list})

    for measurement_angle in measurement_angles:
        line, point = get_intersection_at_angle(
            artefact=artefact,
            angle=measurement_angle,
            magnitude=breadth_limits,
            origin=slice_data.origin,
        )
        slice_data.lines.append(line)

        # list of points to log position
        plot_point = vedo.Point(point, r=4)
        plot_points.append(plot_point)

        entry: MeasurementAttributes
        for entry in [
            entry
            for entry in entry_list
            if entry.measurement_angle == measurement_angle
        ]:
            quadrant_data = entry.quadrant_data

            # pylint: disable=too-many-function-args
            this_sample = np.void(0, dtype=SampleType).view(np.recarray)
            this_sample.angle.full_angle = entry.full_angle
            this_sample.angle.quadrant_angle = entry.quadrant_angle
            this_sample.angle.start_angle = quadrant_data.start_angle
            this_sample.angle.clockwise = (
                quadrant_data.angular_direction == AngularDirection.clockwise
            )
            this_sample.angle.breadth_sign = quadrant_data.breadth_sign.value
            this_sample.angle.thickness_sign = quadrant_data.thickness_sign.value

            this_sample.point.breadth = point[0]
            this_sample.point.length = slice_location
            this_sample.point.thickness = point[2]

            slice_samples = stack_arrays(
                (slice_samples, (this_sample,)), asrecarray=True, usemask=False
            )

            # The following code displays the artefact and with a single radial
            # line for each point sample around the current slice. The next
            # plote below displays all points per slice.

        if False:
            artefact_thickness = abs(thickness_min - thickness_max)
            plt = vedo.Plotter()
            plt.camera.SetPosition((0, 0, artefact_thickness))
            plt.camera.SetFocalPoint((0, 0, 0))
            plt.show(artefact.alpha(0.3), line, plot_point, axes=True)

    # The following code displays the Radial Points plot showing the artefact
    # with the point_count located at first slice below the tip. Closing this
    # initial plot opens the same view for each of the slices defined in the
    # slice_data variable.

    if False:  # show radial points per slice
        title = "Radial Points Measured per Slice"
        artefact_thickness = abs(thickness_min - thickness_max)
        plt = vedo.Plotter(title=title)
        plt.camera.SetPosition((0, 0, artefact_thickness))
        plt.camera.SetFocalPoint((0, -20, 0))
        plt.show(artefact.alpha(0.6), slice_data.lines, plot_points, axes=True)

    sort_order = np.argsort(slice_samples.angle.full_angle)
    slice_samples = slice_samples[sort_order]

    return slice_data, slice_samples


def get_artefact_samples(
    artefact: vedo.Mesh,
    sample_parameters: SampleParameters,
) -> ArtefactInfo:
    """Get a set of samples for the artefact working down the y axis slice by
    slice"""

    tip, analysis_end = get_artefact_y_intersect(artefact=artefact)

    artefact_info = ArtefactInfo(
        end_points=(tip, analysis_end),
    )

    tip_spacing = sample_parameters.tip_spacing.value
    butt_spacing = sample_parameters.butt_spacing.value
    slice_count = sample_parameters.slice_count.value
    point_count = sample_parameters.point_count.value

    # TODO: slicing at the actual bounds doesn't always work reduce the start by
    # one and the end by 1 to make sure

    length_max = tip[1]

    length_min = analysis_end[1]

    overall_length = abs(length_max - length_min)
    portion_to_slice = 100 - tip_spacing - butt_spacing

    # reduce the start by a percentage
    start = length_max - overall_length * tip_spacing / 100

    portion_length = overall_length * portion_to_slice / 100

    inter_slice_distance = portion_length / (slice_count - 1)

    for i in tqdm(range(slice_count), desc="     Radial Points Sampling"):
        # work along length from first slice (tip end]) to last slice (butt end)

        slice_location = start - inter_slice_distance * i

        slice_data, slice_samples = get_slice_points(
            artefact=artefact,
            slice_location=slice_location,
            point_count=point_count,
        )

        artefact_info.samples = np.concatenate(
            (artefact_info.samples, slice_samples)
        ).view(np.recarray)

        artefact_info.original_slice_data.append(slice_data)

    return artefact_info
