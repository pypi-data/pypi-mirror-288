import dataclasses


@dataclasses.dataclass
class SliceCount:
    value: int

    def __post_init__(self):
        self.text: str = f"s{self.value:04d}"


@dataclasses.dataclass
class PointCount:
    value: int

    def __post_init__(self):
        self.text: str = f"p{self.value:04d}"


@dataclasses.dataclass
class TipSpacing:
    value: float

    def __post_init__(self):
        self.text: str = f"ts{self.value:0.3f}"


@dataclasses.dataclass
class ButtSpacing:
    value: float

    def __post_init__(self):
        self.text: str = f"bs{self.value:0.3f}"


@dataclasses.dataclass
class SampleParameters:
    slice_count: SliceCount
    point_count: PointCount
    tip_spacing: TipSpacing
    butt_spacing: ButtSpacing

    def __init__(
        self,
        slice_count: int,
        point_count: int,
        tip_spacing: float,
        butt_spacing: float,
    ):
        self.slice_count = SliceCount(value=slice_count)
        self.point_count = PointCount(value=point_count)
        self.tip_spacing = TipSpacing(value=tip_spacing)
        self.butt_spacing = ButtSpacing(value=butt_spacing)

    def to_csv_dict_data(self):
        return {
            "Slice_Count": self.slice_count.value,
            "Point_Count": self.point_count.value,
            "Tip_Spacing": self.tip_spacing.value,
            "Butt_Spacing": self.butt_spacing.value,
        }
