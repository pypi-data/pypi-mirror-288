from . import OrientationMethod
from . import SliceData
from . import SampleType

import numpy as np
import dataclasses


@dataclasses.dataclass
class ArtefactInfo:
    end_points: tuple[np.ndarray, np.ndarray]

    name: str | None = None
    original_slice_data: list[SliceData] = dataclasses.field(default_factory=list)
    orientation_method: OrientationMethod | None = None

    samples: np.ndarray = dataclasses.field(
        default_factory=lambda: np.empty(shape=0, dtype=SampleType).view(np.recarray)
    )
