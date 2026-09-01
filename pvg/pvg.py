from common import *

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

# use session for 1 request for all pages without closing
# save all pvg clearance products to csv
all_products = fetch_all_products(json_data)
search_df = products_to_df(all_products)

search_df.to_csv("pvg.csv", index=False, encoding="utf-8-sig")
print("Saved: pvg.csv\n")