import random
import time

import pandas
from curl_cffi import requests
import json
import re
from difflib import SequenceMatcher

def is_chinese(text):

    # 方法1: 使用正则表达式检查是否包含中文字符
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
    return bool(chinese_pattern.search(str(text)))

def jihuanshe_request(keyword,card_name,attach,cardLanguage):
    def is_similar(a, b, threshold=0.85):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio() >= threshold

    headers = {
        "User-Agent": "Model/HONOR,RKY-AN00 OS/32 Version/3.4.1",
        "Host": "api.jihuanshe.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    page = 1
    url = "https://api.jihuanshe.com/api/market/search/match-product"
    cardLanguage = cardLanguage.strip()
    cardLanguage_new = cardLanguage.upper()
    cardLanguageDict = {"JAPANESE":"jp","CHINESE":"sc","ENGLISH":"en"}
    game_sub_key = cardLanguageDict[cardLanguage_new]

    params = {
        "type": "card_version",
        "keyword": keyword,
        "game_key": "pkm",
        "game_sub_key": game_sub_key,
        "page": page,
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbnYiOiJwcm9kdWN0aW9uIiwic3ViIjozMDkwNjU3LCJpc3MiOiJodHRwOi8vYXBpLmppaHVhbnNoZS5jb20vYXBpL21hcmtldC9hdXRoL2xvZ2luLW9yLXNpZ251cCIsImlhdCI6MTc2MTc4OTQ4MSwiZXhwIjoxNzY2OTczNDgxLCJuYmYiOjE3NjE3ODk0ODEsImp0aSI6IjZVMWZRSnVNMldLR1ZQdFkifQ.0gz6bwPm6RsakM2jnRBepSU--EYAONeQF6_Z3DPF5G0"
    }
    response = requests.get(url, headers=headers, params=params)
    data= response.json()
    page_count = data["last_page"]
    print("last_page:",page_count,"keyword:",keyword)
    if page_count > 1:
        for i in range(page_count):
            print (f"第{i+1}页")
            if i>0:
                params_new = {
                    "type": "card_version",
                    "keyword": keyword,
                    "game_key": "pkm",
                    "game_sub_key": game_sub_key,
                    "page": i+1,
                    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbnYiOiJwcm9kdWN0aW9uIiwic3ViIjozMDkwNjU3LCJpc3MiOiJodHRwOi8vYXBpLmppaHVhbnNoZS5jb20vYXBpL21hcmtldC9hdXRoL2xvZ2luLW9yLXNpZ251cCIsImlhdCI6MTc2MTc4OTQ4MSwiZXhwIjoxNzY2OTczNDgxLCJuYmYiOjE3NjE3ODk0ODEsImp0aSI6IjZVMWZRSnVNMldLR1ZQdFkifQ.0gz6bwPm6RsakM2jnRBepSU--EYAONeQF6_Z3DPF5G0"
                }
                response_new = requests.get(url, headers=headers, params=params_new)
                data_new= response_new.json()
                for item in data_new["data"]:
                    min_price = item["min_price"]
                    number = item["number"]
                    name = item["name_cn"]

                    print (f"card_name:{card_name} vs name_jihuanshe:{name}")
                    name_new = name.strip()
                    card_name_new = card_name.strip()
                    if is_similar(name_new, card_name_new):
                        if attach == "SM":
                            complete_number = attach + keyword
                            if complete_number in number:
                                print ("匹配到了")
                                min_price = item["min_price"]
                                if min_price is None:
                                    min_price = 0
                                    print ("但是没货")
                                return min_price,number
                        else:
                            print ("匹配到了")
                            min_price = item["min_price"]
                            if min_price is None:
                                min_price = 0
                                print ("但是没货")
                            return min_price,number
                    else:

                        continue
            else:
                data= response.json()
                for item in data["data"]:
                    min_price = item["min_price"]
                    name = item["name_cn"]
                    number = item["number"]
                    name = str(name)
                    card_name = str(card_name)
                    print (f"card_name:{card_name} vs name_jihuanshe:{name}")
                    name_new = name.strip()
                    card_name_new = card_name.strip()

                    if is_similar(name_new, card_name_new):
                        if attach == "SM":
                            complete_number = attach + keyword
                            if complete_number in number:
                                print ("匹配到了")
                                min_price = item["min_price"]
                                if min_price is None:
                                    min_price = 0
                                    print ("但是没货")
                                return min_price,number
                        else:
                            print ("匹配到了")
                            min_price = item["min_price"]
                            if min_price is None:
                                min_price = 0
                                print ("但是没货")
                            return min_price,number
                    else:
                        delay = random.uniform(0.1,0.3)
                        time.sleep(delay)
                        continue

    else:
        for item in data["data"]:
            min_price = item["min_price"]
            number = item["number"]
            name = item["name_cn"]
            print (f"card_name:{card_name} vs name_jihuanshe:{name}")
            name_new = name.strip()
            card_name_new = card_name.strip()
            if cardLanguage != "Japanese":
                if is_similar(name_new, card_name_new):
                    if attach == "SM":
                        complete_number = attach + keyword
                        if complete_number in number:
                            print ("匹配到了")
                            min_price = item["min_price"]
                            if min_price is None:
                                min_price = 0
                                print ("但是没货")
                            return min_price,number
                    else:
                        print ("匹配到了")
                        min_price = item["min_price"]
                        if min_price is None:
                            min_price = 0
                            print ("但是没货")
                        return min_price,number
            else:
                print ("匹配到了")
                min_price = item["min_price"]
                if min_price is None:
                    min_price = 0
                    print ("但是没货")
                return min_price,number
    return None,None


df = pandas.read_excel("2.xlsx")
item_code_list = []
card_name_list = []
ebay_price_list = []
jihuanshe_price_list = []
diff_price_list = []
card_number_list = []
cardLanguageList = []
for index,row in df.iterrows():
    cardNumber = str(row["CardNumber"])
    if cardNumber is None:
        continue
    keyword  = cardNumber.removeprefix("'")
    item_code = row["ItemId"]
    card_name = row["CardName"]
    Ebay_CardPrice = row["CardPrice-US"]
    cardLanguage = row["CardLanguage"]
    cardLanguageList.append(cardLanguage)
    print (f"itemCode:{item_code} |cardName:{card_name} | CardNumber:{cardNumber} |ebayCardPrice:{Ebay_CardPrice} | cardLanguage:{cardLanguage} | keyword:{keyword}")
    keyword = keyword.strip()
    if cardLanguage != "Japanese":
        if "/" in keyword and " " not in keyword:
            parts = keyword.split("/")
            keyword = parts[0]
            attach = None
        elif "NO." in keyword:
            keyword = keyword.removeprefix("NO.")
            attach = None
        elif "SM" in keyword:
            keyword = keyword.removeprefix("SM")
            attach = "SM"
        else:
            keyword = keyword
            attach = None
    else:
        attach = None
    print ("cardName:",card_name,"cardNumber",cardNumber,"keyword:",keyword,attach,"cardLanguage:",cardLanguage)
    min_price,jihuanshe_code = jihuanshe_request(keyword,card_name,attach,cardLanguage)
    jihuanshe_code = str(jihuanshe_code)
    if min_price is None or min_price == 0:
        item_code_list.append(item_code)
        card_name_list.append(card_name)
        ebay_price_list.append(Ebay_CardPrice)
        jihuanshe_price_list.append(min_price)
        if min_price == 0:
            diff_price_list.append('该产品缺货')
        if min_price is None:
            diff_price_list.append("未找到该产品")
        jihuanshe_code = "'" + jihuanshe_code
        card_number_list.append(jihuanshe_code)
        continue
    jihuanshe_price = float(min_price)
    jihuanshe_price *= 0.14
    diff_price = Ebay_CardPrice - jihuanshe_price
    print ("cardName:",card_name,"cardNumber",cardNumber,"keyword:","jihuanshe_price:",jihuanshe_price,"ebay_price:",Ebay_CardPrice,"diff_price-us:",diff_price,"cardLanguage:",cardLanguage)
    item_code_list.append(item_code)
    card_name_list.append(card_name)
    ebay_price_list.append(Ebay_CardPrice)
    jihuanshe_price_list.append(min_price)
    diff_price_list.append(diff_price)
    jihuanshe_code = "'" + jihuanshe_code
    card_number_list.append(jihuanshe_code)
    time.sleep(5)
data = {
    "ebay_itemCode":item_code_list,
    "jihuanshe_code":card_number_list,
    "cardName":card_name_list,
    "ebayPrice-us":ebay_price_list,
    "jihuanshePrice-us":jihuanshe_price_list,
    "diffPrice-us":diff_price_list,
    "CardLanguage":cardLanguageList
}
df = pandas.DataFrame(data)
df.to_csv("2-jp.csv",index=False)









