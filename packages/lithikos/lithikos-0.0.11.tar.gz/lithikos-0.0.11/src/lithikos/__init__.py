"""Artefact Utils library supporting analysis of 3D scanned artefacts"""

import logging

from .exceptions import ArtefactUtilsParseException

from .Scale import Scale

from ._sample import (
    # PointXyzType,
    # PointBltType,
    # AngleType,
    SampleType,
)

from .sample_parameters import SampleParameters
from .slice_data import SliceData
from .orientation_method import OrientationMethod
from .analysis_method import AnalysisMethod
from .construction_data import ConstructionData
from .contructed_result import ConstructedResult
from .artefact_info import ArtefactInfo

from .quadrant_data import AngularDirection
from .quadrant_data import QuadrantAttributes
from .quadrant_data import Quadrant

from .measurement_data import MeasurementData

from .artefact_segments import ArtefactSegments
from .quadrant_measurements import QuadrantMeasurements
from .artefact_analysis import ArtefactAnalysis


logger = logging.getLogger(__name__)

__all__ = [
    "AnalysisMethod",
    "AngularDirection",
    "ArtefactAnalysis",
    "ArtefactInfo",
    "ArtefactSegments",
    "ArtefactUtilsParseException",
    "ConstructedResult",
    "ConstructionData",
    "MeasurementData",
    "OrientationMethod",
    "Quadrant",
    "SampleParameters",
    "SampleType",
    "Scale",
    "SliceData",
    "QuadrantAttributes",
    "QuadrantMeasurements",
]
