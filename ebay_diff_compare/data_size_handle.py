import re
import pandas

async def main(sku_list_str):
    sku_list = sku_list_str.split(",")
    for sku in sku_list:
        df =  pandas.read_csv(f"title_handled/raw_{sku}_title_handled.csv")
        for index,row in df.iterrows():
            if "/" in row["尺码"]:
                 size_str_list = row["尺码"].split("/")
                 men_size_str = size_str_list[0]
                 match = re.search(r'\d+\.?\d*', men_size_str)
                 if match:
                    number_str = match.group()
                    size = number_str + " " + "Men"
                    df.at[index, "尺码"] = size
                    continue

            def is_number(s):
                try:
                    float(s)
                    return True
                except ValueError:
                    return False

            if " " in row["尺码"] and "/" not in row["尺码"]:
                size_str_part = row["尺码"].split(" ")
                for part in size_str_part:
                    flag = is_number(part)
                    if flag:
                        df.at[index, "尺码"] = str(part) + " " + "Men"
                        continue

            if " " not in row["尺码"] and "/" not in row["尺码"]:
                flag = is_number(row["尺码"])
                if flag:
                    df.at[index, "尺码"] = str(row["尺码"]) + " " + "Men"
                    continue

            pattern = r'^[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?$'
            if bool(re.match(pattern, row["尺码"])):
                df.at[index, "尺码"] = str(row["尺码"]) + " " + "Men"


        df.to_csv(f"./size_handled/raw_{sku}_title_size_handled.csv",index=False)
