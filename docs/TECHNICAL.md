# AI智能客服助手 - 技术文档

## 目录
1. [系统架构](#系统架构)
2. [核心模块](#核心模块)
3. [API接口](#api接口)
4. [数据库设计](#数据库设计)
5. [安全机制](#安全机制)
6. [部署方案](#部署方案)

## 系统架构

### 架构图
```
┌─────────────────────────────────────────────────────────┐
│                    用户层 (微信小程序)                    │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│              接入层 (Streamlit + Flask API)              │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│           业务逻辑层 (对话管理 + 知识库 + AI)            │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│               数据层 (MongoDB + 文件系统)                │
└─────────────────────────────────────────────────────────┘
```

### 技术栈说明
- **前端**: Streamlit (快速原型开发)
- **AI引擎**: LangChain + OpenAI/DeepSeek
- **数据存储**: MongoDB (结构化数据)
- **日志系统**: Python logging

## 核心模块

### 1. 用户认证模块

```python
class AuthManager:
    """用户认证管理器"""
    
    def __init__(self):
        self.users = {}
    
    def login(self, phone, user_type, company=None):
        """用户登录"""
        # 验证手机号
        if not self._validate_phone(phone):
            raise ValueError("无效的手机号")
        
        # 创建用户会话
        session = {
            "phone": phone,
            "user_type": user_type,
            "company": company,
            "login_time": datetime.now(),
            "session_id": self._generate_session_id()
        }
        
        return session
    
    def _validate_phone(self, phone):
        """验证手机号格式"""
        pattern = r'^1[3-9]\d{9}$'
        return bool(re.match(pattern, phone.replace(" ", "").replace("-", "")))
    
    def _generate_session_id(self):
        """生成会话ID"""
        return hashlib.md5(f"{datetime.now()}{random.random()}".encode()).hexdigest()
```

### 2. 知识库管理模块

```python
class KnowledgeBase:
    """知识库管理系统"""
    
    def __init__(self):
        self.kb = {
            "电商用户": {},
            "企业用户": {}
        }
    
    def add_knowledge(self, user_type, question, answer):
        """添加知识条目"""
        self.kb[user_type][question] = answer
    
    def search(self, user_type, query):
        """搜索知识库"""
        kb = self.kb.get(user_type, {})
        
        # 精确匹配
        if query in kb:
            return kb[query]
        
        # 模糊匹配
        for key, value in kb.items():
            if query in key or key in query:
                return value
        
        return None
    
    def load_from_db(self):
        """从数据库加载知识库"""
        # TODO: 从MongoDB加载
        pass
```

### 3. AI对话引擎

```python
class AIEngine:
    """AI对话引擎"""
    
    def __init__(self, api_key, model="gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def generate_response(self, user_input, user_type, context=None):
        """生成AI回复"""
        system_message = system_messages.get(user_type, "")
        
        messages = [{"role": "system", "content": system_message}]
        
        # 添加上下文
        if context:
            messages.extend(context)
        
        messages.append({"role": "user", "content": user_input})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    def analyze_sentiment(self, text):
        """情感分析"""
        # 使用AI分析用户情感
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "分析文本的情感倾向,返回 positive/neutral/negative"},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
```

### 4. 对话管理模块

```python
class ConversationManager:
    """对话管理器"""
    
    def __init__(self):
        self.conversations = {}
    
    def add_message(self, session_id, role, content):
        """添加消息"""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.conversations[session_id].append(message)
        
        # 保存到数据库
        self._save_to_db(session_id, message)
    
    def get_history(self, session_id, limit=10):
        """获取对话历史"""
        return self.conversations.get(session_id, [])[-limit:]
    
    def _save_to_db(self, session_id, message):
        """保存消息到数据库"""
        # TODO: 保存到MongoDB
        pass
```

## API接口

### 1. 对话接口

**POST /api/chat**

请求:
```json
{
  "session_id": "abc123",
  "message": "如何查询订单?",
  "user_type": "电商用户"
}
```

响应:
```json
{
  "success": true,
  "reply": "您可以通过订单号在官网查询订单状态...",
  "timestamp": "2026-09-09T10:30:00",
  "message_id": "msg_123"
}
```

### 2. 用户认证接口

**POST /api/login**

请求:
```json
{
  "phone": "13800138000",
  "user_type": "电商用户",
  "company": "XX公司"
}
```

响应:
```json
{
  "success": true,
  "session_id": "sess_abc123",
  "user_info": {
    "phone": "13800138000",
    "user_type": "电商用户"
  }
}
```

### 3. 知识库查询接口

**GET /api/knowledge/{question}**

响应:
```json
{
  "question": "如何查询订单?",
  "answer": "您可以通过订单号在官网查询...",
  "user_type": "电商用户"
}
```

## 数据库设计

### MongoDB集合

#### 1. users (用户表)
```json
{
  "_id": ObjectId,
  "phone": "13800138000",
  "user_type": "电商用户",
  "company": "XX公司",
  "created_at": ISODate("2026-09-09T10:00:00"),
  "updated_at": ISODate("2026-09-09T10:00:00")
}
```

#### 2. conversations (对话记录)
```json
{
  "_id": ObjectId,
  "session_id": "sess_abc123",
  "user_id": ObjectId,
  "messages": [
    {
      "role": "user",
      "content": "如何查询订单?",
      "timestamp": ISODate("2026-09-09T10:05:00")
    },
    {
      "role": "assistant",
      "content": "您可以通过...",
      "timestamp": ISODate("2026-09-09T10:05:02")
    }
  ],
  "created_at": ISODate("2026-09-09T10:05:00")
}
```

#### 3. knowledge_base (知识库)
```json
{
  "_id": ObjectId,
  "user_type": "电商用户",
  "question": "如何查询订单?",
  "answer": "您可以通过订单号...",
  "category": "订单管理",
  "created_at": ISODate("2026-09-09T09:00:00"),
  "updated_at": ISODate("2026-09-09T09:00:00")
}
```

#### 4. analytics (分析数据)
```json
{
  "_id": ObjectId,
  "date": ISODate("2026-09-09"),
  "total_conversations": 100,
  "avg_response_time": 2.5,
  "satisfaction_rate": 0.95,
  "common_questions": ["订单查询", "物流跟踪", ...]
}
```

## 安全机制

### 1. 输入验证
```python
def validate_input(user_input, max_length=1000):
    """输入验证"""
    # 长度检查
    if len(user_input) > max_length:
        raise ValueError(f"输入过长,最大{max_length}字符")
    
    # XSS防护
    if "<script>" in user_input.lower():
        raise ValueError("包含非法字符")
    
    # 敏感词过滤
    sensitive_words = ["admin", "password", "root"]
    if any(word in user_input.lower() for word in sensitive_words):
        raise ValueError("包含敏感词汇")
    
    return True
```

### 2. API密钥管理
```python
# 使用环境变量
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 定期轮换密钥
def rotate_api_key():
    """API密钥轮换"""
    # 实现密钥轮换逻辑
    pass
```

### 3. 会话安全
```python
def generate_secure_token():
    """生成安全令牌"""
    return secrets.token_urlsafe(32)

def verify_token(token):
    """验证令牌"""
    # 验证逻辑
    pass
```

## 部署方案

### 1. 本地开发
```bash
# 启动应用
streamlit run app.py --server.port 8501
```

### 2. Docker部署
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8501

# 启动应用
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 3. Kubernetes部署
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-customer-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-customer-service
  template:
    metadata:
      labels:
        app: ai-customer-service
    spec:
      containers:
      - name: streamlit
        image: ai-customer-service:latest
        ports:
        - containerPort: 8501
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: ai-secrets
              key: openai-api-key
---
apiVersion: v1
kind: Service
metadata:
  name: ai-customer-service
spec:
  selector:
    app: ai-customer-service
  ports:
  - port: 80
    targetPort: 8501
  type: LoadBalancer
```

### 4. CI/CD流程
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest
    
    - name: Deploy to Streamlit Cloud
      run: |
        # 部署命令
```

## 性能优化

### 1. 缓存策略
```python
@st.cache_data(ttl=3600)  # 缓存1小时
def get_cached_response(question, user_type):
    return get_ai_response(question, user_type)
```

### 2. 异步处理
```python
import asyncio

async def async_ai_response(question, user_type):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None, 
        get_ai_response, 
        question, 
        user_type
    )
    return response
```

### 3. 负载均衡
- 使用Nginx进行负载均衡
- 部署多个实例
- 数据库读写分离

## 监控与日志

### 日志配置
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### 监控指标
- 响应时间
- API调用次数
- 错误率
- 用户满意度
- 系统资源使用率

---

**文档版本**: v1.0
**最后更新**: 2026-09-09
