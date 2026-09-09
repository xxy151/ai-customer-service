# -*- coding: utf-8 -*-
"""
AI 智能客服助手 - Web 界面（Streamlit）
========================================
运行：streamlit run app.py
依赖 ai_core.py（知识库 + 百炼大模型 + SQLite 历史）
"""
import logging
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

import ai_core

load_dotenv()

try:
    logging.basicConfig(filename="app.log", level=logging.INFO,
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
except Exception:
    # 云端只读目录无法写日志文件时退化为控制台日志
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("app")

# 页面配置
st.set_page_config(page_title="AI智能客服助手", page_icon="🤖",
                   layout="wide", initial_sidebar_state="expanded")

# 会话状态初始化
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_type" not in st.session_state:
    st.session_state.user_type = "电商用户"
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "session_id" not in st.session_state:
    st.session_state.session_id = None


def login_page():
    st.title("🤖 AI智能客服助手")
    st.markdown("### 欢迎使用智能客服系统")
    st.divider()

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("请登录（演示：模拟微信登录）")
        user_type = st.selectbox("选择用户类型", ["电商用户", "企业用户"],
                                 help="电商用户适用于个人购物，企业用户适用于商业采购")
        phone = st.text_input("手机号码", placeholder="请输入您的手机号")
        company = st.text_input("公司名称（企业用户必填）", placeholder="请输入公司名称") if user_type == "企业用户" else ""

        if st.button("📱 微信登录", type="primary", use_container_width=True):
            digits = phone.replace(" ", "").replace("-", "")
            if digits.isdigit() and len(digits) >= 11:
                st.session_state.logged_in = True
                st.session_state.user_type = user_type
                st.session_state.user_info = {"phone": digits, "company": company or None}
                # 真实微信登录需后端换取 openid；演示环境用手机号占位。
                st.session_state.session_id = ai_core.create_session(
                    user_type, phone=digits, company=company or "")
                logger.info("用户登录: %s", user_type)
                st.success("✅ 登录成功！会话已建立（SQLite 持久化）")
                st.rerun()
            else:
                st.error("❌ 请输入有效的手机号码")

        st.info("💡 提示：界面为演示版微信登录；真实微信小程序接入见 wechat_bot.py 与 docs/WECHAT_MINIPROGRAM.md")

    with col2:
        st.info("✨ **功能特色**\n"
                "- 🎯 多用户类型支持（电商/企业）\n"
                "- 📚 知识库秒回（不耗 API）\n"
                "- 🧠 未命中走真实大模型（百炼 qwen）\n"
                "- 💾 SQLite 多轮历史持久化\n"
                "- 📱 微信公众号服务器（wechat_bot.py）")


def main_interface():
    st.title("🤖 AI智能客服助手")
    st.subheader(f"👋 欢迎{st.session_state.user_type}使用AI智能客服")

    with st.expander("👤 用户信息", expanded=False):
        info = st.session_state.user_info or {}
        st.write(f"手机号: {info.get('phone', 'N/A')}")
        if st.session_state.user_type == "企业用户":
            st.write(f"公司: {info.get('company', 'N/A')}")
        st.write(f"登录时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"会话ID: {st.session_state.session_id}")
        if ai_core.LLM_API_KEY:
            st.write(f"模型: {ai_core.LLM_MODEL}")
        else:
            st.warning("⚠️ 未配置 DASHSCOPE_API_KEY，大模型不可用（仅知识库/兜底回复）")

    with st.sidebar:
        st.title("⚙️ 服务设置")
        new_type = st.selectbox("切换用户类型", ["电商用户", "企业用户"],
                                index=["电商用户", "企业用户"].index(st.session_state.user_type))
        if new_type != st.session_state.user_type:
            st.session_state.user_type = new_type
            # 切换类型后新开会话，避免类型混淆
            st.session_state.session_id = ai_core.create_session(new_type)
            st.rerun()

        st.divider()
        st.subheader("🚀 快捷问题")
        for topic in ai_core.KNOWLEDGE_BASE.get(st.session_state.user_type, {}):
            if st.button(f"📌 {topic}", key=f"quick_{topic}", use_container_width=True):
                _send(topic)
                st.rerun()

        st.divider()
        st.subheader("📊 会话统计")
        msgs = ai_core.load_messages(st.session_state.session_id) if st.session_state.session_id else []
        st.metric("历史消息", len(msgs))
        if st.button("🗑️ 清空对话", use_container_width=True):
            if st.session_state.session_id:
                conn = ai_core._connect()
                conn.execute("DELETE FROM messages WHERE session_id=?", (st.session_state.session_id,))
                conn.commit()
                conn.close()
            st.success("对话已清空")
            st.rerun()
        if st.button("🚪 退出登录", type="primary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.session_id = None
            st.session_state.user_info = None
            st.rerun()

    # 历史消息
    history = ai_core.load_messages(st.session_state.session_id) if st.session_state.session_id else []
    for m in history:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if m["role"] == "assistant" and m.get("source"):
                st.caption(f"来源: {m['source']}")

    prompt = st.chat_input("💬 请输入您的问题（按回车发送）")
    if prompt:
        _send(prompt)
        st.rerun()

    st.caption("💡 知识库话题会秒回（不调用模型）；其他问题将由大模型回答，历史保存在 ai_customer.db")


def _send(text):
    """把用户输入交给 ai_core 并展示结果。"""
    with st.chat_message("user"):
        st.markdown(text)
    result = ai_core.ask(text, st.session_state.user_type,
                         session_id=st.session_state.session_id)
    st.session_state.session_id = result["session_id"]
    with st.chat_message("assistant"):
        st.markdown(result["answer"])
        src = result["source"]
        if src == "kb":
            st.caption("来源: 知识库（秒回）")
        elif src == "llm":
            st.caption(f"来源: 大模型 {result['model']}")
        else:
            st.caption("来源: 兜底话术（大模型不可用）")
    logger.info("Q: %s | A(source=%s)", text[:50], src)


if __name__ == "__main__":
    main = main_interface if st.session_state.get("logged_in") else login_page
    main()
