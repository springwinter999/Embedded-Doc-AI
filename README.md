# Embedded Doc AI

AI 辅助嵌入式文档查询系统 — 基于 RAG（检索增强生成）架构，支持上传 PDF 技术手册并通过自然语言提问，由 LLM 结合文档内容生成回答。

## 技术栈

| 层 | 技术 |
|---|---|
| 后端框架 | FastAPI (Python 3.13) |
| 前端框架 | Next.js 16 + React 19 + TypeScript |
| 样式 | Tailwind CSS v4 |
| 嵌入模型 | BAAI/bge-base-zh-v1.5 (sentence-transformers) |
| 向量数据库 | ChromaDB |
| LLM | DeepSeek Chat API |
| 对话存储 | SQLite |
| PDF 解析 | pdfplumber |

## 项目结构

```
search/
├── backend/                          # FastAPI 后端
│   ├── main.py                       # 应用入口，CORS 配置，路由注册
│   ├── config.py                     # 配置常量（路径、模型名称、分块参数等）
│   ├── requirements.txt              # Python 依赖
│   ├── routers/
│   │   ├── chat.py                   # POST /api/chat — 发送消息
│   │   ├── conversation.py           # GET/DELETE /api/conversations — 对话管理
│   │   └── document.py               # 文档上传、索引、列表、删除
│   ├── services/
│   │   ├── embedding.py              # 文本嵌入（GPU 加速）
│   │   ├── parser.py                 # PDF 解析 + 文本分块
│   │   ├── vector_store.py           # ChromaDB 增删查操作
│   │   ├── llm.py                    # DeepSeek Chat API 调用
│   │   └── auth.py                   # API Key 验证
│   ├── db/
│   │   ├── chroma.py                 # ChromaDB 客户端与集合管理
│   │   └── sqlite.py                 # SQLite 对话数据库
│   ├── models/
│   │   ├── chat.py                   # 聊天相关数据模型
│   │   └── conversation.py           # 对话数据模型
│   ├── tests/                        # 后端测试
│   ├── data/                         # 上传的 PDF 文件（gitignore）
│   ├── chroma_db/                    # ChromaDB 持久化数据（gitignore）
│   └── models_cache/                 # 缓存的嵌入模型（gitignore）
├── frontend/                         # Next.js 前端
│   ├── app/
│   │   ├── layout.tsx                # 根布局（zh-CN）
│   │   ├── page.tsx                  # 主页面（单页应用入口）
│   │   └── globals.css               # CSS 变量 + Tailwind 导入
│   ├── components/
│   │   ├── ChatPanel.tsx             # 消息展示区域
│   │   ├── ChatInput.tsx             # 输入框 + 发送按钮
│   │   ├── ConversationList.tsx      # 对话列表侧边栏
│   │   ├── SourceBadge.tsx           # 来源引用标签
│   │   └── DocumentManager.tsx       # 文档管理面板（上传/删除）
│   ├── hooks/
│   │   ├── useChat.ts               # 聊天状态管理
│   │   ├── useConversations.ts      # 对话列表管理
│   │   └── useDocuments.ts          # 文档管理状态
│   ├── lib/
│   │   └── api.ts                    # API 客户端（类型定义 + 请求函数）
│   └── package.json
├── .gitignore
└── README.md
```

## 功能

- **对话问答**：基于索引的 PDF 文档进行语义搜索，由 DeepSeek 结合检索结果生成回答，附来源引用
- **文档管理**：前端上传 PDF 自动解析、GPU 嵌入、存入向量数据库；支持按文件名删除索引
- **对话管理**：多轮对话，历史持久化，可删除历史对话

## 前置条件

- Python 3.11+（推荐 3.13）
- Node.js 20+
- NVIDIA GPU + CUDA 12.6+（CPU 也可运行，但嵌入速度较慢）
- DeepSeek API Key

## 快速启动

### 1. 克隆并配置

```bash
git clone <repo-url>
cd search
```

在项目根目录创建 `.env` 文件：

```
DEEPSEEK_API_KEY=你的DeepSeek_API_Key
```

### 2. 安装依赖

**后端：**

```bash
cd backend
pip install -r requirements.txt

# 如需 GPU 加速（推荐），安装 CUDA 版 PyTorch：
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```

首次运行时会自动从 ModelScope 下载嵌入模型（BAAI/bge-base-zh-v1.5）到 `backend/models_cache/`。

**前端：**

```bash
cd frontend
npm install
```

### 3. 启动项目

**启动后端**（终端 1）：

```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**启动前端**（终端 2）：

```bash
cd frontend
npm run dev
```

### 4. 使用

- 前端访问 `http://localhost:3000`
- 后端 API 文档 `http://localhost:8000/docs`
- 在左侧"文档管理"面板上传 PDF 文件，自动 GPU 索引
- 创建新对话，输入问题，AI 基于文档内容回答

## API 端点概览

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/health` | 健康检查 |
| POST | `/api/chat` | 发送消息，获取 AI 回答 |
| GET | `/api/chat/{id}` | 获取对话历史 |
| GET | `/api/conversations` | 获取对话列表 |
| DELETE | `/api/conversations/{id}` | 删除对话 |
| GET | `/api/documents` | 列出已索引文档 |
| POST | `/api/documents/upload` | 上传并索引 PDF |
| DELETE | `/api/documents/{filename}` | 删除文档索引 |
| POST | `/api/documents/index` | 批量索引 data/ 目录下所有 PDF |
