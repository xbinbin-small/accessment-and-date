# API 接口规范与 Text-to-SQL 逻辑

## 1. 核心接口
- `POST /api/agent/chat`: 
  - 接收自然语言，返回 AI 分析结果和生成的 SQL（用于调试）。
  - 内部流程：Query -> LlamaIndex -> DeepSeek -> SQL -> Neon -> Result -> DeepSeek Summary -> Response。
- `GET /api/patients/{doctor_id}`: 获取医生名下的患者列表。
- `GET /api/records/{patient_id}`: 获取用于前端绘图的历史数据。

## 2. Text-to-SQL 限制 (Guardrails)
- **Read-Only**: 生成的 SQL 必须是 `SELECT` 语句，严禁 `DROP`, `DELETE`, `UPDATE`。
- **Limit**: 为了防止 Token 溢出，所有列表查询默认 `LIMIT 100`。