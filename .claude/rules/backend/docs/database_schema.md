# 数据库架构与数据规范 (Neon)

## 1. 连接信息
- 数据源：Neon Serverless PostgreSQL
- 模式：请使用 SQLAlchemy 的 `create_engine` 进行连接池管理。

## 2. 表结构定义 (Schema Context)
**重要**：这是 AI 理解数据的唯一来源，请确保 LlamaIndex 的 `TableContext` 包含以下描述。

### 表 A: `patients` (患者信息)
- `id_number` (PK, VARCHAR): 患者唯一标识（身份证号）。
- `name`: 姓名。
- `doctor`: 责任医生。

### 表 B: `medical_records` (检查记录)
- `id` (PK, SERIAL): 自增主键。
- `id_number` (FK): 关联 `patients` 表。
- `assessment_time` (TIMESTAMP): **关键时序字段**。
  - AI 规则：当用户查询“最近”、“趋势”、“上个月”时，必须使用此字段进行 `ORDER BY` 或 `WHERE` 过滤。
- `systolic_blood_pressure` / `diastolic_pressure`: 血压数据 (Numeric)。
- `hba1c`: 糖化血红蛋白 (Numeric)。
- `ldl_c`: 低密度脂蛋白 (Numeric, 可能包含 NULL)。
- `risk_level`: 风险等级 (String: '低危', '高危', '极高危')。

## 3. 数据处理规则
- **空值处理**: `ldl_c` 等字段可能为 NULL，聚合计算（如平均值）时需忽略 NULL。
- **时间格式**: 数据库存储为 UTC，API 返回时请保持 ISO 8601 格式，由前端转换为本地时间。