# Changelog

所有重要的项目变更都会记录在这个文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
项目版本遵循 [语义化版本 (Semantic Versioning)](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2026-06-12

### Added
- ✨ 新增健康检查端点 `/health`，返回服务状态信息
- ✨ 新增根端点 `/`，显示服务说明页面
- ✨ 新增 `.env.example` 配置模板文件
- 📝 补充 AI 编辑器配置示例（本地 stdio 和远程 HTTP 模式）
- 📝 重构 README 文档结构，优化阅读体验
- 📝 完善 `.gitignore` 注释说明

### Changed
- 🔧 使用 FastMCP 官方的 `custom_route` 方式添加自定义端点
- 📝 更新 README 的"运行"章节，增加健康检查说明
- 📝 调整文档顺序，将用户最关注的配置示例提前

### Technical
- 🐳 Dockerfile 默认使用 HTTP Stream 模式启动
- 🔧 所有自定义端点使用 Starlette 响应类型（JSONResponse、PlainTextResponse）

---

## [0.1.0] - 初始版本

### Added
- 🎉 基础 MCP 服务器实现
- 🛠️ `say_hello` 工具：向单个用户问候
- 🛠️ `say_hello_multiple` 工具：同时向多个用户问候
- 📚 MCP Resource：提供使用文档
- 💬 MCP Prompt：提供问候消息模板
- 🐳 Docker 支持
- 📦 pyproject.toml 项目配置
- 📝 基础 README 文档
