"""
Functions to analyse data based on the analysis method and produce a set of
symmetrised samples
"""

import copy

from tqdm import tqdm

import numpy as np

from . import ConstructionData
from . import AnalysisMethod
from . import ArtefactInfo


def analyse_artefact_samples(
    artefact_info: ArtefactInfo,
    analysis_method: AnalysisMethod,
) -> ConstructionData:
    """
    Works down the artefact samples, slice by slice and produces a set of
    symmetrised points based on the analysis method
    """

    construction_data = ConstructionData(
        analysis_method=analysis_method,
        end_points=artefact_info.end_points,
    )

    samples = artefact_info.samples

    long_samples: np.recarray = copy.deepcopy(samples).view(np.recarray)

    quadrant_angles = np.unique(long_samples.angle.quadrant_angle)
    quadrant_angles.sort()

    sample_lengths = np.unique(samples.point.length)
    sample_lengths[::-1].sort()  # sort descending
    slice_count = sample_lengths.size

    desc = f"Symmetrising Radial Slices:"
    for i in tqdm(range(slice_count), desc=desc):
        sample_length = sample_lengths[i]
        length_match = long_samples.point.length == sample_length
        for angle in quadrant_angles:
            angle_match = long_samples.angle.quadrant_angle == angle

            points = long_samples.point[angle_match & length_match]
            angles = long_samples.angle[angle_match & length_match]

            # point_magnitudes = np.sqrt(points.breadth**2 + points.thickness**2)
            point_magnitudes = np.hypot(points.breadth, points.thickness)

            match analysis_method:
                case AnalysisMethod.ENDO_SYM:
                    magnitude_to_use = point_magnitudes.min()
                case AnalysisMethod.MEAN_SYM:
                    magnitude_to_use = point_magnitudes.mean()
                case AnalysisMethod.EXO_SYM:
                    magnitude_to_use = point_magnitudes.max()

            new_breadth = magnitude_to_use * np.cos(angle * np.pi / 180)
            new_thickness = magnitude_to_use * np.sin(angle * np.pi / 180)

            long_samples.point.breadth[angle_match & length_match] = (
                new_breadth * angles.breadth_sign
            )
            long_samples.point.thickness[angle_match & length_match] = (
                new_thickness * angles.thickness_sign
            )

    construction_data.sample_data = long_samples
    return construction_data
