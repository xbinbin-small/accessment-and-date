"""
Pydantic Schema 定义

用于 API 请求和响应的数据验证
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# ========== 患者相关 Schema ==========
class PatientBase(BaseModel):
    """患者基础信息"""

    id_number: str = Field(..., description="患者身份证号")
    name: str = Field(..., description="患者姓名")
    doctor: str = Field(..., description="责任医生")


class PatientResponse(PatientBase):
    """患者信息响应"""

    class Config:
        """Pydantic 配置"""

        from_attributes = True


# ========== 检查记录相关 Schema ==========
class MedicalRecordBase(BaseModel):
    """检查记录基础信息"""

    id_number: str = Field(..., description="患者身份证号")
    assessment_time: datetime = Field(..., description="检查时间")
    systolic_blood_pressure: Optional[float] = Field(None, description="收缩压")
    diastolic_pressure: Optional[float] = Field(None, description="舒张压")
    hba1c: Optional[float] = Field(None, description="糖化血红蛋白")
    ldl_c: Optional[float] = Field(None, description="低密度脂蛋白")
    risk_level: str = Field(..., description="风险等级")


class MedicalRecordResponse(MedicalRecordBase):
    """检查记录响应"""

    id: int = Field(..., description="记录ID")

    class Config:
        """Pydantic 配置"""

        from_attributes = True


# ========== AI Agent 相关 Schema ==========
class ChatRequest(BaseModel):
    """AI 对话请求"""

    query: str = Field(..., description="用户自然语言查询")
    patient_id: Optional[str] = Field(None, description="当前查看的患者ID（可选，用于上下文）")


class ChatResponse(BaseModel):
    """AI 对话响应"""

    answer: str = Field(..., description="AI 分析结果")
    generated_sql: Optional[str] = Field(None, description="生成的 SQL（调试用）")
    data: Optional[List[dict]] = Field(None, description="查询结果数据")


# ========== 通用响应 Schema ==========
class ErrorResponse(BaseModel):
    """错误响应"""

    detail: str = Field(..., description="错误详情")
