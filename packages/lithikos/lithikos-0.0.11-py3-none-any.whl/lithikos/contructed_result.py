import dataclasses

import vedo


@dataclasses.dataclass
class ConstructedResult:
    points: vedo.Points
    mesh: vedo.Mesh
