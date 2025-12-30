"""
数据库初始化脚本

功能：
1. 创建所有数据表（如果不存在）
2. 插入示例患者和医疗记录数据
"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from datetime import datetime, timedelta
from app.core.database import engine, SessionLocal
from app.models.models import Base, Patient, MedicalRecord


def create_tables():
    """创建所有数据表"""
    print("📦 正在创建数据表...")
    Base.metadata.create_all(bind=engine)
    print("✅ 数据表创建完成")


def insert_sample_data():
    """插入示例数据"""
    db = SessionLocal()

    try:
        print("\n📊 正在插入示例数据...")

        # 检查是否已有 doctor_001 的患者
        existing_demo_patients = db.query(Patient).filter(
            Patient.doctor == "doctor_001"
        ).count()

        if existing_demo_patients > 0:
            print(f"⚠️  数据库中已有 {existing_demo_patients} 位 doctor_001 的演示患者，跳过数据插入")
            return

        total_patients = db.query(Patient).count()
        print(f"ℹ️  数据库中已有 {total_patients} 位患者，现在添加演示用的 doctor_001 患者...")

        # 创建示例患者
        patients = [
            Patient(
                id_number="330123199001011234",
                name="张三",
                doctor="doctor_001"
            ),
            Patient(
                id_number="330123199002022345",
                name="李四",
                doctor="doctor_001"
            ),
            Patient(
                id_number="330123199003033456",
                name="王五",
                doctor="doctor_001"
            ),
        ]

        db.add_all(patients)
        db.commit()
        print(f"✅ 成功创建 {len(patients)} 位患者")

        # 为每位患者创建过去6个月的医疗记录
        now = datetime.utcnow()
        records = []

        for patient in patients:
            for i in range(6):
                # 从最近到最早
                assessment_date = now - timedelta(days=30 * i)

                # 模拟不同的健康状态趋势
                if patient.name == "张三":
                    # 张三：血压逐渐改善
                    systolic = 150 - i * 3
                    diastolic = 95 - i * 2
                    hba1c = 7.5 - i * 0.2
                    risk_level = "高危" if i < 2 else "低危"
                elif patient.name == "李四":
                    # 李四：糖尿病控制良好
                    systolic = 125 + i * 2
                    diastolic = 80 + i
                    hba1c = 6.5 + i * 0.1
                    risk_level = "低危"
                else:  # 王五
                    # 王五：情况恶化需要关注
                    systolic = 140 + i * 5
                    diastolic = 85 + i * 3
                    hba1c = 8.0 + i * 0.3
                    risk_level = "极高危" if i >= 4 else "高危"

                record = MedicalRecord(
                    id_number=patient.id_number,
                    assessment_time=assessment_date,
                    systolic_blood_pressure=systolic,
                    diastolic_pressure=diastolic,
                    hba1c=hba1c,
                    ldl_c=2.5 + (i % 3) * 0.3,  # LDL 在 2.5-3.4 之间波动
                    risk_level=risk_level
                )
                records.append(record)

        db.add_all(records)
        db.commit()
        print(f"✅ 成功创建 {len(records)} 条医疗记录")

        # 打印统计信息
        print("\n📈 数据统计：")
        for patient in patients:
            record_count = db.query(MedicalRecord).filter(
                MedicalRecord.id_number == patient.id_number
            ).count()
            print(f"   - {patient.name} ({patient.id_number}): {record_count} 条记录")

    except Exception as e:
        print(f"❌ 错误：{e}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    """主函数"""
    print("🚀 开始初始化数据库...\n")

    try:
        # 1. 创建表
        create_tables()

        # 2. 插入示例数据
        insert_sample_data()

        print("\n✅ 数据库初始化完成！")
        print("\n💡 提示：现在可以刷新前端页面，查看真实数据")

    except Exception as e:
        print(f"\n❌ 初始化失败：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
