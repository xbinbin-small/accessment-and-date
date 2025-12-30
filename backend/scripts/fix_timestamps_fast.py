"""
快速修复数据库中的时间戳（批量更新版本）
将每位患者的多条记录分布到不同的时间点
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.database import SessionLocal, engine
from app.models.models import MedicalRecord
from sqlalchemy import text


def main():
    """主函数"""
    db = SessionLocal()

    try:
        print("🔧 开始批量修复医疗记录的时间戳...\n")

        # 使用原生SQL进行批量更新，提高速度
        print("📊 正在计算新的时间戳...")

        # 策略：为每条记录分配一个随机的过去时间
        # 使用 ROW_NUMBER() 为同一患者的记录分配序号
        update_sql = """
        WITH ranked_records AS (
            SELECT
                id,
                id_number,
                ROW_NUMBER() OVER (PARTITION BY id_number ORDER BY id) as row_num,
                COUNT(*) OVER (PARTITION BY id_number) as total_records
            FROM medical_records
        )
        UPDATE medical_records mr
        SET assessment_time = NOW() - INTERVAL '1 day' * (
            -- 根据记录序号计算天数偏移
            -- 第一条记录：最近（0-7天前）
            -- 最后一条记录：最远（根据总记录数，最多2年前）
            CASE
                WHEN rr.total_records <= 3 THEN (rr.row_num - 1) * 30  -- 3条记录：每月一次，共3个月
                WHEN rr.total_records <= 6 THEN (rr.row_num - 1) * 30  -- 6条记录：每月一次，共6个月
                WHEN rr.total_records <= 12 THEN (rr.row_num - 1) * 30 -- 12条记录：每月一次，共1年
                ELSE (rr.row_num - 1) * 60  -- 更多记录：每2个月一次，最多10年
            END
            + (RANDOM() * 5 - 2.5)::int  -- 添加±2.5天的随机偏移
        )
        FROM ranked_records rr
        WHERE mr.id = rr.id
        """

        print("⏳ 正在执行批量更新（可能需要1-2分钟）...")

        with engine.connect() as conn:
            result = conn.execute(text(update_sql))
            conn.commit()

        print(f"✅ 批量更新完成！")

        # 统计结果
        total_records = db.query(MedicalRecord).count()
        print(f"\n📈 统计信息：")
        print(f"   - 总记录数：{total_records}")

        # 显示几个示例患者的时间分布
        print(f"\n📅 示例 - 随机3位患者的时间分布：")

        # 随机选择3位有多条记录的患者
        sample_patients_sql = """
        SELECT id_number, COUNT(*) as cnt
        FROM medical_records
        GROUP BY id_number
        HAVING COUNT(*) >= 3
        ORDER BY RANDOM()
        LIMIT 3
        """

        with engine.connect() as conn:
            sample_patients = conn.execute(text(sample_patients_sql)).fetchall()

        for patient_id, count in sample_patients:
            records = (
                db.query(MedicalRecord)
                .filter(MedicalRecord.id_number == patient_id)
                .order_by(MedicalRecord.assessment_time.desc())
                .limit(5)
                .all()
            )

            print(f"\n患者 {patient_id} ({count} 条记录):")
            for record in records:
                print(f"   - {record.assessment_time.strftime('%Y-%m-%d %H:%M')}")

        print(f"\n💡 完成！现在刷新前端页面，即可看到真实的时序趋势图！")

    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
