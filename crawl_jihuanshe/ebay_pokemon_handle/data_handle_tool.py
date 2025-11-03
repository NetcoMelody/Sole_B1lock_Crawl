import pandas
from decimal import Decimal, ROUND_HALF_UP
import re

def rountd_digied(digit):
    number = Decimal(digit)
    rounded = number.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return rounded

def contains_chinese(text):
    if not isinstance(text, str):
        return False
    # 匹配基本汉字 + 扩展A + 常见中文标点
    pattern = r'[\u4e00-\u9fff\u3400-\u4dbf\u3000-\u303f]'
    return bool(re.search(pattern, text))

df = pandas.read_csv("test.csv")
for index,row in df.iterrows():
    diffprice_us = row["diffPrice-us"]
    jihuanshePrice_rmb = row["jihuanshePrice-rmb"]
    flag = contains_chinese(diffprice_us)

    if flag:
        continue
    else:
        diffprice_us_handle = rountd_digied(diffprice_us)
        df.loc[index,"diffPrice-us"] = diffprice_us_handle

    if not jihuanshePrice_rmb is None:
        jihuanshePrice_us = jihuanshePrice_rmb*0.14
        jihuanshePrice_us = rountd_digied(jihuanshePrice_us)
        df.loc[index,"jihuanshePrice-rmb"] = float(jihuanshePrice_us)

df.to_csv("testv2.csv",index=False)





