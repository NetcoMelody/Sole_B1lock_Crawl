import pandas
import pandas as pd
from collections import defaultdict
import numpy as np

async def main(sku_list_str ):
    sku_list = sku_list_str.split(",")

    store_item_perSkuPerSize = {}
    itemID_list = []
    for item_sku in sku_list:
        df =  pandas.read_csv(f"./size_handled/raw_{item_sku}_title_size_handled.csv")
        for index,row in df.iterrows():
            store = row["店铺名"]
            itemID = row["ItemID"]
            sku = row["货号"]
            size = row["尺码"]
            price = row["价格"]
            if store not in store_item_perSkuPerSize:
                store_item_perSkuPerSize[store]={"items":{}}
            if itemID not in itemID_list:
                itemID_list.append(itemID)
                store_item_perSkuPerSize[store]["items"][sku] = {}
                store_item_perSkuPerSize[store]["items"][sku] = {"itemID":itemID,"variations":[]}
            store_item_perSkuPerSize[store]["items"][sku]["variations"].append({size: price})
    data = store_item_perSkuPerSize

    # 1. 提取所有 (item, size) 组合作为列
    all_columns = set()
    shop_data = {}

    for shop_name, shop_info in data.items():
        shop_dict = {}
        for item_id, item_info in shop_info['items'].items():
            # 合并所有 variations（注意：原始数据有重复，我们取最后一次或任意一次即可）
            size_price_map = {}
            for var in item_info['variations']:
                # var 是一个字典，如 {'9 Men': 381.0}
                size = list(var.keys())[0]
                price = var[size]
                size_price_map[size] = price  # 重复会覆盖，但值相同
            # 存入 shop_dict: key 为 (item_id, size)
            for size, price in size_price_map.items():
                shop_dict[(item_id, size)] = price
                all_columns.add((item_id, size))
        shop_data[shop_name] = shop_dict

    # 2. 创建 MultiIndex 列
    columns = sorted(all_columns)  # 排序以便阅读
    multi_cols = pd.MultiIndex.from_tuples(columns, names=['Item', 'Size'])

    # 3. 构建 DataFrame
    df = pd.DataFrame(index=shop_data.keys(), columns=multi_cols, dtype='float64')

    # 4. 向量化填充：使用 pd.Series 自动对齐索引
    for shop, price_dict in shop_data.items():
        series = pd.Series(price_dict, dtype='float64')
        df.loc[shop] = series

    # 5. 可选：转置以便商品-尺码为行，店铺为列（更常见）
    result_df = df.T  # 转置后：行是 (Item, Size)，列是店铺

    # 确保特殊店铺存在（若不存在则添加 NaN 列）
    special_stores = ['sole_b1ock', 'all_in_domain']
    for store in special_stores:
        if store not in result_df.columns:
            result_df[store] = np.nan

    # 其他店铺
    other_stores = [col for col in result_df.columns if col not in special_stores]

    # Step 1: 计算非特殊店铺的最低价（每行）
    min_other = result_df[other_stores].min(axis=1, skipna=True)

    # Step 2: 获取特殊店铺价格
    p_sole = result_df['sole_b1ock']
    p_all = result_df['all_in_domain']

    # Step 3: 构造候选价格，找全局最低
    # 将 min_other, p_sole, p_all 合并成 DataFrame
    candidates = pd.DataFrame({
        'min_other': min_other,
        'sole_b1ock': p_sole,
        'all_in_domain': p_all
    })

    # 找出每行的最小值（忽略 NaN）
    global_min = candidates.min(axis=1)


    # 新逻辑：计算 special 店铺中的最低价（sole_b1ock 和 all_in_domain 中的 min）
    min_special = pd.concat([p_sole, p_all], axis=1).min(axis=1)

    # 差距 = 非特殊最低价 - 特殊店铺最低价
    gap = min_other - min_special

    # 如果 min_special 是 NaN（即两个 special 店都无报价），则 gap 也应为 NaN
    gap = gap.where(min_special.notna(), np.nan)

    # Step 5: 找出 global_min 来自哪个店铺（用于标红）
    # 我们需要知道在原始 result_df 中，哪个店铺提供了 global_min
    def find_min_store(row, global_min_val):
        # 检查所有店铺列
        for col in result_df.columns:
            if pd.notna(row[col]) and row[col] == global_min_val:
                return col
        return None

    min_store_series = result_df.apply(lambda row: find_min_store(row, global_min[row.name]), axis=1)

    # Step 6: 创建最终展示 DataFrame（包含所有店铺 + 差距列）
    final_df = result_df.copy()
    final_df['我们店铺最低价与剩余店铺最低据的差距(+为我们店铺更低，-为剩余店铺更低)'] = gap

    # Step 7: 定义高亮函数
    def highlight_min_price(row):
        styles = [''] * len(row)
        min_store = min_store_series[row.name]
        if min_store and min_store in row.index:
            idx = row.index.get_loc(min_store)
            styles[idx] = 'background-color: blue; color: white'
        return styles

    # 应用样式（注意：'差距'列不参与标红）
    styled_df = final_df.style.apply(highlight_min_price, axis=1, subset=result_df.columns)

    # ... [你原有的代码直到 styled_df 定义] ...

    # 应用红色高亮（最低价）
    styled_df = final_df.style.apply(highlight_min_price, axis=1, subset=result_df.columns)

    # === 新增：蓝色高亮每个 Item 中各 Size 的最高价（按 Item 分组）===
    def highlight_max_per_item(df):
        # df 是 final_df 的视图（含所有列）
        # 我们只关心店铺列（不含“差距”列）
        store_cols = result_df.columns.tolist()  # 这些是店铺列
        styles = pd.DataFrame('', index=df.index, columns=df.columns)

        # 按 Item 分组（MultiIndex 的 level=0）
        for item, group in df.groupby(level=0):
            # 提取该 item 下所有行（不同 size）在店铺列中的子集
            sub_df = group[store_cols]
            # 找出每个 size 行中的最大值（按行找 max，但我们要的是：在该 item 内所有 (size, store) 中的最大值？）
            # 但注意：需求是“每个 sku 中的每个尺码中的最高价” → 实际上是：对每个 (Item, Size) 行，在所有店铺中找最高价？
            # 然而你描述是：“每个 sku 中的每个尺码中的最高价” → 即：对每个 (Item, Size) 行，在所有店铺中，谁最高？
            # 所以其实是 **每行内的最大值**（和红色最低价对称）

            # 因此：对 group 中的每一行（即每个 (Item, Size)），找该行在 store_cols 中的最大值
            for idx in group.index:
                row = sub_df.loc[idx]
                max_val = row.max()
                if pd.notna(max_val):
                    # 找出哪些列等于 max_val（可能多个店铺同价）
                    max_cols = row[row == max_val].index
                    for col in max_cols:
                        styles.loc[idx, col] = 'background-color: red'  # 或 'blue'，但 lightblue 更可读

        return styles

    # 应用蓝色高亮（叠加到已有样式）
    styled_df = styled_df.apply(lambda x: highlight_max_per_item(final_df), axis=None)

    # 导出
    output_file = "final_excel.xlsx"
    styled_df.to_excel(output_file, engine='openpyxl', index=True)

    # === 新增：冻结首行和首列（关键！放在这里）===
    from openpyxl import load_workbook
    wb = load_workbook(output_file)
    ws = wb.active
    ws.freeze_panes = 'B2'  # 冻结第1行（列标题）和第1列（Item/Size 索引）
    wb.save(output_file)
    # ===================

    print(f"✅ 已成功导出结果到: {output_file}")
    print("📌 说明：")
    print("- 红色背景 = 该 (Item, Size) 下三家（非特殊最低、sole_b1ock、all_in_domain）中的最低价")
    print("- '差距' 列 = 非特殊店铺最低价 - 全局最低价（正数表示特殊店铺更便宜）")



