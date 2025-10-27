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
                for i in results_value:
                    await aprint(i[""])
                # async for i in self.async_list_for(results_value):
                #     id = i['id']
                #     await self.get_product_detail(id)


    async def get_product_detail(self,id):
        api_url = f'{self.base_url}/products/{id}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=api_url,headers=self.header) as response:
                json_data = await response.json()
                size_complete_list = []
                sku = json_data['sku']
                str_sku = str(sku)
                if '（' in str_sku:
                    return
                if '(' in str_sku:
                    return
                if '/'  in str_sku:
                    return
                brand = json_data['main_brand']
                name = json_data['short_name']
                if '（' in name:
                    return
                if '(' in name:
                    return
                if '/' in name:
                    return
                class_attr = json_data['class']
                gellery = json_data['gallery']
                gellery = str(gellery).replace(']','').replace('[','').replace("'",'')
                self.name_list.append(str(name).strip()+' '+str(sku).strip())
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

    async def handle(self,skus:str):
        sku_list = skus.split(',')

        async for sku in self.async_list_for(sku_list):
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
            print (self.sku_list)
            df.to_csv('./file/ns产品查询结果.csv', index=False)
        await aprint('结束')

if __name__ == '__main__':
    xiaoming = Products_Export()
    asyncio.run(xiaoming.get_products("474193"))
    # asyncio.run(xiaoming.handle(['474193']))
