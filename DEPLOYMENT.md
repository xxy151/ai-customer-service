# AI智能客服助手 - 部署指南

## 🚀 本地开发部署

### 1. 环境准备

```bash
# 安装Python 3.10+
python --version

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

编辑 `.env` 文件:
```env
OPENAI_API_KEY=your_openai_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
WECHAT_APP_ID=your_wechat_app_id_here
WECHAT_APP_SECRET=your_wechat_app_secret_here
HOST=0.0.0.0
PORT=8501
DEBUG=True
```

### 3. 启动应用

```bash
# 基本启动
streamlit run app.py

# 指定端口
streamlit run app.py --server.port 8502

# 指定主机
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### 4. 访问应用

浏览器访问: `http://localhost:8501`

---

## ☁️ Streamlit Cloud 部署

### 1. 准备工作

1. 创建GitHub账号(如没有)
2. 安装Git
3. 创建GitHub仓库

### 2. 推送代码到GitHub

```bash
# 初始化git仓库(如果还没初始化)
git init
git add .
git commit -m "Initial commit"

# 创建GitHub仓库后,添加远程仓库
git remote add origin https://github.com/yourusername/ai-customer-service.git
git branch -M main
git push -u origin main
```

### 3. 部署到Streamlit Cloud

1. 访问 https://streamlit.io/cloud
2. 登录GitHub账号
3. 点击"New app"
4. 选择仓库和分支
5. 设置:
   - **Main file path**: `app.py`
   - **Python version**: 3.10
6. 点击"Deploy"

### 4. 配置Secrets

1. 在Streamlit Cloud项目页面,点击"⚙️ Settings"
2. 找到"Secrets"部分
3. 添加环境变量:
   ```
   OPENAI_API_KEY="your_api_key"
   DEEPSEEK_API_KEY="your_api_key"
   ```
4. 点击"Save"

### 5. 验证部署

访问生成的URL: `https://yourusername-ai-customer-service.streamlit.app`

---

## 🐳 Docker 部署

### 1. 创建Dockerfile

```dockerfile
# 使用官方Python运行时作为父镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 8501

# 运行应用
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. 创建.dockerignore

```
__pycache__/
*.pyc
.git
.gitignore
.env
venv/
.env.local
*.log
```

### 3. 构建镜像

```bash
# 构建镜像
docker build -t ai-customer-service .

# 查看镜像
docker images
```

### 4. 运行容器

```bash
# 基本运行
docker run -p 8501:8501 ai-customer-service

# 后台运行
docker run -d -p 8501:8501 --name ai-service ai-customer-service

# 挂载配置文件
docker run -d -p 8501:8501 \
  -v $(pwd)/.env:/app/.env \
  --name ai-service \
  ai-customer-service

# 查看日志
docker logs -f ai-service
```

### 5. 访问应用

浏览器访问: `http://localhost:8501`

---

## 🌐 Nginx 反向代理

### 1. 安装Nginx

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx

# CentOS/RHEL
sudo yum install nginx
```

### 2. 配置Nginx

创建配置文件 `/etc/nginx/sites-available/ai-customer-service`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 日志
    access_log /var/log/nginx/ai-customer-service-access.log;
    error_log /var/log/nginx/ai-customer-service-error.log;

    # 反向代理到Streamlit
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 静态文件缓存
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 3. 启用配置

```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/ai-customer-service /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
```

### 4. 配置HTTPS (可选)

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

---

## 🔄 Docker Compose 部署

### 1. 创建docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: ai-customer-service
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
      - HOST=0.0.0.0
      - PORT=8501
    volumes:
      - ./app.log:/app/app.log
    restart: unless-stopped
    networks:
      - ai-network

  nginx:
    image: nginx:alpine
    container_name: ai-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - app
    networks:
      - ai-network

networks:
  ai-network:
    driver: bridge
```

### 2. 创建nginx.conf

```nginx
upstream streamlit_app {
    server app:8501;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://streamlit_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. 启动服务

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart
```

---

## 🗄️ MongoDB 集成

### 1. 安装MongoDB

```bash
# Docker方式
docker run -d -p 27017:27017 --name mongodb mongo

# 本地安装(Windows)
# 下载安装包: https://www.mongodb.com/try/download/community
```

### 2. 配置数据库

