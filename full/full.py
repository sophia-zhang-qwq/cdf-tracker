import requests
import json
import pandas as pd

cookies = {
    '_gcl_au': '1.1.1842803474.1780732880',
    '_ga': 'GA1.1.1923441225.1780732883',
    '_fbp': 'fb.1.1780732895126.148030225784856703',
    '_token': '2C5FBFA3CAB5CF6538F9F4EDDFED0A65A7796614B90DF3ADE68C1D9E84636ED199A1C8CD23870EA51FF5B97C929ABCD5E90DB2D30F62F47C',
    'cookies_agreement__604163145': '{%22necessary%22:true%2C%22feature%22:true%2C%22performance%22:true}',
    '_ga_GXZMXL96VN': 'GS2.1.s1780732883$o1$g1$t1780735426$j13$l0$h343998664',
    '_ga_GR528RWW2C': 'GS2.1.s1780732885$o1$g1$t1780735426$j13$l0$h2088253321',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://www.cdf-beauty.com',
    'Referer': 'https://www.cdf-beauty.com/search?keyword',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'accept-version': '1.0.0',
    'app-key': 'pcsqbuyer_604158472',
    'app-version': '6.6.88',
    'cookieid': 'e0cc8901-96fc-ce36-bb52-9fe9e42e83cb',
    'deviceid': '0c27fc48-8691-7934-08f2-9992e0eec712',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'ymt-pars': 'format=json&appid=77&requestid=7bdc21a8-878f-3bde-afd9-8256e1f47d5f&accesstoken=2C5FBFA3CAB5CF6538F9F4EDDFED0A65A7796614B90DF3ADE68C1D9E84636ED199A1C8CD23870EA51FF5B97C929ABCD5E90DB2D30F62F47C&userid=626699686&idfa=0c27fc48-8691-7934-08f2-9992e0eec712&imei=0c27fc48-8691-7934-08f2-9992e0eec712&mchId=604163145&language=zh_TW',
    # 'Cookie': '_gcl_au=1.1.1842803474.1780732880; _ga=GA1.1.1923441225.1780732883; _fbp=fb.1.1780732895126.148030225784856703; _token=2C5FBFA3CAB5CF6538F9F4EDDFED0A65A7796614B90DF3ADE68C1D9E84636ED199A1C8CD23870EA51FF5B97C929ABCD5E90DB2D30F62F47C; cookies_agreement__604163145={%22necessary%22:true%2C%22feature%22:true%2C%22performance%22:true}; _ga_GXZMXL96VN=GS2.1.s1780732883$o1$g1$t1780735426$j13$l0$h343998664; _ga_GR528RWW2C=GS2.1.s1780732885$o1$g1$t1780735426$j13$l0$h2088253321',
}

json_data = {
    'pageIndex': 1,
    'sortType': 1,
    'sortMode': 0,
    'refreshProduct': True,
}

session = requests.Session()
# 关闭VPN(不要读取系统代理 直接连网站)
session.trust_env = False

def get_page(page):
    json_data = {
        'pageIndex': page,
        'sortType': 1,
        'sortMode': 0,
        'refreshProduct': True,
    }
    response = session.post('https://www.cdf-beauty.com/api/nodesearch/sqsearch',
                         cookies=cookies, 
                         headers=headers, 
                         json=json_data)
    return response.json()

clean_all_products = []

# count #pages
total_pages = get_page(1)["count"]
print(f"Total pages: {total_pages}")

# 测试: 前9页
for page in range(1, total_pages+1):
#for page in range(1, 10):
    try:
        data = get_page(page)
    except Exception as e:
        print(f"FAILED PAGE = {page}")
        print(e)
        break

    for p in data["list"]:
        clean_all_products.append({
            # 电商中SKU#: unique identifier for a specific product across diff platforms
            "productId": p.get("productId"),
            "sku": p.get("catalogInfo", {}).get("sku"),

            "brandName": p.get("brandName"),
            "brandEnName": p.get("brandEnName"),
            "productName": p.get("name"),

            "price": p.get("price"),
            "originalPrice": p.get("originalPrice"),

            "discount": p.get("discount"),
            "reducePrice": p.get("reducePrice"),

            "futurePrice": p.get("futurePrice"),

            # 活动库存 vs 总库存
            "activityStock": p.get("activityStock"),
            "stock": p.get("stock"),

            # 销量, 限量
            "sellNum": p.get("sellNum"),
            "limitNum": p.get("catalogInfo", {}).get("limitNum"),

            # 出售日期
            "validStart": p.get("validStart"),
            
            # 这个到底是啥啊 不像是汇率啊 像会员积分兑换价格 50->46.6
            "exchangePrice": p.get("exchangePrice"),

            # extra
            "hiddenPrice": p.get("hiddenPrice"),
            "specialSale": p.get("specialSale"),
            "vipPrice":p.get("vipPrice"),
            "priceType":p.get("priceType")
        })
    if page % 50 == 0 or page == total_pages:
        print(
            f"Page {page}/{total_pages} | "
            f"Products: {len(clean_all_products)}"
        )

print(f"Total products: {len(clean_all_products)}")

"""
{
  "productId": "p15866247",
  "name": "SHISEIDO資生堂安熱沙金燦倍護防曬乳 90ML",
  "price": 143,
  "originalPrice": 280,
  "stock": 169,
  "brandName": "資生堂",
  "futurePrice": null
}
"""
# 本地保存在csv
df = pd.DataFrame(clean_all_products)
df.to_csv(
    "clean_products.csv",
    index=False,
    encoding="utf-8-sig"
)
print("Success, CSV saved!")

#with open("response.json", "w", encoding="utf-8") as f:
#   json.dump(data, f, ensure_ascii=False, indent=2)
