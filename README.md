# 👋 MCP Hello Server (Python)

简单的 Hello MCP 服务器 - 接收输入的姓名，并用英语打招呼！

## 📂 结构

```
mcp-hello-py/
├── src/
│   ├── __init__.py       # 包初始化
│   └── server.py         # MCP 服务器
├── .env                  # 环境变量配置（本地）
├── .env.example          # 环境变量配置模板
├── requirements.txt      # 依赖项
├── pyproject.toml        # 项目元数据
├── Dockerfile            # Docker 配置
└── README.md             # 此文件
```

## ✨ 主要功能

- **say_hello**: 以 `"Hello, {name}!" 的格式打招呼
- **say_hello_multiple**: 一次向多个人打招呼
- **MCP 协议**: 支持 Tools、Resources、Prompts

## 📦 安装

```bash
# 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

## 🔧 环境变量配置

创建 `.env` 文件：

```bash
# .env 文件内容
PORT=8080
```

## 🚀 运行

### 🌐 Streamable HTTP 模式 (Cloud Run, Web)
```bash
python3 src/server.py --http-stream

# 使用自定义端口
PORT=3000 python3 src/server.py --http-stream
```

启动后有以下端点可用：
- **MCP 协议**: `http://localhost:8080/mcp`
- **健康检查**: `http://localhost:8080/health`
- **服务信息**: `http://localhost:8080/`

健康检查返回示例：
```json
{
  "status": "healthy",
  "service": "mcp-hello",
  "version": "1.0.0"
}
```

## 🔌 AI 编辑器配置示例

### 1️⃣ 本地 stdio 模式配置
适用于本地运行服务器的情况，直接通过 stdin/stdout 通信：

```json
{
  "mcpServers": {
    "mcp-hello": {
      "command": "/Users/wuxian/.pyenv/shims/python3",
      "args": [
        "/Users/wuxian/Desktop/codes/mcp-hello-py/src/server.py"
      ]
    }
  }
}
```

### 2️⃣ 远程 HTTP 模式配置
适用于服务器部署在局域网或公网的情况，通过 HTTP 连接：

```json
{
  "mcpServers": {
    "mcp-hello-remote": {
      "url": "http://192.168.100.5:8080/mcp"
    }
  }
}
```

> 注意：请将 `http://192.168.100.5:8080/mcp` 替换为你实际的服务器地址。

## 📡 传输模式

| 模式 | 使用场景 | 端点 |
|------|--------|-----------|
| stdio | Claude Desktop, MCP Inspector | stdin/stdout |
| Streamable HTTP | Cloud Run, Web | `POST /mcp` |

## 🏗️ 架构

```
┌─────────────┐       ┌─────────────────┐
│  Postman /  │ ───▶  │  MCP Hello      │
│  MCP Client │       │  Server         │
│             │ ◀───  │  (Python)       │
└─────────────┘       └─────────────────┘
     HTTP                  MCP
   POST /mcp             Protocol
```

## 🧪 测试（Postman）

### 📋 Headers 设置（所有请求必填）

| Header | Value |
|--------|-------|
| `Content-Type` | `application/json` |
| `Accept` | `application/json` |

### 1️⃣ 初始化 MCP 服务器

- **Method**: `POST`
- **URL**: `http://localhost:8080/mcp`
- **Body** (raw JSON):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "postman", "version": "1.0.0"}
  }
}
```

### 2️⃣ 查看 Tool 列表

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

### 3️⃣ say_hello 调用

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "say_hello",
    "arguments": {"name": "John"}
  }
}
```

**响应示例:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [{"type": "text", "text": "Hello, John!"}]
  }
}
```

### 4️⃣ say_hello_multiple 调用

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "say_hello_multiple",
    "arguments": {"names": ["John", "Jane", "Bob"]}
  }
}
```

**响应示例:**
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "content": [{"type": "text", "text": "• Hello, John!\n• Hello, Jane!\n• Hello, Bob!"}]
  }
}
```

## ☁️ Cloud Run 部署

### 🧪 测试已部署的服务器

部署 URL 示例: `https://mcp-hello-py-xxxxxx.asia-northeast3.run.app/mcp`

在 Postman 中仅修改 URL 即可用同样方式测试。

### 🔧 环境变量配置（Cloud Run）

| 变量 | 值 | 说明 |
|------|-----|------|
| `PORT` | `8080` | Cloud Run 默认端口（自动设置） |

## 🛠️ MCP Tools

### say_hello

向一个人打招呼。

| 参数 | 类型 | 必填 | 说明 |
|---------|------|------|------|
| `name` | string | 是 | 要问候的人的姓名 |

### say_hello_multiple

同时向多个人打招呼。

| 参数 | 类型 | 必填 | 说明 |
|---------|------|------|------|
| `names` | array | 是 | 姓名列表 |

##  技术栈

- **Python**: 3.11+
- **MCP SDK**: 1.23.0+ (FastMCP)
- **Pydantic**: 2.x
- **Uvicorn**: ASGI 服务器
- **Docker**: 容器化

## 📖 参考

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP 文档](https://github.com/modelcontextprotocol/python-sdk)

## 📄 许可证

MIT License
