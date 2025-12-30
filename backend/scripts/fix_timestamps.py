"""
修复数据库中的时间戳
将每位患者的多条记录分布到不同的时间点，以便展示时序趋势
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# 添加项目根目录到 Python 路径
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.database import SessionLocal
from app.models.models import MedicalRecord
from sqlalchemy import func


def fix_patient_timestamps(db, patient_id: str, record_count: int):
    """
    为单个患者的记录设置不同的时间戳

    Args:
        db: 数据库会话
        patient_id: 患者ID
        record_count: 该患者的记录数量
    """
    # 获取该患者的所有记录，按ID排序（保证每次运行结果一致）
    records = (
        db.query(MedicalRecord)
        .filter(MedicalRecord.id_number == patient_id)
        .order_by(MedicalRecord.id)
        .all()
    )

    if not records:
        return 0

    # 当前时间
    now = datetime.now()

    # 根据记录数量，分配时间跨度
    # 记录越多，时间跨度越长
    if record_count <= 3:
        # 3条以内：最近3个月，每月一次
        months_span = 3
    elif record_count <= 6:
        # 4-6条：最近6个月
        months_span = 6
    elif record_count <= 12:
        # 7-12条：最近一年
        months_span = 12
    else:
        # 超过12条：最近2年
        months_span = 24

    # 计算每条记录之间的平均间隔（天数）
    days_span = months_span * 30
    interval_days = days_span / max(len(records), 1)

    # 为每条记录分配时间戳（从最近到最远）
    updated_count = 0
    for i, record in enumerate(records):
        # 从现在往前推算时间
        # 第一条记录是最近的，最后一条是最早的
        days_ago = i * interval_days

        # 添加随机偏移（±3天），使时间更自然
        random_offset = random.uniform(-3, 3)
        total_days_ago = days_ago + random_offset

        # 计算新的时间戳
        new_timestamp = now - timedelta(days=total_days_ago)

        # 更新记录
        record.assessment_time = new_timestamp
        updated_count += 1

    return updated_count


def main():
    """主函数"""
    db = SessionLocal()

    try:
        print("🔧 开始修复医疗记录的时间戳...\n")

        # 统计信息
        total_patients = 0
        total_records_updated = 0

        # 获取所有有记录的患者
        patients_with_records = (
            db.query(
                MedicalRecord.id_number,
                func.count(MedicalRecord.id).label('record_count')
            )
            .group_by(MedicalRecord.id_number)
            .all()
        )

        print(f"📊 找到 {len(patients_with_records)} 位有医疗记录的患者\n")

        # 为每位患者修复时间戳
        for patient_id, record_count in patients_with_records:
            updated = fix_patient_timestamps(db, patient_id, record_count)
            total_records_updated += updated
            total_patients += 1

            if total_patients % 100 == 0:
                print(f"已处理 {total_patients} 位患者...")

        # 提交更改
        db.commit()

        print(f"\n✅ 时间戳修复完成！")
        print(f"   - 处理患者数：{total_patients}")
        print(f"   - 更新记录数：{total_records_updated}")

        # 显示示例：查看前3位患者的时间分布
        print(f"\n📅 示例 - 前3位患者的时间分布：")
        for i, (patient_id, _) in enumerate(patients_with_records[:3]):
            records = (
                db.query(MedicalRecord)
                .filter(MedicalRecord.id_number == patient_id)
                .order_by(MedicalRecord.assessment_time.desc())
                .all()
            )

            print(f"\n患者 {patient_id} ({len(records)} 条记录):")
            for record in records[:5]:  # 只显示最近5条
                print(f"   - {record.assessment_time.strftime('%Y-%m-%d %H:%M')}")

        print(f"\n💡 提示：现在刷新前端页面，即可看到时序趋势图！")

    except Exception as e:
        print(f"\n❌ 错误：{e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
