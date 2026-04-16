# AI Partner 🤖

一个基于 Streamlit + 大模型 API 的 AI 智能伴侣应用，支持多会话管理、个性化角色设定，以及流式对话体验。

---

## ✨ 功能

- 💬 多会话聊天（支持历史记录查看与切换）
- 🧠 自定义 AI 伴侣昵称与性格
- ⚡ 流式输出 AI 回复（模拟真实对话）
- 💾 会话本地持久化（JSON 存储）
- 🗂️ 历史会话管理（加载 / 删除 / 高亮当前会话）

---

## 🛠 技术栈

- Python
- Streamlit（前端 UI 与交互）
- OpenAI / DeepSeek API（大模型调用）
- JSON（本地数据存储）

---

## 📁 项目结构

```text
ai-partner/
│
├── ai_partner_project.py   # 主程序（AI伴侣应用）
├── sessions/               # 会话数据（自动生成）
├── README.md
```
---

## 🚀 如何运行

### 1. 安装依赖

```bash
pip install streamlit openai
```

### **2.配置 API Key（以 DeepSeek 为例)**
- Mac / Linux：
```bash
export DEEPSEEK_API_KEY=你的APIKey
```
- Windows：
```bash
set DEEPSEEK_API_KEY=你的APIKey
```

### **3. 运行项目指令**
```bash
streamlit run ai_partner_project.py
```



