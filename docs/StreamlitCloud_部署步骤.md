# 部署到 Streamlit Cloud（免费，生成简历链接）保姆级步骤

目标：把网页版 AI 客服部署到公网，得到链接如：
`https://你的用户名-ai-kehu-xxxx.streamlit.app`，放进简历。

## 你需要准备的（免费，一次性）
1. **GitHub 账号**：https://github.com 注册（QQ 邮箱即可，免费）。
2. 注册后能登录 GitHub 网页、能看到自己的头像。

---

## 第 1 步：在 GitHub 建一个公开仓库
1. 登录 GitHub → 右上角 **+ → New repository**。
2. Repository name 填：`ai-customer-service`（随便起英文名都行）。
3. **Public**（公开）→ 不要勾选任何初始化选项（README/LICENSE 都不勾）→ Create repository。
4. 创建后页面会显示一段命令。**把页面里 `git remote add origin ...` 那一行复制下来**（形如：
   `git remote add origin https://github.com/你的用户名/ai-customer-service.git`），发给我。

## 第 2 步：把项目推到 GitHub（我会帮你执行大部分）
我会在你的项目目录执行：
```
git remote add origin <你发的地址>
git branch -M main
git push -u origin main
```
推送前我已确认 `.env`（含 API Key）、数据库文件不会被上传——它们已在 `.gitignore` 里。

## 第 3 步：部署到 Streamlit Cloud
1. 打开 https://share.streamlit.io 用 **GitHub 账号**登录（授权一次）。
2. 点 **New app**（或 Create app）：
   - Repository：选 `你的用户名/ai-customer-service`
   - Branch：`main`
   - Main file path：填 `app.py`
   - 点 **Deploy**。
3. 等 1~3 分钟，显示 running 后点 **View app** 就是你的公网链接。
4. 此时还缺 API Key（云端没有你的 .env）。

## 第 4 步：把百炼 API Key 配到云端（Secrets）
1. 在 Streamlit Cloud 你的 app 页面 → 右上角 **⋮ → Settings → Secrets**。
2. 粘贴以下内容（把 `sk-你的key` 换成你的百炼 key）：
```
DASHSCOPE_API_KEY=sk-你的key
LLM_MODEL=qwen3-max
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```
3. 保存后点 **Rerun / Restart app**。

## 第 5 步：验证 + 收进简历
- 打开链接 → 微信登录（随便填手机号）→ 问“订单查询”（秒回=知识库）和“你们几点营业”（几秒=真 AI）。
- 简历项目条目里加一行：
  > 在线 Demo：https://你的用户名-xxxx.streamlit.app（可直接体验）

---

## 常见问题
| 问题 | 解决 |
|---|---|
| Deploy 报错找不到 app.py | Main file path 填 `app.py`（不是完整路径） |
| 页面能开但回复是“兜底话术” | Secrets 没配对 → 重配第 4 步并 Restart |
| 国内访问慢/打不开 | 属网络原因，一般刷新可开；面试建议提前演示 |
| 代码公开了没关系吗？ | 简历项目公开是加分项；你的 API Key 未上传，安全 |

**做到哪步卡住，把屏幕文字发我。**
