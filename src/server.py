#!/usr/bin/env python3
"""
Simple Hello MCP Server

此模块提供一个接收姓名并用英语打招呼的简单 MCP 服务器。

主要功能:
    - 单人问候: 向一个人说 "Hello, {name}!"
    - 多人问候: 同时向多个人问候
    - MCP 协议: 支持 Tools、Resources、Prompts
    - Streamable HTTP 传输: 支持 Cloud Run 等无服务器环境

使用示例:
    HTTP 模式运行:
        $ python src/server.py --http-stream
        -> http://localhost:8080/mcp
    
    stdio 模式运行:
        $ python src/server.py
    
    工具调用:
        {"name": "say_hello", "arguments": {"name": "John"}}
        -> "Hello, John!"

作者: MCP Hello Team
版本: 1.0.0
许可证: MIT
"""

import os

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

# ============================================================================
# FastMCP 服务器创建
# ============================================================================

mcp = FastMCP(
    name="mcp-hello",
    instructions="一个接收姓名并用英语打招呼的简单 MCP 服务器。",
    stateless_http=True,
    json_response=True,
    host="0.0.0.0",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False,
    ),
)


# ============================================================================
# Tools (工具)
# ============================================================================

@mcp.tool()
def say_hello(name: str) -> str:
    """
    接收姓名并用英语问候。
    
    返回简单格式的问候语，如果姓名为空则返回默认消息。
    
    Args:
        name: 要问候的人的姓名（例如："John", "Jane", "Bob"）
    
    Returns:
        "Hello, {name}!" 格式的问候语字符串
    
    Examples:
        >>> say_hello("John")
        'Hello, John!'
    """
    if not name or name.strip() == "":
        return "Hello!"
    
    return f"Hello, {name}!"


@mcp.tool()
def say_hello_multiple(names: list[str]) -> str:
    """
    同时向多个人问候。
    
    接收姓名列表，为每个姓名生成问候语，
    并用项目符号（•）分隔为单个字符串返回。
    
    Args:
        names: 要问候的人的姓名列表（例如：["John", "Jane", "Bob"]）
    
    Returns:
        每个问候语按换行分隔的字符串
    
    Examples:
        >>> say_hello_multiple(["John", "Jane"])
        '• Hello, John!\\n• Hello, Jane!'
    """
    if not names:
        return ""
    
    greetings = []
    for name in names:
        greeting = say_hello(name)
        greetings.append(f"• {greeting}")
    
    return "\n".join(greetings)


# ============================================================================
# Resources (资源)
# ============================================================================

@mcp.resource("docs://hello/readme")
def get_readme() -> str:
    """
    提供 Hello MCP 服务器使用指南。
    
    Returns:
        Markdown 格式的文档
    """
    return """# Hello MCP Server Documentation

## 概述
一个接收姓名并用英语问候的简单 MCP 服务器。

## 可用工具

### say_hello
向一个人问候。

**参数:**
- `name` (string, 必填): 要问候的人的姓名

**示例:**
```json
{
  "name": "John"
}
```

**结果:**
```
Hello, John!
```

### say_hello_multiple
同时向多个人问候。

**参数:**
- `names` (array, 必填): 要问候的人的姓名列表

**示例:**
```json
{
  "names": ["John", "Jane", "Bob"]
}
```

**结果:**
```
• Hello, John!
• Hello, Jane!
• Hello, Bob!
```

## 使用方法

1. 在 MCP 客户端连接服务器
2. 调用 `say_hello` 或 `say_hello_multiple` 工具
3. 查看问候语结果

## 技术栈
- Python 3.11+
- MCP Python SDK (FastMCP)
- Pydantic (类型校验)
- Starlette + Uvicorn (HTTP Stream)
"""


# ============================================================================
# Prompts (提示词)
# ============================================================================

@mcp.prompt()
def greeting_message(recipient: str) -> str:
    """
    提供问候消息撰写模板。
    
    Args:
        recipient: 要问候的人的姓名
    
    Returns:
        给 AI 助手的提示词模板
    """
    greeting = say_hello(recipient)
    
    return f"""请撰写发送给 {recipient} 的问候消息。

以下列格式开头：
{greeting}

消息中应包含：
1. 温馨的问候
2. 简单的介绍或目的
3. 礼貌的结尾

语气：亲切且礼貌
长度：3-5 个句子
"""


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    """
    MCP 服务器的主入口点。
    
    通过命令行参数选择传输模式：
    - --http-stream: HTTP Stream 模式
    - 默认值: stdio 模式（标准输入输出）
    
    环境变量：
        PORT: HTTP 服务器端口（默认值：8080）
    
    使用示例：
        HTTP 模式：
            $ python src/server.py --http-stream
            $ PORT=3000 python src/server.py --http-stream
        
        stdio 模式：
            $ python src/server.py
    """
    import sys
    
    if "--http-stream" in sys.argv:
        port = int(os.environ.get("PORT", 8080))
        mcp.settings.port = port
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
