import os.path
from aioconsole import aprint,ainput
import asyncio
import fake_useragent
import datetime
import aiopandas
import aiohttp
import random
import tenacity
import aiofiles
import plotly.graph_objects as go

class api_ops:
    def __init__(self):
        UA = fake_useragent.UserAgent()
        self.start_time = datetime.datetime.now()
        random_UA = UA.random
        self.lock = asyncio.Lock()
        self.header = {
            'User-Agent': UA.random,
            'X-API-KEY': "65597d5ed20c860d77edcdb11da81411",
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        self.get_all_products_api = 'https://soleb1ock.com/wp-json/product-api/v1/products'  # 获取所有产品 Get
        self.use_id_get_products_api = 'https://soleb1ock.com/wp-json/product-api/v1/product/{id}'  # 通过ID获取产品 Get
        self.use_sku_get_size_price_api = 'https://soleb1ock.com/wp-json/product-api/v1/product/sku/{sku}/variations'  # 通过SKU获取产品尺码和价格  Get
        self.record_txt = ''
        self.sizes = []
        self.only_in_api_list = []
        self._sku_list = []
        self._size_list = []
        self._price_list = []
    def data_visulation(self,sku_size_list,price_list):
        change_list = price_list
        positive_values = [max(0, val) for val in change_list]
        negative_values = [min(0, val) for val in change_list]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='增加量',
            x=sku_size_list,
            y=positive_values,
            marker_color='lightgreen',
            text=[f'+{val}' if val > 0 else '' for val in positive_values],
            textposition='outside'
        ))
        fig.add_trace(go.Bar(
            name='减少量',
            x=sku_size_list,
            y=negative_values,
            marker_color='lightcoral',
            text=[f'{val}' if val < 0 else '' for val in negative_values],
            textposition='outside'
        ))
        fig.update_layout(
            title={
                'text': '10小时价格变动分析',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            xaxis_title='sku-size',
            yaxis_title='变动价格',
            barmode='stack',
            template='plotly_white',
            height=600,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        fig.update_xaxes(tickangle=45)
        fig.show()
        html_string = fig.to_html(include_plotlyjs='cdn',  # 使用 CDN 加载 Plotly.js 库
                                  full_html=True,  # 返回完整的 HTML 页面
                                  default_height='100vh',  # 设置默认高度
                                  default_width='100vw'  # 设置默认宽度
                                  )
        return html_string

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), wait=tenacity.wait_fixed(60))
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
                    await aprint(e)
    @tenacity.retry(stop=tenacity.stop_after_attempt(3), wait=tenacity.wait_fixed(60))
    async def _use_sku_get_size_price_handle(self, sku, session, url_com):
        async with session.get(url_com, headers=self.header, timeout=60) as response:
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
                async with aiofiles.open('sku.txt', mode='r', encoding='utf-8') as file:
                    n = 0
                    async for sku in file:
                        sku = sku.strip()
                        n += 1
                        await aprint(f'正在获取第{n}个SKU的数据', flush=True)
                        url_com = self.use_sku_get_size_price_api.replace('{sku}', sku)
                        tg = TG.create_task(self._use_sku_get_size_price_handle(sku, session, url_com))
                        tasks.append(tg)
                        await asyncio.sleep(random.uniform(0.3, 0.5))
                m = 0
                for task in tasks:
                    m += 1
                    await aprint(f'正在获取第{m}个Task的数据', flush=True)
                    json_data = await task
                    TG.create_task(self._task_handle(json_data, sku_list, eu_size_list, price_list))
                    await asyncio.sleep(random.uniform(0.3, 0.5))

            a = aiopandas.Series(sku_list)
            b = aiopandas.Series(eu_size_list)
            sku_size_list = ('sku:' + a.values[:, None] + '——' + 'size:' + b.values[None, :]).flatten()
            self.data_visulation(sku_size_list, price_list)

    async def get_all_products(self):
        async with aiohttp.ClientSession() as session:
            sku_list = []
            sku_white_list = []
            sku_sale_white_list = []
            async with session.get(self.get_all_products_api, headers=self.header, timeout=30) as response:
                text_list = await response.json()
                n = 0
                for text in text_list:
                    n += 1
                    sku_text = text['sku']
                    if (sku_text not in sku_list) and sku_text and (sku_text not in sku_white_list) and (
                            sku_text not in sku_sale_white_list):
                        sku_list.append(sku_text)
                        sku_text_txt = sku_text + '\n'
                        async with aiofiles.open('sku.txt', mode='a', encoding='utf-8') as file:
                            await file.write(sku_text_txt)
                await aprint(f'sku.txt文件生成完毕,总共{n}个SKU', flush=True)

    async def handle(self):
        await self.get_all_products()
        await self.use_sku_get_size_price()

def main():
    while 1:
        try:
            if os.path.exists('sku.txt'):
                os.remove('sku.txt')
            xiaoming=api_ops()
            asyncio.run(xiaoming.handle())
            if os.path.exists('sku.txt'):
                os.remove('sku.txt')
            for i in range(36000):
                print(f'距离下次程序执行，还剩余{36000-i}秒',end='\r',flush=True)
        except Exception as e:
            if os.path.exists('sku.txt'):
                os.remove('sku.txt')
            print ('死亡原因：',e)



