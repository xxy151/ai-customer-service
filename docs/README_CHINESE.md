# AI智能客服助手 - 详细文档

## 📋 项目概述

一个基于Streamlit的AI智能客服系统，支持微信小程序接入，主要服务电商用户和企业用户。该项目在2小时内完成了基础原型开发，展示了快速开发和部署的能力。

## 🎯 项目目标

- **快速原型开发**：2小时内完成可用原型
- **双用户类型支持**：电商用户和企业用户
- **知识库系统**：针对不同用户类型的专业知识库
- **AI智能回复**：基于大语言模型的智能对话
- **微信生态接入**：支持微信小程序

## 🏗️ 项目结构

```
AI客服助手项目/
├── app.py              # 主应用文件
├── requirements.txt    # Python依赖包
├── .env               # 环境变量配置
├── .gitignore         # Git忽略文件
├── README.md          # 项目说明文档
├── app.log           # 应用运行日志
└── docs/             # 项目文档目录
    └── README_CHINESE.md
```

## 🛠️ 技术栈详解

### 前端框架
- **Streamlit** (v1.30.0): 快速构建数据应用的Python框架
- **Streamlit-chat**: 专门的聊天界面组件
- **Pillow**: 图像处理库

### 后端服务
- **LangChain**: 构建AI应用的框架
- **OpenAI SDK**: 调用OpenAI API
- **Requests**: HTTP请求处理
- **Pydantic**: 数据验证

### 数据存储
- **MongoDB**: 用户数据和对话记录存储
- **本地文件**: 日志和配置文件

### 环境配置
- **Python-dotenv**: 环境变量管理
- **Logging**: 日志记录系统

## 📦 安装与配置

### 1. 环境要求
- Python 3.8+
- pip 包管理器
- Git (可选)

### 2. 安装步骤

```bash
# 克隆项目
cd D:/求职简历修改方案/AI客服助手项目

# 创建虚拟环境(推荐)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt

# 升级pip(可选)
python -m pip install --upgrade pip
```

### 3. 配置环境变量

编辑 `.env` 文件:

```env
# AI API配置
OPENAI_API_KEY=your_openai_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# 微信配置
WECHAT_APP_ID=your_wechat_app_id_here
WECHAT_APP_SECRET=your_wechat_app_secret_here

# 项目配置
USER_TYPES=["电商用户", "企业用户"]
LOG_FILE="app.log"

# 服务器配置
HOST=0.0.0.0
PORT=8501
DEBUG=True
```

**获取API密钥:**
- OpenAI API: https://platform.openai.com/api-keys
- DeepSeek API: 访问DeepSeek开发者平台

## 🚀 运行应用

### 本地运行

```bash
# 确保在虚拟环境中
streamlit run app.py
```

### 访问应用
- 默认地址: http://localhost:8501
- 如需修改端口,在 `.env` 中设置 PORT

### 生产部署

#### Streamlit Cloud
1. 创建GitHub仓库
2. 推送代码到GitHub
3. 登录 https://streamlit.io/cloud
4. 选择仓库部署

#### Docker部署
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 📱 微信小程序接入

### 1. 准备工作

