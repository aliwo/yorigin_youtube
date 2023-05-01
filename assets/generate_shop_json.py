import json

from app.entities.collections.category.category_codes import CategoryCode

SHOP_NAME = "버거집 mk2"
SHOP_CATEGORIES = [CategoryCode.BURGER]
POLYGON_NUM = 2
DUMP_LOCATION = "shops/total_80k/burger_shops.json"


with open(f"random_polygons/total_80k/{POLYGON_NUM}.json") as f:
    polygon_list = json.load(f)


result = []
for i, polygon in enumerate(polygon_list):
    result.append(
        {
            "name": f"{SHOP_NAME} #{i}",
            "category_codes": SHOP_CATEGORIES,
            "delivery_area": [
                {
                    "poly": {
                        "type": "Polygon",
                        "coordinates": polygon,
                    }
                }
            ],
        }
    )

with open(DUMP_LOCATION, "w", encoding="utf-8") as json_file:
    json.dump(result, json_file, ensure_ascii=False)
