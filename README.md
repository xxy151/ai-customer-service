# AI智能客服助手

一个基于Streamlit的AI智能客服系统，支持微信小程序接入，主要服务电商用户和企业用户。

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置环境
编辑 `.env` 文件，填入你的API密钥:
```env
OPENAI_API_KEY=your_openai_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

### 运行应用
```bash
streamlit run app.py
```

访问 http://localhost:8501

## 📁 项目结构

```
AI客服助手项目/
├── app.py              # 主应用文件
├── requirements.txt    # 依赖包列表
├── .env               # 环境配置
├── .gitignore         # Git忽略文件
├── README.md          # 本文件
├── app.log           # 运行日志
└── docs/             # 文档目录
    ├── README_CHINESE.md      # 详细中文文档
    ├── TECHNICAL.md           # 技术文档
    ├── WECHAT_MINIPROGRAM.md  # 小程序集成指南
    └── INTERVIEW_PREP.md      # 面试答辩准备
```

## 🎯 核心功能

- ✨ **双用户类型**: 电商用户、企业用户
- 📚 **知识库系统**: 12+常见问题快速响应
- 🤖 **AI智能对话**: 基于GPT-4的自然语言交互
- 📱 **微信小程序**: 支持无缝接入
- ⚡ **快速响应**: 知识库<100ms, AI<5秒
- 🔒 **安全可靠**: 多层安全防护

## 📊 技术栈

- **前端**: Streamlit, Streamlit-chat
- **AI**: LangChain, OpenAI GPT-4, DeepSeek
- **后端**: Python 3.10+, Flask
- **数据库**: MongoDB
- **部署**: Streamlit Cloud, Docker

## 💡 项目亮点

- ⏱️ **2小时原型**: 快速开发能力
- 🎯 **精准定位**: 电商+企业双赛道
- 📈 **性能优异**: 80%问题毫秒级响应
- 🔄 **易于扩展**: 模块化设计
- 📱 **生态集成**: 微信小程序支持

## 📖 详细文档

- [完整中文文档](docs/README_CHINESE.md)
- [技术文档](docs/TECHNICAL.md)
- [小程序集成指南](docs/WECHAT_MINIPROGRAM.md)
- [面试答辩准备](docs/INTERVIEW_PREP.md)

## 🎥 演示

### 登录界面
选择用户类型,输入手机号,点击微信登录

### 聊天界面
- 输入问题,获取智能回复
- 侧边栏常见问题快速访问
- 用户类型随时切换
- 对话记录自动保存

## 🤝 贡献

欢迎提交Issue和Pull Request!

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

MIT License - 自由使用、修改和分发

## 📞 联系方式

- 邮箱: support@example.com
- GitHub: [项目地址]

---

**版本**: v1.0.0  
**最后更新**: 2026-09-09
