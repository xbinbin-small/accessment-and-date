"""
API 路由：患者和医疗记录接口
"""
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import MedicalRecord, Patient
from app.schemas.schemas import MedicalRecordResponse, PatientResponse

router = APIRouter(prefix="/api", tags=["Patients & Records"])
logger = logging.getLogger(__name__)


@router.get("/doctors")
async def get_all_doctors(db: Session = Depends(get_db)):
    """
    获取所有医生列表（用于管理员查看）

    Returns:
        医生列表，包含医生ID和患者数量
    """
    try:
        # 查询所有不同的医生及其患者数量
        from sqlalchemy import func

        doctors = (
            db.query(
                Patient.doctor,
                func.count(Patient.id_number).label('patient_count')
            )
            .group_by(Patient.doctor)
            .order_by(func.count(Patient.id_number).desc())
            .all()
        )

        result = [
            {"doctor_id": doctor, "patient_count": count}
            for doctor, count in doctors
        ]

        logger.info(f"✅ Found {len(result)} doctors in database")
        return result

    except Exception as e:
        logger.error(f"Failed to get doctors: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取医生列表失败：{str(e)}")


@router.get("/patients")
async def get_all_patients(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    获取所有患者列表（用于管理员查看）

    Args:
        limit: 返回数量限制
        offset: 偏移量（用于分页）
        db: 数据库会话

    Returns:
        患者列表
    """
    try:
        total = db.query(Patient).count()
        patients = db.query(Patient).offset(offset).limit(limit).all()

        logger.info(f"✅ Returning {len(patients)} patients (total: {total})")
        return {
            "total": total,
            "offset": offset,
            "limit": limit,
            "patients": patients
        }

    except Exception as e:
        logger.error(f"Failed to get all patients: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取患者列表失败：{str(e)}")


@router.get("/patients/{doctor_id}", response_model=List[PatientResponse])
async def get_patients_by_doctor(doctor_id: str, db: Session = Depends(get_db)) -> List[Patient]:
    """
    获取医生名下的患者列表

    Args:
        doctor_id: 医生ID
        db: 数据库会话

    Returns:
        患者列表
    """
    try:
        patients = db.query(Patient).filter(Patient.doctor == doctor_id).limit(100).all()

        if not patients:
            logger.info(f"No patients found for doctor: {doctor_id}")
            return []

        logger.info(f"✅ Found {len(patients)} patients for doctor: {doctor_id}")
        return patients

    except Exception as e:
        logger.error(f"Failed to get patients: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取患者列表失败：{str(e)}")


@router.get("/records/{patient_id}", response_model=List[MedicalRecordResponse])
async def get_medical_records(
    patient_id: str, db: Session = Depends(get_db)
) -> List[MedicalRecord]:
    """
    获取患者的历史医疗记录（用于前端绘图）

    Args:
        patient_id: 患者身份证号
        db: 数据库会话

    Returns:
        医疗记录列表（按时间倒序）
    """
    try:
        # 按时间倒序查询，限制 100 条
        records = (
            db.query(MedicalRecord)
            .filter(MedicalRecord.id_number == patient_id)
            .order_by(MedicalRecord.assessment_time.desc())
            .limit(100)
            .all()
        )

        if not records:
            logger.info(f"No records found for patient: {patient_id}")
            return []

        logger.info(f"✅ Found {len(records)} records for patient: {patient_id}")
        return records

    except Exception as e:
        logger.error(f"Failed to get medical records: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取医疗记录失败：{str(e)}")
