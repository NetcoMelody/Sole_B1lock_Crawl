import datetime
import random
import time
import json
import logging as logger
from asyncio import TaskGroup
import re
import numpy as np
import aiohttp
from aioconsole import aprint
import fake_useragent
import asyncio
import os
import tenacity
import aiomysql
import aiofiles
import aiocsv
import aiopandas

class api_handle:
    def __init__(self ,query_sku:str):
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
        count_need = query_sku.count(',')
        self.sku_list = query_sku.split(',' ,count_need)
        self.sku_list_new = []
        for i in self.sku_list:
            items = i.strip()
            self.sku_list_new.append(items)
        self._sku_list = []
        self._size_list = []
        self._price_list = []

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
            async with session.post(self.api_url, headers=self.header, json=processed_payload ,timeout=60) as response:
                json_text = await response.text()
                json_dict = json.loads(json_text)
                json_dict_data = json_dict['data']
                if 'spuList' in json_dict_data and json_dict_data['spuList']:

                    spu_list = json_dict_data['spuList']
                    for i in spu_list:
                        for j in i.items():
                            print (j)
                        # 测试，最后应放进鞋码循环
                        name = i['distSpuTitle']
                        sku = i['dwDesignerId']
                        short_desc = ''
                        normal_desc = ''
                        sale_price = 100000
                        normal_price = 100000
                        class_ = ''
                        sku_list = i['skuList']
                        brand = i['distBrandName']
                        # base_image = str(i['baseImage']).replace('[','').replace(']','').replace("'",'')
                        # await aprint(base_image)
                        # for item in i.items():
                        #     await aprint(item)
                        skulist = i['skuList']
                        for size_attr in skulist:
                            sku = i['dwDesignerId']
                            self._sku_list.append(sku)
                            size_attrs = size_attr['saleAttr']
                            for s in size_attrs:
                                if s['cnName'] == '尺码':
                                    self._size_list.append(s['cnValue'])
                            price = size_attr['minBidPrice']
                            print (price)
                            if price != 0:
                                price = int(str(price)[:-2])
                            else:
                                price = 100000
                            self._price_list.append(price)

if __name__ == '__main__':
    xiaoming = api_handle('1183A201-250(Team1024-原木时代BOX)')
    asyncio.run(xiaoming.request_api())
