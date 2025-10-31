from curl_cffi import requests

# URL with query parameters
url = "https://api.jihuanshe.com/api/market/search/match-product"

keyword = "皮卡丘"
page = 1
params = {
    "type": "card_version",
    "keyword": keyword,
    "game_key": "pkm",
    "game_sub_key": "tc",
    "page": page,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbnYiOiJwcm9kdWN0aW9uIiwic3ViIjozMDkwNjU3LCJpc3MiOiJodHRwOi8vYXBpLmppaHVhbnNoZS5jb20vYXBpL21hcmtldC9hdXRoL2xvZ2luLW9yLXNpZ251cCIsImlhdCI6MTc2MTc4OTQ4MSwiZXhwIjoxNzY2OTczNDgxLCJuYmYiOjE3NjE3ODk0ODEsImp0aSI6IjZVMWZRSnVNMldLR1ZQdFkifQ.0gz6bwPm6RsakM2jnRBepSU--EYAONeQF6_Z3DPF5G0"
}

# Headers
headers = {
    "User-Agent": "Model/HONOR,RKY-AN00 OS/32 Version/3.4.1",
    "Host": "api.jihuanshe.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip"
}

# Send GET request
response = requests.get(url, params=params, headers=headers)

# Print response
print("Status Code:", response.status_code)
print("Response Body:")
print(response.text)