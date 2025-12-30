"""
LlamaIndex Text-to-SQL 引擎服务

使用 DeepSeek 进行自然语言转 SQL 查询
"""
import logging
from typing import Any, Dict, List, Optional

from llama_index.core import SQLDatabase, VectorStoreIndex
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.llms.openai import OpenAI
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SQLGuardrails:
    """SQL 安全防护规则"""

    @staticmethod
    def validate_sql(sql_query: str) -> tuple[bool, str]:
        """
        验证 SQL 是否符合安全规则

        Args:
            sql_query: 生成的 SQL 查询

        Returns:
            (是否合法, 错误信息)
        """
        # 转换为小写便于检查
        sql_lower = sql_query.lower().strip()

        # 规则1：必须是 SELECT 语句
        if not sql_lower.startswith("select"):
            return False, "只允许执行 SELECT 查询"

        # 规则2：禁止危险操作
        dangerous_keywords = ["drop", "delete", "update", "insert", "alter", "truncate", "create"]
        for keyword in dangerous_keywords:
            if keyword in sql_lower:
                return False, f"禁止使用 {keyword.upper()} 操作"

        # 规则3：必须有 LIMIT 限制（防止 Token 溢出）
        if "limit" not in sql_lower:
            return False, "查询必须包含 LIMIT 限制（建议 LIMIT 100）"

        return True, ""


class TextToSQLService:
    """Text-to-SQL 服务"""

    def __init__(self) -> None:
        """初始化 Text-to-SQL 引擎"""
        # 初始化 DeepSeek LLM（使用 OpenAI 兼容接口）
        self.llm = OpenAI(
            api_key=settings.deepseek_api_key,
            api_base="https://api.deepseek.com",
            model="gpt-4",  # LlamaIndex需要识别的模型名，实际使用deepseek
            temperature=0.1,  # 低温度保证 SQL 生成的准确性
            additional_kwargs={"model": "deepseek-chat"},  # 实际发送给DeepSeek的模型名
        )

        # 初始化 SQL 数据库连接
        self.sql_database = SQLDatabase(engine)

        # 创建查询引擎（禁用 embedding，Text-to-SQL 不需要）
        from llama_index.core.utilities.sql_wrapper import SQLDatabase as LISQLDatabase
        from llama_index.core.embeddings import MockEmbedding

        self.query_engine = NLSQLTableQueryEngine(
            sql_database=self.sql_database,
            llm=self.llm,
            tables=["patients", "medical_records"],  # 指定可查询的表
            embed_model=MockEmbedding(embed_dim=1),  # 使用mock embedding避免依赖
        )

        # 配置表上下文（帮助 AI 理解数据）
        self._setup_table_context()

    def _setup_table_context(self) -> None:
        """
        设置表上下文描述

        根据 database_schema.md 提供表和字段的语义信息
        """
        table_context = """
        数据库包含两张表：

        1. patients（患者信息表）：
           - id_number: 患者唯一标识（身份证号）
           - name: 姓名
           - doctor: 责任医生

        2. medical_records（检查记录表）：
           - id: 自增主键
           - id_number: 患者身份证号（外键，关联 patients 表）
           - assessment_time: 检查时间（TIMESTAMP 类型，用于时序查询）
           - systolic_blood_pressure: 收缩压
           - diastolic_pressure: 舒张压
           - hba1c: 糖化血红蛋白
           - ldl_c: 低密度脂蛋白（可能为 NULL）
           - risk_level: 风险等级（'低危', '高危', '极高危'）

        查询规则：
        - 当用户查询"最近"、"趋势"、"上个月"时，必须使用 assessment_time 字段进行排序或过滤
        - 聚合计算时需忽略 NULL 值
        - 所有查询必须添加 LIMIT 100 限制
        """
        # 注入到 LLM 的系统提示中
        self.system_prompt = table_context

    async def query(
        self, user_query: str, patient_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        处理自然语言查询

        Args:
            user_query: 用户自然语言查询
            patient_id: 当前患者ID（可选，用于上下文）

        Returns:
            包含 answer, generated_sql, data 的字典
        """
        try:
            # 如果提供了患者ID，增强查询上下文
            enhanced_query = user_query
            if patient_id:
                enhanced_query = f"针对患者 {patient_id}：{user_query}"

            # 使用 LlamaIndex 生成 SQL
            logger.info(f"Processing query: {enhanced_query}")
            response = await self.query_engine.aquery(enhanced_query)

            # 提取生成的 SQL
            generated_sql = response.metadata.get("sql_query", "")
            logger.info(f"Generated SQL: {generated_sql}")

            # 自动添加 LIMIT（如果缺失）
            if "limit" not in generated_sql.lower():
                # 去除SQL末尾的分号（如果有）
                generated_sql = generated_sql.rstrip("; \n")
                generated_sql += " LIMIT 100"
                logger.info(f"Auto-added LIMIT: {generated_sql}")

            # 安全检查
            is_valid, error_msg = SQLGuardrails.validate_sql(generated_sql)
            if not is_valid:
                raise ValueError(f"SQL 安全检查失败：{error_msg}")

            # 执行 SQL 获取数据
            with engine.connect() as conn:
                result = conn.execute(text(generated_sql))
                data = [dict(row._mapping) for row in result]

            # 使用 DeepSeek 生成自然语言总结
            summary_prompt = f"""
            基于以下查询结果，用中文为医生生成简洁的分析总结：

            查询：{user_query}
            数据：{data}

            请提供：
            1. 数据概要
            2. 关键发现（如异常值、趋势）
            3. 医学建议（如有必要）
            """
            summary_response = await self.llm.acomplete(summary_prompt)
            answer = summary_response.text

            return {"answer": answer, "generated_sql": generated_sql, "data": data}

        except Exception as e:
            logger.error(f"Query processing failed: {str(e)}")
            raise


# 全局服务实例
text_to_sql_service: Optional[TextToSQLService] = None


def get_text_to_sql_service() -> TextToSQLService:
    """
    获取 Text-to-SQL 服务实例（依赖注入）

    Returns:
        TextToSQLService 实例
    """
    global text_to_sql_service
    if text_to_sql_service is None:
        text_to_sql_service = TextToSQLService()
    return text_to_sql_service
