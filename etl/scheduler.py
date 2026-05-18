from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from collector import collect_bed_status, collect_hospital_list
from transformer import transform_bed_status, transform_hospital
from loader import (
    load_bed_status_local,
    load_hospitals_local,
    transfer_to_cloud,
    save_etl_log,
    get_local_connection,
    get_cloud_connection
)

scheduler = BlockingScheduler()

def realtime_job():
    """실시간 병상현황 수집 (매 5분)"""
    print(f"\n[실시간] 병상현황 수집 시작: {datetime.now()}")
    try:
        bed_list = collect_bed_status()
        bed_list = transform_bed_status(bed_list)
        count = load_bed_status_local(bed_list)
        save_etl_log(get_local_connection, "SUCCESS", count)
        print(f"[실시간] 완료 - {count}건 적재")
    except Exception as e:
        print(f"[실시간] 오류: {e}")
        save_etl_log(get_local_connection, "FAIL", 0, str(e))

def batch_job():
    """배치 전체 파이프라인 (매 1시간)"""
    print(f"\n[배치] 전체 파이프라인 시작: {datetime.now()}")
    try:
        # 병원 기본정보 수집 및 로컬 적재
        hospitals = collect_hospital_list()
        hospitals = transform_hospital(hospitals)
        h_count = load_hospitals_local(hospitals)

        # 클라우드 이관
        h_cnt, b_cnt = transfer_to_cloud()
        total = h_count + b_cnt

        save_etl_log(get_local_connection, "SUCCESS", total)
        save_etl_log(get_cloud_connection, "SUCCESS", total)
        print(f"[배치] 완료 - 병원: {h_cnt}건, 병상: {b_cnt}건 클라우드 이관")
    except Exception as e:
        print(f"[배치] 오류: {e}")
        save_etl_log(get_local_connection, "FAIL", 0, str(e))
        save_etl_log(get_cloud_connection, "FAIL", 0, str(e))

# 스케줄 등록
scheduler.add_job(realtime_job, IntervalTrigger(minutes=5), id='realtime')
scheduler.add_job(batch_job, IntervalTrigger(hours=1), id='batch')

if __name__ == "__main__":
    print("=" * 50)
    print("ETL 스케줄러 시작")
    print("  - 실시간 병상수집: 매 5분")
    print("  - 배치 전체파이프라인: 매 1시간")
    print("=" * 50)

    # 시작 시 즉시 한 번 실행
    realtime_job()
    batch_job()

    scheduler.start()