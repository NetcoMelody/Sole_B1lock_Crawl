import datetime
from DB_Model.sizeCharts_model import sizeCharts
from tortoise import Tortoise
import asyncio
from aioconsole import aprint
from StockX_crawl.handle import crawl_productSizeChart_handle
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from decimal import Decimal, ROUND_HALF_UP
from concurrent.futures import ThreadPoolExecutor
import threading
from tortoise.queryset import Q

async def stockx_db_init():
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
                'models': ['DB_Model.sizeCharts_model'],
                'default_connection': 'default',
            }
        }
    }

    await Tortoise.init(config=config)
    await Tortoise.generate_schemas()


async def soleProducts_db_init():
    config = {
        'connections': {
            'default': {
                'engine': 'tortoise.backends.mysql',
                'credentials': {
                    'host': '192.168.0.88',
                    'port': 3306,
                    'user': 'root',
                    'password': '123456',
                    'database': 'copydate',
                    'minsize': 10,
                    'maxsize': 1000,
                    'pool_recycle': 3600,
                    'charset': 'utf8mb4',
                }
            }
        },
        'apps': {
            'models': {
                'models': ['DB_Model.soleProducts_model'],
                'default_connection': 'default',
            }
        }
    }
    await Tortoise.init(config=config)


async def ebayProducts_db_init():
    config = {
        'connections': {
            'default': {
                'engine': 'tortoise.backends.mysql',
                'credentials': {
                    'host': '192.168.0.88',
                    'port': 3306,
                    'user': 'root',
                    'password': '123456',
                    'database': 'copydate',
                    'minsize': 10,
                    'maxsize': 1000,
                    'pool_recycle': 3600,
                    'charset': 'utf8mb4',
                }
            }
        },
        'apps': {
            'models': {
                'models': ['DB_Model.ebayProducts_model'],
                'default_connection': 'default',
            }
        }
    }

    await Tortoise.init(config=config)




