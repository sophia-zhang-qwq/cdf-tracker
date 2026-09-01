import requests
import pandas as pd
import urllib3

from common import headers

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

"""
for p in products:
    print(
        p.get("chineseBrandName"),
        p.get("goodsName"),
        p.get("goodsSubName"),
        p.get("price"),
        p.get("buyPrice"),
        p.get("stock"),
    )
"""

def products_to_df(products):
    rows = []
    for p in products:

        rows.append({
            # sku
            "goodsID": p.get("goodsID"),
            "goodsCode": p.get("goodsCode"),
            "leFoxID": p.get("leFoxID"),
            
            "chineseBrandName": p.get("chineseBrandName"),
            "englishBrandName": p.get("englishBrandName"),
            "goodsName": p.get("goodsName"),
            "goodsSubName": p.get("goodsSubName"),
            "backstageCategory": p.get("backstageCategory"),

            "price": p.get("price"),
            "originalPrice": p.get("originalPrice"),
            "costPrice": p.get("costPrice"),
            "buyPrice": p.get("buyPrice"),
            "lowestPrice": p.get("lowestPrice"),
            "lowestPriceText": p.get("lowestPriceText"),

            "stock": p.get("stock"),

            "onSale": p.get("onSale"),
            "purchaseTypeId": p.get("purchaseTypeId"),
            "purchaseModeType": p.get("purchaseModeType"),
            # promotion end time
            "timestamp": p.get("timestamp"),
        })

    df = pd.DataFrame(rows)
    return df

# use session for 1 request for all pages without closing
session = requests.Session()
all_products = []
page = 1
fetched = 0

while True:
    json_data["pageNumber"] = page

    #response = requests.post(
    response = session.post(
        url,
        headers=headers,
        json=json_data,
        timeout=20,
        # 我靠这个傻逼Bug 加了这行就成功了
        verify=False,
    )
    data = response.json()
    products = data.get("goodsList", [])
    # 滑到底部 没有商品了
    if not products:
        break
    fetched += len(products)
    print(
        f"page {page}: "
        f"{len(products)} products "
        f"({fetched}/{data['totalCount']} total)"
    )


    all_products.extend(products)
    page += 1
print(
    f"商品数: {len(all_products)}/{data['totalCount']} "
    f"(缺货 {data['totalCount'] - len(all_products)} 个)"
)

# save all pvg fragrance clearance products to csv
search_df = products_to_df(all_products)

search_df.to_csv("fragrance.csv", index=False, encoding="utf-8-sig")
print("Saved: fragrance.csv\n")