# common library
import urllib3
import pandas as pd
import requests

"""
# TO-DO: hide in Github, do not share or commit real access token to public
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
"""

# =========================
# Auth
# =========================
# TO-DO: hide the access tokens, do not commit directly to github
# 从 Proxyman「未登录」请求里复制
#ali_sign_whash = "05c0a66ec40519f2960e3579e572587f08df1702a97c01ad1089f1351cceb999"
ali_sign_whash = "ccf470544370f478d9e74f859cf708c7546c79aa503c9d94e78b7340d2ea43f1"
#wToken = "0004_A0601F8466370D3B832D2830833DC045A3F4F933D6C2EE413EFFDA35D4A65C3BAB69B431DBE38737AEC4DB46D9DD28398A13EA30CC070wK2g1A9DNbZERXCJ+TsgDZToIvKwBbRT6EJGJmLXVgo5V3h4T/hEevjK7CshWX/qsaYyrMEVUZxxiwrk5ZwZlNOTWUnIDaxEkkVhgBEpFRWq96Bg1jhJOYBdYwn5BE+zrVvSEmP+NtSwYcFbtScRVskgSO05MBxDbNR2FuxFLhAAWcJx8fe7A7iP46a+12eYcD6n9R33oBkyGJKSY4A4wbODQf9PDwSFZ9eQWFze57awg95P6RTiPtnRIJDVRy6rSc9/eKEyz/KdFxcSSAMlpK6PNWDQSeFc3HW8hd8UEcP+5xKIZ6GhmvHLJ20NtaWVmhiO5lIosIoQOCsYFiOhUjQM0vIl+RZdNPhbC53bi0haxzaFsr1E5xmJZ6ydowLZr+28R/+/Y+VjkhVK2yeBo4dvvRPZk4HyBWO+/tAfOW6DBxHF1PgdwZsqJJlNjwfm79mcYuzfPxwZIfzRhdABV9qXvp0i4cTfconoAsZrEuyg51X5Pk4CzyirbqpU746K/EGFX2DlJ58BvGHKca+Yrrkq1YkSjefF/WY3lNGN1EDWdtiGYCxS/nEzb+wuMmXuXvkDO4auHFerYAIVzYdgVc9VMRLfDO34QaY7LnMKx3YuNvYA5rsEiHxNGMsRPDLa12vWpuXLdx/N7j2BtO7mN+wCPJD99wVdxOIo4z9kZ4bl1Nvfu0LkAY76S4KEeZZ+GngTovuT2dKKCp/yf4Bdw==_fHw=_3cd77725ab46f7a3-h-1788318644180-a40dbf3136154d87a50e6e7cba6d6644"
wToken = "0004_A06D53231A370D3B832D2830833D8341A6A08930A4CADD413AFF4345A3072B4ED96CB331AAB58046D9D9CA43AADAA0488E139D39BA070wK2g1A9DNbZERXCJ+TsgDZToIvKwBbRT6EJGJmLXVgo5V3h4T/hEevjK7CshWX/qsaYyrMEVUZxxiwrk5ZwZlNOTWUnIDaxEkkVhgBEpFRWq96Bg1jhJOYBdYwn5BE+zrVvSEmP+NtSwYcFbtScRVskgSO05MBxDbNR2FuxFLhAAWcJx8fe7A7iP46a+12eYcD6n9R33oBkyGJKSY4A4wbODQf9PDwSFZ9eQWFze57awg95P6RTiPtnRIJDVRy6rSc9/eKEyz/KdFxcSSAMlpK6PNWDQSeFc3HW8hd8UEcP+5xKIZ6GhmvHLJ20NtaWVmhiO5lIosIoQOCsYFiOhUjQM0vIl+RZdNPhbC53bi0haxzaFsr1E5xmJZ6ydowLZr+28R/+/Y+VjkhVK2yeBo4dvvRPZk4HyBWO+/tAfOW6DBxHF1PgdwZsqJJlNjwfm79mcYuzfPxwZIfzRhdABV9qXvp0i4cTfconoAsZrEuyg51X5Pk4CzyirbqpU746K/EGFX2DlJ58BvGHKca+Yrrkq1YkSjefF/WY3lNGN1EDWdtiGYCxS/nEzb+wuMmXuXvkDO4auHFerYAIVzYdgVc9VMRLfDO34QaY7LnMKx3YuNvYA5rsEiHxNGMsRPDLa12vWpuXLdx/N7j2BtO7mN+wCPJD99wVdxOIo4z9kZ4bl1Nvfu0LkAY76S4KEeZZ+GngTovuT2dKKCp/yf4Bdw==_fHw=_3cd77725ab46f7a3-h-1788318644180-a40dbf3136154d87a50e6e7cba6d6644"
#accessToken = "WyI5MjlFNUUyQ0Q4RjkxRDlCLUEwQjkyMzgyMERDQzUwOUEtMjI4MjA5NTA1IiwiOTI5RTVFMkNEOEY5MUQ5Qi1BMEI5MjM4MjBEQ0M1MDlBLTIyODIwOTUwNSJd;0;ZXlKMGVYQmxJam9pU1U5VElpd2liVzlrWld3aU9pSnBVR0ZrSWl3aWMzbHpkR1Z0SWpvaWFWQmhaRTlUTVRndU1TSXNJbUZ3Y0Y5dVlXMWxJam9pYkdWb2RVRndjQ0lzSW5abGNuTnBiMjRpT2lJeExqZ3lMallpTENKelpYSnBZV3hPVHlJNklrUkZNekkxUmpoR0xVSTNOVGd0TlRKRU9DMDRRamd5TFVFNU9VVkdRakUxTkRreFJpSXNJbUZqWTI5MWJuUkpSQ0k2SWpreU9VVTFSVEpEUkRoR09URkVPVUl0UVRCQ09USXpPREl3UkVORE5UQTVRUzB5TWpneU1EazFNRFVpTENKemFXZHVJam9pTkRVeFpqQmhPREJoT1RJMllUazVZMlEyWkRSa1pXRXpOakpoT1dGa1pHSWlmUT09;;;W10=;0e946d66114d831fe294dd93212f746e57bc6efc80f0b6964bce794ff9d8aa886503916253e22594866376bfc425f7c4e34e4b68599a2b4064fe2d8e80d6cfdd"
accessToken = "WyI5MjlFNUUyQ0Q4RjkxRDlCLUEwQjkyMzgyMERDQzUwOUEtMjI4MjA5NTA1IiwiOTI5RTVFMkNEOEY5MUQ5Qi1BMEI5MjM4MjBEQ0M1MDlBLTIyODIwOTUwNSJd;0;ZXlKMGVYQmxJam9pU1U5VElpd2liVzlrWld3aU9pSnBVR0ZrSWl3aWMzbHpkR1Z0SWpvaWFWQmhaRTlUTVRndU1TSXNJbUZ3Y0Y5dVlXMWxJam9pYkdWb2RVRndjQ0lzSW5abGNuTnBiMjRpT2lJeExqZ3lMallpTENKelpYSnBZV3hPVHlJNklrUkZNekkxUmpoR0xVSTNOVGd0TlRKRU9DMDRRamd5TFVFNU9VVkdRakUxTkRreFJpSXNJbUZqWTI5MWJuUkpSQ0k2SWpreU9VVTFSVEpEUkRoR09URkVPVUl0UVRCQ09USXpPREl3UkVORE5UQTVRUzB5TWpneU1EazFNRFVpTENKemFXZHVJam9pTkRVeFpqQmhPREJoT1RJMllUazVZMlEyWkRSa1pXRXpOakpoT1dGa1pHSWlmUT09;;;W10=;0e946d66114d831fe294dd93212f746e57bc6efc80f0b6964bce794ff9d8aa886503916253e22594866376bfc425f7c4e34e4b68599a2b4064fe2d8e80d6cfdd"

