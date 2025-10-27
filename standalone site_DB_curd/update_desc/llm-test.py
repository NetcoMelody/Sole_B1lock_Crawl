import asyncio

from langchain.memory import ConversationBufferMemory
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
import re

class apply_llm():
    def __init__(self):
        self.full_response = ''

    def llm_use(self,name):
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
        result1 =chain.invoke({'input': msg1, 'chat_history': memory.chat_memory})
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

if __name__ == '__main__':
    xiaoming = apply_llm()
    a,b = xiaoming.llm_use('Fragment Design x Travis Scott x Air Jordan 1 Retro Low ‘Military Blue’ DM7866-140')
    print ('desc',a)
    print ('short_desc',b)