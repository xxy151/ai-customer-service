# -*- coding: utf-8 -*-
"""
AI 客服问答核心
==========================
- 知识库关键词快速命中（秒回，不消耗 API）
- 未命中时调用真实大模型（阿里云百炼 qwen 系列，OpenAI 兼容接口）
- 会话与消息用 SQLite 持久化（标准库 sqlite3，零额外依赖）

环境变量（.env）：
    DASHSCOPE_API_KEY  必填，百炼 API Key（也可退而用 OPENAI_API_KEY）
    LLM_BASE_URL       默认 https://dashscope.aliyuncs.com/compatible-mode/v1
    LLM_MODEL          默认 qwen3-max（可按免费额度换成 qwen-plus / qwen-turbo）
    DB_PATH            可选，sqlite 文件路径
"""
import os
import sqlite3
import time
import logging
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("ai_core")
if not logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(_h)
    logger.setLevel(logging.INFO)

# --------------------------------------------------------------------------
# 配置
# --------------------------------------------------------------------------
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.getenv("DB_PATH", os.path.join(_BASE_DIR, "ai_customer.db"))
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
LLM_API_KEY = os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY") or ""
LLM_MODEL = os.getenv("LLM_MODEL", "qwen3-max")
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "40"))
HISTORY_LIMIT = int(os.getenv("HISTORY_LIMIT", "8"))   # 携带最近 N 轮历史

# --------------------------------------------------------------------------
# 知识库（关键词快速命中，命中即秒回、不调大模型）
# --------------------------------------------------------------------------
KNOWLEDGE_BASE = {
    "电商用户": {
        "订单查询": "您可以通过订单号在官网查询订单状态，通常在24小时内更新。如需人工协助，请提供订单号。",
        "物流跟踪": "物流信息可通过快递单号查询，支持圆通、中通、顺丰等主流快递。",
        "退换货": "7天内可申请退换货，请提供订单号和退换货原因，我们会尽快处理。",
        "支付问题": "支持微信支付、支付宝、银行卡等多种支付方式，如遇支付问题可联系客服。",
        "优惠券": "可在购物车页面使用优惠券，满100减20等优惠活动持续进行中。",
        "会员服务": "成为会员可享受积分兑换、专属折扣、优先发货等权益。",
    },
    "企业用户": {
        "订单管理": "企业客户可通过企业账户批量管理订单，支持批量导出和统计分析。",
        "批量采购": "支持批量下单和定制化服务，量大从优，详情咨询专属客户经理。",
        "售后服务": "提供7×24小时技术支持，专业响应时间≤30分钟，保障企业业务连续性。",
        "定制开发": "可根据企业需求提供定制化解决方案，包括API对接、系统集成等。",
        "数据报表": "提供详细的销售数据和客户分析报表，支持自定义报表和数据导出。",
        "API对接": "支持标准化API接口对接，实现系统自动化，提升运营效率。",
    },
}

SYSTEM_PROMPTS = {
    "电商用户": "你是一名专业、友好、简洁的电商在线客服。基于下面的知识库回答用户问题；"
                "知识库没有的内容，请用你自己的能力给出准确、有帮助的回答，不要编造订单/物流等敏感信息，"
                "需要更多信息时先向用户询问。回答控制在200字以内。",
    "企业用户": "你是一名专业、严谨的企业服务顾问。基于下面的知识库回答企业客户问题；"
                "超出知识库时用你的能力回答，涉及定制方案时给出清晰建议，不要虚构价格与承诺。"
                "回答控制在300字以内。",
}

# --------------------------------------------------------------------------
# SQLite
# --------------------------------------------------------------------------
def _connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """CREATE TABLE IF NOT EXISTS sessions(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_type TEXT NOT NULL,
               phone TEXT DEFAULT '',
               company TEXT DEFAULT '',
               created_at TEXT NOT NULL)"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS messages(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               session_id INTEGER NOT NULL,
               role TEXT NOT NULL,
               content TEXT NOT NULL,
               source TEXT DEFAULT '',
               created_at TEXT NOT NULL)"""
    )
    conn.commit()
    return conn


