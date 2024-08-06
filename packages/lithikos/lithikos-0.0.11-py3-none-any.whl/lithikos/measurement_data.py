import dataclasses

from . import QuadrantAttributes
from . import Quadrant


@dataclasses.dataclass
class MeasurementAttributes:
    full_angle: float
    measurement_angle: float
    quadrant_angle: float
    quadrant_data: QuadrantAttributes


class MeasurementData:
    def __init__(
        self,
        quadrant: Quadrant,
        segment_count: int,
    ):
        self.quadrant = quadrant
        self.quadrant_attributes = quadrant.value

        self.segment_count = segment_count
        self.segment_angle = 90 / (segment_count + 1)
        self.angles = [0.0]
        self.angles += list(
            [angle * self.segment_angle for angle in range(1, self.segment_count + 1)]
        )
        self.angles.append(90)
        self.angle_iter = iter(self.angles)

    def __iter__(self):
        self.angle_iter = iter(self.angles)
        return self

    def __next__(self) -> MeasurementAttributes:
        angle = next(self.angle_iter)

        match angle:
            case 0:
                full_angle = self.quadrant_attributes.start_angle
                # measurement angles 0 and 360 should yield the same result,
                # so we only need to measure once.
                if full_angle == 360:
                    measurement_angle = 0
                else:
                    measurement_angle = full_angle

                return_val = MeasurementAttributes(
                    full_angle=full_angle,
                    measurement_angle=measurement_angle,
                    quadrant_angle=angle,
                    quadrant_data=self.quadrant_attributes,
                )
            case 90:
                full_angle = self.quadrant_attributes.end_angle
                measurement_angle = full_angle
                return_val = MeasurementAttributes(
                    full_angle=full_angle,
                    measurement_angle=measurement_angle,
                    quadrant_angle=90,
                    quadrant_data=self.quadrant_attributes,
                )

            case _:
                full_angle = (
                    self.quadrant_attributes.start_angle
                    + angle * self.quadrant_attributes.angular_direction.value
                )
                measurement_angle = full_angle

                return_val = MeasurementAttributes(
                    full_angle=full_angle,
                    measurement_angle=measurement_angle,
                    quadrant_angle=angle,
                    quadrant_data=self.quadrant_attributes,
                )
        return return_val
