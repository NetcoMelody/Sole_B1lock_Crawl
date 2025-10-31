from curl_cffi import requests

headers = {
    "User-Agent": "Model/HONOR,RKY-AN00 OS/32 Version/3.4.1",
    "Host": "api.jihuanshe.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
}

url = "https://api.jihuanshe.com/api/market/search/match-product"
params = {
    "type": "card_version",
    "keyword": "mew v",
    "game_key": "pkm",
    "game_sub_key": "en",
    "page": 1,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbnYiOiJwcm9kdWN0aW9uIiwic3ViIjozMDkwNjU3LCJpc3MiOiJodHRwOi8vYXBpLmppaHVhbnNoZS5jb20vYXBpL21hcmtldC9hdXRoL2xvZ2luLW9yLXNpZ251cCIsImlhdCI6MTc2MTc4OTQ4MSwiZXhwIjoxNzY2OTczNDgxLCJuYmYiOjE3NjE3ODk0ODEsImp0aSI6IjZVMWZRSnVNMldLR1ZQdFkifQ.0gz6bwPm6RsakM2jnRBepSU--EYAONeQF6_Z3DPF5G0"
}

response = requests.get(url, headers=headers, params=params)
print(response.text)