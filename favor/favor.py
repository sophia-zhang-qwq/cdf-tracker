import json
import time
import requests
import pandas as pd
import sys
from pathlib import Path
import math
import random

# put file root directory into the Python search path,
# so that we can import modules from the root directory
sys.path.append(str(Path(__file__).resolve().parent.parent))
from common.headers import HEADERS, COOKIES, get_headers

#URL = "https://www.cdf-beauty.com/api/prod/sqactivityproductsearch"
URL = "https://www.cdf-beauty.com/api/social/sqgetcollectlist"
# -------------------------
# 填自己的 Header
# -------------------------
#referer = "https://www.cdf-beauty.com/myorderlist?selectedTabState=0&source=usercenter"
referer = "https://www.cdf-beauty.com/mycollection"
headers = get_headers(referer)

all_products = []

# Session不会重复打开界面,防止被踢
session = requests.Session()
session.headers.update(headers)
session.cookies.update(COOKIES)
favor_token = "2C5FBFA3CAB5CF65ED75D7A68373927085C413F2D1FC4AE9A2C9336FAC35E9F0890BA0A7D317F27B9A3D97F277FF4319DAEA26752A1D56B6"
favor_ymt = "format=json&appid=71&accesstoken=2C5FBFA3CAB5CF657BD268641840AF206586FAED73C79637DEAF025B52B56367279D2E7C27A2A48462D1FA6A593C96CDDB370432B9514C68&userid=626699686&os=iOS&client=iOS&requestid=a34b7689-8ae0-c586-b622-fb87284019ec&idfa=e38dacf2-22ce-79ce-b7c1-910aca56b78f&imei=e38dacf2-22ce-79ce-b7c1-910aca56b78f&mchId=604163145&language=zh_TW"
session.cookies.update({"_token": favor_token})
session.headers["ymt-pars"] = favor_ymt

page = 1
all_products = []

payload = {
    "pageIndex": 1
}

r = session.post(URL, json=payload)
data = r.json()

# -------------------------
# iterate through pages to fetch member-exclusive products
# -------------------------
page = 1
while True:
#for page in range(1, total_pages + 1):
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
    orders = data.get("productList", [])

    if len(orders) == 0:
        break

    all_products.extend(orders)
    page += 1
    # 搞个随机 让傻逼对面认为我们是人类,不要被封
    # time.sleep(0.5)
    time.sleep(random.uniform(0,1))

print("=" * 60)
print(f"Summary: Page {page} | Products: {len(all_products)}")

rows = []

for p in all_products:

    price = p.get("price")
    #original_price = p.get("originalPriceCopy")
    original_price = p.get("originalPrice")
    # check if yes/no discount
    if not p.get("activityDiscount"):
        original_price = price        

    rows.append({
        "productId": p.get("id"),
        "brand_id": p.get("brandId"),
        "name": p.get("name"),

        "price": price,
        "original_price": original_price,
        "vipPrice": p.get("vipPrice"),
    
        "discount": round(price*10.0/original_price,1) if original_price else None,
        "activity_stock": p.get("stockStatus"),

        "discountInfo": p.get("discountInfo"),
        "promotionInfo": p.get("promotionInfo"),})

df = pd.DataFrame(rows)

df.to_csv("favor.csv",index=False,encoding="utf-8-sig")
print("=" * 60)
print("Done.")