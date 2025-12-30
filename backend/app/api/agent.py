"""
API 路由：AI Agent 对话接口
"""
import logging
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.schemas import ChatRequest, ChatResponse
from app.services.text_to_sql import TextToSQLService, get_text_to_sql_service

router = APIRouter(prefix="/api/agent", tags=["AI Agent"])
logger = logging.getLogger(__name__)


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest,
    text_to_sql_service: TextToSQLService = Depends(get_text_to_sql_service),
) -> Dict[str, Any]:
    """
    AI 对话接口

    **流程**：
    1. 接收用户自然语言查询
    2. LlamaIndex + DeepSeek 生成 SQL
    3. 执行 SQL 查询 Neon 数据库
    4. DeepSeek 生成医学分析总结
    5. 返回结果和生成的 SQL（调试用）

    **安全保障**：
    - SQL Guardrails 确保只执行 SELECT 查询
    - 强制添加 LIMIT 100 限制
    """
    try:
        logger.info(f"Received chat request: {request.query}")

        # 调用 Text-to-SQL 服务
        result = await text_to_sql_service.query(
            user_query=request.query, patient_id=request.patient_id
        )

        return ChatResponse(
            answer=result["answer"],
            generated_sql=result["generated_sql"],
            data=result["data"],
        )

    except ValueError as e:
        # SQL 安全检查失败
        logger.warning(f"SQL validation failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # 其他错误
        logger.error(f"Chat request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI 处理失败：{str(e)}")
