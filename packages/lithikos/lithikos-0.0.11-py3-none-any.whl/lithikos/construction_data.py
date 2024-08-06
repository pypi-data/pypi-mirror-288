from ._sample import SampleType
from . import AnalysisMethod

import numpy as np

import dataclasses


@dataclasses.dataclass
class ConstructionData:
    analysis_method: AnalysisMethod
    end_points: tuple[np.ndarray, np.ndarray]

    sample_data: np.ndarray = dataclasses.field(
        default_factory=lambda: np.empty(shape=0, dtype=SampleType).view(np.recarray)
    )
