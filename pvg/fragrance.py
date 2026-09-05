import pandas as pd

from common import *

json_data = {
    "sceneId": 0,
    "pickUpPoints": [
        "6a1e461e4bb3fe78284074e2"
    ],
    "frontCateIds": [],
    "pageNumber": 1,
    "brandNewFilter": "0",
    "param": {
        "searchName": "家居香氛",
        "pickUpMultiple": "1",
        "pickUpPoints": "[{\"name\":\"浦东T2入境\",\"pickupCode\":[\"6a1e461e4bb3fe78284074e2\"],\"isDefault\":true}]",
        "newMerchantIds": "cdfshanghai",
        #"topItemIds": "4871646",
        "topItemIds": "4872910",
        "searchField": "免税店_6a1e461e4bb3fe78284074e2",
        "threeCategoryIds": "6214d97cf8e5c40001fe5f90",
        "purchaseTypes": "2"
    },
    "source": 0,
    "goodsActivityId": "",
    "frontBrandIds": [],
    "isRange": 2,
    "goodsID": "",
    "brandId": "",
    "saleType": "",
    "keys": {
        "": ""
    },
    "activityIds": [],
    "recallGoodsIds": [],
    "pageSize": 20,
    "chipId": "",
    "order": 0,
    "activityType": 0,
    "filter": {
        "categoryList": [],
        "brandShortIdlist": [],
        "brandList": [],
        "endPrice": "",
        "efficacys": [],
        "merchantList": [],
        "traceCategoryNames": [],
        "traceAdressNames": [],
        "startPrice": ""
    }
}

"""
r = requests.post(
    url=url,
    headers=headers,
    json=json_data,
    timeout=20,
    verify=False,
)

"""

import json

body = json.dumps(
    json_data,
    ensure_ascii=False,
    separators=(",", ":")
)
body = r'''{
  "frontBrandIds": [],
  "goodsID": "",
  "param": {
    "purchaseTypes": "2",
    "pickUpMultiple": "1",
    "pickUpPoints": "[{\"name\":\"浦东T2入境\",\"pickupCode\":[\"6a1e461e4bb3fe78284074e2\"],\"isDefault\":true}]",
    "newMerchantIds": "cdfshanghai",
    "searchName": "家居香氛",
    "topItemIds": "4872910",
    "searchField": "免税店_6a1e461e4bb3fe78284074e2",
    "threeCategoryIds": "6214d97cf8e5c40001fe5f90"
  },
  "chipId": "",
  "pageNumber": 1,
  "activityType": 0,
  "pageSize": 20,
  "goodsActivityId": "",
  "recallGoodsIds": [],
  "source": 0,
  "filter": {
    "startPrice": "",
    "efficacys": [],
    "merchantList": [],
    "traceCategoryNames": [],
    "traceAdressNames": [],
    "brandList": [],
    "categoryList": [],
    "endPrice": "",
    "brandShortIdlist": []
  },
  "activityIds": [],
  "keys": {
    "": ""
  },
  "isRange": 2,
  "brandNewFilter": "0",
  "order": 0,
  "brandId": "",
  "saleType": "",
  "sceneId": 0,
  "frontCateIds": [],
  "pickUpPoints": [
    "6a1e461e4bb3fe78284074e2"
  ]
}'''
r = requests.post(
    url=url,
    headers=headers,
    data=body.encode("utf-8"),
    timeout=20,
    verify=False,
)

print("CONTENT-LENGTH:", r.request.headers.get("Content-Length"))
print("BODY:", r.request.body)
print("STATUS:", r.status_code)

r.raise_for_status()

data = r.json()

print("REQUEST HEADERS:")
print(r.request.headers)

print("REQUEST BODY:")
print(r.request.body)

print("STATUS:", r.status_code)
print("CONTENT-TYPE:", r.headers.get("Content-Type"))
print("BODY:", repr(r.text[:1000]))

print("STATUS:", r.status_code)
print("CONTENT-TYPE:", r.headers.get("Content-Type"))
print("ALLOW:", r.headers.get("Allow"))
print("URL:", r.url)
print("BODY:", repr(r.text[:1000]))

data = r.json()
#print(r.status_code)
#print(data["responseHead"])
print("total:", data.get("totalCount"))

products = data.get("goodsList", [])
print("products:", len(products))

# use session for 1 request for all pages without closing
# save all pvg fragrance clearance products to csv
all_products = fetch_all_products(json_data)
search_df = products_to_df(all_products)

search_df.to_csv("fragrance.csv", index=False, encoding="utf-8-sig")
print("Saved: fragrance.csv\n")