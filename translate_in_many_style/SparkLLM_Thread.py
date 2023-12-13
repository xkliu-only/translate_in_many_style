# encoding: UTF-8
import _thread as thread
import base64
import hashlib
import hmac
import json
import time
from urllib.parse import urlparse
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import websocket


answer =''
tokens = 0

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(gpt_url).netloc
        self.path = urlparse(gpt_url).path
        self.gpt_url = gpt_url

    # 生成待鉴权的url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        print("signature_origin:\n" + str(signature_origin))
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.gpt_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url

# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)

# 收到websocket关闭的处理
def on_close(ws,content,test):
    return 0
    # print("### closed ###")

# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))
# 连接建立，发送数据
def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, question=ws.question,uid=ws.uid,chat_id=ws.chat_id))
    ws.send(data)

# 收到websocket消息的处理
def on_message(ws, message):
    # uid = ws.uid
    # chat_id = ws.chat_id
    endTime = time.time()
    print(endTime)
    data = json.loads(message)
    print("data: \n" + str(data))
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]

        # global answer
        ws.answer += content
        # print(content, end='')
        # print("用户：" + ws.uid + "   会话：" +ws.chat_id  +"\n返回结果：" +ws.answer)
        if status == 2:
            global tokens
            tokens = data["payload"]["usage"]
            ws.close()

def gen_params(appid, question,uid,chat_id):
    """
    通过appid和用户的提问来生成请参数
    """
    data = {
        "header": {
            "app_id": appid,
            "uid": uid # 用于区分业务层用户
        },
        "parameter": {
            "chat": {
                "domain": "generalv3",  # 通用场景
                "temperature": 0.8,
                "top_k" : 6,
                "max_tokens": 4096,
                "auditing": "default",
                "stream": True,
                "chat_id":chat_id

            }
        },
        "payload": {
            "message": {
                "text": question
            }
        }
    }
    return data

def main(uid,chat_id,appid, api_key, api_secret, gpt_url, question):

    # answer = ''
    #构造对象，参数创建的对象
    wsParam = Ws_Param(appid, api_key, api_secret, gpt_url)
    # websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.appid = appid
    ws.uid = uid
    ws.chat_id = chat_id
    ws.answer = ''
    ws.question = question
    # print(str(question))
    # ws.question = [{"role":"user","content":question}]

    # print("question:" + str(ws.question))
    begTime = time.time()
    print(begTime)
    ws.run_forever()
    # return {
    #     "uid":ws.uid,
    #     "chat_id":ws.chat_id,
    #     "answer":ws.answer
    # }
    return ws.answer


if __name__ == "__main__":
    result = main(uid='lxk', chat_id='lxk001', appid='XXXXXXXX', api_key='XXXXXXXXXXXXXXXXXXXXXXXX',
                  api_secret='XXXXXXXXXXXXXXXXXXXXXXXX',
                  gpt_url='wss://spark-api.xf-yun.com/v3.1/chat',
                  # gpt_url='wss://spark-api-knowledge.xf-yun.com/v2.1/multimodal',
                  question=[{"role": "user", "content": "湖北襄阳唐城出现了什么舆论？"}])

    print()
    print("返回结果为:\n" + str(result) )