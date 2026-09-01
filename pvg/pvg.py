import requests
import pandas as pd
import urllib3

from header import headers

# 把傻逼Warning给屏蔽了
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://api.cdfsunrise.com/restapi/search/list"

json_data = {
    "pageNumber": 2,
    "pageSize": 20,
    "order": 1,
    "buyTypes": [2],
    "sort": 2,
    "merchantIds": ["cdfshanghai"],
    "pickUpPoints": ["6a1e461e4bb3fe78284074e2"],
    "merchantId": "cdfshanghai",
    "purchaseType": [2],
    "param": {
        "newMerchantIds": "cdfshanghai",
        "purchaseTypes": "2"
    },
    "isRange": 2,
}

r = requests.post(
#r = requests.get(
    url,
    headers=headers,
    json=json_data,
    timeout=20,
    # 我靠这个傻逼Bug 加了这行就成功了
    verify=False,
)

data = r.json()
print("total:", data.get("totalCount"))
products = data.get("goodsList", [])
print("#products/page:", len(products))

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
page = 2
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


# save all skincare clearance products to csv
search_df = products_to_df(all_products)

search_df.to_csv("pvg.csv", index=False, encoding="utf-8-sig")
print("Saved: pvg.csv\n")