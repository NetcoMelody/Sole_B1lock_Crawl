import shutil

from sqlalchemy.dialects.mssql.information_schema import columns
from tortoise import Tortoise, fields
from tortoise.models import Model
import asyncio
import asyncio
from aioconsole import aprint
import datetime
import re
import aiomysql
import aiopandas
import fake_useragent
import aiohttp
import numpy as np
import time
import logging as logger
from tenacity import retry, stop_after_attempt, wait_exponential
import json
import os
import aiofiles


while 1:
    try:
        class api_handle:
            def __init__(self, query_sku):
                ua = fake_useragent.UserAgent()
                random_ua = ua.random
                self.api_url = 'http://dewu.ccrotate.com/dewu.php/queryspulist'
                self.header = {
                    "Content-Type": "application/json",
                    "User-Agent": random_ua,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                }
                self.sku_list_new = query_sku

            @retry(stop=stop_after_attempt(10),
                            wait=wait_exponential(multiplier=2, max=60, exp_base=2))
            async def request_api(self, _sku_list, _size_list, _price_list):
                ua = fake_useragent.UserAgent()
                random_ua = ua.random
                processed_payload = {'code': 'sdue23487s8y234yhjHJHh2348hH', 'dwDesignerId': self.sku_list_new}
                start_time = time.time()
                logger.debug(f"正在发送API请求: {json.dumps(processed_payload, ensure_ascii=False)}")
                logger.debug(f"API请求体: {processed_payload}")
                logger.debug(f"URL::: {self.api_url}")
                async with aiohttp.ClientSession() as session:
                    async with session.post(self.api_url, headers=self.header, json=processed_payload,
                                            timeout=60) as response:
                        json_text = await response.text()
                        json_dict = json.loads(json_text)
                        json_dict_data = json_dict['data']
                        if 'spuList' in json_dict_data and json_dict_data['spuList']:
                            spu_list = json_dict_data['spuList']
                            await aprint(spu_list)
                            for i in spu_list:
                                skulist = i['skuList']
                                for size_attr in skulist:
                                    sku = i['dwDesignerId']
                                    size_attrs = size_attr['saleAttr']
                                    for s in size_attrs:
                                        if s['cnName'] == '尺码':
                                            if s['cnValue']:
                                                _size_list.append(s['cnValue'])
                                                _sku_list.append(sku)
                                                price = size_attr['minBidPrice']
                                                if price != 0:
                                                    price = int(str(price)[:-2])
                                                else:
                                                    price = None
                                                _price_list.append(price)
                await aprint(len(_sku_list))
                await aprint(len(_size_list))
                await aprint(len(_price_list))
                return _sku_list, _size_list, _price_list
        class data_handle:
            async def handle_query_data(self):
                if not os.path.exists('./temp/query_info.csv'):
                    print("query_info.csv 文件不存在，请确保 api_handle.request_api() 已成功执行", flush=True)
                    return
                df = aiopandas.read_csv('./temp/query_info.csv')
                df['size'] = df['size'].astype(str).str.strip()
                # 检查是否有特殊字符
                if df['size'].str.contains('⅔|⅓', na=False).any():
                    print('检测到特殊字符', flush=True)
                    if df['size'].str.contains('⅓', na=False).any():
                        mask = df['size'].str.contains('⅓', na=False)
                        df.loc[mask, 'size'] = df.loc[mask, 'size'].str.replace('⅓', '')
                    if df['size'].str.contains('⅔', na=False).any():
                        mask = df['size'].str.contains('⅔', na=False)
                        df.loc[mask, 'size'] = df.loc[mask, 'size'].str.replace('⅔', '').astype(float) + 0.5
                    now_time = datetime.datetime.now()
                    now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
                    df.to_csv(f'./temp/query_info.csv', index=False)
                    shutil.copy("./temp/query_info.csv",f"D:/PythonProject/log/query_info日志/query_info-{now_time_str}.csv")
                    await aprint('写入成功', flush=True)

            async def diff_data(self):
                import pandas as pd
                import re

                query_info_df = pd.read_csv('./temp/query_info.csv', encoding='utf-8-sig')
                only_in_api_df = pd.read_csv('./temp/only_in_api.csv', encoding='utf-8-sig')

                only_in_api_df['sku'] = only_in_api_df['sku'].astype(str).str.strip()
                query_info_df['sku'] = query_info_df['sku'].astype(str).str.strip()

                def extract_eu_number(size_str):
                    eu_match = re.search(r'EU\s*(\d+(?:\.\d+)?)\s*(1/3|2/3|1/2)', size_str)
                    if eu_match:
                        base_size = float(eu_match.group(1))
                        fraction = eu_match.group(2)
                        if fraction == '1/3':
                            return None
                        if fraction == '2/3':
                            total_size = base_size + 0.5
                            return str(round(total_size, 2))
                        elif fraction == '1/2':
                            total_size = base_size + 0.5
                            return str(round(total_size, 2))
                    eu_match_simple = re.search(r'EU\s*(\d+(?:\.\d+)?)', size_str)
                    if eu_match_simple:
                        return str(eu_match_simple.group(1))
                    return None

                only_in_api_df['eu_number'] = only_in_api_df['size'].apply(extract_eu_number)
                query_info_df['eu_number'] = query_info_df['size'].astype(str).str.replace('.0', '', regex=False)

                only_in_api_df = only_in_api_df[['post_id', 'sku', 'variation_id', 'eu_number']]
                query_info_df = query_info_df[['sku', 'eu_number', 'price(RMB)']]
                matched = aiopandas.merge(
                    only_in_api_df,
                    query_info_df,
                    on=['sku', 'eu_number'],
                    how='left'
                )
                matched['price(RMB)'] = pd.to_numeric(matched['price(RMB)'], errors='coerce')
                # matched['price(RMB)'] = matched['price(RMB)'].fillna(100000)
                matched['price(RMB)'] = matched['price(RMB)'].astype('float64')
                matched.rename(columns={'price(RMB)': 'final_price'}, inplace=True)
                mask = matched['final_price'] != 100000
                matched['final_price'] = pd.to_numeric(matched['final_price'], errors='coerce').astype('float64')
                #dw价格公式
                #  (成本_CNY ÷ 7.2 + 50) ÷ 0.95 - 29.9
                matched.loc[mask, 'final_price'] = ( (matched.loc[mask, 'final_price'] /7.2 + 75) / 0.91 - 29.9).round(2)
                now_time = datetime.datetime.now()
                now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
                matched = matched[['post_id', 'sku', 'variation_id', 'eu_number', 'final_price']]



                left_pattern = r'[（(]'
                right_pattern = r'[）)]'
                mask = matched['sku'].str.contains(left_pattern) | matched['sku'].str.contains(right_pattern)
                matched.loc[mask,"final_price"] = matched.loc[mask,"final_price"] + 50

                # # 1028832单独加价
                mask = matched["sku"] == '1028832'
                matched.loc[mask, "final_price"] = matched.loc[mask, "final_price"] + 20

                matched.to_csv('./temp/matched_update.csv', index=False)
                shutil.copy("./temp/matched_update.csv",f"D:/PythonProject/log/matched_update日志/matched_update-{now_time_str}.csv")
                await aprint(f"已生成 matched_update.csv，共 {len(matched)} 条记录", flush=True)
        class ebay_db_op:
            def __init__(self):
                self.db_user = 'root'
                self.db_passwd = '123456'
                self.db_host = '192.168.0.88'
                self.db_name = 'copydate'
                self.db_table = 'ebay_product_variations'
                self.batch_size = 12000

            @retry(
                stop=stop_after_attempt(3),  # 最多重试3次
                wait=wait_exponential(multiplier=1, min=4, max=10)  # 指数退避
            )
            async def select_db(self):
                start_time = datetime.datetime.now()
                print("开始导出数据库数据...", flush=True)
                # 使用 SSCursor 流式读取
                conn = await aiomysql.connect(
                    host=self.db_host,
                    user=self.db_user,
                    password=self.db_passwd,
                    db=self.db_name,
                    port=3306,
                    cursorclass=aiomysql.SSCursor  # 关键：流式游标
                )
                async with conn.cursor() as curs:
                    sql = f"SELECT title, variation, price FROM {self.db_table} WHERE variation NOT LIKE '%无原装鞋盒%' order by scrape_time DESC"
                    await curs.execute(sql)
                    all_data = await curs.fetchall()
                    df = aiopandas.DataFrame(all_data, columns=['title', 'variation', 'price'])

                    mask = df["variation"].str.contains('-')
                    df.loc[mask, 'variation'] = df.loc[mask, 'variation'].str.split('-').str[0]

                    df.to_csv(path_or_buf='./temp/raw.csv', index=False)
                conn.close()
                print(f"\nDB表写完了，耗时: {datetime.datetime.now() - start_time}", flush=True)


        class PostMeta(Model):
            meta_id = fields.BigIntField(primary_key=True)
            post_id = fields.BigIntField()
            meta_key = fields.CharField(255)
            meta_value = fields.TextField()
            class Meta:
                table = "fiw_postmeta"
        class Post(Model):
            id = fields.BigIntField(primary_key=True)
            post_author = fields.BigIntField()
            post_date = fields.DatetimeField()
            post_date_gmt = fields.DatetimeField()
            post_content = fields.TextField()
            post_title = fields.TextField()
            post_excerpt = fields.TextField()
            post_status = fields.CharField(20)
            comment_status = fields.CharField(20)
            ping_status = fields.CharField(20)
            post_password = fields.CharField(255)
            post_name = fields.CharField(200)
            to_ping = fields.TextField()
            pinged = fields.TextField()
            post_modified = fields.DatetimeField()
            post_modified_gmt = fields.DatetimeField()
            post_content_filtered = fields.TextField()
            post_parent = fields.BigIntField()
            guid = fields.CharField(255)
            menu_order = fields.IntField()
            post_type = fields.CharField(20)
            post_mime_type = fields.CharField(200)
            comment_count = fields.BigIntField()

            class Meta:
                table = "fiw_posts"
        class site_db_ops:
            def __init__(self):
                self.sku_id_list = []  # [sku:'',post_id='']
                self.sku_variation_info_list = []  # [{sku:'',post_id='',size:'',variation_id:'',price:''}]
                self.sku_list = []
                self.post_id_list = []
                self.size_list = []
                self.variation_id_list = []
                self.price_list = []
                self.lock = asyncio.Lock()
                self.semaphore_db = asyncio.Semaphore(20)

            async def db_init(self):
                config = {
                    'connections': {
                        'default': {
                            'engine': 'tortoise.backends.mysql',
                            'credentials': {
                                'host': '35.213.179.76',
                                'port': 3306,
                                'user': 'ujykd9ucwlisd',
                                'password': '#Fd%3(]42_5_',
                                'database': 'dbok22gen1qz2c',
                                'minsize': 10,
                                'maxsize': 200,
                                'pool_recycle': 3600,
                                'charset': 'utf8mb4',
                            }
                        }
                    },
                    'apps': {
                        'models': {
                            'models': ['__main__'],
                            'default_connection': 'default',
                        }
                    }
                }

                await Tortoise.init(config=config)

            @retry(
                stop=stop_after_attempt(3),  # 最多重试3次
                wait=wait_exponential(multiplier=1, min=4, max=10)  # 指数退避
            )
            async def search_sku(self):
                if os.path.exists("D:/PythonProject_UV/Fusion/SKU_white_list.csv"):
                    df = aiopandas.read_csv('D:/PythonProject_UV/Fusion/SKU_white_list.csv', encoding='utf-8-sig')
                    sku_white_list = df['sku'].tolist()
                    all_sku = await PostMeta.filter(meta_key='_sku')
                    for sku in all_sku:
                        sku_value = sku.meta_value
                        sku_id = sku.post_id
                        if sku_value != 'HQ8487-300':
                            data = {'sku': sku_value, 'post_id': sku_id}
                            self.sku_id_list.append(data)
                else:
                    all_sku = await PostMeta.filter(meta_key='_sku')
                    for sku in all_sku:
                        sku_value = sku.meta_value
                        sku_id = sku.post_id
                        data = {'sku': sku_value, 'post_id': sku_id}
                        self.sku_id_list.append(data)

            async def limited_search_variation_size_info_handle(self, sku, post_id):
                async with self.semaphore_db:
                    await self.search_variation_size_info_handle(sku, post_id)

            async def limited_search_variation_price_info_handle(self, info):
                async with self.semaphore_db:
                    await self.search_variation_price_info_handle(info)


            @retry(
                stop=stop_after_attempt(3),  # 最多重试3次
                wait=wait_exponential(multiplier=1, min=4, max=10)  # 指数退避
            )
            async def search_variation_size_info_handle(self, sku, post_id):
                all_variation = await Post.filter(post_parent=post_id, post_type='product_variation')
                for i in all_variation:
                    size = i.post_excerpt
                    variation_id = i.id
                    size_value = (re.sub(r'(?i)size:\s*', '', size)).strip()
                    variation_info = {'sku': sku, 'post_id': post_id, 'size': size_value, 'variation_id': variation_id}
                    self.sku_variation_info_list.append(variation_info)
                    await aprint(variation_info, flush=True)

            @retry(
                stop=stop_after_attempt(3),  # 最多重试3次
                wait=wait_exponential(multiplier=1, min=4, max=10)  # 指数退避
            )
            async def search_variation_price_info_handle(self, info):
                if 'variation_id' in info:
                    variation_price_info = await PostMeta.filter(post_id=info['variation_id'], meta_key='_price')
                    for i in variation_price_info:
                        price = i.meta_value
                        info['price'] = price
                        await aprint(info, flush=True)
                        self.sku_variation_info_list.append(info)
                        self.post_id_list.append(info['post_id'])
                        self.sku_list.append(info['sku'])
                        self.price_list.append(info['price'])
                        self.size_list.append(info['size'])
                        self.variation_id_list.append(info['variation_id'])


            async def search_variation_info(self):
                async with asyncio.TaskGroup() as tg:
                    for data in self.sku_id_list:
                        post_id = data['post_id']
                        sku = data['sku']
                        tg.create_task(self.limited_search_variation_size_info_handle(sku, post_id))
                async with asyncio.TaskGroup() as tg:
                    for info in self.sku_variation_info_list:
                        tg.create_task(self.limited_search_variation_price_info_handle(info))

                data = {
                    'post_id': self.post_id_list,
                    'sku': self.sku_list,
                    'variation_id': self.variation_id_list,
                    'size': self.size_list,
                    'price': self.price_list
                }
                df = aiopandas.DataFrame(data)
                df_sorted = df.sort_values('sku')
                df_sorted.to_csv('./temp/sku_variation_info.csv', index=False)
                now_time = datetime.datetime.now()
                now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
                shutil.copy("./temp/sku_variation_info.csv",f"D:/PythonProject/log/sku_variation_info日志/sku_variation_info-{now_time_str}.csv")

            def chunk_list(self, it, size):
                from itertools import islice
                it = iter(it)
                return list(iter(lambda: list(islice(it, size)), []))

            @retry(
                stop=stop_after_attempt(3),  # 最多重试3次
                wait=wait_exponential(multiplier=1, min=4, max=10)  # 指数退避
            )
            async def generate_need_update(self):
                api_df = aiopandas.read_csv('./temp/sku_variation_info.csv', encoding='utf-8-sig')
                # post_id sku var_id size price
                api_df['price'] = api_df['price'].astype(float)
                api_df['sku'] = api_df['sku'].astype(str)

                def extract_eu_number(size_str):
                    size_str = str(size_str)
                    eu_match = re.search(r'EU\s*(\d+(?:\.\d+)?)\s*(1/3|2/3|1/2)', size_str)
                    if eu_match:
                        base_size = float(eu_match.group(1))
                        fraction = eu_match.group(2)
                        if fraction == '1/3':
                            return None
                        if fraction == '2/3':
                            total_size = base_size + 0.5
                            return str(round(total_size, 2))
                        elif fraction == '1/2':
                            total_size = base_size + 0.5
                            return str(round(total_size, 2))
                    eu_match_simple = re.search(r'EU\s*(\d+(?:\.\d+)?)', size_str)
                    if eu_match_simple:
                        return str(eu_match_simple.group(1))
                    return None

                api_df['eu_number'] = api_df['size'].apply(extract_eu_number)
                api_df = api_df.dropna(subset=['eu_number'])

                raw_df = aiopandas.read_csv('./temp/raw.csv', encoding='utf-8-sig')
                raw_df = raw_df[['title', 'variation', 'price']]
                raw_df.columns = ['sku', 'size', 'ebay_price']
                mask = raw_df['size'].str.contains('-', na=False)
                raw_df.loc[mask, 'size'] = raw_df.loc[mask, 'size'].str.split('-').str[0]
                raw_df['ebay_price'] = raw_df['ebay_price'].astype(float)
                raw_df = raw_df.drop_duplicates(subset=['sku', 'size'])

                merged = aiopandas.merge(
                    api_df,
                    raw_df,
                    left_on=['sku', 'eu_number'],
                    right_on=['sku', 'size'],
                    how='left',
                )
                print(f"原始 api_df 行数: {len(api_df)}")
                print(f"合并后 merged 行数: {len(merged)}")
                merged = merged.drop(columns=['size_y'])
                merged = merged.rename(columns={'size_x': 'size'})
                merged = merged.sort_values(by=['sku', 'size'])

                mask = (merged['ebay_price'].isna()) | (merged['ebay_price'] == 0)
                merged.loc[mask, 'calculated_price'] = None
                #ebay价格公式

                #(成本_CNY ÷ 7.2 + 75) ÷ 0.91 - 29.9
                merged.loc[~mask, 'calculated_price'] = ( (merged['ebay_price'] / 7.2 + 75) / 0.91 - 29.9 ).round(2)
                merged['calculated_price'] = merged['calculated_price'].fillna(0)
                merged['price_diff'] = abs(merged['price'] - merged['calculated_price']).round(2)

                def all_price_None(group):
                    return (group['ebay_price'].isna()).all()

                only_sku_df_filtered = merged.groupby('sku').filter(all_price_None)

                sku_result = only_sku_df_filtered[['sku']]
                sku_result = sku_result.drop_duplicates()
                sku_list = sku_result['sku'].tolist()
                if sku_list:
                    left_pattern = r'[（(]'
                    right_pattern = r'[）)]'
                    need_use_sku_list = []
                    if os.path.exists('./temp/exec_day.json'):
                        async with aiofiles.open('./temp/exec_day.json', 'r', encoding='utf-8') as file:
                            data_json = await file.read()
                            data = json.loads(data_json)
                            exec_day = data['七日之期']
                    else:
                        exec_day = 0
                        async with aiofiles.open('./temp/exec_day.json', 'w', encoding='utf-8') as file:
                            data = {"七日之期": exec_day}
                            await file.write(json.dumps(data, ensure_ascii=False))
                    for i in sku_list:
                        if exec_day >= 7:
                            need_use_sku_list.append(i)
                        else:
                            if re.search(left_pattern, i) or re.search(right_pattern, i):
                                continue
                            else:
                                need_use_sku_list.append(i)
                    with open('./temp/dw_sku_list.txt', 'a', encoding='utf-8') as file:
                        file.write('\n'.join(need_use_sku_list))

                    now_time = datetime.datetime.now()
                    now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
                    shutil.copy('./temp/dw_sku_list.txt', f'D:/PythonProject/log/dw_sku_list日志/dw_sku_list-{now_time_str}.txt')

                self.need_update_list = merged.to_dict(orient='records')
                result_df = merged
                if len(result_df) > 0:
                    now_time = datetime.datetime.now()
                    now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
                    mask = (result_df['ebay_price'].isna()) | (result_df['ebay_price'] == 0)
                    result_df.loc[mask, 'calculated_price'] = None
                    result_df.loc[mask, 'calculated_price'] = result_df.loc[mask, 'calculated_price']

                    # 给IH4383-300单独加价
                    result_df["eu_number"] = result_df["eu_number"].astype(float)
                    mask = result_df["sku"] == 'IH4383-300'
                    result_df.loc[mask, "calculated_price"] = result_df.loc[mask, "calculated_price"] + 20
                    result_df["eu_number"] = result_df["eu_number"].astype(str)

                    result_df.to_csv('./temp/need_update.csv', index=False, encoding='utf-8-sig')
                    shutil.copy("./temp/need_update.csv",f"D:/PythonProject/log/need_update日志/need_update-{now_time_str}.csv")
                if len(only_sku_df_filtered) > 0:
                    now_time = datetime.datetime.now()
                    only_sku_df_filtered = only_sku_df_filtered[['post_id', 'sku', 'variation_id', 'size']]
                    if exec_day <7:
                        left_pattern = r'[（(]'
                        right_pattern = r'[）)]'
                        mask = only_sku_df_filtered['sku'].str.contains(left_pattern) | only_sku_df_filtered['sku'].str.contains(right_pattern)
                        only_sku_df_filtered = only_sku_df_filtered[~mask]

                        only_sku_df_filtered.to_csv('./temp/only_in_api.csv', index=False, encoding='utf-8-sig')
                        now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
                        shutil.copy("./temp/only_in_api.csv",f"D:/PythonProject/log/only_in_api日志/only_in_api-{now_time_str}.csv")
                        print(f"已生成 only_in_api.csv，共 {len(only_sku_df_filtered)} 条记录", flush=True)
                    else:
                        exec_day = 0
                        async with aiofiles.open('./temp/exec_day.json', 'w', encoding='utf-8') as file:
                            data = {"七日之期": exec_day}
                            await file.write(json.dumps(data, ensure_ascii=False))
                        only_sku_df_filtered.to_csv('./temp/only_in_api.csv', index=False, encoding='utf-8-sig')
                        now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
                        shutil.copy("./temp/only_in_api.csv",
                                    f"D:/PythonProject/log/only_in_api日志/only_in_api-{now_time_str}.csv")
                        print(f"已生成 only_in_api.csv，共 {len(only_sku_df_filtered)} 条记录", flush=True)


                    _sku_list_ = []
                    async with aiofiles.open('./temp/dw_sku_list.txt', 'r', encoding='utf-8') as file:
                        async for i in file:
                            _sku_list_.append(i.strip())
                    if os.path.exists('./temp/dw_time.json'):
                        async with aiofiles.open('./temp/dw_time.json', 'r', encoding='utf-8') as file:
                            load_json = await file.read()
                            load_dw_time = json.loads(load_json)
                        current_dw_time = len(_sku_list_)
                        now_dw_time = load_dw_time + current_dw_time
                        async with aiofiles.open('./temp/dw_time.json', 'w', encoding='utf-8') as file:
                            await file.write(json.dumps(now_dw_time, ensure_ascii=False))
                    else:
                        current_dw_time = len(_sku_list_)
                        async with aiofiles.open('./temp/dw_time.json', 'w', encoding='utf-8') as file:
                            await file.write(json.dumps(current_dw_time, ensure_ascii=False))
                    chunked_list = self.chunk_list(_sku_list_, 200)
                    print(chunked_list)
                    _sku_list = []
                    _size_list = []
                    _price_list = []
                    for i in chunked_list:
                        xiaoming = api_handle(i)
                        _sku_list, _size_list, _price_list = await xiaoming.request_api(_sku_list, _size_list, _price_list)
                    data = {
                        'sku': _sku_list,
                        'size': _size_list,
                        'price(RMB)': _price_list
                    }
                    df = aiopandas.DataFrame(data)
                    df.to_csv('./temp/query_info.csv', index=False)
                    handler_a = data_handle()
                    await handler_a.handle_query_data()
                    await handler_a.diff_data()
                else:
                    print("没有发现仅存在于 API 的商品记录", flush=True)

            async def limited_need_update_handle(self, row):
                async with self.semaphore_db:
                    await self.need_update_handle(row)

            async def limited_matched_update_handle(self, row):
                async with self.semaphore_db:
                    await self.matched_update_handle(row)

            @retry(
                stop=stop_after_attempt(3),  # 最多重试3次
                wait=wait_exponential(multiplier=1, min=4, max=10)  # 指数退避
            )
            async def need_update_handle(self, row):
                variation_id = row['variation_id']
                calculated_price = row['calculated_price']
                await aprint(f'need_update | var_id:{variation_id} | calculated_price:{calculated_price}')
                await PostMeta.filter(post_id=variation_id, meta_key='_regular_price').update(
                    meta_value=calculated_price)
                await PostMeta.filter(post_id=variation_id, meta_key='_price').update(meta_value=calculated_price)

            @retry(
                stop=stop_after_attempt(3),  # 最多重试3次
                wait=wait_exponential(multiplier=1, min=4, max=10)  # 指数退避
            )
            async def matched_update_handle(self, row):
                variation_id = row['variation_id']
                final_price = row['final_price']
                await aprint(f'matched_update | var_id:{variation_id} | final_price:{final_price}')
                await PostMeta.filter(post_id=variation_id, meta_key='_regular_price').update(meta_value=final_price)
                await PostMeta.filter(post_id=variation_id, meta_key='_price').update(meta_value=final_price)


            async def update_price(self):
                if os.path.exists('./temp/need_update.csv'):
                    need_df = aiopandas.read_csv('./temp/need_update.csv', encoding='utf-8-sig')
                    async with asyncio.TaskGroup() as TG:
                        for index, row in need_df.iterrows():
                            TG.create_task(self.limited_need_update_handle(row))
                    await aprint('need_update执行完毕')

                if os.path.exists('./temp/matched_update.csv'):
                    matched_df = aiopandas.read_csv('./temp/matched_update.csv', encoding='utf-8-sig')
                    async with asyncio.TaskGroup() as tg:
                        for index, row in matched_df.iterrows():
                            tg.create_task(self.limited_matched_update_handle(row))
                    await aprint('matched_update执行完毕')

        async def main():
            xiaoming = site_db_ops()
            xiaogang = ebay_db_op()
            start_time = datetime.datetime.now()
            if os.path.exists('./temp/only_in_api.csv'):
                os.remove('./temp/only_in_api.csv')
            if os.path.exists('./temp/raw.csv'):
                os.remove('./temp/raw.csv')
            if os.path.exists('./temp/need_update.csv'):
                os.remove('./temp/need_update.csv')
            if os.path.exists('./temp/matched_update.csv'):
                os.remove('./temp/matched_update.csv')
            if os.path.exists('./temp/query_info.csv'):
                os.remove('./temp/query_info.csv')
            if os.path.exists('./temp/sku_variation_info.csv'):
                os.remove('./temp/sku_variation_info.csv')
            if os.path.exists('./temp/dw_sku_list.txt'):
                os.remove('./temp/dw_sku_list.txt')
            await xiaoming.db_init()
            await xiaogang.select_db()
            await xiaoming.search_sku()
            await xiaoming.search_variation_info()
            await xiaoming.generate_need_update()
            await xiaoming.update_price()
            await Tortoise.close_connections()
            end_time = datetime.datetime.now()
            exec_time = (end_time-start_time).total_seconds()
            if os.path.exists('./temp/only_in_api.csv'):
                os.remove('./temp/only_in_api.csv')
            if os.path.exists('./temp/raw.csv'):
                os.remove('./temp/raw.csv')
            if os.path.exists('./temp/need_update.csv'):
                os.remove('./temp/need_update.csv')
            if os.path.exists('./temp/matched_update.csv'):
                os.remove('./temp/matched_update.csv')
            if os.path.exists('./temp/query_info.csv'):
                os.remove('./temp/query_info.csv')
            if os.path.exists('./temp/sku_variation_info.csv'):
                os.remove('./temp/sku_variation_info.csv')
            if os.path.exists('./temp/dw_sku_list.txt'):
                os.remove('./temp/dw_sku_list.txt')

            async with aiofiles.open("./temp/exec_day.json", 'r', encoding='utf-8') as f:
                data = json.loads(await f.read())
                exec_day = data['七日之期']
            exec_day += 0.5
            async with aiofiles.open('./temp/exec_day.json', 'w', encoding='utf-8') as f:
                data = {"七日之期":exec_day}
                await f.write(json.dumps(data,ensure_ascii=False))

            for i in range(43200):
                await aprint(f'本次执行花费时间:{exec_time}秒 | 距离下次执行剩余{43200-i}秒 | 距离上次过去{exec_day}天', end='\r', flush=True)
                await asyncio.sleep(1)

        if __name__ == '__main__':
            asyncio.run(main())

    except Exception as e:
        import smtplib
        from email.mime.text import MIMEText
        from email.header import Header
        from email.utils import formataddr
        from email.mime.multipart import MIMEMultipart
        time.sleep(10)
        if os.path.exists('./temp/only_in_api.csv'):
            os.remove('./temp/only_in_api.csv')
        if os.path.exists('./temp/raw.csv'):
            os.remove('./temp/raw.csv')
        if os.path.exists('./temp/need_update.csv'):
            os.remove('./temp/need_update.csv')
        if os.path.exists('./temp/matched_update.csv'):
            os.remove('./temp/matched_update.csv')
        if os.path.exists('./temp/query_info.csv'):
            os.remove('./temp/query_info.csv')
        if os.path.exists('./temp/sku_variation_info.csv'):
            os.remove('./temp/sku_variation_info.csv')
        if os.path.exists('./temp/dw_sku_list.txt'):
            os.remove('./temp/dw_sku_list.txt')
        sender = '17816258635@163.com'
        receiver = '728800637@qq.com'
        auth_code = 'WPtjWi8A8DKYnuYW'
        smtp_host = 'smtp.163.com'

        msg = MIMEMultipart('mixed')
        msg['from'] = formataddr(pair=('脚本讣告者', sender), charset='utf-8')
        msg['to'] = formataddr(pair=(None, receiver), charset='utf-8')
        msg['subject'] = Header('脚本死亡通告', charset='utf-8')
        text = f'脚本死亡，死亡原因：{e}'
        mime_text = MIMEText(text, _subtype='plain', _charset='utf-8')
        msg.attach(mime_text)
        smtp_conn = smtplib.SMTP_SSL(smtp_host, 465)
        smtp_conn.login(user=sender, password=auth_code)
        smtp_conn.sendmail(from_addr=sender, to_addrs=receiver, msg=msg.as_string())
        print('脚本死亡，死亡原因：', e, flush=True)






