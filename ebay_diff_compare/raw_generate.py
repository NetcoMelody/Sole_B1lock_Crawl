import asyncio
from aioconsole import aprint,ainput
import aiohttp
import xmltodict
import pandas
import sys

class diff_compare:
    def __init__(self):
        self.browser_search_base_url = "https://api.ebay.com/buy/browse/v1/item_summary/search?q=[sku]&limit=100&&filter=itemLocationCountry:HK"
        self.browser_header = {
            "Authorization":"Bearer v^1.1#i^1#I^3#f^0#r^0#p^3#t^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",
            "X-EBAY-C-MARKETPLACE-ID":"EBAY_US"}
        self.trading_getitem_api = "https://api.ebay.com/ws/api.dll"
        self.trading_getitem_header = {
            "X-EBAY-API-SITEID":"0",
            "X-EBAY-API-COMPATIBILITY-LEVEL":"1421",
            "X-EBAY-API-CALL-NAME":"GetItem"
        }
        self.getitem_reqBody = """
        <?xml version="1.0" encoding="utf-8"?>
<GetItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
  <RequesterCredentials>
    <eBayAuthToken>v^1.1#i^1#r^1#p^3#I^3#f^0#t^Ul4xMF81Ojg1MTU0QTcyMjdFNUZEQzhEMkM1Q0I3NEMwN0IwOTE1XzFfMSNFXjI2MA==</eBayAuthToken>
  </RequesterCredentials>
	<ErrorLanguage>en_US</ErrorLanguage>
	<WarningLevel>High</WarningLevel>
      <!--Enter an ItemID-->
  <ItemID>【itemID】</ItemID>
</GetItemRequest>
        """
        self.browser_getitem_base_url = "https://api.ebay.com/buy/browse/v1/item/[browser_itemID]"

        self.sellerName_list = []
        self.sku_list = []
        self.size_list = []
        self.price_list = []
        self.itemID_list = []
        self.Lock = asyncio.Lock()
        self.Semaphore = asyncio.Semaphore(50)

    async def HK_handle(self,item):
        browser_itemID = item["itemId"]
        flag = await self.verify_Authenticity_Guarantee(browser_itemID)
        if flag == False:
            return
        trading_itemID = item["legacyItemId"]
        await self.get_sku_detail_info(trading_itemID)

    async def limited_HK_handle(self,item):
        async with self.Semaphore:
            await self.HK_handle(item)

    async def get_HK_store_data_with_sku(self,sku):
        self.sellerName_list.clear()
        self.sku_list.clear()
        self.size_list.clear()
        self.price_list.clear()
        self.itemID_list.clear()
        api = self.browser_search_base_url.replace("[sku]",sku)
        async with aiohttp.ClientSession() as session:
            async with session.get(api,headers=self.browser_header) as response:
                data = await response.json()
                itemSummaries = data["itemSummaries"]
                async with asyncio.TaskGroup() as tg:
                    for item in itemSummaries:
                        tg.create_task(self.limited_HK_handle(item))

    async def verify_Authenticity_Guarantee(self,browser_itemID):
        api = self.browser_getitem_base_url.replace("[browser_itemID]",browser_itemID)
        async with aiohttp.ClientSession() as session:
            async with session.get(api,headers=self.browser_header) as response:
                data = await response.json()
                if "qualifiedPrograms" not in data:
                    await aprint("正品验证失败","browser_ItemID:",browser_itemID)
                    return False
                qualifiedPrograms = data["qualifiedPrograms"]
                if "AUTHENTICITY_GUARANTEE" not in qualifiedPrograms:
                    await aprint("正品验证失败","browser_ItemID:",browser_itemID)
                    return False
                await aprint("成功验证正品","browser_ItemID:",browser_itemID)
                return True


    async def get_sku_detail_info_handle(self,test,item_field_data,sku,search_itemID):
        if isinstance(test, str):
            return
        if "StartPrice" not in test:
            return
        Quantity = test["Quantity"]
        SellingStatus = test["SellingStatus"]
        QuantitySold = SellingStatus["QuantitySold"]
        base_remaining = int(Quantity) - int(QuantitySold)
        if base_remaining <= 0:
            return
        startPrice_field = test["StartPrice"]
        price = startPrice_field["#text"]
        VariationSpecifics = test["VariationSpecifics"]
        NameValueList_field = VariationSpecifics["NameValueList"]
        us_size = NameValueList_field["Value"]
        async with self.Lock:
            self.size_list.append(us_size)
            self.price_list.append(price)
            seller = item_field_data["Seller"]
            UserID = seller["UserID"]
            self.sellerName_list.append(UserID)
            self.sku_list.append(sku)
            self.itemID_list.append(search_itemID)

    async def limited_get_sku_detail_info_handle(self,test,item_field_data,sku,search_itemID):
        async with self.Semaphore:
            await self.get_sku_detail_info_handle(test,item_field_data,sku,search_itemID)

    async def get_sku_detail_info(self,search_itemID):
        getitem_reqBody = self.getitem_reqBody.replace("【itemID】",search_itemID)
        async with aiohttp.ClientSession() as session:
            async with session.post(self.trading_getitem_api,headers=self.trading_getitem_header,data=getitem_reqBody) as response:
                await aprint("成功获取数据","trading_ItemID:",search_itemID)
                xml_data = await response.text()
                data = xmltodict.parse(xml_data)
                item_data = data["GetItemResponse"]
                item_field_data = item_data["Item"]
                if item_field_data is None:
                    return
                if "SKU" in item_field_data:
                    sku =  item_field_data["SKU"]
                    if "-L" in sku:
                        return
                sku = item_field_data["Title"]
                Variations_field_attr = item_field_data["Variations"]
                Variations = Variations_field_attr["Variation"]
                async with asyncio.TaskGroup() as tg:
                    for test in Variations:
                        tg.create_task(self.limited_get_sku_detail_info_handle(test,item_field_data,sku,search_itemID))


    async def generate_csv(self,sku):
        data = {
            "店铺名":self.sellerName_list,
            "ItemID":self.itemID_list,
            "货号":self.sku_list,
            "尺码":self.size_list,
            "价格":self.price_list
        }
        df = pandas.DataFrame(data)
        df.to_csv(f"./raw/raw_{sku}.csv",index=False)


async def main(sku_list_str):
    a = diff_compare()
    # while 1:
    # sku_list_str = input("请输入sku,以英文逗号分离多个sku,输入q退出程序")
    # if sku_list_str == "q":
    #     sys.exit()
    sku_list = sku_list_str.split(",")
    for sku in sku_list:
        await a.get_HK_store_data_with_sku(sku)
        await aprint(f"{sku}数据处理完成")
        await a.generate_csv(sku)
        await aprint(f"所有HK店铺的{sku}获取完毕")
    await aprint("raw文件生成完毕")


