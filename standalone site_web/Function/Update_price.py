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
import tenacity
import json
import os
import aiofiles


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

    @tenacity.retry(stop=tenacity.stop_after_attempt(10),
                    wait=tenacity.wait_exponential(multiplier=2, max=60, exp_base=2))
    async def request_api(self, _sku_list, _size_list, _price_list):
        ua = fake_useragent.UserAgent()
        random_ua = ua.random
        processed_payload = {'code': 'sdue23487s8y234yhjHJHh2348hH', 'dwDesignerId': self.sku_list_new}
        start_time = time.time()
        logger.debug(f"正在发送API请求: {json.dumps(processed_payload, ensure_ascii=False)}")
        logger.debug(f"API请求体: {processed_payload}")
        logger.debug(f"URL::: {self.api_url}")
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, headers=self.header, json=processed_payload, timeout=60) as response:
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
        # 强制转换为字符串并去除前后空格
        df['size'] = df['size'].astype(str).str.strip()
        # 检查是否有特殊字符
        if df['size'].str.contains('⅔|⅓', na=False).any():
            print('检测到特殊字符', flush=True)
            # 替换 ⅓
            if df['size'].str.contains('⅓', na=False).any():
                mask = df['size'].str.contains('⅓', na=False)
                df.loc[mask, 'size'] = df.loc[mask, 'size'].str.replace('⅓', '')

            # 替换 ⅔
            if df['size'].str.contains('⅔', na=False).any():
                mask = df['size'].str.contains('⅔', na=False)
                df.loc[mask, 'size'] = df.loc[mask, 'size'].str.replace('⅔', '').astype(float) + 0.5

            # 保存更新后的数据
            now_time = datetime.datetime.now()
            now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
            df.to_csv(f'D:/PythonProject/log/query_info.csv', index=False)
            df.to_csv(f'D:/PythonProject/log/query_info-{now_time_str}.csv', index=False)
            await aprint('写入成功', flush=True)

    async def diff_data(self,dw_price_factor):
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
        # dw价格公式
        # (成本_CNY ÷ 7.2 + 75) ÷ 0.91 - 29.9
        matched.loc[mask, 'final_price'] = ((matched.loc[mask, 'final_price'] / 7.2 + 75) / 0.91 - 29.9).round(2)
        # matched.loc[mask, 'final_price'] = (matched.loc[mask, 'final_price'] * 0.14 / dw_price_factor + 7.5).round(2)
        now_time = datetime.datetime.now()
        now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
        matched = matched[['post_id', 'sku', 'variation_id', 'eu_number', 'final_price']]


        left_pattern = r'[（(]'
        right_pattern = r'[）)]'
        mask = matched['sku'].str.contains(left_pattern) | matched['sku'].str.contains(right_pattern)
        matched.loc[mask, "final_price"] = matched.loc[mask, "final_price"] + 50

        # # 1028832单独加价
        mask = matched["sku"] == '1028832'
        matched.loc[mask, "final_price"] = matched.loc[mask, "final_price"] + 20




        matched.to_csv('./temp/matched_update.csv', index=False)
        matched.to_csv(f'D:/PythonProject/log/matched_update-{now_time_str}.csv', index=False)
        await aprint(f"已生成 matched_update.csv，共 {len(matched)} 条记录", flush=True)


