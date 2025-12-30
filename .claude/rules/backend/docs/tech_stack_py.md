# 后端技术栈与 AI 配置

## 1. 核心语言
- **Language**: Python 3.10+
- **Framework**: FastAPI (异步高性能 Web 框架)
- **Package Manager**: Poetry 或 pip (requirements.txt)

## 2. AI 引擎配置
- **Framework**: LlamaIndex (核心库, `llama-index-core`, `llama-index-llms-deepseek` 等)
- **Model Provider**: DeepSeek (DeepSeek-V3 或 R1)
- **Reasoning**:
  - 使用 DeepSeek 进行意图识别和医学建议生成。
  - 使用 DeepSeek 进行 Text-to-SQL 转换（因其 Coding 能力强）。

## 3. 数据库驱动
- **ORM**: SQLAlchemy (用于基础 CRUD)
- **Driver**: `psycopg2-binary` (用于连接 Neon PostgreSQL)