import pymysql
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def get_local_connection():
    return pymysql.connect(
        host=os.getenv("LOCAL_DB_HOST"),
        port=int(os.getenv("LOCAL_DB_PORT")),
        user=os.getenv("LOCAL_DB_USER"),
        password=os.getenv("LOCAL_DB_PASSWORD"),
        db=os.getenv("LOCAL_DB_NAME"),
        charset="utf8mb4"
    )

def get_cloud_connection():
    return pymysql.connect(
        host=os.getenv("CLOUD_DB_HOST"),
        port=int(os.getenv("CLOUD_DB_PORT")),
        user=os.getenv("CLOUD_DB_USER"),
        password=os.getenv("CLOUD_DB_PASSWORD"),
        db=os.getenv("CLOUD_DB_NAME"),
        charset="utf8mb4"
    )

def load_hospitals_local(hospitals):
    """로컬 DB에 병원 기본정보 적재"""
    conn = get_local_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO tb_hospital_info 
        (hpid, duty_name, duty_addr, duty_emcls, duty_emcls_name, duty_tel1, duty_tel3, wgs84_lat, wgs84_lon)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        duty_name=VALUES(duty_name),
        duty_addr=VALUES(duty_addr),
        duty_tel1=VALUES(duty_tel1),
        duty_tel3=VALUES(duty_tel3)
    """
    for h in hospitals:
        cursor.execute(sql, (
            h["hpid"], h["duty_name"], h["duty_addr"],
            h["duty_emcls"], h["duty_emcls_name"],
            h["duty_tel1"], h["duty_tel3"],
            h["wgs84_lat"], h["wgs84_lon"]
        ))
    conn.commit()
    cursor.close()
    conn.close()
    return len(hospitals)

def load_bed_status_local(bed_list):
    """로컬 DB에 병상현황 적재 (존재하는 hpid만)"""
    conn = get_local_connection()
    cursor = conn.cursor()

    # 존재하는 hpid 목록 조회
    cursor.execute("SELECT hpid FROM tb_hospital_info")
    valid_hpids = {row[0] for row in cursor.fetchall()}

    # 유효한 hpid만 필터링
    filtered = [b for b in bed_list if b["hpid"] in valid_hpids]

    sql = """
        INSERT INTO tb_bed_status (hpid, hv_ec, hv_oc, hv_cc, hv_ncc, hv_gc)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    for b in filtered:
        cursor.execute(sql, (
            b["hpid"], b["hv_ec"], b["hv_oc"],
            b["hv_cc"], b["hv_ncc"], b["hv_gc"]
        ))
    conn.commit()
    cursor.close()
    conn.close()
    return len(filtered)

def transfer_to_cloud():
    """로컬 DB → 클라우드 DB 이관"""
    local_conn = get_local_connection()
    cloud_conn = get_cloud_connection()
    local_cursor = local_conn.cursor()
    cloud_cursor = cloud_conn.cursor()

    # 병원 기본정보 이관
    local_cursor.execute("SELECT * FROM tb_hospital_info")
    hospitals = local_cursor.fetchall()
    sql = """
        INSERT INTO tb_hospital_info 
        (hpid, duty_name, duty_addr, duty_emcls, duty_emcls_name, duty_tel1, duty_tel3, wgs84_lat, wgs84_lon, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        duty_name=VALUES(duty_name),
        duty_addr=VALUES(duty_addr)
    """
    cloud_cursor.executemany(sql, hospitals)

    # 병상현황 이관
    local_cursor.execute("SELECT * FROM tb_bed_status")
    beds = local_cursor.fetchall()
    sql = """
        INSERT INTO tb_bed_status (id, hpid, hv_ec, hv_oc, hv_cc, hv_ncc, hv_gc, collected_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        hv_ec=VALUES(hv_ec),
        hv_oc=VALUES(hv_oc)
    """
    cloud_cursor.executemany(sql, beds)

    cloud_conn.commit()
    local_cursor.close()
    cloud_cursor.close()
    local_conn.close()
    cloud_conn.close()
    return len(hospitals), len(beds)

def save_etl_log(conn_func, status, record_count, message=""):
    """ETL 로그 저장"""
    conn = conn_func()
    cursor = conn.cursor()
    sql = """
        INSERT INTO tb_etl_log (status, record_count, message)
        VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (status, record_count, message))
    conn.commit()
    cursor.close()
    conn.close()