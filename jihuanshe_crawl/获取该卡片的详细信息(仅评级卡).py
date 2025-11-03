from curl_cffi import requests

# 公共 headers（部分请求使用）
common_headers = {
    "User-Agent": "Model/OPPO,PJJ110 OS/32 Version/3.4.1",
    "Host": "api.jihuanshe.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip"
}

# Token（所有带 token 的请求共用）
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbnYiOiJwcm9kdWN0aW9uIiwic3ViIjozMDkwNjU3LCJpc3MiOiJodHRwOi8vYXBpLmppaHVhbnNoZS5jb20vYXBpL21hcmtldC9hdXRoL2xvZ2luLW9yLXNpZ251cCIsImlhdCI6MTc2MTY2NTgyNywiZXhwIjoxNzY2ODQ5ODI3LCJuYmYiOjE3NjE2NjU4MjcsImp0aSI6Imo2dlNVUkpGdnZzYkIyOTEifQ.TTHrYWCXtBP_3UAJsrUPwMAttLyZ799SBVxpkKFVPkk"

# raw_data 参数（用于加密请求）
raw_data = "qfFrKMsqVyba%2FR08hYiThNoTuKod3Ei%2BYRHFET6MI3KzhT59nJRzZK5iG7SF%2F6CkdZGdLc4jQ088461ySYvbt6zrFZFLOpX1QHwzBgBzRssflfDCSrkSb3iURH5QMqVOiPxN5jk25b%2BcUd%2F9DugRs8QoDzLqONa9E1yCKaekRLH%2Bvvafjd6cpD5N0UavKrXumGC%2BZV5yMdri1aOK9SiS%2Bp5sg3RcYn06Tua%2BiWs%2BbwP9CqmnBPAM6OO%2F5jzV1JkVieTngw4mwEKCc396f9hsBGivi07N8qxWDjxXTdN0%2Fr0y8O7Qv1cG7v3XSrq7Gcw0yNDPorsDSmxxVA6sbhg6J1f%2FIjp9hjt4oTzJbyK1e7K0DbwM0ZFR3hbmel%2BEtLc7dxGJdvzcvALnTsMVAfxn77egEcuTdgXNxx%2BnpPXvn1rV3%2F9iIiVj2EbP9dH%2BdTEzkXYFnus4eTCzIKExw7B%2Bn6lAyYlnmjjLz5LhoY59g8v7yeXQ2zr3LqlF1Ws0irRKEzNq8xJeHA4o91Br9aseBjKMDDFN9kuXDU0ckQxrJot2rkV6gFNAcB9YmSqwncaJP3lhZAR7lYEUKtJc%2BzoAmETI"

# 使用 impersonate 模拟浏览器指纹（可选）
impersonate = "chrome110"  # 或 "chrome120", "safari15_5" 等


card_version_id = "83192"

# 3. grading-products（preview=1），仅 User-Agent
print("\n→ Request 3: Grading products (User-Agent only)")
url3 = f"https://api.jihuanshe.com/api/market/card-versions/grading-products?card_version_id={card_version_id}&preview=0&game_key=pkm&page=1"
resp3 = requests.get(url3, headers={"User-Agent": common_headers["User-Agent"]}, impersonate=impersonate)
print(f"Status: {resp3.status_code}, Preview: {resp3.text}")