async def main_handle(sku,executor:ThreadPoolExecutor,captcha_event,lock):
    await aprint(f"正在进入入口")
    loop = asyncio.get_running_loop()
    args = (sku, captcha_event,lock)
    single_sku_variations = await loop.run_in_executor(executor, lambda: crawl_productSizeChart_handle.main(*args))
    if single_sku_variations == "not_Found":
        single_sku_variations = [{"msg":"商品未找到"}]
    elif single_sku_variations is None:
        single_sku_variations = [{"msg":"变体信息为空"}]
    for variation in single_sku_variations:
        print (sku,":",variation)
        if "msg" in variation:
            msg = variation["msg"]
            if "US M" in variation:
                us_men_size = variation["US M"]
            else:
                us_men_size = ''
            if "US W" in variation:
                us_won_size = variation["US W"]
            else:
                us_won_size = ''
            if "US" in variation:
                us_size = variation["US"]
            else:
                us_size = ''
            if "UK" in variation:
                uk_size = variation["UK"]
            else:
                uk_size =''
            if "CM" in variation:
                cm_size = variation["CM"]
            else:
                cm_size = ''
            if "KR" in variation:
                kr_size = variation["KR"]
            else:
                kr_size = ''
            if "EU" in variation:
                eu_size = variation["EU"]
            else:
                eu_size = ''
            if "variation_id" in variation:
                variation_id = variation["variation_id"]
            else:
                variation_id = ''
            if "product_id" in variation:
                product_id = variation["product_id"]
            else:
                product_id = ''
            if "start_price" in variation:
                start_price = variation["start_price"]
            else:
                start_price = 0
            if "raw_price" in variation:
                raw_price = variation["raw_price"]
            else:
                raw_price = 0
        else:
            if "US M" in variation:
                us_men_size = variation["US M"]
            else:
                us_men_size = ''
            if "US W" in variation:
                us_won_size = variation["US W"]
            else:
                us_won_size = ''
            if "US" in variation:
                us_size = variation["US"]
            else:
                us_size = ''
            if "UK" in variation:
                uk_size = variation["UK"]
            else:
                uk_size =''
            if "CM" in variation:
                cm_size = variation["CM"]
            else:
                cm_size = ''
            if "KR" in variation:
                kr_size = variation["KR"]
            else:
                kr_size = ''
            if "EU" in variation:
                eu_size = variation["EU"]
            else:
                eu_size = ''
            if "variation_id" in variation:
                variation_id = variation["variation_id"]
            else:
                variation_id = ''
            if "product_id" in variation:
                product_id = variation["product_id"]
            else:
                product_id = ''
            if "start_price" in variation:
                start_price = variation["start_price"]
            else:
                start_price = 0
            if "raw_price" in variation:
                raw_price = variation["raw_price"]
            elif "raw_price" not in variation:
                raw_price = 0

            if "msg" not in variation:
                msg = "获取成功"
            else:
                msg = variation["msg"]
        if msg == "获取成功" and raw_price !=0 and start_price !=0:
            fee = float(start_price) - float(raw_price) - 25
            fee_proportion = fee/raw_price
            fee_proportion_like = Decimal(str(fee_proportion)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        else:
            fee_proportion_like = 0

        #创建
        # await sizeCharts.create(sku=sku,variation_id=variation_id,
        #                         us_M_size=us_men_size,us_W_size=us_won_size,
        #                         us_size=us_size,uk_size=uk_size,
        #                         cm_size=cm_size,kr_size=kr_size,
        #                         eu_size=eu_size,product_id = product_id,
        #                         msg=msg,fee=fee_proportion_like)

        await sizeCharts.filter(sku=sku, variation_id=variation_id).update(
            us_M_size=us_men_size,
            us_W_size=us_won_size,
            us_size=us_size,
            uk_size=uk_size,
            cm_size=cm_size,
            kr_size=kr_size,
            eu_size=eu_size,
            product_id=product_id,
            msg=msg,
            fee=fee_proportion_like
        )


def send_email():
    sender = '17816258635@163.com'
    receiver = '728800637@qq.com'
    auth_code = 'WPtjWi8A8DKYnuYW'
    smtp_host = 'smtp.163.com'
    msg = MIMEMultipart('mixed')
    msg['from'] = formataddr(pair=('系统通知', sender), charset='utf-8')
    msg['to'] = formataddr(pair=(None, receiver), charset='utf-8')
    msg['subject'] = Header('通告', charset='utf-8')
    mime_text = MIMEText("任务结束", _subtype='plain', _charset='utf-8')
    msg.attach(mime_text)
    smtp_conn = smtplib.SMTP_SSL(smtp_host, 465)
    smtp_conn.login(user=sender, password=auth_code)
    smtp_conn.sendmail(from_addr=sender, to_addrs=receiver, msg=msg.as_string())


max_workers = 100
semaphore = asyncio.Semaphore(max_workers)
async def limited_main_handle(sku,executor:ThreadPoolExecutor,captcha_event,lock):
    async with semaphore:
        await main_handle(sku,executor,captcha_event,lock)

# 抢占式并发
# async def sizeCharts_main():
#     # await soleProducts_db_init()
#     # sole_sku_list = await soleProducts.all().distinct().values_list("title", flat=True)
#     # await Tortoise.close_connections()
#
#     await stockx_db_init()
#
#     # skus = "1155350-AFC"
#     # sku_list = str(skus).split(",")
#     # set_sku_list = set(sku_list)
#
#     # sole_new_sku_list = []
#     # for sku in sole_sku_list:
#     #     if "{" in sku or "}" in sku:
#     #         sku = sku.replace("{",'').replace("}",'')
#     #     sole_new_sku_list.append(sku)
#
#     # set_sku_list  = set(sole_new_sku_list)
#     query = sizeCharts.filter(
#         product_id__isnull=True
#     ).filter(
#         Q(msg__not="商品未找到") & Q(msg__not="变体信息为空")
#     )
#     stock_sku_list = await query.distinct().values_list("sku", flat=True)
#     # missing_skus = list(set_sku_list  - stock_sku_set)
#     count_total = len( stock_sku_list)
#
#     await aprint ("脚本启动,初始SKU总数：",count_total)
#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         async with asyncio.TaskGroup() as tg:
#             captcha_event = threading.Event()
#             lock = threading.Lock()
#             for sku in stock_sku_list:
#                 tg.create_task(limited_main_handle(sku,executor,captcha_event,lock))
#     await Tortoise.close_connections()
#
#     send_email()


# 批处理并发
def chunk_list(lst, n):
    """将列表 lst 按每 n 个元素分块"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


async def sizeCharts_main():
    await stockx_db_init()

    query = sizeCharts.filter(
        product_id__isnull=True
    ).filter(
        Q(msg__not="商品未找到") & Q(msg__not="变体信息为空")
    )
    stock_sku_list = await query.distinct().values_list("sku", flat=True)
    count_total = len(stock_sku_list)
    await aprint("脚本启动, 初始SKU总数：", count_total)

    batch_size =100
    batches = list(chunk_list(stock_sku_list, batch_size))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for idx, batch in enumerate(batches, 1):
            start_time = datetime.datetime.now()
            await aprint(f"正在处理第 {idx}/{len(batches)} 批，共 {len(batch)} 个 SKU")
            async with asyncio.TaskGroup() as tg:
                captcha_event = threading.Event()
                lock = threading.Lock()
                for sku in batch:
                    tg.create_task(limited_main_handle(sku, executor, captcha_event, lock))
            end_time = datetime.datetime.now()
            exec_time = (end_time - start_time).seconds
            await aprint(f"第 {idx} 批处理完成,本次花费{exec_time}s")

            print ("")

    await Tortoise.close_connections()
    send_email()


if __name__ == '__main__':
    asyncio.run(sizeCharts_main())
