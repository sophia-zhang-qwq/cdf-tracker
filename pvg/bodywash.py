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
        # TO-DO: change according to category
        #"searchName": "家居香氛",
        "searchName": "沐浴露", 

        "pickUpMultiple": "1",
        "pickUpPoints": "[{\"name\":\"浦东T2入境\",\"pickupCode\":[\"6a1e461e4bb3fe78284074e2\"],\"isDefault\":true}]",
        "newMerchantIds": "cdfshanghai",

        # TO-DO: change according to category
        #"topItemIds": "4871646",
        "topItemIds":"4875856",

        "searchField": "免税店_6a1e461e4bb3fe78284074e2",

        # TO-DO: change according to category
        #"threeCategoryIds": "6214d97cf8e5c40001fe5f90",
        "threeCategoryIds":"63563cb1bd1d9c0001344405",

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

#print(r.status_code)
data = r.json()
#print(data["responseHead"])
print("total:", data.get("totalCount"))

products = data.get("goodsList", [])

print("products:", len(products))

# use session for 1 request for all pages without closing
# save all pvg fragrance clearance products to csv
all_products = fetch_all_products(json_data)
search_df = products_to_df(all_products)

search_df.to_csv("bodywash.csv", index=False, encoding="utf-8-sig")
print("Saved: bodywash.csv\n")