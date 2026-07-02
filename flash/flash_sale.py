import requests
import pandas as pd
import json

# Difference btw perfume_clearance.py and flash_sale.py:
# 1. change referer 
# 2. change payload 
# 3. add flash_parts


cookies = {
    '_gcl_au': '1.1.1842803474.1780732880',
    '_ga': 'GA1.1.1923441225.1780732883',
    '_fbp': 'fb.1.1780732895126.148030225784856703',
    '_token': '2C5FBFA3CAB5CF6538F9F4EDDFED0A65A7796614B90DF3ADE68C1D9E84636ED199A1C8CD23870EA51FF5B97C929ABCD5E90DB2D30F62F47C',
    'cookies_agreement__604163145': '{%22necessary%22:true%2C%22feature%22:true%2C%22performance%22:true}',
    'h5_cookies_agreement__604163145': '{%22necessary%22:true%2C%22feature%22:true%2C%22performance%22:true}',
    'TDC_itoken': '1965225349%3A1780975031',
    '_ga_GXZMXL96VN': 'GS2.1.s1780969768$o5$g1$t1780977696$j53$l0$h873855105',
    '_ga_GR528RWW2C': 'GS2.1.s1780969768$o5$g1$t1780977696$j53$l0$h1300337362',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://www.cdf-beauty.com',

    #'Referer': 'https://www.cdf-beauty.com/search?item=%7B%22firstCategoryId%22%3A3008%2C%22title%22%3A%22%E9%A6%99%E6%B0%B4%22%7D&topicId=1119010',
    'Referer':'https://www.cdf-beauty.com/showactivity?pageId=46236',

    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1',
    'accept-version': '1.0.0',
    'app-key': 'h5sqBuyer_604158472',
    'app-version': '6.8.1',
    'cookieid': '8dde34a1-396d-0722-596e-75e441370463',
    'deviceid': '8dde34a1-396d-0722-596e-75e441370463',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"iOS"',
    'timestamp': '1780977696657',
    'ymt-pars': 'format=json&appid=71&accesstoken=2C5FBFA3CAB5CF659354E130A22CB80D225BE3A51A2A3357FBBDA092D369D05A0E72A0EFEAB24B9A947201746E359B5DAB065F5F128F8D81&userid=626699686&os=iOS&client=iOS&requestid=6d8049f6-f7d6-4578-c200-a3c3ad0fc762&idfa=e38dacf2-22ce-79ce-b7c1-910aca56b78f&imei=e38dacf2-22ce-79ce-b7c1-910aca56b78f&mchId=604163145&language=zh_TW',
}

json_data = {
    'pageIndex': 1,
    'refreshProduct': True,
    'resultRec': True,
    #'firstCategoryList': [3008,],
    #'partId': '1119010',
    'partId': '1134997',
    'soldOutShowType': '3',
}

# get home top-listed products for a given section (partId)
def get_home_products(part_id):

    url = "https://www.cdf-beauty.com/api/prod/shophomepartdata"

    params = {
        "PartId": part_id,
        "pageSize": 21,
        "tokenCode": "",
    }

    r = requests.get(
        url,
        params=params,
        headers=headers,
        cookies=cookies,
    )

    data = r.json()

    return data.get("list", [])

def products_to_df(products):
    rows = []
    for p in products:

        rows.append({

            "productId": p.get("id"),
            # sku

            #"brandName": p.get("brandName"),
            #"brandEnName": p.get("brandEnName"),
            "brandId": p.get("brandId"),
            "productName": p.get("name"),


            "price": p.get("price"),
            "originalPrice": p.get("originalPrice"),
            
            # discount
            "priceDiscount": p.get("priceDiscount"), #3.5折
            "activityDiscount": p.get("activityDiscount"), #3.5折
            "discount": p.get("discount"), # actualy price
            #"reducePrice": p.get("reducePrice"),
            #"futurePrice": p.get("futurePrice"),

            # 活动库存 vs 总库存
            "activityStock": p.get("activityStock"),
            "stock": p.get("stock"),

            # 销量, 限量
            "sellNum": p.get("sellNum"),
            #"limitNum": p.get("catalogInfo", {}).get("limitNum"),


            # promotion end time
            "timeLabel": p.get("timeLabel"),

            "activityId": p.get("activityId"),
            "activityProductId": p.get("activityProductId"),

            "categoryId": p.get("categoryId"),
            "thirdCategoryId": p.get("thirdCategoryId"),

        })

    df = pd.DataFrame(rows)
    return df

# Below added

FLASH_PARTS = {
    "featured":1025537,
    "skincare":926222,
    "makeup":922282,
    "perfume":922283,
    "body":922284,
    "food":1038583,
}

dfs=[]
"""
for name,part in FLASH_PARTS.items():
    print("="*60)
    print(name)
    print("="*60)
    home=get_home_products(part)
    df_home=products_to_df(home)
    print(f"{len(df_home)} products")
    dfs.append(df_home)

flash_df = pd.concat(dfs,ignore_index=True)
"""

session = requests.Session()

all_products = []

for name, part in FLASH_PARTS.items():

    print("=" * 60)
    print(name)
    print("=" * 60)

    page = 1

    print(part)
    print(json_data)
    print(json_data.keys())
    print(json_data.get("count"))
    print(json_data.get("msg"))

    while True:

        json_data["partId"] = part
        json_data["pageIndex"] = page

        response = session.post(
            "https://www.cdf-beauty.com/api/nodesearch/sqsearch",
            headers=headers,
            cookies=cookies,
            json=json_data,
        )

        data = response.json()

        products = data.get("list", [])

        print(
            f"page {page}: "
            f"{len(products)} products"
        )

        if len(products) == 0:
            break

        all_products.extend(products)

        page += 1

#flash_df = pd.concat(dfs,ignore_index=True)
flash_df = products_to_df(all_products)

flash_df = flash_df.drop_duplicates(subset="productId",keep="first")
flash_df.to_csv("today_flash.csv",index=False,encoding="utf-8-sig",)
# Summary
print("\n" + "=" * 60)
print("Done")
print("=" * 60)

print(f"Flash Products: {len(flash_df)} products")

print("CSV Files")
print("  today_flash.csv")