# =========================
# Fixed device / app info
# =========================
headers = {
    "Accept": "*/*",

    "User-Agent": (
        "lehu/1.82.6 "
        "(com.cdfsunrise.cdflehu; build:1; iOS 18.1.0) "
        "Alamofire/5.10.2"
    ),

    "UserSystem": "iOS",
    "ClientID": "5dc72d66-12b1-9500-8b0a-f32c70e71e13",
    "AppVersion": "1.82.6",
    "OS": "iOS",
    "DeviceId": "DE325F8F-B758-52D8-8B82-A99EFB15491F",
    "AliTigerInit": "1",
    "AliTigerInitCode": "0",
    "ClientNetwork": "WIFI",
    "OSVersion": "18.1",
    "Device": "iPad Pro 12.9-inch 3rd-gen",
    "Content-Type": "application/json",
}

# =========================
# Dynamic auth headers
# =========================
headers.update({
    "ali_sign_whash": ali_sign_whash,
    "wToken": wToken,
    "accessToken": accessToken,
})

# common api
url = "https://api.cdfsunrise.com/restapi/search/list"

# 把傻逼Warning给屏蔽了
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# common helper function

# def products_to_df(products):
# retrieve each individual product -> df
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

# def fetch_all_products(json_data, page=1):
# 实现翻页, default page=1 -> output: list of all products of the same category
def fetch_all_products(json_data, page=1):
    session = requests.Session()

    all_products = []
    #page = 1
    fetched = 0

    while True:
        json_data["pageNumber"] = page

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

    return all_products