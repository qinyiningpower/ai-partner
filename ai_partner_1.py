import streamlit as st
import os
from openai import OpenAI

# 设置页面的配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🐷",
    layout="wide", 
    initial_sidebar_state="expanded",
    menu_items={}
)
# 大标题
st.title("AI智能伴侣")

# 系统提示词
system_prompt = "你是一个长得像严屹宽的霸道总裁"

# 创建与ai大模型交互的客户端
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

# 消息输入框
prompt=st.chat_input("请输入你的问题")
if prompt: #prompt这个字符串自动转化为bool值, 如果字符串为非空,则为True
    # 美化输入的信息
    st.chat_message("user").write(prompt) #chat_message()的提示词：user, assistant；用户输入的信息，ai的信息
    # 输出在终端里，便于调试使用
    print("用户输入的提示词：",prompt) 

    # 调用ai大模型 与大模型进行交互(参数)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )
    # 输出大模型返回的结果
    print("-------------->大模型返回的结果:",response.choices[0].message.content)
    st.chat_message("assistant").write(response.choices[0].message.content)