def create_session(user_type, phone="", company=""):
    """新建会话，返回 session_id。"""
    conn = _connect()
    cur = conn.execute(
        "INSERT INTO sessions(user_type, phone, company, created_at) VALUES(?,?,?,?)",
        (user_type, phone or "", company or "", datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()
    sid = cur.lastrowid
    conn.close()
    return sid


def get_sessions(limit=20):
    conn = _connect()
    rows = conn.execute(
        "SELECT * FROM sessions ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def save_message(session_id, role, content, source=""):
    conn = _connect()
    conn.execute(
        "INSERT INTO messages(session_id, role, content, source, created_at) VALUES(?,?,?,?,?)",
        (session_id, role, content, source, datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()
    conn.close()


def load_messages(session_id, limit=100):
    conn = _connect()
    rows = conn.execute(
        "SELECT * FROM messages WHERE session_id=? ORDER BY id", (session_id,)
    ).fetchall()
    conn.close()
    msgs = [dict(r) for r in rows]
    return msgs[-limit:] if len(msgs) > limit else msgs


def recent_turns(session_id, n=HISTORY_LIMIT):
    """最近 n 轮 (user, assistant) 供大模型作为多轮上下文。"""
    msgs = load_messages(session_id)
    turns = []
    for m in msgs:
        if m["role"] == "user":
            turns.append({"role": "user", "content": m["content"]})
        elif m["role"] == "assistant" and turns and turns[-1]["role"] == "user":
            turns.append({"role": "assistant", "content": m["content"]})
    return turns[-n:]


# --------------------------------------------------------------------------
# 知识库命中
# --------------------------------------------------------------------------
def kb_match(user_input, user_type):
    """关键词命中知识库 -> (answer, source)；未命中 -> (None, 'kb')。"""
    user_input = (user_input or "").strip()
    kb = KNOWLEDGE_BASE.get(user_type) or {}
    # 先按整句包含命中，再按主题关键词弱匹配
    for topic, answer in kb.items():
        if topic in user_input or any(k in user_input for k in _topic_alias(topic)):
            return answer, topic
    return None, "kb"


def _topic_alias(topic):
    alias = {
        "订单查询": ["订单", "快递到哪", "我的单"],
        "物流跟踪": ["物流", "快递", "发货"],
        "退换货": ["退货", "换货", "退款"],
        "支付问题": ["支付", "付款", "付钱"],
        "优惠券": ["优惠", "券", "折扣"],
        "会员服务": ["会员", "积分"],
        "订单管理": ["批量订单", "企业订单"],
        "批量采购": ["采购", "批发", "大单"],
        "售后服务": ["售后", "技术支持", "报修"],
        "定制开发": ["定制", "开发方案"],
        "数据报表": ["报表", "数据导出", "分析"],
        "API对接": ["API", "接口", "系统对接"],
    }
    return alias.get(topic, [])


# --------------------------------------------------------------------------
# 大模型
# --------------------------------------------------------------------------
def llm_answer(user_type, user_input, session_id=None):
    """调用百炼大模型（OpenAI 兼容接口，用 requests 实现，避免额外依赖）。
    返回 (text, model)；失败时返回 (None, None)。"""
    if not LLM_API_KEY:
        logger.warning("缺少 DASHSCOPE_API_KEY / OPENAI_API_KEY，跳过 LLM")
        return None, None
    try:
        import requests
    except ImportError:
        logger.warning("未安装 requests 库，跳过 LLM")
        return None, None

    kb_text = "\n".join(
        f"- {k}: {v}" for k, v in (KNOWLEDGE_BASE.get(user_type) or {}).items()
    )
    system = SYSTEM_PROMPTS.get(user_type, SYSTEM_PROMPTS["电商用户"]) + "\n知识库：\n" + kb_text

    messages = [{"role": "system", "content": system}]
    if session_id:
        messages += recent_turns(session_id)
    messages.append({"role": "user", "content": user_input})

    url = LLM_BASE_URL.rstrip("/") + "/chat/completions"
    headers = {"Authorization": f"Bearer {LLM_API_KEY}",
               "Content-Type": "application/json"}
    payload = {
        "model": LLM_MODEL,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 2048,
        "stream": False,
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=LLM_TIMEOUT)
        if resp.status_code != 200:
            logger.warning("LLM HTTP %s: %s", resp.status_code, resp.text[:300])
            return None, None
        data = resp.json()
        text = (data["choices"][0]["message"]["content"] or "").strip()
        return text, data.get("model") or LLM_MODEL
    except Exception as e:  # noqa: BLE001
        logger.exception("LLM 调用失败: %s", e)
        return None, None


# --------------------------------------------------------------------------
# 对外入口
# --------------------------------------------------------------------------
def ask(user_input, user_type, session_id=None, save=True):
    """
    回答一个问题。
    返回 dict: {answer, source, model, session_id}
      source: 'kb'(知识库) / 'llm'(大模型) / 'fallback'(兜底话术)
    """
    user_input = (user_input or "").strip()
    if not user_input:
        return {"answer": "请输入您的问题。", "source": "fallback", "model": "", "session_id": session_id}

    if session_id is None:
        session_id = create_session(user_type)

    # 1) 知识库快速命中
    answer, topic = kb_match(user_input, user_type)
    source = "kb"
    if answer:
        if save:
            save_message(session_id, "user", user_input, source="user")
            save_message(session_id, "assistant", answer, source=f"kb:{topic}")
    else:
        # 2) 大模型
        llm_text, model = llm_answer(user_type, user_input, session_id)
        if llm_text:
            answer, source = llm_text, "llm"
            if save:
                save_message(session_id, "user", user_input, source="user")
                save_message(session_id, "assistant", llm_text, source=f"llm:{model}")
        else:
            # 3) 兜底（不落库，避免污染历史）
            answer = (
                f"您好！关于“{user_input[:50]}”，知识库暂时没有现成答案，"
                f"大模型服务当前不可用（请检查 .env 中 DASHSCOPE_API_KEY 与网络）。"
                f"您可以先尝试“订单查询 / 物流跟踪 / 退换货”等快捷问题。"
            )
            source = "fallback"

    return {"answer": answer, "source": source, "model": model if source == "llm" else "",
            "session_id": session_id}
