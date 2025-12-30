# 安全与配置规范

## 1. 敏感信息管理
- **严禁硬编码**: 任何 API Key、数据库密码、Secret Key 绝对不能出现在代码中。
- **本地开发**: 所有机密信息必须存储在 `.env` 文件中。
- **Git 忽略**: 确保 `.env` 已加入 `.gitignore`。

## 2. 环境变量清单 (Example)
后端 (`backend/.env`):
- `OPENAI_API_KEY` (如果是 DeepSeek 兼容接口，配置此处)
- `DEEPSEEK_API_KEY`
- `NEON_DB_URL` (格式: `postgresql+psycopg2://user:pass@host/db?sslmode=require`)

前端 (`frontend/.env.local`):
- `NEXT_PUBLIC_API_BASE_URL` (后端 API 地址)

## 3. 数据隐私
- 这是一个医疗项目，在 Log 日志中严禁打印患者的真实姓名和完整身份证号。
- API 返回给前端的数据，如非必要，应进行脱敏处理。