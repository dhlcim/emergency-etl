from database import get_cloud_connection

def get_all_hospitals():
    """전체 병원 목록 조회"""
    conn = get_cloud_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_hospital_info")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_hospital_by_id(hpid: str):
    """병원 단건 조회"""
    conn = get_cloud_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_hospital_info WHERE hpid = %s", (hpid,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def get_latest_bed_status():
    """최신 병상현황 조회 (병원정보 포함)"""
    conn = get_cloud_connection()
    cursor = conn.cursor()
    sql = """
        SELECT 
            h.hpid, h.duty_name, h.duty_addr, h.duty_tel3,
            h.wgs84_lat, h.wgs84_lon,
            b.hv_ec, b.hv_oc, b.hv_cc, b.hv_ncc, b.hv_gc, b.collected_at
        FROM tb_hospital_info h
        JOIN tb_bed_status b ON h.hpid = b.hpid
        WHERE b.collected_at = (
            SELECT MAX(collected_at) FROM tb_bed_status WHERE hpid = h.hpid
        )
        ORDER BY h.duty_name
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_available_beds():
    """가용병상 있는 병원만 조회"""
    conn = get_cloud_connection()
    cursor = conn.cursor()
    sql = """
        SELECT 
            h.hpid, h.duty_name, h.duty_addr, h.duty_tel3,
            h.wgs84_lat, h.wgs84_lon,
            b.hv_ec, b.hv_oc, b.hv_cc, b.hv_ncc, b.hv_gc, b.collected_at
        FROM tb_hospital_info h
        JOIN tb_bed_status b ON h.hpid = b.hpid
        WHERE b.collected_at = (
            SELECT MAX(collected_at) FROM tb_bed_status WHERE hpid = h.hpid
        )
        AND (b.hv_ec > 0 OR b.hv_oc > 0 OR b.hv_gc > 0)
        ORDER BY b.hv_ec DESC
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result