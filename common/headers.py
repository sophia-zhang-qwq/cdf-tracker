import time

# =====================================================
# Cookies
# =====================================================
COOKIES = {
    # TO-DO
    #"_gcl_au": "你的",
    '_gcl_au': '1.1.1842803474.1780732880',

    # TO-DO
    #"_ga": "你的",
    '_ga': 'GA1.1.1923441225.1780732883',

    # TO-DO
    #"_fbp": "你的",
    '_fbp': 'fb.1.1780732895126.148030225784856703',
    
    # TO-DO
    #"_token": "你的",
    '_token': '2C5FBFA3CAB5CF6538F9F4EDDFED0A65A7796614B90DF3ADE68C1D9E84636ED199A1C8CD23870EA51FF5B97C929ABCD5E90DB2D30F62F47C',

    "cookies_agreement__604163145":
        "{%22necessary%22:true%2C%22feature%22:true%2C%22performance%22:true}",

    "h5_cookies_agreement__604163145":
        "{%22necessary%22:true%2C%22feature%22:true%2C%22performance%22:true}",
    # TO-DO
    #"TDC_itoken": "你的",
    'TDC_itoken': '1965225349%3A1780975031',

    # TO-DO
    #"_ga_GXZMXL96VN": "你的",
    '_ga_GXZMXL96VN': 'GS2.1.s1780969768$o5$g1$t1780977696$j53$l0$h873855105',

    # TO-DO
    #"_ga_GR528RWW2C": "你的",
    '_ga_GR528RWW2C': 'GS2.1.s1780969768$o5$g1$t1780977696$j53$l0$h1300337362',

}

# =====================================================
# Common Headers
# =====================================================
HEADERS = {
    "Accept":"application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection":"keep-alive",
    "Content-Type":"application/json;charset=UTF-8",
    "Origin":"https://www.cdf-beauty.com",
    "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1",
    "accept-version":"1.0.0",
    "app-key":"h5sqBuyer_604158472",
    "app-version":"6.8.1",
    "cookieid":"8dde34a1-396d-0722-596e-75e441370463",
    "deviceid":"8dde34a1-396d-0722-596e-75e441370463",
    "sec-ch-ua":'"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    "sec-ch-ua-mobile":"?1",
    "sec-ch-ua-platform":'"iOS"',

    # TO-DO
    #"ymt-pars":"你的ymt-pars",
    'ymt-pars': 'format=json&appid=71&accesstoken=2C5FBFA3CAB5CF659354E130A22CB80D225BE3A51A2A3357FBBDA092D369D05A0E72A0EFEAB24B9A947201746E359B5DAB065F5F128F8D81&userid=626699686&os=iOS&client=iOS&requestid=6d8049f6-f7d6-4578-c200-a3c3ad0fc762&idfa=e38dacf2-22ce-79ce-b7c1-910aca56b78f&imei=e38dacf2-22ce-79ce-b7c1-910aca56b78f&mchId=604163145&language=zh_TW',

}

# =====================================================
# Helper
# =====================================================
def get_headers(referer):
    headers = HEADERS.copy()
    headers["Referer"] = referer
    headers["timestamp"] = str(int(time.time() * 1000))
    return headers