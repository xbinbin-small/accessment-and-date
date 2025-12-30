"""
数据库模型定义

根据 database_schema.md 定义的表结构
"""
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Patient(Base):
    """患者信息表"""

    __tablename__ = "patients"

    id_number = Column(String, primary_key=True, index=True, comment="患者唯一标识（身份证号）")
    name = Column(String, nullable=False, comment="姓名")
    doctor = Column(String, nullable=False, comment="责任医生")

    # 关系：一个患者有多条检查记录
    medical_records = relationship("MedicalRecord", back_populates="patient")

    def __repr__(self) -> str:
        """模型字符串表示"""
        return f"<Patient(id_number={self.id_number}, name={self.name})>"


class MedicalRecord(Base):
    """检查记录表"""

    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="自增主键")
    id_number = Column(
        String,
        ForeignKey("patients.id_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="患者身份证号（外键）",
    )
    assessment_time = Column(
        DateTime,
        nullable=False,
        index=True,
        default=datetime.utcnow,
        comment="检查时间（关键时序字段）",
    )

    # 生化指标数据
    systolic_blood_pressure = Column(Numeric(5, 2), comment="收缩压")
    diastolic_pressure = Column(Numeric(5, 2), comment="舒张压")
    hba1c = Column(Numeric(4, 2), comment="糖化血红蛋白")
    ldl_c = Column(Numeric(5, 2), nullable=True, comment="低密度脂蛋白（可为空）")

    # 风险评估
    risk_level = Column(
        String,
        nullable=False,
        comment="风险等级（低危/高危/极高危）",
    )

    # 关系：多条记录属于一个患者
    patient = relationship("Patient", back_populates="medical_records")

    def __repr__(self) -> str:
        """模型字符串表示"""
        return f"<MedicalRecord(id={self.id}, id_number={self.id_number}, risk_level={self.risk_level})>"
