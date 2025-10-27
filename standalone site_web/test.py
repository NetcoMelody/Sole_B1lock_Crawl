import fake_useragent
import aiohttp
import asyncio
from aioconsole import aprint
import pandas
import re


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
                data = await response.json()
                size_complete_list = []
                sku = data['sku']
                str_sku = str(sku)
                if '（' in str_sku:
                    return
                if '(' in str_sku:
                    return
                if '/'  in str_sku:
                    return
                size_chart = data['size_chart']
                await aprint(size_chart)


    async def handle(self,skus:str):
        sku_list = skus.split(',')
        async for sku in self.async_list_for(sku_list):
            await self.get_products(sku)
        await aprint('结束')

if __name__ == '__main__':
    xiaoming = Products_Export()
    asyncio.run(xiaoming.handle('474193'))