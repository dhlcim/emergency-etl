def transform_hospital(hospitals):
    """병원 기본정보 변환"""
    transformed = []
    for h in hospitals:
        transformed.append({
            "hpid": h.get("hpid", "").strip() if h.get("hpid") else None,
            "duty_name": h.get("duty_name", "").strip() if h.get("duty_name") else None,
            "duty_addr": h.get("duty_addr", "").strip() if h.get("duty_addr") else None,
            "duty_emcls": h.get("duty_emcls", "").strip() if h.get("duty_emcls") else None,
            "duty_emcls_name": h.get("duty_emcls_name", "").strip() if h.get("duty_emcls_name") else None,
            "duty_tel1": h.get("duty_tel1", "").strip() if h.get("duty_tel1") else None,
            "duty_tel3": h.get("duty_tel3", "").strip() if h.get("duty_tel3") else None,
            "wgs84_lat": float(h["wgs84_lat"]) if h.get("wgs84_lat") else None,
            "wgs84_lon": float(h["wgs84_lon"]) if h.get("wgs84_lon") else None,
        })
    
    # hpid 없는 데이터 제거
    transformed = [h for h in transformed if h["hpid"]]
    return transformed


def transform_bed_status(bed_list):
    """병상현황 변환"""
    transformed = []
    for b in bed_list:
        transformed.append({
            "hpid": b.get("hpid", "").strip() if b.get("hpid") else None,
            "hv_ec": int(b["hv_ec"]) if b.get("hv_ec") else 0,
            "hv_oc": int(b["hv_oc"]) if b.get("hv_oc") else 0,
            "hv_cc": int(b["hv_cc"]) if b.get("hv_cc") else 0,
            "hv_ncc": int(b["hv_ncc"]) if b.get("hv_ncc") else 0,
            "hv_gc": int(b["hv_gc"]) if b.get("hv_gc") else 0,
        })
    
    # hpid 없는 데이터 제거
    transformed = [b for b in transformed if b["hpid"]]
    return transformed