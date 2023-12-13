项目描述：
本项目使用了streamlit框架来构建前端，展示一些标语、输入框和按钮。后端的大模型是星火大模型V3.0版本。

项目运行说明：
1、首先，从开放平台获取密钥信息，用于调用星火大模型时的鉴权密钥（前提是已经获得了token授权）。获取地址：https://console.xfyun.cn/services/bm3
2、将密钥填入代码中： 修改 main_translate.py 文件中，line 39 的appid、api_key、api_secret等信息；
3、安装必要的依赖库： 在终端（Terminal）中执行命令：pip install -r requirements.txt ；
4、运行项目：在终端（Terminal）中执行命令：streamlit run .\main_translate.py  ；
5、通过浏览器访问本地的8501端口： 地址栏输入：http://localhost:8501  进行访问。
