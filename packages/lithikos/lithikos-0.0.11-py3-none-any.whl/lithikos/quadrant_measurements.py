"""
Measurements from Quadrants of original orientated mesh
"""

import dataclasses

from . import Scale
from . import ArtefactSegments


@dataclasses.dataclass
class QuadrantMeasurements:
    """Derive quadrant volume measurements from oriented artefact"""

    artefact_segments: (
        ArtefactSegments  # Attribute storing information about artefact segments
    )

    def __post_init__(self):
        """
        Post-initialization method to calculate additional attributes after the
        object is created.
        """

        # Calculating the original artefact model volume and storing it in a
        # variable.
        self.original_artefact_volume: float = self.artefact_segments.artefact.volume()

        # REFINEMENT: Defining variables for minimum and maximum breadth,
        # length, and thickness values.

        self.breadth_min: float  # Minimum breadth value
        self.breadth_max: float  # Maximum breadth value
        self.length_min: float  # Minimum length value
        self.length_max: float  # Maximum length value
        self.thickness_min: float  # Minimum thickness value
        self.thickness_max: float  # Maximum thickness value

        # Extracting minimum and maximum values for breadth, length, and
        # thickness from artefact bounds.
        (
            self.breadth_min,
            self.breadth_max,
            self.length_min,
            self.length_max,
            self.thickness_min,
            self.thickness_max,
        ) = self.artefact_segments.artefact.bounds()

    def to_volume_data_dict(self):
        return {
            "Artefact_Volume": self.artefact_segments.volume * Scale.VOLUME,
            "Length_Max": self.length_max * Scale.LENGTH,
            "Length_Min": self.length_min * Scale.LENGTH,
            "Thickness_Max": self.thickness_max * Scale.LENGTH,
            "Thickness_Min": self.thickness_min * Scale.LENGTH,
            "Breadth_Max": self.breadth_max * Scale.LENGTH,
            "Breadth_Min": self.breadth_min * Scale.LENGTH,
            "Volume_QI": self.artefact_segments.ventral_right.volume() * Scale.VOLUME,
            "Volume_QII": self.artefact_segments.dorsal_right.volume() * Scale.VOLUME,
            "Volume_QIII": self.artefact_segments.dorsal_left.volume() * Scale.VOLUME,
            "Volume_QIV": self.artefact_segments.ventral_left.volume() * Scale.VOLUME,
        }
