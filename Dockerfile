# MCP Hello Server - Docker 镜像构建配置
# 构建: docker build -t mcp-hello-py .
# stdio 运行: docker run -it mcp-hello-py
# HTTP 运行: docker run -p 8890:8890 mcp-hello-py

# Python 3.11 Slim 镜像（轻量化）
FROM python:3.11-slim

# 工作目录设置
WORKDIR /app

# 依赖安装（缓存优化）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 源代码复制
COPY . .

# HTTP Stream 端口暴露
EXPOSE 8080

# 环境变量设置（默认值）
ENV PORT=8080

# 服务器启动（默认：HTTP Stream 模式）
CMD ["python", "src/server.py", "--http-stream"]
