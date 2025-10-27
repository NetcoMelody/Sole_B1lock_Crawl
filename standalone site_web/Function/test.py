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
                                            price = 100000
                                        _price_list.append(price)
        await aprint(len(_sku_list))
        await aprint(len(_size_list))
        await aprint(len(_price_list))
        return _sku_list, _size_list, _price_list

class data_handle:
    async def handle_query_data(self):
        if not os.path.exists('query_info.csv'):
            print("query_info.csv 文件不存在，请确保 api_handle.request_api() 已成功执行",flush=True)
            return
        df = aiopandas.read_csv('query_info.csv')
        # 强制转换为字符串并去除前后空格
        df['size'] = df['size'].astype(str).str.strip()
        # 检查是否有特殊字符
        if df['size'].str.contains('⅔|⅓', na=False).any():
            print('检测到特殊字符',flush=True)
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
            await aprint('写入成功',flush=True)

    async def diff_data(self):
        import pandas as pd
        import re

        query_info_df = pd.read_csv('query_info.csv', encoding='utf-8-sig')
        only_in_api_df = pd.read_csv('only_in_api.csv', encoding='utf-8-sig')

        only_in_api_df['sku'] = only_in_api_df['sku'].astype(str).str.strip()
        query_info_df['sku'] = query_info_df['sku'].astype(str).str.strip()

        def extract_eu_number(size_str):
            size_str = str(size_str).strip()
            eu_match = re.search(r'EU\s*([\d\.]+(?:-[\d\.]+)?)', size_str)
            if eu_match:
                # 返回 'EU' 后面匹配到的整个数字或范围部分
                return eu_match.group(1)
            range_or_single_match = re.search(r'([\d\.]+(?:-[\d\.]+)?)', size_str)
            if range_or_single_match:
                # 返回匹配到的第一个数字或范围
                return range_or_single_match.group(1)
            return None
        only_in_api_df['eu_number'] = only_in_api_df['size'].apply(extract_eu_number)
        query_info_df['eu_number'] = query_info_df['size'].apply(extract_eu_number)
        matched = pd.merge(
            only_in_api_df,
            query_info_df[['sku', 'eu_number', 'price(RMB)']],
            on=['sku', 'eu_number'],
            how='left'
        )
        matched['price(RMB)'] = pd.to_numeric(matched['price(RMB)'], errors='coerce')
        matched['price(RMB)'] = matched['price(RMB)'].fillna(100000)
        matched['price(RMB)'] = matched['price(RMB)'].astype('Int64')
        matched.rename(columns={'price(RMB)':'final_price'},inplace=True)
        mask = matched['final_price'] != 100000
        matched['final_price'] = pd.to_numeric(matched['final_price'], errors='coerce').astype('float64')
        matched.loc[mask, 'final_price'] = (matched.loc[mask, 'final_price'] * 0.14 / 0.85 +7.5).round(2)
        now_time = datetime.datetime.now()
        now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
        matched = matched[['post_id','sku','variation_id','size','eu_number','final_price']]
        matched.to_csv('matched_update.csv', index=False, encoding='utf-8-sig')
        matched.to_csv(f'D:/PythonProject/log/matched_update-{now_time_str}.csv',index=False, encoding='utf-8-sig')
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
            df.to_csv(path_or_buf='raw.csv', index=False)
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
        self.sku_id_list = [] #[sku:'',post_id='']
        self.sku_variation_info_list = [] #[{sku:'',post_id='',size:'',variation_id:'',price:''}]

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
                    'models': ['__main__'],
                    'default_connection': 'default',
                }
            }
        }

        await Tortoise.init(config=config)

    async def search_sku(self):
        df = aiopandas.read_csv('D:/PythonProject_UV/Fusion/SKU_white_list.csv', encoding='utf-8-sig')
        sku_white_list = df['sku'].tolist()
        all_sku = await PostMeta.filter(meta_key='_sku')
        for sku in all_sku:
            sku_value = sku.meta_value
            sku_id = sku.post_id
            if (sku_value not in sku_white_list) and (sku != 'HQ8487-300'):
                data = {'sku':sku_value,'post_id':sku_id}
                self.sku_id_list.append(data)

    async def limited_search_variation_size_info_handle(self, sku, post_id):
        async with self.semaphore:
            await self.search_variation_size_info_handle(sku, post_id)

    async def limited_search_variation_price_info_handle(self, info):
        async with self.semaphore:
            await self.search_variation_price_info_handle(info)

    async def search_variation_size_info_handle(self,sku,post_id):
        all_variation = await Post.filter(post_parent=post_id, post_type='product_variation')
        for i in all_variation:
            size = i.post_excerpt
            variation_id = i.id
            size_value = (re.sub(r'(?i)size:\s*', '', size)).strip()
            variation_info = {'sku': sku, 'post_id': post_id, 'size': size_value, 'variation_id': variation_id}
            self.sku_variation_info_list.append(variation_info)
            await aprint(variation_info,flush=True)

    async def search_variation_price_info_handle(self,info):
        if 'variation_id' in info:
            variation_price_info = await PostMeta.filter(post_id=info['variation_id'], meta_key='_price')
            for i in variation_price_info:
                price = i.meta_value
                info['price'] = price
                await aprint(info,flush=True)
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
        df_sorted.to_csv('sku_variation_info.csv', index=False)

    def chunk_list(self, it, size):
        from itertools import islice
        it = iter(it)
        return list(iter(lambda: list(islice(it, size)), []))

    async def generate_need_update(self):
        api_df = aiopandas.read_csv('sku_variation_info.csv', encoding='utf-8-sig')
        # post_id sku var_id size price
        api_df['price'] = api_df['price'].astype(float)
        def extract_eu_number(size_str):
            size_str = str(size_str).strip()
            eu_match = re.search(r'EU\s*([\d\.]+(?:-[\d\.]+)?)', size_str)
            if eu_match:
                return eu_match.group(1)
            range_or_single_match = re.search(r'([\d\.]+(?:-[\d\.]+)?)', size_str)
            if range_or_single_match:
                return range_or_single_match.group(1)
            return None
        api_df['eu_number'] = api_df['size'].apply(extract_eu_number)
        api_df = api_df.dropna(subset=['eu_number'])
        raw_df = aiopandas.read_csv('raw.csv', encoding='utf-8-sig')
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

        merged = merged.drop(columns=['eu_number', 'size_y'])
        merged = merged.rename(columns={'size_x': 'size'})
        merged = merged.sort_values(by=['sku', 'size'])

        merged['calculated_price'] = (merged['ebay_price'] * 0.14 / 0.85).round(2)
        merged['calculated_price'] = merged['calculated_price'].fillna(0)
        merged['price_diff'] = abs(merged['price'] - merged['calculated_price']).round(2)

        # updated_rows = merged[~np.isclose(merged['price'], merged['calculated_price'], atol=0.01)]
        merged.loc[np.isclose(merged['calculated_price'], 0.0), 'calculated_price'] = 100000

        def all_price_100000(group):
            return (group['calculated_price'] == 100000).all()
        only_sku_df_filtered = merged.groupby('sku').filter(all_price_100000)
        sku_result = only_sku_df_filtered[['sku']]
        sku_result = sku_result.drop_duplicates()
        sku_list = sku_result['sku'].tolist()
        for i in sku_list:
            with open('dw_sku_list.txt', 'a', encoding='utf-8-sig') as file:
                file.write(i + '\n')
        now_time = datetime.datetime.now()
        now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
        shutil.copy('dw_sku_list.txt', f'D:/PythonProject/log/dw_sku_list-{now_time_str}.txt')

        self.need_update_list = merged.to_dict(orient='records')
        result_df = merged.dropna(subset=['calculated_price'])
        if len(result_df) > 0:
            now_time = datetime.datetime.now()
            now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
            result_df = result_df[result_df['price_diff'] != 0]
            result_df = result_df[result_df['ebay_price'].notna()]
            mask = result_df['calculated_price'] != 100000
            result_df.loc[mask, 'calculated_price'] = result_df.loc[mask, 'calculated_price'] + 7.5
            # result_df = result_df[['post_id','sku','variation_id','size','calculated_price']]
            result_df.to_csv(f'D:/PythonProject/log/need_update-{now_time_str}.csv', index=False, encoding='utf-8-sig')
            result_df.to_csv('need_update.csv', index=False, encoding='utf-8-sig')

        if len(only_sku_df_filtered)>0:
            now_time = datetime.datetime.now()
            now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
            only_sku_df_filtered.to_csv(f'D:/PythonProject/log/only_in_api-{now_time_str}.csv', index=False,
                                  encoding='utf-8-sig')
            only_sku_df_filtered.to_csv('only_in_api.csv', index=False, encoding='utf-8-sig')
            print(f"已生成 only_in_api.csv，共 {len(only_sku_df_filtered)} 条记录", flush=True)

            _sku_list_ = []
            async with aiofiles.open('dw_sku_list.txt', 'r', encoding='utf-8') as file:
                async for i in file:
                    _sku_list_.append(i.strip())
            if os.path.exists('dw_time.json'):
                async with aiofiles.open('dw_time.json', 'r', encoding='utf-8') as file:
                    load_json = await file.read()
                    load_dw_time = json.loads(load_json)
                current_dw_time = len(_sku_list_)
                now_dw_time = load_dw_time+current_dw_time
                async with aiofiles.open('dw_time.json', 'w', encoding='utf-8') as file:
                    await file.write(json.dumps(now_dw_time, ensure_ascii=False))
            else:
                current_dw_time = len(_sku_list_)
                async with aiofiles.open('dw_time.json', 'w', encoding='utf-8') as file:
                    await file.write(json.dumps(current_dw_time, ensure_ascii=False))
            chunked_list = self.chunk_list(_sku_list_, 200)
            print(chunked_list)
            _sku_list = []
            _size_list = []
            _price_list = []
            for i in chunked_list:
                xiaoming = api_handle(i)
                _sku_list, _size_list, _price_list = await xiaoming.request_api(_sku_list, _size_list, _price_list)
            for i in _sku_list:
                with open('sku_list.txt', 'a', encoding='utf-8') as file:
                    file.write(i + '\n')
            for i in _size_list:
                with open('size_list.txt', 'a', encoding='utf-8') as file:
                    file.write(i + '\n')
            for i in _price_list:
                with open('price_list.txt', 'a', encoding='utf-8') as file:
                    file.write(str(i) + '\n')
            await aprint(len(_sku_list))
            await aprint(len(_size_list))
            await aprint(len(_price_list))
            data = {
                'sku': _sku_list,
                'size': _size_list,
                'price(RMB)': _price_list
            }
            df = aiopandas.DataFrame(data)
            df.to_csv('query_info.csv', index=False)
            handler_a = data_handle()
            await handler_a.handle_query_data()
            await handler_a.diff_data()
        else:
            print("没有发现仅存在于 API 的商品记录", flush=True)
    async def limited_need_update_handle(self, row):
        async with self.semaphore:
            await self.need_update_handle(row)
    async def limited_matched_update_handle(self, row):
        async with self.semaphore:
            await self.matched_update_handle(row)

    async def need_update_handle(self,row):
        variation_id = row['variation_id']
        calculated_price = row['calculated_price']
        await aprint(f'need_update | var_id:{variation_id} | calculated_price:{calculated_price}')
        await PostMeta.filter(post_id=variation_id, meta_key='_regular_price').update(meta_value=calculated_price)

    async def matched_update_handle(self,row):
        variation_id = row['variation_id']
        final_price = row['final_price']
        await aprint(f'matched_update | var_id:{variation_id} | final_price:{final_price}')
        await PostMeta.filter(post_id=variation_id, meta_key='_regular_price').update(meta_value=final_price)

    async def update_price(self):
        if os.path.exists('need_update.csv'):
            need_df = aiopandas.read_csv('need_update.csv',encoding='utf-8-sig')
            async with asyncio.TaskGroup() as TG:
                for index,row in need_df.iterrows():
                    TG.create_task(self.limited_need_update_handle(row))
            await aprint('need_update执行完毕')

        if os.path.exists('matched_update.csv'):
            matched_df = aiopandas.read_csv('matched_update.csv',encoding='utf-8-sig')
            async with asyncio.TaskGroup() as tg:
                for index, row in matched_df.iterrows():
                    tg.create_task(self.limited_matched_update_handle(row))
            await aprint('matched_update执行完毕')

