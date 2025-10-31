sku_list_str = "HF4340-800,DM7866-202,DM7866-200,DR5415-103,DR5415-100,IB8958-001,M2002RDB,M2002RDA"
sku_list = sku_list_str.split(",")

replace_sku_list = []
for sku in sku_list:
    replace_sku_list.append(sku)  # 始终保留原始 SKU
    if '-' in sku:
        replace_sku_list.append(sku.replace('-', ' '))  # 添加去掉 '-' 的版本


