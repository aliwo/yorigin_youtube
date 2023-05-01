import dataclasses

from app.entities.collections.base_document import BaseDocument
from app.entities.collections.category.category_codes import CategoryCode


@dataclasses.dataclass(kw_only=True)
class CategoryDocument(BaseDocument):
    code: CategoryCode
    name: str
    image_url: str
    deep_link: str
    priority: int
