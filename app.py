import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

# 加载环境变量
load_dotenv()

# 设置日志
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 设置页面配置
st.set_page_config(
    page_title="AI智能客服助手",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化会话状态
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_type' not in st.session_state:
    st.session_state.user_type = "电商用户"
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

# 知识库数据
knowledge_base = {
    "电商用户": {
        "订单查询": "您可以通过订单号在官网查询订单状态，通常在24小时内更新",
        "物流跟踪": "物流信息可通过快递单号查询，支持圆通、中通、顺丰等主流快递",
        "退换货": "7天内可申请退换货,请提供订单号和退换货原因,我们会尽快处理",
        "支付问题": "支持微信支付、支付宝、银行卡等多种支付方式,如遇支付问题可联系客服",
        "优惠券": "可在购物车页面使用优惠券,满100减20等优惠活动持续进行中",
        "会员服务": "成为会员可享受积分兑换、专属折扣、优先发货等权益"
    },
    "企业用户": {
        "订单管理": "企业客户可通过企业账户批量管理订单,支持批量导出和统计分析",
        "批量采购": "支持批量下单和定制化服务,量大从优,详情咨询专属客户经理",
        "售后服务": "提供7×24小时技术支持,专业响应时间≤30分钟,保障企业业务连续性",
        "定制开发": "可根据企业需求提供定制化解决方案,包括API对接、系统集成等",
        "数据报表": "提供详细的销售数据和客户分析报表,支持自定义报表和数据导出",
        "API对接": "支持标准化API接口对接,实现系统自动化,提升运营效率"
    }
}

# 系统消息
system_messages = {
    "电商用户": "你是一个专业的电商客服人员,用友好专业的语气回答客户问题,了解订单查询、物流跟踪、退换货等常见问题",
    "企业用户": "你是一个专业的企业服务顾问,用专业严谨的语气回答企业客户问题,了解订单管理、批量采购、售后服务等"
}

def get_ai_response(user_input, user_type):
    """根据用户输入获取AI回复"""
    # 检查知识库
    kb = knowledge_base.get(user_type, {})
    for key, value in kb.items():
        if key in user_input:
            logger.info(f"知识库匹配: {key}")
            return value

    # 通用回复
    return f"您好!关于您的问题:{user_input},我会尽快为您解答。如需更详细的信息,请提供更多细节。"

def main():
    """主函数"""
    # 登录界面
    if not st.session_state.logged_in:
        login_page()
    else:
        # 主界面
        main_interface()

def login_page():
    """登录页面"""
    st.title("🤖 AI智能客服助手")
    st.markdown("### 欢迎使用智能客服系统")
    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("请登录微信账号")

        # 用户类型选择
        user_type = st.selectbox(
            "选择用户类型",
            ["电商用户", "企业用户"],
            help="电商用户适用于个人购物,企业用户适用于商业采购"
        )

        # 输入框
        phone = st.text_input("手机号码", placeholder="请输入您的手机号")
        company = st.text_input("公司名称(企业用户必填)", placeholder="请输入公司名称") if user_type == "企业用户" else ""

        st.divider()

        # 模拟微信登录
        if st.button("📱 微信登录", type="primary", use_container_width=True):
            if phone and phone.replace(" ", "").replace("-", "").isdigit() and len(phone) >= 11:
                st.session_state.logged_in = True
                st.session_state.user_type = user_type
                st.session_state.user_info = {
                    "phone": phone,
                    "company": company if user_type == "企业用户" else None
                }
                logger.info(f"用户登录: {user_type}")
                st.success("✅ 登录成功!")
                st.rerun()
            else:
                st.error("❌ 请输入有效的手机号码")

        st.info("💡 提示: 本系统支持微信一键登录,保护您的隐私安全")

    with col2:
        st.info("✨ **功能特色**\n"
               "- 🎯 多用户类型支持(电商/企业)\n"
               "- 📚 专业知识库系统\n"
               "- 💬 AI智能对话回复\n"
               "- 📱 微信小程序接入准备")

def main_interface():
    """主界面"""
    st.title("🤖 AI智能客服助手")
    st.subheader(f"👋 欢迎{st.session_state.user_type}使用AI智能客服")

    # 显示用户信息
    if st.session_state.user_info:
        with st.expander("👤 用户信息", expanded=False):
            st.write(f"手机号: {st.session_state.user_info.get('phone', 'N/A')}")
            if st.session_state.user_type == "企业用户":
                st.write(f"公司: {st.session_state.user_info.get('company', 'N/A')}")
            st.write(f"登录时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 侧边栏设置
    with st.sidebar:
        st.title("⚙️ 服务设置")

        # 用户类型切换
        new_user_type = st.selectbox(
            "切换用户类型",
            ["电商用户", "企业用户"],
            index=["电商用户", "企业用户"].index(st.session_state.user_type)
        )

        if new_user_type != st.session_state.user_type:
            st.session_state.user_type = new_user_type
            st.session_state.messages = []  # 清空消息
            logger.info(f"切换用户类型: {new_user_type}")
            st.rerun()

        st.divider()

        # 快速问题
        st.subheader("🚀 常见问题")
        kb = knowledge_base.get(st.session_state.user_type, {})
        for key, value in kb.items():
            if st.button(f"📌 {key}", key=f"quick_{key}"):
                st.session_state.messages.append({"role": "user", "content": key})
                st.session_state.messages.append({"role": "assistant", "content": value})
                logger.info(f"快速问题: {key}")
                st.rerun()

        st.divider()

        # 统计信息
        st.subheader("📊 会话统计")
        st.metric("消息数量", len(st.session_state.messages) // 2)

        if st.button("🗑️ 清空对话", type="secondary"):
            st.session_state.messages = []
            st.success("对话已清空")
            st.rerun()

        if st.button("🚪 退出登录", type="primary"):
            st.session_state.logged_in = False
            st.session_state.messages = []
            st.session_state.user_info = None
            logger.info("用户退出")
            st.rerun()

    # 聊天界面
    chat_container = st.container()

    with chat_container:
        # 显示历史消息
        for message_data in st.session_state.messages:
            with st.chat_message(message_data["role"]):
                st.markdown(message_data["content"])

    # 用户输入
    st.divider()
    col1, col2 = st.columns([4, 1])

    with col1:
        prompt = st.chat_input("💬 请输入您的问题(按回车发送)")

    with col2:
        st.empty()

    if prompt:
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        logger.info(f"用户提问: {prompt}")

        with st.chat_message("user"):
            st.markdown(prompt)

        # AI回复
        response = get_ai_response(prompt, st.session_state.user_type)
        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown(response)

        logger.info(f"AI回复: {response}")

    # 底部提示
    st.divider()
    st.caption("💡 提示: 您可以随时切换用户类型,或点击侧边栏的常见问题快速获取帮助")

if __name__ == "__main__":
    main()
