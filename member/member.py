import json
import time
import requests
import pandas as pd
import sys
from pathlib import Path
import math

# put file root directory into the Python search path, so that we can import modules from the root directory
sys.path.append(str(Path(__file__).resolve().parent.parent))
from common.headers import HEADERS, COOKIES, get_headers

#URL = "https://www.cdf-beauty.com/api/ordercenter/sqorderlist"
URL = "https://www.cdf-beauty.com/api/prod/sqactivityproductsearch"
# -------------------------
# 填自己的 Header
# -------------------------
referer = "https://www.cdf-beauty.com/myorderlist?selectedTabState=0&source=usercenter"
headers = get_headers(referer)

all_products = []


# session不会重复打开界面,防止被踢
session = requests.Session()
session.headers.update(headers)
session.cookies.update(COOKIES)

page = 1
all_products = []

payload = {
    "pageIndex": 1,
    "activityType": 23,
    "status": "1",
    "refreshProduct": True,
    "activityId": "500022208",
}

r = session.post(URL, json=payload)
data = r.json()
total_products = data["count"]
print(f"Total products: {total_products}")
page_size = len(data["list"])
print(page_size)
total_pages = math.ceil(total_products / page_size)
print(f"Total pages: {total_pages}")

# -------------------------
# Save brand/category mapping
# -------------------------
brand_map = data["filterList"]["brandList"]
category_map = data["filterList"]["categoryList"]

with open("brand_map.json", "w", encoding="utf-8") as f:
    json.dump(brand_map,f,ensure_ascii=False,indent=2)

with open("category_map.json", "w", encoding="utf-8") as f:
    json.dump(category_map,f,ensure_ascii=False,indent=2)

# -------------------------
# iterate through pages to fetch member-exclusive products
# -------------------------
#while True:
for page in range(1, total_pages + 1):
    payload["pageIndex"] = page

    # sqactivityproductsearch API does not allow GET requests, 
    # so we use POST instead
    #r = session.get(URL,json=payload,timeout=30)
    r = session.post(URL,json=payload,timeout=30)

    r.raise_for_status()

    data = r.json()

    # -------------------------
    # 这里可能叫 data / result / orders / list
    # 根据实际 response 调一下即可
    # -------------------------
    orders = data.get("list", [])

    if len(orders) == 0:
        break

    all_products.extend(orders)

    if page % 10 == 0 or page == total_pages:
        print(f"Page {page}/{total_pages} | " f"Products: {len(all_products)}")

    page += 1

    time.sleep(0.5)

print("=" * 60)
print(f"Page 1/{total_pages} | Products: {len(all_products)}")

# 保存完整 JSON
with open("member.json","w",encoding="utf-8") as f:
    json.dump(all_products,f,ensure_ascii=False,indent=2)

rows = []

for p in all_products:

    price = p.get("price")
    original_price = p.get("originalPriceCopy")
    if price!=0 and original_price!=0:
        discount = round(price/original_price * 10, 1)
    else:
        discount = None
                            
    rows.append({

        "product_id": p.get("id"),

        "activity_product_id": p.get("activityProductId"),

        "brand_id": p.get("brandId"),

        "brand": p.get("brandLogoUrl"),

        "name": p.get("name"),

        "category": p.get("categoryId"),

        "subcategory": p.get("thirdCategoryId"),

        "price": price,

        "original_price": original_price,

        "discount": discount,

        "stock": p.get("stock"),

        "activity_stock": p.get("activityStock"),

        "sell_num": p.get("sellNum"),

        "activity_id": p.get("activityId"),

        "activity_type": p.get("activityType"),

        "catalog_id": p.get("catalogId"),

        "sku": p.get("minCatalogPriceVo", {}).get("sku"),

    })

df = pd.DataFrame(rows)

df.to_csv(
    "member.csv",
    index=False,
    encoding="utf-8-sig",
)

print(df.head())

print("=" * 60)
print("Done.")