async def main():
    xiaoming = site_db_ops()
    xiaogang = ebay_db_op()
    start_time = datetime.datetime.now()
    if os.path.exists('only_in_api.csv'):
        os.remove('only_in_api.csv')
    if os.path.exists('raw.csv'):
        os.remove('raw.csv')
    if os.path.exists('need_update.csv'):
        os.remove('need_update.csv')
    if os.path.exists('matched_update.csv'):
        os.remove('matched_update.csv')
    if os.path.exists('query_info.csv'):
        os.remove('query_info.csv')
    if os.path.exists('sku_variation_info.csv'):
        os.remove('sku_variation_info.csv')
    if os.path.exists('dw_sku_list.txt'):
        os.remove('dw_sku_list.txt')
    await xiaogang.select_db()
    await xiaoming.db_init()
    await xiaoming.search_sku()
    await xiaoming.search_variation_info()
    await xiaoming.generate_need_update()
    await xiaoming.update_price()
    end_time = datetime.datetime.now()
    exec_time = (end_time-start_time).total_seconds()
    if os.path.exists('only_in_api.csv'):
        os.remove('only_in_api.csv')
    if os.path.exists('raw.csv'):
        os.remove('raw.csv')
    if os.path.exists('need_update.csv'):
        os.remove('need_update.csv')
    if os.path.exists('matched_update.csv'):
        os.remove('matched_update.csv')
    if os.path.exists('query_info.csv'):
        os.remove('query_info.csv')
    if os.path.exists('sku_variation_info.csv'):
        os.remove('sku_variation_info.csv')
    if os.path.exists('dw_sku_list.txt'):
        os.remove('dw_sku_list.txt')
    await Tortoise.close_connections()
    for i in range(36000):
        await aprint(f'本次执行花费时间:{exec_time}秒,距离下次执行剩余{36000-i}秒', end='\r', flush=True)
        await asyncio.sleep(1)