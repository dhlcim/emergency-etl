from collector import collect_hospital_list, collect_bed_status
from transformer import transform_hospital, transform_bed_status
from loader import (
    load_hospitals_local,
    load_bed_status_local,
    transfer_to_cloud,
    save_etl_log,
    get_local_connection,
    get_cloud_connection
)
from datetime import datetime

def run_pipeline():
    print(f"\n{'='*50}")
    print(f"ETL 파이프라인 시작: {datetime.now()}")
    print(f"{'='*50}")

    try:
        # 1. 수집 (Extract)
        print("\n[1단계] 데이터 수집 중...")
        hospitals = collect_hospital_list()
        bed_list = collect_bed_status()
        print(f"  병원 기본정보: {len(hospitals)}건")
        print(f"  병상현황: {len(bed_list)}건")

        # 2. 변환 (Transform)
        print("\n[2단계] 데이터 변환 중...")
        hospitals = transform_hospital(hospitals)
        bed_list = transform_bed_status(bed_list)
        print(f"  변환 완료 - 병원: {len(hospitals)}건, 병상: {len(bed_list)}건")

        # 3. 로컬 DB 적재 (Load)
        print("\n[3단계] 로컬 DB 적재 중...")
        h_count = load_hospitals_local(hospitals)
        b_count = load_bed_status_local(bed_list)
        print(f"  적재 완료 - 병원: {h_count}건, 병상: {b_count}건")

        # 4. 클라우드 DB 이관 (Transfer)
        print("\n[4단계] 클라우드 DB 이관 중...")
        h_cnt, b_cnt = transfer_to_cloud()
        print(f"  이관 완료 - 병원: {h_cnt}건, 병상: {b_cnt}건")

        # 5. 로그 저장
        total = h_count + b_count
        save_etl_log(get_local_connection, "SUCCESS", total)
        save_etl_log(get_cloud_connection, "SUCCESS", total)
        print(f"\n✅ ETL 파이프라인 완료!")

    except Exception as e:
        print(f"\n❌ ETL 오류 발생: {e}")
        save_etl_log(get_local_connection, "FAIL", 0, str(e))
        save_etl_log(get_cloud_connection, "FAIL", 0, str(e))

if __name__ == "__main__":
    run_pipeline()