class ebay_db_op:
    def __init__(self):
        self.db_user = 'root'
        self.db_passwd = '123456'
        self.db_host = '192.168.0.88'
        self.db_name = 'copydate'
        self.db_table = 'ebay_product_variations'
        self.batch_size = 12000  # 每次读取5000行

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
            df.loc[mask, 'variation']= df.loc[mask, 'variation'].str.split('-').str[0]

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
        self.semaphore = asyncio.Semaphore(50)

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
                    'models': ['Function.Update_price'],
                    'default_connection': 'default',
                }
            }
        }

        await Tortoise.init(config=config)

    async def search_sku(self,sku_list):
        sku_white_list = []
        if os.path.exists("SKU_white_list.csv"):
            df = aiopandas.read_csv('D:/PythonProject_UV/Fusion/SKU_white_list.csv', encoding='utf-8-sig')
            sku_white_list = df['sku'].tolist()
        all_sku = await PostMeta.filter(meta_key='_sku')
        await aprint(len(all_sku))
        sku_upper_list = []
        for sku in all_sku:
            sku_value = sku.meta_value
            sku_id = sku.post_id
            for sku_input in sku_list:
                sku_input = sku_input.upper()
                sku_upper_list.append(sku_input)
            sku_value = sku_value.upper()
            if (sku_value in sku_upper_list):
                data = {'sku': sku_value, 'post_id': sku_id}
                self.sku_id_list.append(data)
                await aprint("进来了")
        await aprint("sku_id_list:",self.sku_id_list)


    async def limited_search_variation_size_info_handle(self, sku, post_id):
        async with self.semaphore:
            await self.search_variation_size_info_handle(sku, post_id)

    async def limited_search_variation_price_info_handle(self, info):
        async with self.semaphore:
            await self.search_variation_price_info_handle(info)

    async def search_variation_size_info_handle(self, sku, post_id):
        all_variation = await Post.filter(post_parent=post_id, post_type='product_variation')
        for i in all_variation:
            size = i.post_excerpt
            variation_id = i.id
            size_value = (re.sub(r'(?i)size:\s*', '', size)).strip()
            variation_info = {'sku': sku, 'post_id': post_id, 'size': size_value, 'variation_id': variation_id}
            self.sku_variation_info_list.append(variation_info)
            await aprint("variation_info:",variation_info, flush=True)

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

    def chunk_list(self, it, size):
        from itertools import islice
        it = iter(it)
        return list(iter(lambda: list(islice(it, size)), []))

    async def generate_need_update(self,my_price_factor,dw_price_factor):
        api_df = aiopandas.read_csv('./temp/sku_variation_info.csv', encoding='utf-8-sig')
        # post_id sku var_id size price
        api_df['price'] = api_df['price'].astype(float)
        api_df['sku'] = api_df['sku'].astype(str)
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
        merged.loc[mask,'calculated_price'] = merged.loc[mask,'ebay_price']
        # ebay价格公式
        # (成本_CNY ÷ 7.2 + 75) ÷ 0.91 - 29.9
        merged.loc[~mask, 'calculated_price'] = ((merged['ebay_price'] / 7.2 + 75) / 0.91 - 29.9).round(2)
        merged['calculated_price'] = merged['calculated_price'].fillna(0)
        merged['price_diff'] = abs(merged['price'] - merged['calculated_price']).round(2)

        # updated_rows = merged[~np.isclose(merged['price'], merged['calculated_price'], atol=0.01)]
        # merged.loc[np.isclose(merged['calculated_price'], 0.0), 'calculated_price'] = None

        def all_price_None(group):
            return (group['ebay_price'].isna()).all()
        only_sku_df_filtered = merged.groupby('sku').filter(all_price_None)

        sku_result = only_sku_df_filtered[['sku']]
        sku_result = sku_result.drop_duplicates()
        sku_list = sku_result['sku'].tolist()
        await aprint(sku_list)
        if sku_list:
            with open('./temp/dw_sku_list.txt', 'a', encoding='utf-8') as file:
                file.write('\n'.join(sku_list))
            now_time = datetime.datetime.now()
            now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
            shutil.copy('./temp/dw_sku_list.txt', f'D:/PythonProject/log/dw_sku_list-{now_time_str}.txt')

        self.need_update_list = merged.to_dict(orient='records')
        result_df = merged
        if len(result_df) > 0:
            now_time = datetime.datetime.now()
            now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
            mask = (result_df['ebay_price'].isna()) | (result_df['ebay_price'] == 0)
            result_df.loc[mask, 'calculated_price'] = None
            mask2 = result_df['ebay_price'].isna()
            result_df.loc[mask, 'calculated_price'] = result_df.loc[mask, 'calculated_price']

            # 给IH4383-300单独加价
            result_df["eu_number"] = result_df["eu_number"].astype(float)
            mask = result_df["sku"] == 'IH4383-300'
            result_df.loc[mask, "calculated_price"] = result_df.loc[mask, "calculated_price"] + 20
            result_df["eu_number"] = result_df["eu_number"].astype(str)



            result_df.to_csv(f'D:/PythonProject/log/need_update-{now_time_str}.csv', index=False, encoding='utf-8-sig')
            result_df.to_csv('./temp/need_update.csv', index=False, encoding='utf-8-sig')
        if len(only_sku_df_filtered) > 0:
            now_time = datetime.datetime.now()
            now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
            only_sku_df_filtered.to_csv(f'D:/PythonProject/log/only_in_api-{now_time_str}.csv', index=False,
                                        encoding='utf-8-sig')
            only_sku_df_filtered = only_sku_df_filtered[['post_id', 'sku', 'variation_id', 'size']]
            only_sku_df_filtered.to_csv('./temp/only_in_api.csv', index=False, encoding='utf-8-sig')
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
            now_time = datetime.datetime.now()
            now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
            df.to_csv(f'D:/PythonProject/log/query_info-{now_time_str}.csv', index=False)
            handler_a = data_handle()
            await handler_a.handle_query_data()
            await handler_a.diff_data(dw_price_factor)
        else:
            print("没有发现仅存在于 API 的商品记录", flush=True)

    async def limited_need_update_handle(self, row):
        async with self.semaphore:
            await self.need_update_handle(row)

    async def limited_matched_update_handle(self, row):
        async with self.semaphore:
            await self.matched_update_handle(row)

    async def need_update_handle(self, row):
        variation_id = row['variation_id']
        calculated_price = row['calculated_price']
        await aprint(f'need_update | var_id:{variation_id} | calculated_price:{calculated_price}')
        await PostMeta.filter(post_id=variation_id, meta_key='_regular_price').update(meta_value=calculated_price)
        await PostMeta.filter(post_id=variation_id, meta_key='_price').update(meta_value=calculated_price)

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


async def update_main(skus:list,my_price_factor:float,dw_price_factor:float,flag:str):
    xiaoming = site_db_ops()
    xiaogang = ebay_db_op()
    if os.path.exists('./temp/dw_sku_list.txt'):
        os.remove('./temp/dw_sku_list.txt')
    await xiaogang.select_db()
    await xiaoming.db_init()
    await xiaoming.search_sku(skus)
    await xiaoming.search_variation_info()
    await xiaoming.generate_need_update(my_price_factor,dw_price_factor)
    await xiaoming.update_price()
    if os.path.exists('./temp/dw_sku_list.txt'):
        os.remove('./temp/dw_sku_list.txt')
    await Tortoise.close_connections()