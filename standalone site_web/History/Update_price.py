import aiomysql
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
import os
import tenacity
import aiocsv
import aiofiles


class db_op:
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
            sql = f"SELECT title, variation, price FROM {self.db_table} order by scrape_time DESC"
            await curs.execute(sql)
            all_data = await curs.fetchall()
            df = pandas.DataFrame(all_data, columns=['title', 'variation', 'price'])
            df.to_csv(path_or_buf='D:/PythonProject_UV/Fusion/temp/raw.csv', index=False)
        conn.close()
        print(f"\nDB表写完了，耗时: {datetime.datetime.now() - start_time}", flush=True)

class api_ops:
    def __init__(self):
        UA = fake_useragent.UserAgent()
        random_UA = UA.random
        self.lock = asyncio.Lock()
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
        async with session.post(url_com, headers=self.header, json=payload,timeout=60) as response:
            await aprint(f"Status for {sku}: {response.status}", flush=True)
            self.record_txt = sku
    async def update_if_handle(self,reader,session,tg):
        sizes = []
        current_sku = None
        async for value in reader:
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
                    tg.create_task(self.update_handle(session, url_com, payload, current_sku))
                    await asyncio.sleep(0.5)
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
            tg.create_task(self.update_handle(session, url_com, payload, current_sku))
            await asyncio.sleep(0.5)


    async def use_api_update_price(self):
        async with aiohttp.ClientSession() as session:
            async with TaskGroup() as tg:
                if os.path.exists('D:/PythonProject_UV/Fusion/temp/need_update.csv'):
                    async with aiofiles.open('D:/PythonProject_UV/Fusion/temp/need_update.csv', mode='r', encoding='utf-8-sig') as f:
                        reader = aiocsv.AsyncDictReader(f)
                        await self.update_if_handle(reader,session,tg)


                if os.path.exists('D:/PythonProject_UV/Fusion/temp/matched_update.csv'):
                    async with aiofiles.open('D:/PythonProject_UV/Fusion/temp/matched_update.csv', mode='r', encoding='utf-8-sig') as f:
                        reader = aiocsv.AsyncDictReader(f)
                        await self.update_if_handle(reader, session, tg)

    async def _task_handle(self, json_data, sku_list, eu_size_list, price_list):

        if 'variations' in json_data:
            var_content = json_data['variations']
            async with self.lock:
                try:
                    for i in var_content:
                        sku = i['sku']
                        size = i['size']
                        price = i['price']
                        sku_list.append(sku)
                        eu_size_list.append(size)
                        price_list.append(price)
                except Exception as e:
                    await aprint (e)

    async def _use_sku_get_size_price_handle(self, sku,session,url_com):
            async with session.get(url_com, headers=self.header,timeout=60) as response:
                response.raise_for_status()
                json_data = await response.json()
                return json_data
    async def use_sku_get_size_price(self):
        sku_list = []
        price_list = []
        eu_size_list = []
        tasks = []
        async with asyncio.TaskGroup() as TG:
            async with aiohttp.ClientSession() as session:
                async with aiofiles.open('D:/PythonProject_UV/Fusion/temp/sku.txt', mode='r', encoding='utf-8') as file:
                        n=0
                        async for sku in file:
                            sku = sku.strip()
                            n+=1
                            await aprint(f'正在获取第{n}个SKU的数据',flush=True)
                            url_com = self.use_sku_get_size_price_api.replace('{sku}', sku)
                            tg = TG.create_task(self._use_sku_get_size_price_handle(sku,session,url_com))
                            tasks.append(tg)

                m=0
                for task in tasks:
                    m+=1
                    await aprint(f'正在获取第{m}个Task的数据', flush=True)
                    json_data = await task
                    TG.create_task(self._task_handle(json_data, sku_list, eu_size_list, price_list))


        if sku_list:  # 确保有数据才写入
            data = {
                'sku': sku_list,
                'api_size': eu_size_list,
                'api_price': price_list
            }
            df = pandas.DataFrame(data)
            df = df.sort_values(by='sku')
            now_time = datetime.datetime.now()
            now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
            df.to_csv('D:/PythonProject_UV/Fusion/temp/get_api_data.csv', index=False)
            await aprint('get_api_data.csv文件写入完毕', flush=True)

    async def get_all_products(self):
        async with aiohttp.ClientSession() as session:
            sku_list = []
            async with session.get(self.get_all_products_api,headers=self.header,timeout=30) as response:
                text_list = await response.json()
                n=0
                for text in text_list:
                    n+=1
                    sku_text = text['sku']
                    if sku_text not in sku_list and sku_text :
                        sku_list.append(sku_text)
                        sku_text_txt = sku_text + '\n'
                        async with aiofiles.open('D:/PythonProject_UV/Fusion/temp/sku.txt', mode='a', encoding='utf-8') as file:
                            await file.write(sku_text_txt)
                        await aprint(f'第{n}条SKU添加成功', flush=True)
                await aprint (f'sku.txt文件生成完毕,总共{n}个SKU',flush=True)


    def chunk_list(self,it, size):
        from itertools import islice
        it = iter(it)
        return list(iter(lambda: list(islice(it, size)), []))

    async def generate_need_update_price(self,my_price_factor,dw_price_factor):
        import pandas as pd
        import numpy as np
        import re

        # 读取 API 数据
        api_df = pd.read_csv('D:/PythonProject_UV/Fusion/temp/get_api_data.csv', encoding='utf-8')
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
        raw_df = pd.read_csv('D:/PythonProject_UV/Fusion/temp/raw.csv', encoding='utf-8')
        raw_df = raw_df[['title', 'variation', 'price']]
        raw_df.columns = ['sku', 'size', 'price']
        raw_df['price'] = raw_df['price'].astype(float)
        raw_df = raw_df.drop_duplicates(subset=['sku', 'size'])

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

        #独立站价格公式
        merged['calculated_price'] = (merged['price'] * 0.14 / my_price_factor).round(2)

        merged['api_price'] = merged['api_price'].fillna(0)
        merged['price_diff'] = abs(merged['api_price'] - merged['calculated_price']).round(2)

        # 筛选需要更新的行（允许误差）
        updated_rows = merged[~np.isclose(merged['api_price'], merged['calculated_price'], atol=0.01)]

        # 新增部分：找出只存在于 API，不在 raw 中的记录
        only_in_api = merged[merged['price'].isna()]
        only_in_api_list = only_in_api[['sku', 'size']].to_dict(orient='records')

        # 构造输出 DataFrame
        result_df = updated_rows[['sku', 'size', 'calculated_price']]
        result_df.columns = ['货号', '尺码', '价格']

        # 如果 calculated_price == 0，则设置为 100000（默认值）
        result_df.loc[np.isclose(result_df['价格'], 0.0), '价格'] = 100000

        #结果存入类属性中
        self.need_update_list = result_df.to_dict(orient='records')  # 存入类属性
        self.only_in_api_list = only_in_api_list  # 存入类属性

        result_df = result_df.dropna(subset=['价格'])

        if len(result_df)>0:
            # 写入 CSV 文件（使用 utf-8-sig 避免 Excel 打开乱码）
            now_time = datetime.datetime.now()
            now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
            result_df.to_csv('D:/PythonProject_UV/Fusion/temp/need_update.csv', index=False, encoding='utf-8-sig')


        #将 only_in_api_list 写入 CSV 文件
        if self.only_in_api_list:
            only_in_api_df = pd.DataFrame(self.only_in_api_list)

            now_time = datetime.datetime.now()
            now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
            only_in_api_df.to_csv('D:/PythonProject_UV/Fusion/temp/only_in_api.csv', index=False,encoding='utf-8-sig')
            await aprint(f"已生成 only_in_api.csv，共 {len(self.only_in_api_list)} 条记录",flush=True)
            only_api_data = self.only_in_api_list
            _sku_list=[]
            for i in only_api_data:
                _sku_list.append(i['sku'])
            chunked_list = self.chunk_list(_sku_list, 200)
            for i in chunked_list:
                query_sku_list_str = str(i).replace('"', '').replace("'", '').replace(']', '').replace('[', '').strip()
                xiaoming = api_handle(query_sku_list_str)
                await xiaoming.request_api()

            data = {
                'sku': xiaoming._sku_list,
                'size': xiaoming._size_list,
                'price(RMB)': xiaoming._price_list
            }
            df = pandas.DataFrame(data)
            df.to_csv('D:/PythonProject_UV/Fusion/temp/query_info.csv', index=False)
            handler_a = data_handle()
            await handler_a.handle_query_data()
            await handler_a.diff_data(dw_price_factor)
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
        processed_payload =  {'code': 'sdue23487s8y234yhjHJHh2348hH', 'dwDesignerId': self.sku_list_new}
        start_time = time.time()
        logger.debug(f"正在发送API请求: {json.dumps(processed_payload, ensure_ascii=False)}")
        logger.debug(f"API请求体: {processed_payload}")
        logger.debug(f"URL::: {self.api_url}")
        # 关键修改：使用processed_payload而非payload
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, headers=self.header, json=processed_payload,timeout=60) as response:
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
                        if price !=0:
                            price = int(str(price)[:-2])
                        else:
                            price = 100000
                        self._price_list.append(price)


