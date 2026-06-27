import requests
import pandas as pd
import json

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
    'Referer': 'https://www.cdf-beauty.com/search?item=%7B%22firstCategoryId%22%3A3008%2C%22title%22%3A%22%E9%A6%99%E6%B0%B4%22%7D&topicId=1119010',
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
    'firstCategoryList': [
        3008,
    ],
    'partId': '1119010',
    'soldOutShowType': '3',
}

# use session for 1 request for all pages without closing
session = requests.Session()

all_products = []
page = 1
fetched = 0

while True:

    json_data["pageIndex"] = page

    response = session.post(
        'https://www.cdf-beauty.com/api/nodesearch/sqsearch',
        cookies=cookies,
        headers=headers,
        json=json_data
    )

    data = response.json()

    products = data.get("list", [])

    fetched += len(products)
    print(
        f"page {page}: "
        f"{len(products)} products "
        f"({fetched}/{data['count']} total)"
    )

    # 滑到底部 没有商品了
    if len(products) == 0:
        break

    all_products.extend(products)
    page += 1

print(
    f"商品数: {len(all_products)}/{data['count']} "
    f"(缺货 {data['count'] - len(all_products)} 个)"
)

rows = []
for p in all_products:

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

df.to_csv(
    "clearance_perfume.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved: clearance_perfume.csv")


"""
print("\n========== ALL KEYS ==========\n")

all_keys = set()

for p in all_products:
    all_keys.update(p.keys())

for k in sorted(all_keys):
    print(k)

print("\n========== FIRST PRODUCT ==========\n")

print(
    json.dumps(
        all_products[0],
        indent=2,
        ensure_ascii=False
    )
)
"""


"""
{
  "price": [
    290,
    290
  ],
  "flashDiscountType": 1,
  "discount": [
    3,
    3
  ],
  "couponUseType": 1,
  "promotionUseType": 0,
  "useType": [
    3
  ],
  "remind": 0,
  "endTime": 0,
  "shipDays": 0,
  "design": {
    "btnColor": "",
    "header": "https://staticontent.shop2cn.cn/shop2cn/mp/images/item/item_purchasein_bg.png",
    "labelColor": null,
    "titlePicUrl": "https://staticontent.shop2cn.cn/shop2cn/mp/images/item/purchasein_icon.png",
    "priceLabel": "清倉價"
  },
  "notice": null,
  "canOriginalPriceBuy": false,
  "conditionType": 3,
  "showInbuyWatermark": false,
  "lotteryState": 0,
  "newProductStateEnum": 0,
  "newProductReservation": false,
  "canBuyNewProduct": false,
  "buyingTime": "2026.05.29 00:00",
  "buyingEndTime": "2026.06.30 23:59",
  "endPreviewTime": "2026.05.29 00:00",
  "newProductReservationNum": 0,
  "reservationSuccessPrompt": null,
  "hiddenPrice": null,
  "specialHandling": false,
  "description": [
    "活動價 HK$290，特惠清倉",
    "距結束21 天 11 小時"
  ],
  "state": 1,
  "activityUrl": "",
  "joinDesc": null,
  "introUrl": null,
  "remainTime": 1855552221,
  "remainTimeDesc": "",
  "remainTimeTitle": "",
  "specialRemainTimeTitle": "",
  "great": true,
  "earnestDesc": null,
  "finalPayDesc": null,
  "earnestCountDesc": null,
  "type": 22,
  "countDown": false,
  "activityId": 500021865,
  "stockType": null,
  "activityName": "特惠清倉",
  "isSpecial": true
}
"""
