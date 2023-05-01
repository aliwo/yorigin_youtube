import dataclasses
from typing import Literal, Sequence


@dataclasses.dataclass(kw_only=True)
class GeoJsonPolygon:
    type: Literal["Polygon"] | Literal["MultiPolygon"] = "Polygon"
    coordinates: Sequence[Sequence[Sequence[float]]]


@dataclasses.dataclass(kw_only=True)
class GeoJsonPoint:
    type: Literal["Point"] = "Point"
    coordinates: list[float]