class data_handle:
    async def handle_query_data(self):
        import pandas as pd

        if not os.path.exists('D:/PythonProject_UV/Fusion/temp/query_info.csv'):
            print("❌ query_info.csv 文件不存在，请确保 api_handle.request_api() 已成功执行",flush=True)
            return

        df = pd.read_csv('D:/PythonProject_UV/Fusion/temp/query_info.csv')

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
            df.to_csv(f'D:/PythonProject_UV/Fusion/temp/query_info.csv', index=False)
            await aprint('写入成功',flush=True)

    async def diff_data(self,dw_price_factor):
        import pandas as pd
        import re

        # 读取两个 CSV 文件
        query_info_df = pd.read_csv('D:/PythonProject_UV/Fusion/temp/query_info.csv', encoding='utf-8')
        only_in_api_df = pd.read_csv('D:/PythonProject_UV/Fusion/temp/only_in_api.csv', encoding='utf-8')

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
        #得物的价格公式
        matched.loc[mask, '价格'] = (matched.loc[mask, '价格'] * 0.14 / dw_price_factor).round(2)

        now_time = datetime.datetime.now()
        now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")

        matched.to_csv('D:/PythonProject_UV/Fusion/temp/matched_update.csv', index=False, encoding='utf-8-sig')

        await aprint(f"已生成 matched_update.csv，共 {len(matched)} 条记录",flush=True)


