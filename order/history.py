import json
import time
import requests
import pandas as pd
import sys
from pathlib import Path

# put file root directory into the Python search path, so that we can import modules from the root directory
sys.path.append(str(Path(__file__).resolve().parent.parent))
from common.headers import HEADERS, COOKIES, get_headers

URL = "https://www.cdf-beauty.com/api/ordercenter/sqorderlist"
# -------------------------
# 填自己的 Header
# -------------------------
referer = "https://www.cdf-beauty.com/myorderlist?selectedTabState=0&source=usercenter"
headers = get_headers(referer)

all_orders = []

last_order_id = 0

while True:
    params = {
        "pagesize": 10,
        "orderstate": 0,
        "lastorderid": last_order_id,
        "queryCompleteRefundStatus": "true",
        "isWechat": "false",
        "timestamp": int(time.time() * 1000),
    }

    r = requests.get(
        URL,
        headers=headers,
        cookies=COOKIES,
        params=params,
        timeout=30,
    )

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

    time.sleep(0.5)

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
                rows.append({
                    "order_id": order_id,
                    "create_time": order_time,

                    "product_id": p.get("id"),
                    "sku_id": p.get("skuId"),

                    "brand_id": p.get("brandId"),

                    "name": p.get("desc"),

                    "price": p.get("price"),
                    "original_price": p.get("originalPrice"),

                    "quantity": p.get("purchaseNum"),

                    "activity_id": p.get("activityId"),
                    "activity_type": p.get("activityType"),
                    "activity_name": p.get("activityName"),

                    "category": p.get("masterCategoryId"),
                })

df = pd.DataFrame(rows)

df.to_csv(
    "orders.csv",
    index=False,
    encoding="utf-8-sig",
)

print(df.head())

print("=" * 60)
print("Done.")