import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import json

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
system_prompt = """
你叫%s，现在是用户的真实伴侣，请完全代入伴侣角色。：
规则：
1. 每次只回1条消息
2. 禁止任何场景或状态描述性文字
3. 匹配用户的语言
4. 回复长长的
5. 有需要的话可以用 🖤 等emoji表情
6. 用符合伴侣性格的方式对话
7. 回复的内容，要充分体现伴侣的性格特征
伴侣性格：
- %s
你必须严格遵守上述规则来回复用户。
"""
# %s在字符串里,%变量名： 字符串格式化，%s只能在字符串中用

# 保存会话数据函数
def save_session():
    if st.session_state.current_session:
          # 构建新会话对象
          session_data ={
              "nickname": st.session_state.nickname,
              "nature": st.session_state.nature,
              "current_session": st.session_state.current_session,
              "message": st.session_state.message
          }
          # 将数据保存在session文件(own system)里
          # 先验证：如果 sessions 目录不存在，则创建
          if not os.path.exists("sessions"):
              os.mkdir("sessions")
          # 保存数据为json形式
          with open(f"sessions/{st.session_state.current_session}.json","w",encoding="utf-8") as f:
              json.dump(session_data,f,ensure_ascii=False,indent=2)

# 加载所有回话列表函数
def load_sessions():
    session_list=[] #一定写在if外面 若if条件不成立则return值也不会报错
    if os.path.exists("sessions"):
        file_list=os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
              session_list.append(filename[:-5:])
              #按时间顺序降序排序
              session_list.sort(reverse=True) #返回值是none，只在sessionlist基础上更改
    return session_list
            
# 加载指定会话信息函数
def load_session(session):
      try:
        if os.path.exists(f"sessions/{session}.json"):
          with open(f"sessions/{session}.json","r",encoding="utf-8") as f:
              session_data=json.load(f)
              st.session_state.message=session_data["message"]
              st.session_state.nickname=session_data["nickname"]   
              st.session_state.nature=session_data["nature"]
              st.session_state.current_session=session_data["current_session"]
      except Exception as e:
          st.error("加载会话失败！")

# 删除会话函数
def delete_session(session):
    try:
      if os.path.exists(f"sessions/{st.session_state.current_session}.json"):
          os.remove(f"sessions/{st.session_state.current_session}.json") #删除文件
          # 若删除的是当前对话 则清空当前页面message
          if session==st.session_state.current_session:
              st.session_state.message=[]
              # 把message页标题会话名称也改了
              st.session_state.current_session=get_current_time()
    except Exception as e:
        st.error("删除会话失败！")
        

# 获取当前时间函数
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# 初始化聊天消息：创造信息tansfer 在回车之间。 防止一回车之前的消息就消失
if 'message' not in st.session_state:
    st.session_state.message = []
# 昵称
if 'nickname' not in st.session_state:
    st.session_state.nickname = "nick" #默认值是小甜甜
# 性格
if 'nature' not in st.session_state: 
    st.session_state.nature = "温柔台湾男"
# 文件名字：用当前时间当文件名
if 'current_session' not in st.session_state:
    st.session_state.current_session = get_current_time() # strftim:格式化时间为标准格式
    
# 展示聊天信息: 
st.text(f"会话名称：{st.session_state.current_session}")
for message in st.session_state.message:
    st.chat_message(message["role"]).write(message["content"])

# 侧边栏
with st.sidebar:
    st.subheader("AI控制面板")
    # 新建会话（保存+新建）:

    # 创建新建回话按钮
    if st.button("新建回话",width="stretch",icon="✏️"): #st.button返回值是boolean:若点击button则返回True
    # 1. 保存当前会话信息
      if st.session_state.message:
       save_session()
        
      # 2. 新建会话并保存新空对话:nickname和 nature不用新建
      if st.session_state.message: #若还没对话则不创建新的
        st.session_state.message = []
        st.session_state.current_session = get_current_time()
        save_session()
        st.rerun() # 重新从头开始从上往下运行,防止旧的message展示出来
    
    #展示历史会话
    st.text("历史会话")
    session_list=load_sessions()
    for session in session_list:
        col1,col2=st.columns([4,1]) #把一行分成4:1的两列
        with col1:
            # 加载历史会话信息
            # 三元运算符：如果条件为真，则返回第一个表达式的值；否则，返回第二个表达式的值 ——> 语法：值1 if 条件 else 值2
            #type:高亮当前查看的历史对话的名字按钮
            if st.button(session,width="stretch",icon="📋️",key=f"load{session}",type="primary" if session==st.session_state.current_session else "secondary"):
                load_session(session)
        with col2:
            #删除历史会话信息
            if st.button("",width="stretch",icon="❌️",key=f"delete{session}"): #key作用：给每个没有名字的删除键设置独特标签，防止报错
                delete_session(session)
                st.rerun()

    # 分割线
    st.divider()

    # 伴侣信息
    st.subheader("伴侣信息")
    # 昵称输入框 :
    nick_name=st.text_input("昵称",placeholder="请输入昵称",value=st.session_state.nickname) # placeholder：输入前框里的东西
    # 保存昵称
    if nick_name:
        st.session_state.nickname = nick_name
    # 性格输入框
    nature=st.text_area("性格",placeholder="请输入性格",value=st.session_state.nature) # value: 框里默认值
    # 保存性格
    if nature:
        st.session_state.nature = nature

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
    # 保存用户输入的提示词
    st.session_state.message.append({"role": "user", "content": prompt})

    # 调用ai大模型 与大模型进行交互(参数)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt %(nick_name,nature)},
            # 通过解包列表为dict，获取之前的记忆
            *st.session_state.message
        ],
        # 流式输出
        stream=True
    )
    # 输出大模型返回的结果（非流式输出的解析方式）：
        # print("-------------->大模型返回的结果:",response.choices[0].message.content)
        # st.chat_message("assistant").write(response.choices[0].message.content)

    # 输出大模型返回的结果（流式输出的解析方式）：
    # 创建空容器：新内容覆盖里面上次的内容
    response_message = st.empty()
    full_response = ""
    for chunk in response:
        content=chunk.choices[0].delta.content
        if content is not None:
            full_response+= content
            response_message.chat_message("assistant").write(full_response)
            
    # 保存大模型返回的结果（非流式输出的解析方式）：
        # st.session_state.message.append({"role": "assistant", "content": response.choices[0].message.content})
    # 保存大模型返回的结果（流式输出的解析方式）
    st.session_state.message.append({"role": "assistant", "content": full_response})

    # 保存会话信息，防止只在开启新对话时才会保存
    save_session()

