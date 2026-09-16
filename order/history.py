import json
import time
import requests
import pandas as pd
import sys
from pathlib import Path
import random

# put file root directory into the Python search path, 
# so that we can import modules from the root directory
sys.path.append(str(Path(__file__).resolve().parent.parent))
from common.headers import HEADERS, COOKIES, get_headers

URL = "https://www.cdf-beauty.com/api/ordercenter/sqorderlist"
# -------------------------
# 填自己的 Header
# -------------------------
referer = "https://www.cdf-beauty.com/myorderlist?selectedTabState=0&source=usercenter"
headers = get_headers(referer)
# 用浏览器中最新请求的完整 ymt-pars 覆盖公共配置
headers.update({
    "ymt-pars": "format=json&appid=71&accesstoken=2C5FBFA3CAB5CF657BD268641840AF206586FAED73C79637DEAF025B52B56367279D2E7C27A2A48462D1FA6A593C96CDDB370432B9514C68&userid=626699686&os=iOS&client=iOS&requestid=26b0e420-3b89-b571-3089-985b6dec5034&idfa=e38dacf2-22ce-79ce-b7c1-910aca56b78f&imei=e38dacf2-22ce-79ce-b7c1-910aca56b78f&mchId=604163145&language=zh_TW",
})

all_orders = []

last_order_id = 0

# session不会重复打开界面,防止被踢
session = requests.Session()
session.headers.update(headers)
session.cookies.update(COOKIES)

while True:
    params = {
        "pagesize": 10,
        "orderstate": 0,
        "lastorderid": last_order_id,
        "queryCompleteRefundStatus": "true",
        "isWechat": "false",
        "timestamp": int(time.time() * 1000),
    }

    r = session.get(URL,params=params,timeout=30)

    r.raise_for_status()

    data = r.json()

    # -------------------------
    # 这里可能叫 data / result / orders
    # 根据实际 response 调一下即可
    # -------------------------
    orders = data.get("orders", [])

    if len(orders) == 0:
        break

    print(f"Fetched {len(orders)} orders")

    all_orders.extend(orders)

    last_order_id = orders[-1]["id"]

    # 搞个随机 让傻逼对面认为我们是人类,不要被封
    #time.sleep(0.5)
    time.sleep(random.uniform(0,1))

print("=" * 60)
print(f"Total Orders: {len(all_orders)}")

# 保存完整 JSON
with open(
    "orders.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_orders,
        f,
        ensure_ascii=False,
        indent=2,
    )

rows = []

for order in all_orders:

    order_id = order.get("id")
    order_time = order.get("payTime")
    order_status = order.get("stateText")

    for seller in order.get("sellerOrderList", []):
        for sub in seller.get("subOrderList", []):
            for p in sub.get("prodList", []):

                price = p.get("price")
                original_price = p.get("originalPrice")
                if price!=0 and original_price!=0:
                    discount = round(price/original_price * 10, 1)
                else:
                    discount = None
                            
                rows.append({
                    "order_id": order_id,
                    "create_time": order_time,

                    "product_id": p.get("id"),
                    "sku_id": p.get("skuId"),

                    "brand_id": p.get("brandId"),
                    "skuInfo": p.get("skuInfo"),
                    "name": p.get("desc"),

                    "price": p.get("price"),
                    "original_price": p.get("originalPrice"),
                    "discount": discount,

                    "quantity": p.get("purchaseNum"),

                    "activity_id": p.get("activityId"),
                    "activity_type": p.get("activityType"),
                    "activity_name": p.get("activityName"),
                    "activityLabel": p.get("activityLabel"),

                    "category": p.get("masterCategoryId"),
                })

df = pd.DataFrame(rows)

df.to_csv("orders.csv",index=False,encoding="utf-8-sig")
print(df.head())
print("=" * 60)
print("Done.")