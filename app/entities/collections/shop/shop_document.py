import dataclasses

from app.entities.collections.base_document import BaseDocument
from app.entities.collections.category.category_codes import CategoryCode
from app.entities.collections.geo_json import GeoJsonPolygon


@dataclasses.dataclass
class ShopDeliveryAreaDoc:
    poly: GeoJsonPolygon


@dataclasses.dataclass
class ShopDocument(BaseDocument):
    name: str
    category_codes: list[CategoryCode]
    delivery_areas: list[ShopDeliveryAreaDoc]
