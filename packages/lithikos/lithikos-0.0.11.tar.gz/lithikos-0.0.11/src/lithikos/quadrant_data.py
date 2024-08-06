from enum import Enum
import dataclasses


class AngularDirection(Enum):  # viewed from artefact base
    clockwise: int = 1
    anticlockwise: int = -1


@dataclasses.dataclass
class FaceAttributes:
    face_centre_angle: float


class QuadrantFace(Enum):
    ventral: FaceAttributes = FaceAttributes(90)
    dorsal: FaceAttributes = FaceAttributes(270)


class Sign(Enum):
    positive: int = 1
    negative: int = -1


@dataclasses.dataclass
class QuadrantAttributes:
    start_angle: float
    end_angle: float
    breadth_sign: Sign
    thickness_sign: Sign
    quadrant_face: QuadrantFace
    angular_direction: AngularDirection


class Quadrant(Enum):
    Q1 = QuadrantAttributes(
        start_angle=0,
        end_angle=QuadrantFace.ventral.value.face_centre_angle,
        breadth_sign=Sign.positive,
        thickness_sign=Sign.positive,
        quadrant_face=QuadrantFace.ventral,
        angular_direction=AngularDirection.clockwise,
    )
    Q2 = QuadrantAttributes(
        start_angle=180,
        end_angle=QuadrantFace.dorsal.value.face_centre_angle,
        breadth_sign=Sign.positive,
        thickness_sign=Sign.negative,
        quadrant_face=QuadrantFace.dorsal,
        angular_direction=AngularDirection.anticlockwise,
    )
    Q3 = QuadrantAttributes(
        start_angle=180,
        end_angle=QuadrantFace.dorsal.value.face_centre_angle,
        breadth_sign=Sign.negative,
        thickness_sign=Sign.negative,
        quadrant_face=QuadrantFace.dorsal,
        angular_direction=AngularDirection.clockwise,
    )
    Q4 = QuadrantAttributes(
        start_angle=360,
        end_angle=QuadrantFace.ventral.value.face_centre_angle,
        breadth_sign=Sign.negative,
        thickness_sign=Sign.positive,
        quadrant_face=QuadrantFace.ventral,
        angular_direction=AngularDirection.anticlockwise,
    )
