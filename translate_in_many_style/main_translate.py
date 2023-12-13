import SparkLLM_Thread
import streamlit as st
from streamlit_chat import message



# 页面提示语，开场白
st.markdown("#### 您好，我是多风格翻译官小星，很荣幸为您服务。 :sunglasses:")
# 文本输入框
user_input = st.text_input("请输入您需要翻译的英文文本:", key='input')
# 设置一些风格按钮选项，来设置不同的翻译风格
but = st.radio(
    "翻译风格:",
    ('默认风格','古文风格', '学术风格', '琼瑶风格',),horizontal=True)
if  but =='默认风格':
    style = '。 '
elif but =='古文风格':
    style = '，请按照古文风格进行翻译，用古诗词的行文风格，做到辞藻精炼，可用典故。'
elif but =='学术风格':
    style = '，请按照学术风格进行翻译，保持严谨认真的风格。'
elif but == '琼瑶风格':
    style = '，请按照琼瑶风格进行翻译，意境优美，充满诗情画意，或多愁善感，或心花怒放。'
else:
    style = '。 '


# 用于判断模型生成内容是否存在，不存在则创建列表
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

# 用于判断用户输入内容是否存在，不存在则创建列表
if 'past' not in st.session_state:
    st.session_state['past'] = []

if user_input:
    # 组装prompt，最终传入大模型的是text内容
    text = user_input + "\n请将上述英文内容翻译为中文" + style
    # 保存用户输入到列表，用于后续页面展示
    st.session_state['past'].append(user_input)
    # 向星火模型发出请求 ，其中appid、api_key、api_secret 获取地址: https://console.xfyun.cn/services/bm3
    output =SparkLLM_Thread.main(uid='lxk',chat_id='lxk001',appid='XXXXXXXX', api_key='XXXXXXXXXXXXXXXXXXXXXXXX',
         api_secret='XXXXXXXXXXXXXXXXXXXXXXXX', gpt_url='wss://spark-api.xf-yun.com/v3.1/chat',
         question=[{"role":"user","content":text}])
    # 保存大模型输出到列表，用于后续页面展示
    st.session_state['generated'].append(output)

# 在前端页面展示列表中的内容
if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i],
                is_user=True,
                key=str(i) + '_user')