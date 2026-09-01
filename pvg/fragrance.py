import requests
import pandas as pd
import urllib3

from header import headers

url = "https://api.cdfsunrise.com/restapi/search/list"

# 把傻逼Warning给屏蔽了
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        "topItemIds": "4871646",
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

r = requests.post(
    url=url,
    headers=headers,
    json=json_data,
    timeout=20,
    verify=False,
)

print(r.status_code)

data = r.json()

print(data["responseHead"])
print("total:", data.get("totalCount"))

products = data.get("goodsList", [])

print("products:", len(products))

for p in products:
    print(
        p.get("chineseBrandName"),
        p.get("goodsName"),
        p.get("goodsSubName"),
        p.get("price"),
        p.get("buyPrice"),
        p.get("stock"),
    )
