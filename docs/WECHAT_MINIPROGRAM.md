# AI智能客服助手 - 小程序集成指南

## 概述

本指南详细说明如何将AI智能客服系统集成到微信小程序中。

## 第一步: 注册小程序

### 1.1 访问微信公众平台
- 网址: [https://mp.weixin.qq.com](https://mp.weixin.qq.com)
- 点击"立即注册"
- 选择"小程序"类型

### 1.2 填写基本信息
- 邮箱地址
- 密码
- 验证码

### 1.3 主体信息认证
- 个人类型: 身份证认证
- 企业类型: 营业执照认证

### 1.4 获取AppID
注册成功后,在"开发" -> "开发设置"中获取:
- AppID (小程序ID)
- AppSecret (小程序密钥)

## 第二步: 开发环境准备

### 2.1 下载开发者工具
- 下载地址: [https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)
- 选择对应操作系统版本

### 2.2 创建小程序项目
1. 打开微信开发者工具
2. 点击"新建项目"
3. 填写项目配置:
   - AppID: 你的小程序ID
   - 项目名称: AI智能客服
   - 项目目录: 选择本地目录
   - 开发模式: 小程序
   - 后端服务: 不使用云服务

## 第三步: 项目结构

```
miniprogram/
├── pages/
│   ├── index/              # 首页
│   │   ├── index.wxml
│   │   ├── index.wxss
│   │   ├── index.js
│   │   └── index.json
│   └── chat/               # 聊天页
│       ├── chat.wxml
│       ├── chat.wxss
│       ├── chat.js
│       └── chat.json
├── components/             # 组件
│   └── chat-item/         # 聊天消息组件
│       ├── chat-item.wxml
│       ├── chat-item.wxss
│       ├── chat-item.js
│       └── chat-item.json
├── utils/                 # 工具函数
│   ├── api.js            # API请求
│   └── utils.js          # 通用工具
├── app.js                # 小程序入口
├── app.json              # 全局配置
├── app.wxss              # 全局样式
└── project.config.json   # 项目配置
```

## 第四步: 代码实现

### 4.1 全局配置 (app.json)

```json
{
  "pages": [
    "pages/index/index",
    "pages/chat/chat"
  ],
  "window": {
    "navigationBarTitleText": "AI智能客服",
    "navigationBarBackgroundColor": "#007AFF",
    "navigationBarTextStyle": "white",
    "backgroundColor": "#F5F5F9"
  },
  "tabBar": {
    "color": "#999999",
    "selectedColor": "#007AFF",
    "borderStyle": "white",
    "backgroundColor": "#ffffff",
    "list": [
      {
        "pagePath": "pages/index/index",
        "text": "首页",
        "iconPath": "images/home.png",
        "selectedIconPath": "images/home-active.png"
      },
      {
        "pagePath": "pages/chat/chat",
        "text": "客服",
        "iconPath": "images/chat.png",
        "selectedIconPath": "images/chat-active.png"
      }
    ]
  },
  "networkTimeout": {
    "request": 10000
  },
  "debug": true
}
```

### 4.2 首页 (pages/index/index.wxml)

```xml
<view class="container">
  <view class="header">
    <view class="logo">
      <text class="logo-text">🤖</text>
      <text class="logo-name">AI智能客服</text>
    </view>
    <text class="slogan">智能、高效、专业的客服服务</text>
  </view>
  
  <view class="features">
    <view class="feature-item" bindtap="navigateToChat">
      <text class="feature-icon">💬</text>
      <text class="feature-title">在线客服</text>
      <text class="feature-desc">7×24小时智能服务</text>
    </view>
    
    <view class="feature-item" bindtap="navigateToChat">
      <text class="feature-icon">📚</text>
      <text class="feature-title">知识库</text>
      <text class="feature-desc">常见问题快速解答</text>
    </view>
    
    <view class="feature-item" bindtap="navigateToChat">
      <text class="feature-icon">⚡</text>
      <text class="feature-title">快速响应</text>
      <text class="feature-desc">智能匹配最优答案</text>
    </view>
  </view>
  
  <view class="footer">
    <button class="start-btn" bindtap="navigateToChat">🚀 立即咨询</button>
  </view>
</view>
```

### 4.3 首页样式 (pages/index/index.wxss)

```css
.container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40rpx;
  box-sizing: border-box;
}

.header {
  text-align: center;
  padding: 80rpx 0;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20rpx;
}

.logo-text {
  font-size: 80rpx;
  margin-right: 10rpx;
}

.logo-name {
  font-size: 48rpx;
  font-weight: bold;
  color: white;
}

.slogan {
  color: rgba(255, 255, 255, 0.9);
  font-size: 28rpx;
  margin-top: 20rpx;
}

.features {
  background: white;
  border-radius: 20rpx;
  padding: 40rpx;
  margin-bottom: 40rpx;
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.1);
}

.feature-item {
  display: flex;
  align-items: center;
  padding: 30rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}

.feature-item:last-child {
  border-bottom: none;
}

.feature-icon {
  font-size: 48rpx;
  margin-right: 20rpx;
  width: 60rpx;
  text-align: center;
}

.feature-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  flex: 1;
}

.feature-desc {
  font-size: 24rpx;
  color: #999;
}

.footer {
  text-align: center;
}

.start-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 32rpx;
  padding: 20rpx 80rpx;
  border-radius: 50rpx;
  border: none;
}
```

### 4.4 首页逻辑 (pages/index/index.js)

```javascript
Page({
  data: {
    userInfo: null
  },

  onLoad() {
    // 获取用户信息
    this.getUserInfo()
  },

  getUserInfo() {
    wx.getSetting({
      success: (res) => {
        if (res.authSetting['scope.userInfo']) {
          wx.getUserInfo({
            success: (response) => {
              this.setData({
                userInfo: response.userInfo
              })
            }
          })
        }
      }
    })
  },

  navigateToChat() {
    wx.navigateTo({
      url: '/pages/chat/chat'
    })
  },

  onGetUserInfo(e) {
    if (e.detail.userInfo) {
      this.setData({
        userInfo: e.detail.userInfo
      })
      this.navigateToChat()
    }
  }
})
```

### 4.5 聊天页面 (pages/chat/chat.wxml)

```xml
<view class="chat-container">
  <!-- 聊天消息区 -->
  <scroll-view 
    class="chat-box" 
    scroll-y 
    scroll-into-view="{{scrollViewId}}"
    scroll-with-animation
  >
    <block wx:for="{{messages}}" wx:key="id">
      <view 
        class="message-item {{item.role === 'user' ? 'user' : 'ai'}}"
        id="msg-{{index}}"
      >
        <view class="message-avatar">
          <text>{{item.role === 'user' ? '👤' : '🤖'}}</text>
        </view>
        <view class="message-content">
          <text>{{item.content}}</text>
          <view class="message-time">{{item.time}}</view>
        </view>
      </view>
    </block>
    
    <!-- 加载指示器 -->
    <view class="loading" wx:if="{{isLoading}}">
      <text class="loading-dot">···</text>
    </view>
  </scroll-view>

  <!-- 输入区 -->
  <view class="input-box">
    <input 
      class="input-field" 
      placeholder="请输入您的问题..." 
      value="{{inputValue}}"
      bindinput="onInput"
      bindconfirm="sendMessage"
    />
    <button 
      class="send-btn" 
      bindtap="sendMessage"
      disabled="{{!inputValue.trim()}}"
    >
      <text>➤</text>
    </button>
  </view>

  <!-- 快捷问题 -->
  <view class="quick-questions" wx:if="{{showQuickQuestions}}">
    <view class="quick-title">💡 常见问题</view>
    <scroll-view class="quick-list" scroll-x>
      <view 
        class="quick-item" 
        wx:for="{{quickQuestions}}" 
        wx:key="index"
        bindtap="selectQuickQuestion"
        data-question="{{item}}"
      >
        {{item}}
      </view>
    </scroll-view>
  </view>
</view>
```

### 4.6 聊天页面样式 (pages/chat/chat.wxss)

```css
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #F5F5F9;
}

.chat-box {
  flex: 1;
  padding: 20rpx;
  overflow-y: auto;
}

.message-item {
  display: flex;
  margin-bottom: 20rpx;
  max-width: 80%;
}

.message-item.user {
  margin-left: auto;
  flex-direction: row-reverse;
}

.message-item.ai {
  margin-right: auto;
}

.message-avatar {
  width: 80rpx;
  height: 80rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
}

.message-content {
  background-color: white;
  padding: 20rpx 28rpx;
  border-radius: 12rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
  position: relative;
}

.message-item.user .message-content {
  background-color: #007AFF;
  color: white;
}

.message-time {
  font-size: 20rpx;
  color: #999;
  margin-top: 10rpx;
  text-align: right;
}

.message-item.user .message-time {
  color: rgba(255, 255, 255, 0.8);
}

.input-box {
  display: flex;
  padding: 20rpx;
  background-color: white;
  border-top: 1rpx solid #e0e0e0;
}

.input-field {
  flex: 1;
  background-color: #f5f5f5;
  border-radius: 50rpx;
  padding: 20rpx 30rpx;
  font-size: 28rpx;
}

.send-btn {
  width: 80rpx;
  height: 80rpx;
  background-color: #007AFF;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 20rpx;
  font-size: 36rpx;
  border: none;
}

.send-btn:disabled {
  background-color: #ccc;
}

.loading {
  text-align: center;
  padding: 20rpx;
}

.loading-dot {
  animation: blink 1.5s infinite;
  font-size: 32rpx;
}

@keyframes blink {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

.quick-questions {
  padding: 20rpx;
  background-color: white;
  border-top: 1rpx solid #e0e0e0;
}

.quick-title {
  font-size: 24rpx;
  color: #999;
  margin-bottom: 15rpx;
}

.quick-list {
  white-space: nowrap;
}

.quick-item {
  display: inline-block;
  background-color: #f0f0f0;
  padding: 12rpx 24rpx;
  border-radius: 30rpx;
  margin-right: 15rpx;
  font-size: 24rpx;
  color: #666;
}

.quick-item:active {
  background-color: #e0e0e0;
}
```

### 4.7 聊天页面逻辑 (pages/chat/chat.js)

```javascript
import { sendMessage } from '../../utils/api'

Page({
  data: {
    messages: [],
    inputValue: '',
    isLoading: false,
    scrollViewId: '',
    user_type: '电商用户', // 默认用户类型
    quickQuestions: [
      '如何查询订单?',
      '物流跟踪',
      '退换货政策',
      '支付问题',
      '优惠券使用'
    ],
    showQuickQuestions: true
  },

  onLoad(options) {
    // 获取用户类型
    if (options.user_type) {
      this.setData({ user_type: options.user_type })
    }
    
    // 加载历史消息
    this.loadHistory()
  },

  onInput(e) {
    this.setData({
      inputValue: e.detail.value,
      showQuickQuestions: !e.detail.value.trim()
    })
  },

  selectQuickQuestion(e) {
    const question = e.currentTarget.dataset.question
    this.setData({
      inputValue: question,
      showQuickQuestions: false
    })
    this.sendMessage()
  },

  async sendMessage() {
    const message = this.data.inputValue.trim()
    if (!message) return

    // 隐藏快捷问题
    this.setData({ showQuickQuestions: false })

    // 添加用户消息
    const userMsg = {
      role: 'user',
      content: message,
      time: this.formatTime(new Date())
    }

    this.addMessage(userMsg)

    // 清空输入框
    this.setData({ inputValue: '' })

    // 显示加载状态
    this.setData({ isLoading: true })

    try {
      // 调用后端API
      const response = await sendMessage({
        message: message,
        user_type: this.data.user_type
      })

      // 添加AI回复
      const aiMsg = {
        role: 'ai',
        content: response.reply,
        time: this.formatTime(new Date())
      }

      this.addMessage(aiMsg)
    } catch (error) {
      console.error('发送消息失败:', error)
      
      // 添加错误消息
      const errorMsg = {
        role: 'ai',
        content: '❌ 很抱歉,当前服务繁忙,请稍后再试。',
        time: this.formatTime(new Date())
      }

      this.addMessage(errorMsg)
    } finally {
      // 隐藏加载状态
      this.setData({ isLoading: false })
    }
  },

  addMessage(message) {
    const messages = [...this.data.messages, message]
    const scrollViewId = `msg-${messages.length - 1}`
    
    this.setData({
      messages: messages,
      scrollViewId: scrollViewId
    })

    // 保存到本地存储
    wx.setStorageSync('chat_history', messages)
  },

  loadHistory() {
    const history = wx.getStorageSync('chat_history')
    if (history) {
      this.setData({ messages: history })
      
      // 滚动到最新消息
      if (history.length > 0) {
        this.setData({
          scrollViewId: `msg-${history.length - 1}`
        })
      }
    }
  },

  formatTime(date) {
    const hours = date.getHours().toString().padStart(2, '0')
    const minutes = date.getMinutes().toString().padStart(2, '0')
    return `${hours}:${minutes}`
  },

  onUnload() {
    // 清空历史记录(可选)
    // wx.removeStorageSync('chat_history')
  }
})
```

### 4.8 API工具 (utils/api.js)

```javascript
// 后端API地址
const BASE_URL = 'https://your-domain.com/api'

/**
 * 发送消息到后端
 * @param {Object} data - 消息数据
 * @returns {Promise}
 */
export function sendMessage(data) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${BASE_URL}/chat`,
      method: 'POST',
      data: data,
      header: {
        'Content-Type': 'application/json',
        'Authorization': wx.getStorageSync('token') || ''
      },
      success: (res) => {
        if (res.data.success) {
          resolve(res.data)
        } else {
          reject(new Error(res.data.message || '请求失败'))
        }
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}

/**
 * 用户登录
 * @param {Object} data - 登录数据
 * @returns {Promise}
 */
export function login(data) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${BASE_URL}/login`,
      method: 'POST',
      data: data,
      success: (res) => {
        if (res.data.success) {
          // 保存token
          wx.setStorageSync('token', res.data.token)
          resolve(res.data)
        } else {
          reject(new Error(res.data.message || '登录失败'))
        }
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}

/**
 * 获取知识库
 * @param {String} user_type - 用户类型
 * @returns {Promise}
 */
export function getKnowledge(user_type) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${BASE_URL}/knowledge`,
      method: 'GET',
      data: { user_type },
      success: (res) => {
        if (res.data.success) {
          resolve(res.data.data)
        } else {
          reject(new Error(res.data.message || '获取失败'))
        }
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}
```

## 第五步: 后端API接口

### 5.1 Flask后端 (backend/app.py)

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 允许跨域

# 知识库
knowledge_base = {
    "电商用户": {
        "订单查询": "您可以通过订单号在官网查询订单状态...",
        "物流跟踪": "物流信息可通过快递单号查询...",
        # ... 其他问题
    },
    "企业用户": {
        # ... 企业用户知识库
    }
}

@app.route('/api/chat', methods=['POST'])
def chat():
    """对话接口"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        user_type = data.get('user_type', '电商用户')
        
        # 验证输入
        if not message:
            return jsonify({
                'success': False,
                'message': '消息不能为空'
            }), 400
        
        # 搜索知识库
        kb = knowledge_base.get(user_type, {})
        reply = None
        
        for key, value in kb.items():
            if key in message:
                reply = value
                break
        
        # 默认回复
        if not reply:
            reply = f"您好！关于您的问题：{message}，我会尽快为您解答。"
        
        return jsonify({
            'success': True,
            'reply': reply,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/login', methods=['POST'])
def login():
    """登录接口"""
    try:
        data = request.get_json()
        phone = data.get('phone', '')
        
        # 验证手机号
        if not phone or len(phone) < 11:
            return jsonify({
                'success': False,
                'message': '无效的手机号'
            }), 400
        
        # 生成token
        import secrets
        token = secrets.token_urlsafe(32)
        
        return jsonify({
            'success': True,
            'token': token,
            'user_info': {
                'phone': phone,
                'user_type': data.get('user_type', '电商用户')
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/knowledge', methods=['GET'])
def get_knowledge():
    """获取知识库"""
    user_type = request.args.get('user_type', '电商用户')
    kb = knowledge_base.get(user_type, {})
    
    return jsonify({
        'success': True,
        'data': kb
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 5.2 集成AI模型

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_ai_response(message, user_type):
    """调用AI模型"""
    system_message = f"你是一个{user_type}的客服助手"
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": message}
        ]
    )
    
    return response.choices[0].message.content
```

## 第六步: 测试与调试

### 6.1 本地测试
1. 在开发者工具中点击"编译"
2. 使用模拟器测试功能
3. 查看控制台日志

### 6.2 真机调试
1. 点击"真机调试"
2. 使用微信扫码
3. 在手机上测试实际效果

### 6.3 网络调试
1. 配置合法域名
2. 在开发者工具中开启"不校验合法域名"
3. 测试API请求

## 第七步: 发布上线

### 7.1 准备工作
- 完成所有功能测试
- 准备小程序图标(128x128px)
- 编写小程序介绍

### 7.2 上传代码
1. 在开发者工具中点击"上传"
2. 填写版本号和备注
3. 等待上传完成

### 7.3 提交审核
1. 登录微信公众平台
2. 进入"版本管理"
3. 点击"提交审核"
4. 填写审核信息

### 7.4 发布
审核通过后:
1. 进入"版本管理"
2. 点击"发布"
3. 等待发布成功

## 常见问题

### Q1: API请求失败
**A**: 检查:
- 服务器地址是否正确
- 是否配置了合法域名
- 网络连接是否正常

### Q2: 消息发送后没有回复
**A**: 检查:
- 后端接口是否正常
- 网络请求是否成功
- 控制台是否有错误

### Q3: 样式显示不正常
**A**: 检查:
- wxss文件是否正确
- 单位是否使用rpx
- 是否有语法错误

## 参考资源

- 微信小程序官方文档: [https://developers.weixin.qq.com/miniprogram/dev/framework/](https://developers.weixin.qq.com/miniprogram/dev/framework/)
- 微信开发者工具下载: [https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)
- 小程序设计指南: [https://developers.weixin.qq.com/miniprogram/design/](https://developers.weixin.qq.com/miniprogram/design/)

---

**最后更新**: 2026-09-09
