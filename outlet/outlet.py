import json
import time
import requests
import pandas as pd
import sys
from pathlib import Path
import math
import random

# put file root directory into the Python search path, so that we can import modules from the root directory
sys.path.append(str(Path(__file__).resolve().parent.parent))
from common.headers import HEADERS, COOKIES, get_headers

#URL = "https://www.cdf-beauty.com/api/prod/sqactivityproductsearch"
URL = "https://www.cdf-beauty.com/api/nodesearch/sqsearch"
# -------------------------
# 填自己的 Header
# -------------------------
#referer = "https://www.cdf-beauty.com/myorderlist?selectedTabState=0&source=usercenter"
referer = "https://www.cdf-beauty.com/showactivity?pageId=57179&soldOutShowType=1"
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
    "refreshProduct": True,
    #"partId": 1133751,
    "partId": 1144863,
}

r = session.post(URL, json=payload)
data = r.json()
#total_products = data["count"]
total_products = data["recordCount"]
print(f"Total products: {total_products}")
#total_pages是总页数, page_size是每页的商品数量
total_pages = data["count"]
print(f"Total pages: {total_pages}")
page_size = math.ceil(total_products / total_pages)
print(f"#Products each page: {page_size}")

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
    # 搞个随机 让傻逼对面认不出来
    # time.sleep(0.5)
    time.sleep(random.uniform(0,1))

print("=" * 60)
print(f"Summary: Page {total_pages} | Products: {len(all_products)}")

# 保存完整 JSON
with open("outlet.json","w",encoding="utf-8") as f:
    json.dump(all_products,f,ensure_ascii=False,indent=2)

rows = []

for p in all_products:

    price = p.get("price")
    #original_price = p.get("originalPriceCopy")
    original_price = p.get("originalPrice")
                            
    rows.append({

        "product_id": p.get("id"),

        "activity_product_id": p.get("activityProductId"),

        "brand_id": p.get("brandId"),

        "brand": p.get("brandName"),
        "brand_en": p.get("brandEnName"),

        "name": p.get("name"),

        "category": p.get("categoryId"),

        "subcategory": p.get("thirdCategoryId"),

        "price": price,

        "original_price": original_price,

        "discount": p.get("activityDiscount"),

        "stock": p.get("stock"),

        "activity_stock": p.get("activityStock"),

        "sell_num": p.get("sellNum"),

        "activity_id": p.get("activityId"),

        "activity_type": p.get("activityType"),

        "catalog_id": p.get("catalogId"),

        #"sku": p.get("minCatalogPriceVo", {}).get("sku"),
        "sku":p.get("catalogInfo",{}).get("sku")

    })

df = pd.DataFrame(rows)

df.to_csv("outlet.csv",index=False,encoding="utf-8-sig")
print("=" * 60)
print("Done.")