#### 注册微信小程序
1. 访问 [微信公众平台](https://mp.weixin.qq.com)
2. 注册小程序账号
3. 获取 AppID 和 AppSecret

#### 配置服务器
1. 部署应用到公网服务器
2. 配置HTTPS证书
3. 设置服务器域名为微信可信域名

### 2. 小程序端集成

创建小程序项目 `miniprogram/`:

```json
// project.config.json
{
  "appid": "your-appid",
  "projectname": "AI客服助手"
}
```

```wxml
<!-- pages/chat/chat.wxml -->
<view class="container">
  <scroll-view scroll-y class="chat-box">
    <block wx:for="{{messages}}" wx:key="id">
      <view class="message {{item.role === 'user' ? 'user' : 'ai'}}">
        <text>{{item.content}}</text>
      </view>
    </block>
  </scroll-view>
  
  <view class="input-box">
    <input placeholder="请输入您的问题" bindinput="onInput" value="{{inputValue}}" />
    <button bindtap="sendMessage">发送</button>
  </view>
</view>
```

```js
// pages/chat/chat.js
Page({
  data: {
    messages: [],
    inputValue: ''
  },
  
  async onLoad() {
    // 获取用户信息
    const res = await wx.getUserProfile({ desc: '获取用户信息' })
    this.setData({ userInfo: res.userInfo })
  },
  
  onInput(e) {
    this.setData({ inputValue: e.detail.value })
  },
  
  async sendMessage() {
    const message = this.data.inputValue
    if (!message.trim()) return
    
    // 添加用户消息
    this.setData({
      messages: [...this.data.messages, { role: 'user', content: message }],
      inputValue: ''
    })
    
    // 调用后端API
    const response = await wx.request({
      url: 'https://your-domain.com/api/chat',
      method: 'POST',
      data: {
        message: message,
        user_type: '电商用户'
      }
    })
    
    // 添加AI回复
    this.setData({
      messages: [...this.data.messages, { role: 'ai', content: response.data.reply }]
    })
  }
})
```

### 3. 后端API接口

在 `app.py` 中添加API端点:

```python
import streamlit as st
import requests

# API路由
def api_chat():
    import json
    from flask import request, jsonify
    
    # 获取请求数据
    data = request.get_json()
    user_message = data.get('message', '')
    user_type = data.get('user_type', '电商用户')
    
    # 调用AI模型
    response = get_ai_response(user_message, user_type)
    
    return jsonify({
        'success': True,
        'reply': response,
        'timestamp': datetime.now().isoformat()
    })
```

## 💡 功能特性详解

### 1. 用户认证系统

#### 微信登录流程
1. 用户点击"微信登录"
2. 调用微信授权接口
3. 获取用户OpenID
4. 创建/更新用户记录
5. 生成会话Token

#### 用户类型识别
- **电商用户**: 个人消费者,关注购物、物流、售后
- **企业用户**: 商业客户,关注采购、定制、数据

### 2. 知识库系统

#### 电商用户知识库
- 订单查询
- 物流跟踪
- 退换货政策
- 支付方式
- 优惠券使用
- 会员权益

#### 企业用户知识库
- 订单管理
- 批量采购
- 售后服务
- 定制开发
- 数据报表
- API对接

#### 知识库扩展
```python
# 添加新问题到知识库
knowledge_base["电商用户"]["新品推荐"] = "我们每周都有新品上架,关注官网获取最新资讯"

# 从数据库加载知识库
def load_knowledge_from_db():
    # 从MongoDB加载
    pass
```

### 3. AI对话引擎

#### 对话流程
1. 用户输入问题
2. 匹配知识库
3. 调用AI模型
4. 生成回复
5. 记录对话

#### 智能匹配
- 关键词匹配
- 语义理解
- 上下文感知
- 意图识别

### 4. 会话管理

#### 消息持久化
```python
# 保存对话到MongoDB
def save_conversation(user_id, messages):
    db.conversations.insert_one({
        "user_id": user_id,
        "messages": messages,
        "timestamp": datetime.now()
    })
```

#### 会话统计
- 总消息数
- 平均响应时间
- 用户满意度
- 常见问题排行

## 📊 扩展功能规划

### 第一阶段 (已完成)
- ✅ 基础聊天功能
- ✅ 知识库系统
- ✅ 用户类型选择
- ✅ 日志记录

### 第二阶段 (进行中)
- [ ] 微信小程序接入
- [ ] 移动端优化
- [ ] 转人工服务
- [ ] 多轮对话
- [ ] 用户反馈

### 第三阶段 (规划中)
- [ ] 高级AI功能
  - 情感分析
  - 语音识别
  - 图片识别
- [ ] 数据分析
  - 用户行为分析
  - 问题分类统计
  - 效率优化建议
- [ ] 个性化推荐
  - 智能产品推荐
  - 定制化服务
  - 预测性支持

### 第四阶段 (远期规划)
- [ ] 多语言支持
- [ ] 多渠道接入
  - 企业微信
  - 钉钉
  - 飞书
- [ ] 智能工单系统
- [ ] 自动化流程

## 🔧 技术优化建议

### 1. 性能优化
```python
# 使用缓存
@st.cache_data
def get_cached_response(question):
    return get_ai_response(question)

# 异步处理
import asyncio
async def async_ai_response(question):
    # 异步调用AI API
    pass
```

### 2. 安全优化
```python
# 输入验证
def validate_input(user_input):
    if len(user_input) > 1000:
        raise ValueError("输入过长")
    if contains_inappropriate_content(user_input):
        raise ValueError("包含不当内容")
    return True

# XSS防护
import html
def sanitize_output(text):
    return html.escape(text)
```

### 3. 可扩展性
- 使用微服务架构
- 支持横向扩展
- 数据库分片
- 负载均衡

## 📝 代码示例

### 添加自定义命令
```python
# 在知识库中添加命令
def add_custom_command(command, response):
    knowledge_base["电商用户"][command] = response

# 示例
add_custom_command("营业时间", "我们的营业时间是9:00-21:00")
```

### 集成真实AI API
```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_real_ai_response(user_input, user_type):
    system_message = system_messages.get(user_type, "")
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input}
        ]
    )
    
    return response.choices[0].message.content
```

### 数据分析
```python
def analyze_conversations():
    # 统计常见问题
    questions = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
    
    # 分析用户满意度
    positive_keywords = ["谢谢", "很好", "满意"]
    satisfaction = sum(1 for q in questions if any(k in q for k in positive_keywords))
    
    return {
        "total_questions": len(questions),
        "satisfaction_rate": satisfaction / len(questions) if questions else 0
    }
```

## 🐛 常见问题

### 1. Streamlit运行错误
**问题**: `ModuleNotFoundError: No module named 'streamlit'`
**解决**: 确保已激活虚拟环境并安装依赖
```bash
python -m pip install streamlit
```

### 2. API调用失败
**问题**: `OpenAI API error`
**解决**: 
- 检查API密钥是否正确
- 确认网络连接
- 查看API配额

### 3. 端口被占用
**问题**: `Port 8501 is already in use`
**解决**: 
```bash
# 修改端口
streamlit run app.py --server.port 8502
```

### 4. 中文显示问题
**问题**: 中文乱码
**解决**: 确保文件编码为UTF-8
```python
# 在文件开头添加
# -*- coding: utf-8 -*-
```

## 📞 联系与支持

### 开发者
- 项目维护者: AI助手开发团队

### 反馈渠道
- GitHub Issues: 提交Bug和建议
- Email: support@example.com

### 贡献指南
欢迎提交Pull Request改进项目!

1. Fork项目
2. 创建特性分支
3. 提交修改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

MIT License - 自由使用、修改和分发

## 📌 项目亮点

### 技术亮点
- ✨ 2小时快速原型开发
- 🎯 精准的用户类型区分
- 📚 完善的知识库系统
- 🤖 智能化的AI对话
- 📱 微信生态无缝集成

### 业务价值
- 💰 降低客服成本
- ⚡ 提升响应速度
- 📈 提高用户满意度
- 🔄 7×24小时服务
- 📊 数据驱动优化

---

**最后更新**: 2026-09-09
**版本**: v1.0.0
