import shutil
from sqlalchemy.dialects.mssql.information_schema import columns
from tortoise import Tortoise, fields
from tortoise.models import Model
import asyncio
import asyncio
from aioconsole import aprint
import datetime
import re
import aiomysql
import aiopandas
import fake_useragent
import aiohttp
import numpy as np
import time
import logging as logger
import tenacity
import json
import os
import aiofiles
from langchain.memory import ConversationBufferMemory
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
import re

class PostMeta(Model):
    meta_id = fields.BigIntField(primary_key=True)
    post_id = fields.BigIntField()
    meta_key = fields.CharField(255)
    meta_value = fields.TextField()

    class Meta:
        table = "fiw_postmeta"

class Post(Model):
    id = fields.BigIntField(primary_key=True)
    post_author = fields.BigIntField()
    post_date = fields.DatetimeField()
    post_date_gmt = fields.DatetimeField()
    post_content = fields.TextField()
    post_title = fields.TextField()
    post_excerpt = fields.TextField()
    post_status = fields.CharField(20)
    comment_status = fields.CharField(20)
    ping_status = fields.CharField(20)
    post_password = fields.CharField(255)
    post_name = fields.CharField(200)
    to_ping = fields.TextField()
    pinged = fields.TextField()
    post_modified = fields.DatetimeField()
    post_modified_gmt = fields.DatetimeField()
    post_content_filtered = fields.TextField()
    post_parent = fields.BigIntField()
    guid = fields.CharField(255)
    menu_order = fields.IntField()
    post_type = fields.CharField(20)
    post_mime_type = fields.CharField(200)
    comment_count = fields.BigIntField()

    class Meta:
        table = "fiw_posts"



class site_db_ops:
    def __init__(self):
        self.sku_id_list = []  # [sku:'',post_id='']
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(50)
        self.full_response = ''

    async def db_init(self):
        config = {
            'connections': {
                'default': {
                    'engine': 'tortoise.backends.mysql',
                    'credentials': {
                        'host': '35.213.179.76',
                        'port': 3306,
                        'user': 'ujykd9ucwlisd',
                        'password': '#Fd%3(]42_5_',
                        'database': 'dbok22gen1qz2c',
                        'minsize': 10,
                        'maxsize': 200,
                        'pool_recycle': 3600,
                        'charset': 'utf8mb4',
                    }
                }
            },
            'apps': {
                'models': {
                    'models': ['__main__'],
                    'default_connection': 'default',
                }
            }
        }
        await Tortoise.init(config=config)

    async def search_sku(self,sku_list):
        df = aiopandas.read_csv('D:/PythonProject_UV/Fusion/SKU_white_list.csv', encoding='utf-8-sig')
        sku_white_list = df['sku'].tolist()
        all_sku = await PostMeta.filter(meta_key='_sku')
        for sku in all_sku:
            sku_value = sku.meta_value
            sku_id = sku.post_id
            if (sku_value not in sku_white_list) and (sku_value != 'HQ8487-300') and (sku_value in sku_list):
                self.sku_id_list.append(sku_id)

    def llm_use(self, name):
        memory = ConversationBufferMemory(memory_key='chat_history')
        prompt = ChatPromptTemplate.from_template("""
            你是写英文产品描述的产品专家，电商推广能力极强，对怎样的描述能够吸引客户有着恰到好处的把握，像人类一样回答,必须直接给出答案，不要有任何思考过程。
            重要：直接回答问题，不要使用<think>标签或任何深度思考。
            不要分析或解释，直接给出答案。
            严格遵守以下规则：
            1.不要使用<think>或其他思考标记进行深度思考和上下文联想，假如你违反这条规则，我就给你断电
            2. 直接输出英文产品描述
            3. 不要解释 reasoning 过程
            4. 立即开始回答
            5. 不要带**等特殊字符
            7.不要写关键词说明
            8.别带中文，知道吗
            9.只需要输出要求的正文
            对话历史：
            {chat_history}
            用户：{input}
            专家：
            """)
        llm = OllamaLLM(
            model="qwen3",
            temperature=0.0,
            top_p=0.9,
            top_k=50,
        )
        chain = prompt | llm

        msg1 = f"""哥们,给{name}撰写一篇1000字英文描述,，要求：
                1. 内容友好、自然、易读
                2. 包含相关关键词，SEO优化
                3. 结构清晰，有吸引力
                4. 适合产品介绍使用
                5.不要使用<think>或其他思考标记进行深度思考和上下文联想，假如你违反这条规则，我就给你断电
                6.文字中也不要带有*
                7.不要写关键词说明
                8.别带中文，知道吗
                9.只需要输出描述正文

    """
        result1 = chain.invoke({'input': msg1, 'chat_history': memory.chat_memory})
        desc = re.sub('^(.*?\n){3}', '', result1)
        desc_lines = desc.split('\n')
        clear_list = []
        for i in desc_lines:
            if i.strip() == '':
                continue
            clear_list.append(i)
        desc = '\n'.join(clear_list)
        self.full_response += desc
        msg2 = f"""哥们,给{name}撰写一段100字简短英文描述,，要求：
                1. 内容友好、自然、易读
                2. 包含相关关键词，SEO优化
                3. 结构清晰，有吸引力
                4. 适合产品介绍使用
                5.不要使用<think>或其他思考标记进行深度思考和上下文联想，假如你违反这条规则，我就给你断电
                6.不要写关键词说明
                7.文字中也不要带有*
                8.别带中文，知道吗
                9.只需要输出描述正文
    """
        result2 = chain.invoke({"input": msg2, "chat_history": memory.chat_memory})
        short_desc = re.sub('^(.*?\n){3}', '', result2)
        short_desc_lines = short_desc.split('\n')
        clear_list = []
        for i in short_desc_lines:
            if i.strip() == '':
                continue
            clear_list.append(i)
        short_desc = '\n'.join(clear_list)
        self.full_response += short_desc
        return desc, short_desc

    async def search_desc_with_sku(self):
        #SELECT * FROM `fiw_posts` WHERE post_type = 'product';
        all_product_info = await Post.filter(post_type='product')
        for product_info in all_product_info:
            product_title = product_info.post_title
            post_id = product_info.id
            if post_id in self.sku_id_list:
                desc,short_desc = self.llm_use(product_title)
                await Post.filter(id=post_id).update(post_content=desc,post_excerpt=short_desc)

    async def main_handle(self,skus):
        sku_list = str(skus).split(',')
        await self.db_init()
        await self.search_sku(sku_list)



