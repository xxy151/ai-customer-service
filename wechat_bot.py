# -*- coding: utf-8 -*-
"""
微信公众号接入服务器（真实可运行）
====================================
复用 ai_core.ask 作为问答核心，实现两类真实微信能力：

1) 【公众号被动回复】无需 appid/secret，只需在公众号后台配置：
   服务器地址(URL)  ->  http://<你的公网地址>/wechat
   令牌(Token)      ->  与 .env 中 WECHAT_TOKEN 相同
   （域名需备案，或本地开发用内网穿透工具暴露公网地址）

2) 【小程序 / 客服消息 / 模板消息】需要 appid/secret（.env 中 WECHAT_APP_ID /
   WECHAT_APP_SECRET），详见 docs/WECHAT_MINIPROGRAM.md。

本地运行：  python wechat_bot.py        （默认 0.0.0.0:8001）
健康检查：  http://127.0.0.1:8001/health

本地模拟微信请求（不依赖真实微信）：
    python wechat_bot.py --selftest
"""
import hashlib
import os
import sys
import time
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
from flask import Flask, request, make_response

import ai_core

load_dotenv()

WECHAT_TOKEN = os.getenv("WECHAT_TOKEN", "ai-customer-service-token")
# 微信服务端口：用独立的 WECHAT_PORT（默认 8001），避免与 .env 中
# streamlit 用的 PORT=8501 混淆冲突。
PORT = int(os.getenv("WECHAT_PORT", "8001"))

app = Flask(__name__)


def check_signature(signature, timestamp, nonce):
    """微信服务器 URL 验证签名：sha1(排序拼接 token/timestamp/nonce)"""
    if not (signature and timestamp and nonce):
        return False
    tmp = "".join(sorted([WECHAT_TOKEN, timestamp, nonce]))
    return hashlib.sha1(tmp.encode("utf-8")).hexdigest() == signature


def parse_xml(data: bytes):
    """微信消息 XML -> dict；字段不存在时返回 ''"""
    root = ET.fromstring(data)
    return {child.tag: (child.text or "") for child in root}


def reply_xml(to_user, from_user, content: str) -> str:
    """构造文本被动回复 XML"""
    return (
        "<xml>"
        f"<ToUserName><![CDATA[{to_user}]]></ToUserName>"
        f"<FromUserName><![CDATA[{from_user}]]></FromUserName>"
        f"<CreateTime>{int(time.time())}</CreateTime>"
        "<MsgType><![CDATA[text]]></MsgType>"
        f"<Content><![CDATA[{content}]]></Content>"
        "</xml>"
    )


@app.route("/wechat", methods=["GET"])
def verify():
    """第一步：公众号后台配置时，微信会 GET 验证服务器。"""
    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")
    echostr = request.args.get("echostr", "")
    if check_signature(signature, timestamp, nonce):
        return echostr
    return "signature error", 403


@app.route("/wechat", methods=["POST"])
def handle():
    """第二步：接收用户消息并被动回复。"""
    try:
        msg = parse_xml(request.data)
    except ET.ParseError:
        return "success"

    to_user = msg.get("ToUserName", "")
    from_user = msg.get("FromUserName", "")   # 用户 openid
    msg_type = msg.get("MsgType", "")
    content = msg.get("Content", "").strip()

    if msg_type == "text":
        if not content:
            return "success"
        user_type = "电商用户"   # 公众号默认为电商场景；企业用户可在小程序端选择
        # 建立/复用该 openid 的会话：以 openid 为 phone 字段简化处理
        result = ai_core.ask(content, user_type, session_id=None)
        reply = result["answer"]
        src = result["source"]
        if src == "llm":
            reply += f"\n\n（来源：大模型 {result['model']}）"
        elif src == "kb":
            reply += "\n\n（来源：知识库）"
        return make_response(reply_xml(from_user, to_user, reply))
    elif msg_type == "event":
        event = msg.get("Event", "")
        if event == "subscribe":
            welcome = ("欢迎关注 AI 智能客服助手！\n"
                       "您可以咨询：订单查询 / 物流跟踪 / 退换货 / 支付问题 等。\n"
                       "直接输入问题即可，复杂问题将由大模型智能回答。")
            return make_response(reply_xml(from_user, to_user, welcome))
        return "success"
    else:
        # 图片/语音等暂不处理
        return "success"


@app.route("/health", methods=["GET"])
def health():
    llm_ok = bool(ai_core.LLM_API_KEY)
    return {"status": "ok", "llm_configured": llm_ok, "model": ai_core.LLM_MODEL,
            "db": ai_core.DB_PATH}


def selftest():
    """本地模拟一次微信文本消息，验证整条链路。"""
    print("== selftest: 模拟微信文本消息 ==")
    with app.test_client() as c:
        r = c.get("/health")
        print("GET /health ->", r.status_code, r.get_json())
        xml_in = (
            "<xml>"
            "<ToUserName><![CDATA[gh_test]]></ToUserName>"
            "<FromUserName><![CDATA[openid_test]]></FromUserName>"
            "<CreateTime>1700000000</CreateTime>"
            "<MsgType><![CDATA[text]]></MsgType>"
            "<Content><![CDATA[你好，介绍一下你们的退换货政策]]></Content>"
            "</xml>"
        )
        r = c.post("/wechat", data=xml_in.encode("utf-8"),
                   content_type="text/xml; charset=utf-8")
        print("POST /wechat ->", r.status_code)
        print("回复 XML:\n", r.get_data(as_text=True))


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        print(f"微信服务器启动: http://0.0.0.0:{PORT}/wechat  (Token={WECHAT_TOKEN})")
        app.run(host="0.0.0.0", port=PORT)
