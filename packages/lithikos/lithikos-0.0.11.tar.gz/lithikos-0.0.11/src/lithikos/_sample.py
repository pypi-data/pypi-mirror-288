import numpy as np

PointXyzType = np.dtype((np.float64, 3))

AngleType = np.dtype(
    [
        ("full_angle", np.float64),
        ("quadrant_angle", np.float64),
        ("start_angle", np.int16),
        ("clockwise", np.bool_),
        ("breadth_sign", np.int8),
        ("thickness_sign", np.int8),
    ]
)

PointBltType = np.dtype(
    [
        ("breadth", np.float64),
        ("length", np.float64),
        ("thickness", np.float64),
    ]
)

SampleType = np.dtype(
    [
        ("angle", AngleType),
        ("point", PointBltType),
    ]
)
