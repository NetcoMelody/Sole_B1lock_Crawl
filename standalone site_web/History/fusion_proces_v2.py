import aiomysql
from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import datetime
import time
import json
import logging as logger
from asyncio import TaskGroup
import aiohttp
from aioconsole import aprint,ainput
import fake_useragent
import pandas 
import asyncio
import csv
import os
import tenacity
import random
import aiocsv
import aiofiles
import shutil

SEMAPHORE_LIMIT = 100
semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)


class db_op:
    def __init__(self):
        self.db_user = 'root'
        self.db_passwd = '123456'
        self.db_host = '192.168.0.88'
        self.db_name = 'copydate'
        self.db_table = 'ebay_product_variations'
        self.batch_size = 12000 # 每次读取5000行

    async def select_db(self):
        start_time = datetime.datetime.now()
        print("开始导出数据...", flush=True)

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
            sql = f"SELECT title, variation, price FROM {self.db_table}"
            await curs.execute(sql)

            # 准备 CSV 文件
            now_time_str = datetime.datetime.now().strftime("%Y年%m月%d日-%H时%M分")
            filename = f'./raw.csv'

            async with aiofiles.open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = aiocsv.AsyncWriter(f)
                await writer.writerow(['title', 'variation', 'price'])  # 写表头

                rows_read = 0
                while True:
                    batch = await curs.fetchmany(self.batch_size)
                    if not batch:
                        break
                    # 边读边处理：提取 size 并写入文件
                    for row in batch:
                        title, variation, price = row
                        size = variation.split('-')[0] if '-' in variation else variation
                    await writer.writerow([title, size, price])

                    rows_read += len(batch)
                    await aprint(f"已处理 {rows_read} 行...", end='\r', flush=True)

        conn.close()
        print(f"\nDB表写完了，共 {rows_read} 行，耗时: {datetime.datetime.now() - start_time}", flush=True)



