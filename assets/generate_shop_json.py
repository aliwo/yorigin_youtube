import json

from app.entities.collections.category.category_codes import CategoryCode

SHOP_NAMES = ["치킨집", "버거집", "피자집", "샌드위치집", "한식집", "일식집"]

for shop_name, category_code, polygon_num in zip(SHOP_NAMES, CategoryCode, range(1, 7)):
    with open(f"random_polygons/{polygon_num}.json") as f:
        polygon_list = json.load(f)

    result = []
    for i, polygon in enumerate(polygon_list):
        result.append(
            {
                "name": f"{shop_name} #{i}",
                "category_codes": [category_code.value],
                "delivery_areas": [{"poly": polygon}],
            }
        )

    with open(f"shops/{category_code.value}_shops.json", "w", encoding="utf-8") as json_file:
        json.dump(result, json_file, ensure_ascii=False)
        print(f"{category_code.value} 생성 완료")
