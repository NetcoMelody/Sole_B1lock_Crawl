from curl_cffi import requests

# 请求 URL（已包含查询参数）
url = "https://api.jihuanshe.com/api/market/search/match-product"
keyword = "皮卡丘"
page = 1
params = {
    "type": "card_version",
    "keyword": keyword,
    "game_key": "pkm",
    "game_sub_key": "jp",
    "page": page,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbnYiOiJwcm9kdWN0aW9uIiwic3ViIjozMDkwNjU3LCJpc3MiOiJodHRwOi8vYXBpLmppaHVhbnNoZS5jb20vYXBpL21hcmtldC9hdXRoL2xvZ2luLW9yLXNpZ251cCIsImlhdCI6MTc2MTc4OTQ4MSwiZXhwIjoxNzY2OTczNDgxLCJuYmYiOjE3NjE3ODk0ODEsImp0aSI6IjZVMWZRSnVNMldLR1ZQdFkifQ.0gz6bwPm6RsakM2jnRBepSU--EYAONeQF6_Z3DPF5G0"
}

# 请求头
headers = {
    "User-Agent": "Model/HONOR,RKY-AN00 OS/32 Version/3.4.1",
    "Host": "api.jihuanshe.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip"
}

# 发起请求（使用 impersonate 模拟浏览器 TLS 指纹）
response = requests.get(
    url,
    params=params,
    headers=headers,
    impersonate="chrome110"  # 可选：根据目标网站调整，如 "chrome120", "safari15_5" 等
)

# 输出响应
print("Status Code:", response.status_code)
print("Response Body:", response.text)