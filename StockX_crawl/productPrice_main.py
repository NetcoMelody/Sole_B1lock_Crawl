import datetime
from tortoise import Tortoise
import asyncio
from aioconsole import aprint
from concurrent.futures import ThreadPoolExecutor
import threading
import sys
import aiofiles
import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
project_root = r"D:\Multi-Tech-Project"
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 现在就可以正常导入了
from StockX_crawl.handle import crawl_get_productPrice_handle
from StockX_crawl.DB_Model.productPrice_api_log_model import productPrice_api_log

async def productPrice_db_init():
    config = {
        'connections': {
            'default': {
                'engine': 'tortoise.backends.mysql',
                'credentials': {
                    'host': '192.168.0.18',
                    'port': 12345,
                    'user': 'root',
                    'password': 'Karos@123159',
                    'database': 'stockx',
                    'minsize': 10,
                    'maxsize': 1000,
                    'pool_recycle': 3600,
                    'charset': 'utf8mb4',
                }
            }
        },
        'apps': {
            'models': {
                'models': ['StockX_crawl.DB_Model.productPrice_api_log_model'],
                'default_connection': 'default',
            }
        }
    }
    await Tortoise.init(config=config)
    await Tortoise.generate_schemas()

class productPrice :

    def __init__(self):
        self.max_workers = 100
        self.semaphore = asyncio.Semaphore(self.max_workers)
        self.many_skus = []

    async def main_handle(self,product_id,executor:ThreadPoolExecutor,captcha_event,lock):
        loop = asyncio.get_running_loop()
        args = (product_id,captcha_event,lock)
        single_sku_variations_list,sku = await loop.run_in_executor(executor, lambda: crawl_get_productPrice_handle.main(*args))
        single_sku_dict = {}
        single_sku_dict[sku] = single_sku_variations_list
        self.many_skus.append(single_sku_dict)

    async def limited_main_handle(self,product_id,executor:ThreadPoolExecutor,captcha_event,lock):
        async with self.semaphore:
            await self.main_handle(product_id,executor,captcha_event,lock)


    # 批处理并发
    def chunk_list(self,lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    async def productPrice_main(self,productIds):
        productId_list = productIds.split(",")

        count_total = len(productId_list)
        await aprint("脚本启动, 初始SKU总数：", count_total)

        batch_size =100
        batches = list(self.chunk_list(productId_list, batch_size))
        big_start_time = datetime.datetime.now()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for idx, batch in enumerate(batches, 1):
                start_time = datetime.datetime.now()
                await aprint(f"正在处理第 {idx}/{len(batches)} 批，共 {len(batch)} 个 SKU")
                async with asyncio.TaskGroup() as tg:
                    captcha_event = threading.Event()
                    lock = threading.Lock()
                    for productId in batch:
                        tg.create_task(self.limited_main_handle(productId,executor, captcha_event, lock))
                end_time = datetime.datetime.now()
                exec_time = (end_time - start_time).seconds
                await aprint(f"第 {idx} 批处理完成,本次花费{exec_time}s")

        big_end_time = datetime.datetime.now()
        big_exec_time = (big_end_time - big_start_time).seconds
        await aprint(f"完成所有批任务，总计花费{big_exec_time}s")
        return self.many_skus

async def main():
    productIds = sys.argv[1]
    userName = sys.argv[2]
    hashHex = sys.argv[3]
    data_dict = {}
    xiaoming = productPrice()
    many_skusInfo_list = await xiaoming.productPrice_main(productIds)
    skus_length = len(many_skusInfo_list)
    await productPrice_db_init()
    await productPrice_api_log.create(userName=userName,data=many_skusInfo_list,skus_length=skus_length)
    await Tortoise.close_connections()

    data_dict["Data"] = many_skusInfo_list
    filePath = f"D:/Multi-Tech-Project/Dev_getStockxPrice_API/Response_json/{userName}-{hashHex}-data.json"
    async with aiofiles.open(filePath,"w",encoding="utf-8") as file:
        data_dict_json = json.dumps(data_dict)
        await file.write(data_dict_json)
    await aprint(data_dict)

if __name__ == '__main__':
    asyncio.run(main())