```python
# db.py
from pymongo import MongoClient
import os

def get_db():
    """获取数据库连接"""
    client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
    db = client['ai_customer_service']
    return db

def init_collections():
    """初始化集合"""
    db = get_db()
    
    # 用户集合
    if 'users' not in db.list_collection_names():
        db.create_collection('users')
        db.users.create_index('phone', unique=True)
    
    # 对话集合
    if 'conversations' not in db.list_collection_names():
        db.create_collection('conversations')
        db.conversations.create_index('session_id')
    
    # 知识库集合
    if 'knowledge_base' not in db.list_collection_names():
        db.create_collection('knowledge_base')
        db.knowledge_base.create_index([('user_type', 1), ('question', 1)])
```

### 3. 更新app.py

```python
# 在app.py顶部添加
from db import get_db, init_collections

# 初始化数据库
init_collections()
db = get_db()
```

---

## 📊 监控和日志

### 1. 日志配置

```python
import logging
from logging.handlers import RotatingFileHandler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            'app.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### 2. 性能监控

```python
import time
from functools import wraps

def log_execution_time(func):
    """记录函数执行时间"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} executed in {end_time - start_time:.2f}s")
        return result
    return wrapper

@log_execution_time
def get_ai_response(user_input, user_type):
    # ... 函数代码
    pass
```

---

## 🔒 安全加固

### 1. 环境变量安全

```bash
# 不要将.env文件提交到git
echo ".env" >> .gitignore

# 使用环境变量替代硬编码
# ❌ 不推荐
API_KEY = "sk-xxx"

# ✅ 推荐
API_KEY = os.getenv("OPENAI_API_KEY")
```

### 2. 输入验证

```python
import re

def validate_input(user_input, max_length=1000):
    """输入验证"""
    # 长度检查
    if len(user_input) > max_length:
        raise ValueError(f"输入过长,最大{max_length}字符")
    
    # XSS防护
    if "<script>" in user_input.lower():
        raise ValueError("包含非法字符")
    
    # 敏感词过滤
    sensitive_words = ["password", "admin", "root"]
    if any(word in user_input.lower() for word in sensitive_words):
        raise ValueError("包含敏感词汇")
    
    return True
```

### 3. API限流

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/api/chat")
@limiter.limit("10 per minute")
def chat():
    # ... 处理逻辑
    pass
```

---

## 🐛 故障排查

### 问题1: 应用无法启动

**症状**: 端口被占用

**解决**:
```bash
# 查找占用端口的进程
lsof -i :8501  # Linux/Mac
netstat -ano | findstr :8501  # Windows

# 杀死进程
kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows

# 或更换端口
streamlit run app.py --server.port 8502
```

### 问题2: 依赖安装失败

**解决**:
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 逐个安装
pip install streamlit
pip install streamlit-chat
# ...
```

### 问题3: API调用失败

**检查**:
1. API密钥是否正确
2. 网络连接是否正常
3. API配额是否用完
4. 查看日志文件 `app.log`

### 问题4: Docker容器无法访问

**解决**:
```bash
# 检查容器状态
docker ps -a

# 查看容器日志
docker logs ai-customer-service

# 重启容器
docker restart ai-customer-service

# 重新构建
docker-compose build --no-cache
```

---

## 📈 性能优化

### 1. 启用缓存

```python
@st.cache_data(ttl=3600)  # 缓存1小时
def get_cached_response(question, user_type):
    return get_ai_response(question, user_type)
```

### 2. 数据库索引

```python
# 为常用查询字段创建索引
db.conversations.create_index([('user_id', 1), ('created_at', -1)])
db.knowledge_base.create_index([('user_type', 1), ('question', 1)])
```

### 3. 异步处理

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

### 4. 负载均衡

部署多个实例,使用Nginx负载均衡:

```nginx
upstream ai_service {
    server localhost:8501;
    server localhost:8502;
    server localhost:8503;
}

server {
    location / {
        proxy_pass http://ai_service;
    }
}
```

---

## 📞 技术支持

- **文档**: 查看docs目录下的详细文档
- **日志**: 查看 `app.log` 文件
- **Issues**: 提交GitHub Issues
- **邮件**: support@example.com

---

**最后更新**: 2026-09-09  
**版本**: v1.0.0
