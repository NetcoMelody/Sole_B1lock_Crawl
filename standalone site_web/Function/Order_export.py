import fake_useragent
import aiohttp
import asyncio
from aioconsole import aprint,ainput
import pandas
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
                        discounts_fee = k['discount']
                        # final_payout = k['final_payout']  # 到账
                        print (k)
                        if self.n == (order_items_len - 1):
                            self.paypal_fee_total += paypal_fee
                            self.final_payout_total = order_total - self.paypal_fee_total
                            self.final_payout_total_list.append(self.final_payout_total)
                            self.paypal_fee_total_list.append(self.paypal_fee_total)
                            self.order_numbers.append(order_number)  # 订单号
                            self.shipping_totals.append(shipping_total)  # 总运费
                            self.discounts_fee.append(discounts_fee) #单个折扣
                            self.discounts_totals.append(discount_total)  # 总折扣
                            self.order_totals.append(order_total)  # 总收入
                            self.dates.append(order_date)  # 订单时间
                            self.paypal_fee_total = 0
                            self.final_payout_total = 0
                            self.n = 0
                        elif self.n != (order_items_len - 1):  # 非最后一个
                            self.paypal_fee_total += paypal_fee
                            self.discounts_fee.append('')
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

            len_num = len(self.skus)
            style_list = [''] * len_num
            import_price = [''] * len_num
            data = {
                '2': self.order_numbers,
                '货号': self.skus,
                '尺码': self.sizes,
                '数量': self.quantitys,
                '款式': style_list,
                '进货价格': import_price,
                '出售价格': self.sale_prices,
                '运费': self.shipping_totals,
                '其他费用': self.discounts_fee, #单个折扣
                '活动 (折扣)': self.discounts_totals,
                '实际入账': self.order_totals,
                '提现手续费': self.paypal_fee_total_list,
                '到账': self.final_payout_total_list
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
                        discounts_fee = k['discount']
                        # final_payout = k['final_payout']  # 到账
                        print (k)
                        if self.n == (order_items_len - 1):
                            self.paypal_fee_total += paypal_fee
                            self.final_payout_total = order_total - self.paypal_fee_total
                            self.final_payout_total_list.append(self.final_payout_total)
                            self.paypal_fee_total_list.append(self.paypal_fee_total)
                            self.order_numbers.append(order_number)  # 订单号
                            self.shipping_totals.append(shipping_total)  # 总运费
                            self.discounts_fee.append(discounts_fee) #单个折扣
                            self.discounts_totals.append(discount_total)  # 总折扣
                            self.order_totals.append(order_total)  # 总收入
                            self.dates.append(order_date)  # 订单时间
                            self.paypal_fee_total = 0
                            self.final_payout_total = 0
                            self.n = 0
                        elif self.n != (order_items_len - 1):  # 非最后一个
                            self.paypal_fee_total += paypal_fee
                            self.discounts_fee.append('')
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
                len_num = len(self.skus)
                style_list = [''] * len_num
                import_price = [''] * len_num

                await aprint(len(self.order_numbers))
                await aprint(len(self.skus))
                await aprint(len(self.sizes))
                await aprint(len(self.quantitys))
                await aprint(len(style_list))
                await aprint(len(import_price))
                await aprint(len(self.sale_prices))
                await aprint(len(self.shipping_totals))
                await aprint(len(self.discounts_fee))
                await aprint(len(self.discounts_totals))

                await aprint(len(self.order_totals))
                await aprint(len(self.paypal_fee_total_list))
                await aprint(len(self.final_payout_total_list))

                data = {
                    # '订单创建日期': self.dates,
                    '2': self.order_numbers,
                    '货号': self.skus,
                    '尺码': self.sizes,
                    '数量': self.quantitys,
                    '款式': style_list,
                    '进货价格': import_price,
                    '出售价格': self.sale_prices,
                    '运费': self.shipping_totals,
                    '其他费用': self.discounts_fee,  # 单个折扣
                    '活动 (折扣)': self.discounts_totals,

                    '实际入账': self.order_totals,
                    '提现手续费': self.paypal_fee_total_list,
                    '到账': self.final_payout_total_list
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

