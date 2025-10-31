import pandas
from aioconsole import aprint



async def main(sku_list_str):
    sku_list = sku_list_str.split(",")
    replace_sku_list = []
    for sku in sku_list:
        replace_sku_list.append(sku)  # 始终保留原始 SKU
        if '-' in sku:
            replace_sku_list.append(sku.replace('-', ' '))  # 添加去掉 '-' 的版本
    for sku in sku_list:
        df = pandas.read_csv(f"./raw/raw_{sku}.csv")

        import re
        pattern = '|'.join(re.escape(sku) for sku in replace_sku_list)

        # 创建一个函数，用于提取匹配的 SKU
        def extract_sku(hao):
            if pandas.isna(hao):
                return None
            for sku in replace_sku_list:
                if sku in str(hao):
                    return sku
            return None

        # 应用函数，生成新的货号列
        df['new_货号'] = df['货号'].apply(extract_sku)

        # 丢弃未匹配的行（即 new_货号 为 None 的行）
        df = df.dropna(subset=['new_货号']).copy()

        # 替换原列（可选）
        df['货号'] = df['new_货号']
        df = df.drop(columns=['new_货号'])  # 删除临时列

        df.to_csv(f"./title_handled/raw_{sku}_title_handled.csv",index=False)
        await aprint(f"./title_handled/raw_{sku}_title_handled.csv已生成")
        #
        # df = df.drop(columns=["ItemID"])
