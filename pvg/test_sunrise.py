import requests
import pandas as pd
import urllib3

# 把傻逼Warning给屏蔽了
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://api.cdfsunrise.com/restapi/search/list"

# Fill these in locally. Do NOT commit your real access token to GitHub.
headers = {
    "Accept": "application/json",
    "mobile": "13143461882",
    "channel": "cdfsunrise",
    "userid": "929E5E2CD8F91D9B-A0B923820DCC509A-228209505",
    "clientid": "5dc72d66-12b1-9500-8b0a-f32c70e71e13",
    "appversion": "1.82.6",
    "accesstoken": "WyI5MjlFNUUyQ0Q4RjkxRDlCLUEwQjkyMzgyMERDQzUwOUEtMjI4MjA5NTA1IiwiOTI5RTVFMkNEOEY5MUQ5Qi1BMEI5MjM4MjBEQ0M1MDlBLTIyODIwOTUwNSJd;1;ZXlKMGVYQmxJam9pU1U5VElpd2liVzlrWld3aU9pSnBVR0ZrSWl3aWMzbHpkR1Z0SWpvaWFWQmhaRTlUTVRndU1TSXNJbUZ3Y0Y5dVlXMWxJam9pYkdWb2RVRndjQ0lzSW5abGNuTnBiMjRpT2lJeExqZ3lMallpTENKelpYSnBZV3hPVHlJNklrUkZNekkxUmpoR0xVSTNOVGd0TlRKRU9DMDRRamd5TFVFNU9VVkdRakUxTkRreFJpSXNJbUZqWTI5MWJuUkpSQ0k2SWpreU9VVTFSVEpEUkRoR09URkVPVUl0UVRCQ09USXpPREl3UkVORE5UQTVRUzB5TWpneU1EazFNRFVpTENKemFXZHVJam9pTkRVeFpqQmhPREJoT1RJMllUazVZMlEyWkRSa1pXRXpOakpoT1dGa1pHSWlmUT09;;;W3sidHlwZSI6Ik1vYmlsZSIsIm5hbWUiOiIxMzE0MzQ2MTg4MiIsImNyZWF0ZVRpbWUiOiIyMDI2LTA4LTI3IDA5OjEzOjMwLjgyMDgwNyIsImV4cGlyZXMiOiIyMDI3LTAyLTIzIDA5OjEzOjMwLjgyMDgwNiIsInJlbWFpbmluZ1RpbWVzIjpudWxsfV0=;21595244231d250ac671084bec0585e142c1ff7943e09ebc8c990590895c3a17c78346a3c769802a53ccf8fe4da9918ed2afe1fee1d0c5169b5d6b5119c09ba3",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "usersystem": "iOS",
    "deviceid": "DE325F8F-B758-52D8-8B82-A99EFB15491F",
    "User-Agent": "lehu/1 CFNetwork/1568.200.51 Darwin/24.1.0",
    "device": "iPad Pro 12.9-inch 3rd-gen",
    "osversion": "18.1",
    "Content-Type": "application/json",
}

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