import random

import pandas
from playwright.async_api import async_playwright
import undetected_playwright
import asyncio
from aioconsole import aprint,ainput
import json
import aiofiles
from fake_useragent import UserAgent

ua = UserAgent()
random_ua = ua.random  # 每次调用返回一个随机 UA

async def main():
    start_url = "https://www.ebay.com/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&_ssn=pokecolor_official&store_cat=0&store_name=pokecolorofficial&_oac=1&_nkw=pokemon&_dmd=2&rt=nc"
    async with async_playwright() as play:
        browser = await play.chromium.launch(headless=False,channel="msedge")
        context = await browser.new_context()
        page = await context.new_page()
        await undetected_playwright.stealth_async(context)
        await page.set_viewport_size({"width":1920,"height":1080})
        await page.goto(start_url)
        # class="srp-results srp-grid clearfix" ul
        await ainput("显式等待")
        count = 1
        card_number_list = []
        while 1:
            await page.wait_for_load_state()
            ul_tag = page.locator("xpath=//ul[contains(@class,'srp-results') and contains(@class,'srp-grid') and contains(@class,'clearfix')]")
            li_tags = await ul_tag.locator("xpath=./li").all()
            n = 1
            for li_tag in li_tags:
                card_number = await li_tag.get_attribute("data-listingid")
                if card_number is None:
                    try:
                        next_a = page.locator("xpath=//a[@aria-label='前往下一个搜索页面']").first
                        await next_a.click()
                        await aprint(f"前往第{count+1}页")
                    except Exception as e:
                        await aprint(f"第{count}页已经是最后一页")
                        data = {}
                        data = {
                            "itemCode":card_number_list
                        }
                        df = pandas.DataFrame(data)
                        df.to_csv("itemcodes.csv")
                        await aprint("任务结束")
                        return
                else:
                    card_number_list.append(card_number)
                    await aprint(f"第{count}页-第{n}个产品")
                    n+=1
            count+=1



if __name__ == '__main__':
    asyncio.run(main())