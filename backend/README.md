# 后端 - 智能慢病管理系统

基于 FastAPI + LlamaIndex + DeepSeek 的 AI 驱动后端服务

---

## 🚀 快速开始

### 1. 安装依赖

```bash
poetry install
```

### 2. 配置环境变量

复制 `.env.example` 并重命名为 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填写必要的配置：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
NEON_DB_URL=postgresql+psycopg2://user:password@host/database?sslmode=require
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000
```

### 3. 运行服务

```bash
# 方式 1: 使用 main.py
poetry run python -m app.main

# 方式 2: 使用 uvicorn
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问：
- API 服务: `http://localhost:8000`
- API 文档: `http://localhost:8000/docs`
- Redoc 文档: `http://localhost:8000/redoc`

---

## 📚 API 接口

### 1. AI 对话接口

**Endpoint**: `POST /api/agent/chat`

**功能**: 接收自然语言查询，返回 AI 分析结果

**请求体**:
```json
{
  "query": "这位患者最近的血压趋势如何？",
  "patient_id": "330123199001011234"
}
```

**响应**:
```json
{
  "answer": "根据数据分析，该患者最近3次检查的血压呈上升趋势...",
  "generated_sql": "SELECT * FROM medical_records WHERE id_number = '330123199001011234' ORDER BY assessment_time DESC LIMIT 100",
  "data": [...]
}
```

### 2. 患者列表接口

**Endpoint**: `GET /api/patients/{doctor_id}`

**功能**: 获取医生名下的患者列表

**响应**:
```json
[
  {
    "id_number": "330123199001011234",
    "name": "张三",
    "doctor": "doctor_001"
  }
]
```

### 3. 医疗记录接口

**Endpoint**: `GET /api/records/{patient_id}`

**功能**: 获取患者的历史医疗记录

**响应**:
```json
[
  {
    "id": 1,
    "id_number": "330123199001011234",
    "assessment_time": "2024-01-15T10:30:00",
    "systolic_blood_pressure": 135.0,
    "diastolic_pressure": 85.0,
    "hba1c": 6.5,
    "ldl_c": 3.2,
    "risk_level": "低危"
  }
]
```

---

## 🛡️ SQL 安全防护 (Guardrails)

所有 AI 生成的 SQL 查询都会经过严格的安全检查：

1. **Read-Only**: 只允许 `SELECT` 语句
2. **禁止操作**: `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, `CREATE`
3. **强制限制**: 必须包含 `LIMIT` 子句（建议 `LIMIT 100`）

示例：

```python
# ✅ 合法
SELECT * FROM patients WHERE doctor = 'doctor_001' LIMIT 100

# ❌ 非法 - 缺少 LIMIT
SELECT * FROM patients WHERE doctor = 'doctor_001'

# ❌ 非法 - 包含危险操作
DELETE FROM patients WHERE id_number = '...'
```

---

## 🏗️ 项目结构

```
backend/
├── app/
│   ├── api/                    # API 路由
│   │   ├── agent.py           # AI 对话接口
│   │   └── patients.py        # 患者数据接口
│   ├── core/                  # 核心配置
│   │   ├── config.py          # 环境变量配置
│   │   └── database.py        # 数据库连接
│   ├── models/                # 数据库模型
│   │   └── models.py          # SQLAlchemy 模型
│   ├── schemas/               # Pydantic Schema
│   │   └── schemas.py         # 请求/响应模型
│   ├── services/              # 业务逻辑
│   │   └── text_to_sql.py    # Text-to-SQL 服务
│   └── main.py                # 应用入口
├── pyproject.toml             # Poetry 配置
├── .env.example               # 环境变量模板
└── README.md                  # 本文档
```

---

## 🧪 代码质量

### 运行代码格式化

```bash
# Black 格式化
poetry run black app/

# isort 导入排序
poetry run isort app/
```

### 运行代码检查

```bash
# Pylint 检查
poetry run pylint app/

# Mypy 类型检查
poetry run mypy app/
```

### 运行测试

```bash
poetry run pytest
```

---

## 📊 依赖说明

| 依赖 | 版本 | 用途 |
|------|------|------|
| fastapi | ^0.115.0 | Web 框架 |
| uvicorn | ^0.32.0 | ASGI 服务器 |
| sqlalchemy | ^2.0.36 | ORM |
| psycopg2-binary | ^2.9.10 | PostgreSQL 驱动 |
| pydantic | ^2.10.3 | 数据验证 |
| pydantic-settings | ^2.6.1 | 环境变量管理 |
| llama-index-core | ^0.12.0 | AI 编排框架 |
| llama-index-llms-deepseek | ^0.2.3 | DeepSeek 集成 |
| httpx | ^0.28.1 | HTTP 客户端 |

---

## 🔧 开发技巧

### 查看日志

后端使用 Python 的 `logging` 模块，日志级别为 `INFO`。

重要日志包括：
- SQL 查询生成
- SQL 安全检查结果
- 请求处理状态

### 调试 SQL 生成

AI 对话接口返回的 `generated_sql` 字段可用于调试：

```json
{
  "generated_sql": "SELECT * FROM medical_records ..."
}
```

---

## 🚨 常见问题

### 1. 数据库连接失败

**错误**: `Connection refused` 或 `could not translate host name`

**解决**:
- 检查 `NEON_DB_URL` 是否正确
- 确保 Neon 数据库已启动
- 检查网络连接

### 2. DeepSeek API 调用失败

**错误**: `401 Unauthorized` 或 `API key invalid`

**解决**:
- 检查 `DEEPSEEK_API_KEY` 是否正确
- 确认 API Key 是否有效

### 3. CORS 错误

**错误**: `CORS policy: No 'Access-Control-Allow-Origin' header`

**解决**:
- 检查 `ALLOWED_ORIGINS` 环境变量
- 确保前端地址在允许列表中

---

## 📝 开发规范

- 遵循 PEP 8 代码风格
- 所有函数必须包含 Type Hints
- 复杂逻辑需要 Docstring
- 使用 `async/await` 处理 I/O 操作
- 禁止硬编码敏感信息
- 医疗数据必须脱敏处理

---

**Built with ❤️ for better healthcare**