def clear_input_buffer():
    import msvcrt
    while msvcrt.kbhit():
        msvcrt.getch()
async def main(my_price_factor:float,dw_price_factor:float):
    db_use = db_op()
    api_1 = api_ops()
    start_time = datetime.datetime.now()

    await db_use.select_db()
    await api_1.get_all_products()
    await api_1.use_sku_get_size_price()
    await api_1.generate_need_update_price(my_price_factor,dw_price_factor)
    await api_1.use_api_update_price()
    os.remove('D:/PythonProject_UV/Fusion/temp/raw.csv')
    os.remove('D:/PythonProject_UV/Fusion/temp/sku.txt')
    end_time = datetime.datetime.now()
    exec_time = round(((end_time - start_time).total_seconds()/60),2)
    await aprint (f'程序执行完成 | 本次执行花费时间>>{exec_time}分钟',flush=True)
async def update_price_main(skus:str,my_price_factor:float,dw_price_factor:float):
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
    await api_1.generate_need_update_price(my_price_factor,dw_price_factor)
    await api_1.use_api_update_price()
    os.remove('D:/PythonProject_UV/Fusion/temp/raw.csv')
    os.remove('D:/PythonProject_UV/Fusion/temp/sku.txt')
    now_time = datetime.datetime.now()
    now_time_str = now_time.strftime("%Y年%m月%d日-%H时%M分")
    end_time = datetime.datetime.now()
    exec_time = (end_time - start_time).total_seconds()/60
    exec_time = round(exec_time)
    await aprint (f'程序执行完成>>{now_time_str} | 本次执行花费时间>>{exec_time}分钟',flush=True)