class api_ops:
    def __init__(self):
        UA = fake_useragent.UserAgent()
        random_UA = UA.random

        self.header = {
            'User-Agent': UA.random,
            'X-API-KEY': "65597d5ed20c860d77edcdb11da81411",
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        self.get_all_products_api = 'https://soleb1ock.com/wp-json/product-api/v1/products' #获取所有产品 Get
        self.use_id_get_products_api = 'https://soleb1ock.com/wp-json/product-api/v1/product/{id}' #通过ID获取产品 Get
        self.single_update_size_price_api = 'https://soleb1ock.com/wp-json/product-api/v1/product/sku/{sku}/sizes/update' #高性能更新单个产品的多个尺码价格 Post
        self.use_sku_get_size_price_api = 'https://soleb1ock.com/wp-json/product-api/v1/product/sku/{sku}/variations' #通过SKU获取产品尺码和价格  Get
        self.record_txt = ''
        self.sizes = []

    async def update_handle(self, session, url_com, payload, sku):
        async with session.post(url_com, headers=self.header, json=payload, timeout=60) as response:
            print(f"Status for {sku}: {response.status}", flush=True)
            self.record_txt = sku

    async def use_api_update_price(self):
        if os.path.exists('need_update.csv'):
            with open('need_update.csv', mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                sizes = []
                current_sku = None
                async with aiohttp.ClientSession() as session:
                    async with TaskGroup() as TG:
                        for value in reader:
                            sku = value['货号']
                            size = value['尺码']
                            price = value['价格']
                            if current_sku is None:
                                current_sku = sku
                            if sku != current_sku:
                                # 提交上一个 SKU 的数据
                                if sizes:
                                    payload = {'sizes': sizes}
                                    url_com = self.single_update_size_price_api.replace('{sku}', current_sku)
                                    TG.create_task(self.update_handle(session, url_com, payload, current_sku))
                                    await asyncio.sleep(random.uniform(0.5, 1.5))
                                # 重置
                                current_sku = sku
                                sizes = []
                            # 收集当前 SKU 的数据
                            per_size_info = {
                                'size_attribute': size,
                                'price': price,
                                'regular_price': price,
                                'sale_price': price
                            }
                            sizes.append(per_size_info)
                        # 提交最后一个 SKU 的数据
                        if current_sku and sizes:
                            payload = {'sizes': sizes}
                            url_com = self.single_update_size_price_api.replace('{sku}', current_sku)
                            TG.create_task(self.update_handle(session, url_com, payload, current_sku))
                            await asyncio.sleep(random.uniform(0.5, 1.5))

        if os.path.exists('matched_update.csv'):
            with open('matched_update.csv', mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                sizes = []
                current_sku = None
                async with aiohttp.ClientSession() as session:
                    async with TaskGroup() as TG:
                        for value in reader:
                            sku = value['货号']
                            size = value['尺码']
                            price = value['价格']

                            if current_sku is None:
                                current_sku = sku

                            if sku != current_sku:
                                # 提交上一个 SKU 的数据
                                if sizes:
                                    payload = {'sizes': sizes}
                                    url_com = self.single_update_size_price_api.replace('{sku}', current_sku)
                                    TG.create_task(self.update_handle(session, url_com, payload, current_sku))
                                    await asyncio.sleep(random.uniform(0.5, 1.5))
                                # 重置
                                current_sku = sku
                                sizes = []
                            # 收集当前 SKU 的数据
                            per_size_info = {
                                'size_attribute': size,
                                'price': price,
                                'regular_price': price,
                                'sale_price': price
                            }
                            sizes.append(per_size_info)
                        # 提交最后一个 SKU 的数据
                        if current_sku and sizes:
                            payload = {'sizes': sizes}
                            url_com = self.single_update_size_price_api.replace('{sku}', current_sku)
                            TG.create_task(self.update_handle(session, url_com, payload, current_sku))
                            await asyncio.sleep(random.uniform(0.5, 1.5))

    async def _task_handle(self, task, sku_list, eu_size_list, price_list):
        json_data = await task
        if 'variations' in json_data:
            var_content = json_data['variations']
            for i in var_content:
                sku = i['sku']
                size = i['size']
                price = i['price']
                sku_list.append(sku)
                eu_size_list.append(size)
                price_list.append(price)
                data = {
                    'sku': sku_list,
                    'api_size': eu_size_list,
                    'api_price': price_list
                }
                await aprint(data, flush=True)
                df = pandas.DataFrame(data)
                df = df.sort_values(by='sku')
                now_time = datetime.datetime.now()
                now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
                df.to_csv(f'D:/PythonProject/log/get_api_data-{now_time_str}.csv', index=False)
                df.to_csv('get_api_data.csv', index=False)

    async def _use_sku_get_size_price_handle(self, sku, session, url_com):
        async with session.get(url_com, headers=self.header, timeout=60) as response:
            response.raise_for_status()
            json_data = await response.json()
            await aprint(json_data, flush=True)
            return json_data

    async def use_sku_get_size_price(self):
        sku_list = []
        price_list = []
        eu_size_list = []
        tasks = []
        async with aiohttp.ClientSession() as session:
            with open('sku.txt', mode='r', encoding='utf-8') as file:
                async with asyncio.TaskGroup() as TG:
                    for sku in file:
                        url_com = self.use_sku_get_size_price_api.replace('{sku}', sku)
                        tg = TG.create_task(self._use_sku_get_size_price_handle(sku, session, url_com))
                        tasks.append(tg)
                        await asyncio.sleep(random.uniform(0.3, 0.5))

        async with asyncio.TaskGroup() as TG:
            for task in tasks:
                TG.create_task(self._task_handle(task, sku_list, eu_size_list, price_list))
            await aprint('get_api_data.csv文件写入完毕', flush=True)

    async def get_all_products(self):
        async with aiohttp.ClientSession() as session:
            sku_list = []
            async with session.get(self.get_all_products_api,headers=self.header,timeout=30) as response:
                text_list = await response.json()
                for text in text_list:
                    sku_text = text['sku']
                    if sku_text not in sku_list and sku_text :
                        sku_list.append(sku_text)
                        sku_text_txt = sku_text + '\n'
                        with open('sku.txt', mode='a', encoding='utf-8') as file:
                            file.write(sku_text_txt)
                await aprint ('sku.txt文件生成完毕',flush=True)


    def chunk_list(self,it, size):
        from itertools import islice
        it = iter(it)
        return list(iter(lambda: list(islice(it, size)), []))

    async def generate_need_update_price(self):
        import pandas as pd
        import numpy as np
        import re

        # 读取 API 数据
        api_df = pd.read_csv('get_api_data.csv', encoding='utf-8')
        api_df = api_df[['sku', 'api_size', 'api_price']]
        api_df.columns = ['sku', 'size', 'api_price']
        api_df['api_price'] = api_df['api_price'].astype(float)
        api_df = api_df.drop_duplicates(subset=['sku', 'size'])

        #提取EU编号用于匹配原始数据
        def extract_eu_number(size_str):
            match = re.search(r'EU\s*(\d+\.?\d*)', str(size_str))
            if match:
                return match.group(1)
            return None

        api_df['eu_number'] = api_df['size'].apply(extract_eu_number)
        api_df = api_df.dropna(subset=['eu_number'])  # 去掉无法提取 EU 编号的行

        #读取原始数据
        raw_df = pd.read_csv('raw.csv', encoding='utf-8')
        raw_df = raw_df[['title', 'variation', 'price']]
        raw_df.columns = ['sku', 'size', 'price']
        raw_df['price'] = raw_df['price'].astype(float)
        raw_df = raw_df.drop_duplicates(subset=['sku', 'size'])

        #合并逻辑
        merged = pd.merge(
            api_df,
            raw_df,
            left_on=['sku', 'eu_number'],
            right_on=['sku', 'size'],
            how='left'
        )

        # 删除临时字段，保留原始 size 字段
        merged = merged.drop(columns=['eu_number', 'size_y'])
        merged = merged.rename(columns={'size_x': 'size'})

        merged = merged.sort_values(by=['sku', 'size'])

        # 计算期望价格（公式：价格 × 0.14 / 0.8）
        merged['calculated_price'] = (merged['price'] * 0.14 / 0.88).round(2)

        # 处理缺失值 & 计算差异
        merged['api_price'] = merged['api_price'].fillna(0)
        merged['price_diff'] = abs(merged['api_price'] - merged['calculated_price']).round(2)

        # 筛选需要更新的行（允许误差）
        updated_rows = merged[~np.isclose(merged['api_price'], merged['calculated_price'], atol=0.01)]

        # ████████ 新增部分：找出只存在于 API，不在 raw 中的记录 ████████
        only_in_api = merged[merged['price'].isna()]
        only_in_api_list = only_in_api[['sku', 'size']].to_dict(orient='records')

        # 构造输出 DataFrame
        result_df = updated_rows[['sku', 'size', 'calculated_price']]
        result_df.columns = ['货号', '尺码', '价格']

        # 如果 calculated_price == 0，则设置为 100000（默认值）
        result_df.loc[np.isclose(result_df['价格'], 0.0), '价格'] = 100000

        # █████████ 将结果存入类属性中 █████████
        self.need_update_list = result_df.to_dict(orient='records')  # 存入类属性
        self.only_in_api_list = only_in_api_list  # 存入类属性

        result_df = result_df.dropna(subset=['价格'])

        if len(result_df)>0:
            # 写入 CSV 文件（使用 utf-8-sig 避免 Excel 打开乱码）
            now_time = datetime.datetime.now()
            now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
            result_df.to_csv(f'D:/PythonProject/log/need_update-{now_time_str}.csv', index=False,encoding='utf-8-sig')
            result_df.to_csv('need_update.csv', index=False, encoding='utf-8-sig')

        # █████████ 新增：将 only_in_api_list 写入 CSV 文件 █████████
        if self.only_in_api_list:
            only_in_api_df = pd.DataFrame(self.only_in_api_list)

            now_time = datetime.datetime.now()
            now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
            only_in_api_df.to_csv(f'D:/PythonProject/log/only_in_api-{now_time_str}.csv', index=False, encoding='utf-8-sig')
            only_in_api_df.to_csv('only_in_api.csv', index=False,encoding='utf-8-sig')
            print(f"已生成 only_in_api.csv，共 {len(self.only_in_api_list)} 条记录",flush=True)
            only_api_data = self.only_in_api_list
            _sku_list=[]
            for i in only_api_data:
                _sku_list.append(i['sku'])
            chunked_list = self.chunk_list(_sku_list, 200)
            for i in chunked_list:
                query_sku_list_str = str(i).replace('"', '').replace("'", '').replace(']', '').replace('[', '').strip()
                xiaoming = api_handle(query_sku_list_str,)
                await xiaoming.request_api()
                await asyncio.sleep(random.uniform(0.5, 2))
            data = {
                'sku': xiaoming._sku_list,
                'size': xiaoming._size_list,
                'price(RMB)': xiaoming._price_list
            }
            df = pandas.DataFrame(data)
            df.to_csv('query_info.csv', index=False)
            handler_a = data_handle()
            await handler_a.handle_query_data()
            await handler_a.diff_data()
        else:
            print("没有发现仅存在于 API 的商品记录",flush=True)


class api_handle:
    def __init__(self,query_sku):
        ua = fake_useragent.UserAgent()
        random_ua = ua.random

        self.api_url = 'http://dewu.ccrotate.com/dewu.php/queryspulist'
        self.header = {
            "Content-Type": "application/json",
            "User-Agent": random_ua,
            # Accept 字段告知服务器客户端可接受的内容类型
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # Accept-Language 表示客户端偏好的语言
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            # Accept-Encoding 指定可接受的内容编码方式（如压缩）
            'Accept-Encoding': 'gzip, deflate',
            # Connection 通常设置为 keep-alive 以保持连接
            'Connection': 'keep-alive',
            # Upgrade-Insecure-Requests 告知服务器客户端希望将不安全的HTTP请求升级为HTTPS
            'Upgrade-Insecure-Requests': '1',
            # Sec-Fetch-* 系列头部是现代浏览器的安全特性，模拟它们能增加请求的真实性
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
        }
        count_need = query_sku.count(',')
        self.sku_list = query_sku.split(',',count_need)
        self.sku_list_new = []
        for i in self.sku_list:
            items = i.strip()
            self.sku_list_new.append(items)
        self._sku_list = []
        self._size_list = []
        self._price_list = []

    @tenacity.retry(stop=tenacity.stop_after_attempt(10), wait=tenacity.wait_exponential(multiplier=2, max=60, exp_base=2))
    async def request_api(self):
        ua = fake_useragent.UserAgent()
        random_ua = ua.random
        processed_payload = {'code': 'sdue23487s8y234yhjHJHh2348hH', 'dwDesignerId': self.sku_list_new}
        start_time = time.time()
        logger.debug(f"正在发送API请求: {json.dumps(processed_payload, ensure_ascii=False)}")
        logger.debug(f"API请求体: {processed_payload}")
        logger.debug(f"URL::: {self.api_url}")
        # 关键修改：使用processed_payload而非payload
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, headers=self.header, json=processed_payload, timeout=60) as response:
                json_text = await response.text()
                json_dict = json.loads(json_text)
                json_dict_data = json_dict['data']
                spu_list = json_dict_data['spuList']
                for i in spu_list:
                    skulist = i['skuList']
                    for size_attr in skulist:
                        sku = i['dwDesignerId']
                        self._sku_list.append(sku)
                        size_attrs = size_attr['saleAttr']
                        for s in size_attrs:
                            if s['cnName'] == '尺码':
                                self._size_list.append(s['enValue'])
                        price = size_attr['minBidPrice']
                        if price != 0:
                            price = int(str(price)[:-2])
                        else:
                            price = 100000
                        self._price_list.append(price)


class data_handle:
    async def handle_query_data(self):
        import pandas as pd
        if not os.path.exists('query_info.csv'):
            print("❌ query_info.csv 文件不存在，请确保 api_handle.request_api() 已成功执行",flush=True)
            return

        df = pd.read_csv('query_info.csv')

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
            df.to_csv(f'D:/PythonProject/log/query_info-{now_time_str}.csv', index=False)
            await aprint('写入成功',flush=True)

    async def diff_data(self):
        import pandas as pd
        import re

        # 读取两个 CSV 文件
        query_info_df = pd.read_csv('query_info.csv', encoding='utf-8')
        only_in_api_df = pd.read_csv('only_in_api.csv', encoding='utf-8')

        # 统一清洗 sku 字段
        only_in_api_df['sku'] = only_in_api_df['sku'].astype(str).str.strip()
        query_info_df['sku'] = query_info_df['sku'].astype(str).str.strip()

        # 提取 EU 编号函数
        def extract_eu_number(size_str):
            size_str = str(size_str)
            match = re.search(r'EU\s*(\d+\.?\d*)', size_str)
            if match:
                return match.group(1)
            else:
                clean = re.sub(r'[^\d.]', '', size_str)
                return clean if clean else None

        # 提取 EU 编号
        only_in_api_df['eu_number'] = only_in_api_df['size'].apply(extract_eu_number)
        query_info_df['eu_number'] = query_info_df['size'].apply(extract_eu_number)

        # 统一转为 float 并四舍五入
        only_in_api_df['eu_number'] = only_in_api_df['eu_number'].astype(float).round(2).astype(str)
        query_info_df['eu_number'] = query_info_df['eu_number'].astype(float).round(2).astype(str)

        # 合并两个表
        matched = pd.merge(
            only_in_api_df[['sku', 'size', 'eu_number']],
            query_info_df[['sku', 'eu_number', 'price(RMB)']],
            on=['sku', 'eu_number'],
            how='inner'  # 改为 inner 可查看两边都有的
        )

        matched['price(RMB)'] = matched['price(RMB)'].fillna(100000).astype(int)

        matched = matched.rename(columns={'sku': '货号', 'size': '尺码', 'price(RMB)': '价格'})

        matched = matched[['货号', '尺码', '价格']]

        matched['价格'] = matched['价格'].astype(float)
        mask = matched['价格'] != 100000
        matched.loc[mask, '价格'] = (matched.loc[mask, '价格'] * 0.14 / 0.88).round(2)

        now_time = datetime.datetime.now()
        now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")

        matched.to_csv('matched_update.csv', index=False, encoding='utf-8-sig')

        await aprint(f"已生成 matched_update.csv，共 {len(matched)} 条记录",flush=True)

def clear_input_buffer():
    import msvcrt
    while msvcrt.kbhit():
        msvcrt.getch()
async def update_price_main(skus:str):
    db_use = db_op()
    api_1 = api_ops()
    skus_list = skus.split(",")
    await aprint (skus_list)
    await aprint (type(skus_list))
    for sku in skus_list:
        with open('sku.txt',mode='a',encoding='utf-8') as file:
            file.write(sku+'\n')
    start_time = datetime.datetime.now()
    await db_use.select_db()
    await api_1.use_sku_get_size_price()
    await api_1.generate_need_update_price()
    await api_1.use_api_update_price()
    os.remove('raw.csv')
    os.remove('sku.txt')
    os.remove('get_api_data.csv')
    if os.path.exists('only_in_api.csv'):
        os.remove('only_in_api.csv')
    else:
        await aprint("未找到 only_in_api.csv 文件",flush=True)
    if os.path.exists('query_info.csv'):
        os.remove('query_info.csv')
    else:
        await aprint("未找到 query_info.csv 文件",flush=True)
    if os.path.exists('matched_update.csv'):
        os.remove('matched_update.csv')
    else:
        await aprint("未找到 matched_update.csv 文件",flush=True)
    if os.path.exists('need_update.csv'):
        os.remove('need_update.csv')
    else:
        await aprint("未找到 need_update.csv 文件",flush=True)
    now_time = datetime.datetime.now()
    now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
    end_time = datetime.datetime.now()
    exec_time = (end_time - start_time).total_seconds()/60
    exec_time = round(exec_time)
    await aprint (f'程序执行完成>>{now_time_str} | 本次执行花费时间>>{exec_time}分钟',flush=True)



class order_out:
    def __init__(self):
        ua = fake_useragent.UserAgent()
        ua_random = ua.random
        self.get_all_order = 'https://soleb1ock.com/wp-json/product-api/v1/all-orders'  # 获取所有订单，不分页
        self.specify_get_order = '	https://soleb1ock.com/wp-json/product-api/v1/order/{order_id}'  # 指定获取订单
        self.headers = {
            "User-Agent": ua_random,
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            'X-API-KEY': '65597d5ed20c860d77edcdb11da81411'
        }
        self.dates = []
        self.order_numbers = []
        self.sizes = []
        self.skus = []
        self.quantitys = []
        self.styles = []
        self.sale_prices = []
        self.other_fees = []
        self.discounts_totals = []
        self.actual_incomes = []
        self.shipping_totals = []
        self.paypal_fees = []
        self.final_payouts = []
        self.order_totals = []
        self.order_status = []
        self.discounts_fee = []
        self.paypal_fee_total = 0
        self.paypal_fee_total_list = []
        self.n = 0
        self.final_payout_total = 0
        self.final_payout_total_list = []

    async def get_all_order_info(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.get_all_order, headers=self.headers) as response:
                json_data = await response.json()
                orders_data = json_data['orders']
                total_orders = json_data['total_orders']
                for i in orders_data:
                    order_id = i['order_id']
                    order_date = i['order_date']
                    order_status = i['status']
                    shipping_total = i['shipping_total']
                    discount_total = i['discount_total']
                    order_total = i['order_total']
                    items = i['items']
                    order_items_len = len(items)

                    for k in items:
                        order_number = str(k['order_number'])
                        sku = k['sku']
                        quantity = k['quantity']  # 购买数目
                        sale_price = k['sale_price']  # 售出价格
                        paypal_fee = k['paypal_fee']  # 手续费
                        # final_payout = k['final_payout']  # 到账

                        if self.n == (order_items_len - 1):
                            self.paypal_fee_total += paypal_fee
                            self.final_payout_total = order_total - self.paypal_fee_total
                            self.final_payout_total_list.append(self.final_payout_total)
                            self.paypal_fee_total_list.append(self.paypal_fee_total)
                            self.order_numbers.append(order_number)  # 订单号
                            self.shipping_totals.append(shipping_total)  # 总运费
                            self.discounts_totals.append(discount_total)  # 总折扣
                            self.order_totals.append(order_total)  # 总收入
                            self.dates.append(order_date)  # 订单时间
                            self.paypal_fee_total = 0
                            self.final_payout_total = 0
                            self.n = 0
                        elif self.n != (order_items_len - 1):  # 非最后一个
                            self.paypal_fee_total += paypal_fee
                            self.order_numbers.append('')  # 订单号
                            self.paypal_fee_total_list.append('')
                            self.final_payout_total_list.append('')
                            self.shipping_totals.append('')  # 总运费
                            self.discounts_totals.append('')  # 总折扣
                            self.order_totals.append('')  # 总收入
                            self.dates.append('')  # 订单时间
                            self.n += 1

                        size = k['size']
                        parts = size.split(' ')
                        if 'EU' in parts:
                            eu_num = parts[1]
                            try:
                                eu_num = float(eu_num)
                                self.sizes.append(eu_num)
                            except Exception as e:
                                eu_num = eu_num.strip('/US')
                                self.sizes.append(eu_num)
                        else:
                            self.sizes.append(size)  # 尺码

                        self.order_status.append(order_status)  # 订单状态
                        self.skus.append(sku)  # 主货号
                        self.quantitys.append(quantity)  # 购买数目
                        self.sale_prices.append(sale_price)  # 售出价格

            data = {
                '订单创建日期': self.dates,
                '订单号': self.order_numbers,
                '订单状态': self.order_status,
                '主货号': self.skus,
                '购买数目': self.quantitys,
                '商品尺码': self.sizes,
                '出售价格': self.sale_prices,
                '折扣总金额': self.discounts_totals,
                '运输总费用': self.shipping_totals,
                '订单总收入': self.order_totals,
                '手续总费用': self.paypal_fee_total_list,
                '到账总金额': self.final_payout_total_list
            }
            df = pandas.DataFrame(data=data)
            df.to_csv('./file/订单查询结果.csv', encoding='utf-8', index=False)

    async def specify_get_order_info(self, order_id: list):
        async with aiohttp.ClientSession() as session:
            for i in order_id:
                url_com = self.specify_get_order.replace('{order_id}', i)
                async with session.get(url=url_com, headers=self.headers) as response:
                    json_data = await response.json()
                    order_date = json_data['order_date']
                    order_status = json_data['status']
                    shipping_total = json_data['shipping_total']
                    discount_total = json_data['discount_total']
                    order_total = json_data['order_total']
                    items = json_data['items']
                    order_items_len = len(items)
                    for k in items:
                        order_number = str(k['order_number'])
                        sku = k['sku']
                        quantity = k['quantity']  # 购买数目
                        sale_price = k['sale_price']  # 售出价格
                        paypal_fee = k['paypal_fee']  # 手续费
                        # final_payout = k['final_payout']  # 到账

                        if self.n == (order_items_len - 1):
                            self.paypal_fee_total += paypal_fee
                            self.final_payout_total = order_total - self.paypal_fee_total
                            self.final_payout_total_list.append(self.final_payout_total)
                            self.paypal_fee_total_list.append(self.paypal_fee_total)
                            self.order_numbers.append(order_number)  # 订单号
                            self.shipping_totals.append(shipping_total)  # 总运费
                            self.discounts_totals.append(discount_total)  # 总折扣
                            self.order_totals.append(order_total)  # 总收入
                            self.dates.append(order_date)  # 订单时间
                            self.paypal_fee_total = 0
                            self.final_payout_total = 0
                            self.n = 0
                        elif self.n != (order_items_len - 1):  # 非最后一个
                            self.paypal_fee_total += paypal_fee
                            self.order_numbers.append('')  # 订单号
                            self.paypal_fee_total_list.append('')
                            self.final_payout_total_list.append('')
                            self.shipping_totals.append('')  # 总运费
                            self.discounts_totals.append('')  # 总折扣
                            self.order_totals.append('')  # 总收入
                            self.dates.append('')  # 订单时间
                            self.n += 1

                        size = k['size']
                        parts = size.split(' ')
                        if 'EU' in parts:
                            eu_num = parts[1]
                            try:
                                eu_num = float(eu_num)
                                self.sizes.append(eu_num)
                            except Exception as e:
                                eu_num = eu_num.strip('/US')
                                self.sizes.append(eu_num)
                        else:
                            self.sizes.append(size)  # 尺码

                        self.order_status.append(order_status)  # 订单状态
                        self.skus.append(sku)  # 主货号
                        self.quantitys.append(quantity)  # 购买数目
                        self.sale_prices.append(sale_price)  # 售出价格

                data = {
                    '订单创建日期': self.dates,
                    '订单号': self.order_numbers,
                    '订单状态': self.order_status,
                    '主货号': self.skus,
                    '购买数目': self.quantitys,
                    '商品尺码': self.sizes,
                    '出售价格': self.sale_prices,
                    '折扣总金额': self.discounts_totals,
                    '运输总费用': self.shipping_totals,
                    '订单总收入': self.order_totals,
                    '手续总费用': self.paypal_fee_total_list,
                    '到账总金额': self.final_payout_total_list
                }
                df = pandas.DataFrame(data=data)
                df.to_csv('./file/订单查询结果.csv', encoding='utf-8', index=False)
    async def handle(self,command,order_list=None):
        if command == '1':
            await  self.get_all_order_info()
            print('查询完毕')
        elif command == '2':
            await self.specify_get_order_info(order_list)
        elif command == '3':
            await self.specify_get_order_info(order_list)
        else:
            print('输入错误,请选择正确的查询方式')

class Products_Export:
    def __init__(self):
        self.sku = ''
        self.base_url = 'https://api.novelship.com/seller-api/v1'
        self.get_products_api = f'{self.base_url}/products/search?q={self.sku}&page=1'
        self.token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjk5NzM0MSwiaWF0IjoxNzQxMTQxMzI2LCJleHAiOjE4Mjc0NTQ5MjZ9.upPiRR0tx-fjXxraHYkp7xpwkcgHpmgQDzdzJY_KLfI"
        user_agent = fake_useragent.UserAgent()
        ua_random = user_agent.random
        self.header = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'User-Agent':ua_random
        }
        self.size_complete_list = []
        self.name_list = []
        self.class_list  =[]
        self.sku_list = []
        self.image_list = []
        self.id_list =[]
        self.brand_list = []
        self.sizes = []
        self.short_desc = []
        self.desc = []
        self.sale_price = []
        self.regular_price = []
        self.parent = []
        self.type_list = []

    async def async_list_for(self,data_list:list):
        for i in data_list:
            yield i

    async def get_products(self,sku):
        async with aiohttp.ClientSession() as session:
            self.sku = sku
            self.get_products_api = f'{self.base_url}/products/search?q={self.sku}&page=1'
            async with session.get(url=self.get_products_api,headers=self.header) as response:
                json_data = await response.json()
                results_value = json_data['results']
                total_value = json_data['total']
                async for i in self.async_list_for(results_value):
                    id = i['id']
                    await self.get_product_detail(id)


    async def get_product_detail(self,id):
        api_url = f'{self.base_url}/products/{id}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=api_url,headers=self.header) as response:
                json_data = await response.json()
                size_complete_list = []
                brand = json_data['main_brand']
                sku = json_data['sku']
                name = json_data['short_name']
                class_attr = json_data['class']
                gellery = json_data['gallery']
                gellery = str(gellery).replace(']','').replace('[','').replace("'",'')
                self.name_list.append(str(name).strip()+','+str(sku).strip())
                self.brand_list.append(brand)
                self.sizes.append('Size')
                self.short_desc.append('')
                self.desc.append('')
                self.sale_price.append(100000)
                self.regular_price.append(100000)
                self.class_list.append(class_attr)
                self.sku_list.append(sku)
                self.parent.append(sku)
                self.type_list.append('variable')
                self.image_list.append(gellery)
                async for i in self.async_list_for(json_data['size_chart']):
                    gender = i['gender']
                    us_size = i['US']
                    eu_size = i['EU']
                    size_complete = f"EU {eu_size} ~~ US {us_size} {gender}"
                    size_complete_list.append(size_complete)
                    self.brand_list.append('')
                    self.sku_list.append('')
                    self.class_list.append('')
                    self.name_list.append('')
                    self.image_list.append('')
                    self.sizes.append('Size')
                    self.short_desc.append('')
                    self.desc.append('')
                    self.sale_price.append(100000)
                    self.regular_price.append(100000)
                    self.parent.append(sku)
                    self.type_list.append('variation')
                size_complete_list_str = str(size_complete_list).replace("[",'').replace("]",'').replace("'",'')
                self.size_complete_list.append(size_complete_list_str)
                self.size_complete_list += size_complete_list


    async def handle(self,skus):
        async for sku in self.async_list_for(skus):
            await self.get_products(sku)
            data = {
                '类型': self.type_list,
                'SKU': self.sku_list,
                '名称': self.name_list,
                '简短描述': self.short_desc,
                '描述': self.desc,
                '促销价格': self.sale_price,
                '常规售价': self.regular_price,
                '分类': self.class_list,
                '品牌': self.brand_list,
                '图片': self.image_list,
                '父级': self.parent,
                ('属性名1').strip(): self.sizes,
                ('属性值1').strip(): self.size_complete_list
            }
            df = pandas.DataFrame(data)
            df.to_csv('ns产品查询结果.csv', index=False)

        data = {
            '类型': self.type_list,
            'SKU': self.sku_list,
            '名称': self.name_list,
            '简短描述': self.short_desc,
            '描述': self.desc,
            '促销价格': self.sale_price,
            '常规售价': self.regular_price,
            '分类': self.class_list,
            '品牌': self.brand_list,
            '图片': self.image_list,
            '父级': self.parent,
            ('属性名1').strip(): self.sizes,
            ('属性值1').strip(): self.size_complete_list
        }
        df = pandas.DataFrame(data)
        df.to_csv('./file/ns产品查询结果.csv', index=False)
app = FastAPI()
app.mount('../static', StaticFiles(directory='static'), name='static')
@app.get('/')
async def index():
    with open('web/index.html', mode='r', encoding='utf-8') as file:
        dom = file.read()
    return HTMLResponse(content=dom)

@app.get('/get_NS_Export')
async def get_Ns_Export(sku:str):
    data_list = sku.split(',')
    ns_export = Products_Export()
    await ns_export.handle(data_list)
    return FileResponse('../file/ns产品查询结果.csv')

@app.get('/get_orders_export')
async def get_orders_export(order_type:str,order_id:str=None):
    orders_export = order_out()
    if order_id is not None:
        data_list = order_id.split(',')
        await orders_export.handle(order_type, data_list)
        return FileResponse('../file/订单查询结果.csv')
    else:
        await orders_export.handle(order_type)
        return FileResponse('../file/订单查询结果.csv')
@app.post('/post_update')
async def post_update(request: Request):
    form_data = await request.form()
    skus = form_data['skus']
    await update_price_main(skus)
    return HTMLResponse(content='更新成功')



if __name__ == '__main__':
    uvicorn.run('fusion_proces_v2:app', host='192.168.0.18', port=8080)


