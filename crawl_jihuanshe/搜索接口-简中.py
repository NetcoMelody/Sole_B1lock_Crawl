# jihuanshe_search.py
from curl_cffi import requests
import urllib.parse

# ===== 配置 =====

KEYWORD = "皮卡丘"
GAME_KEY = "pkm"
GAME_SUB_KEY = "en"
PAGE = 1

# 从 Frida 获取的有效 token（有效期到 2025-12-27）
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbnYiOiJwcm9kdWN0aW9uIiwic3ViIjozMDkwNjU3LCJpc3MiOiJodHRwOi8vYXBpLmppaHVhbnNoZS5jb20vYXBpL21hcmtldC9hdXRoL2xvZ2luLW9yLXNpZ251cCIsImlhdCI6MTc2MTY2NTgyNywiZXhwIjoxNzY2ODQ5ODI3LCJuYmYiOjE3NjE2NjU4MjcsImp0aSI6Imo2dlNVUkpGdnZzYkIyOTEifQ.TTHrYWCXtBP_3UAJsrUPwMAttLyZ799SBVxpkKFVPkk"

USER_AGENT = "Model/OPPO,PJJ110 OS/32 Version/3.4.1"

# ===== 构造 URL =====
encoded_keyword = urllib.parse.quote(KEYWORD)
url = (
    f"https://api.jihuanshe.com/api/market/search/match-product"
    f"?type=card_version&keyword={encoded_keyword}&game_key={GAME_KEY}&game_sub_key={GAME_SUB_KEY}&page={PAGE}&token={TOKEN}"
)

# ===== 发送请求 =====
try:
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        # impersonate="chrome110",  # 可选：模拟 Chrome（但可能不如原生 UA 有效）
        timeout=10
    )
    print("状态码:", response.status_code)
    print("响应头:", dict(response.headers))
    print("响应体:")
    print(response.text)
except Exception as e:
    print("请求失败:", e)