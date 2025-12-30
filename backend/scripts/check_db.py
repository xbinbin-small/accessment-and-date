"""
检查数据库数据的脚本
"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.database import SessionLocal
from app.models.models import Patient, MedicalRecord


def check_database():
    """检查数据库内容"""
    db = SessionLocal()

    try:
        # 总患者数
        total_patients = db.query(Patient).count()
        print(f"📊 总患者数：{total_patients}")

        # 按医生分组统计
        print("\n👨‍⚕️ 按医生分组：")
        doctors = db.query(Patient.doctor).distinct().all()
        for (doctor,) in doctors[:10]:  # 只显示前10个医生
            count = db.query(Patient).filter(Patient.doctor == doctor).count()
            print(f"   - {doctor}: {count} 位患者")

        # 查看 doctor_001 的患者
        print(f"\n🔍 查询 doctor_001 的患者：")
        patients_001 = db.query(Patient).filter(Patient.doctor == "doctor_001").limit(5).all()
        if patients_001:
            for p in patients_001:
                print(f"   - {p.name} ({p.id_number})")
        else:
            print("   ❌ 没有找到 doctor_001 的患者")

        # 查看前5位患者及其医生ID
        print(f"\n👥 数据库前5位患者：")
        first_patients = db.query(Patient).limit(5).all()
        for p in first_patients:
            record_count = db.query(MedicalRecord).filter(
                MedicalRecord.id_number == p.id_number
            ).count()
            print(f"   - {p.name} ({p.id_number}) - 医生: {p.doctor} - 记录数: {record_count}")

    finally:
        db.close()


if __name__ == "__main__":
    check_database()
