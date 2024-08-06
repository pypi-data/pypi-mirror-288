import vedo

import dataclasses


@dataclasses.dataclass
class SliceData:
    origin: tuple | None = None
    lines: list = dataclasses.field(default_factory=list)
    this_slice = vedo.Mesh | None
