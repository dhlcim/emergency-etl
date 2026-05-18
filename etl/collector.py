import requests
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://apis.data.go.kr/B552657/ErmctInfoInqireService"

def collect_hospital_list():
    """병원 기본정보 수집"""
    url = f"{BASE_URL}/getEgytListInfoInqire"
    params = {
        "serviceKey": API_KEY,
        "pageNo": 1,
        "numOfRows": 100
    }
    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)

    hospitals = []
    for item in root.findall(".//item"):
        hospital = {
            "hpid": item.findtext("hpid"),
            "duty_name": item.findtext("dutyName"),
            "duty_addr": item.findtext("dutyAddr"),
            "duty_emcls": item.findtext("dutyEmcls"),
            "duty_emcls_name": item.findtext("dutyEmclsName"),
            "duty_tel1": item.findtext("dutyTel1"),
            "duty_tel3": item.findtext("dutyTel3"),
            "wgs84_lat": item.findtext("wgs84Lat"),
            "wgs84_lon": item.findtext("wgs84Lon"),
        }
        hospitals.append(hospital)

    return hospitals


def collect_bed_status():
    """실시간 병상현황 수집"""
    url = f"{BASE_URL}/getEmrrmRltmUsefulSckbdInfoInqire"
    params = {
        "serviceKey": API_KEY,
        "pageNo": 1,
        "numOfRows": 100
    }
    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)

    bed_list = []
    for item in root.findall(".//item"):
        bed = {
            "hpid": item.findtext("hpid"),
            "hv_ec": item.findtext("hvec"),
            "hv_oc": item.findtext("hvoc"),
            "hv_cc": item.findtext("hvcc"),
            "hv_ncc": item.findtext("hvncc"),
            "hv_gc": item.findtext("hvgc"),
        }
        bed_list.append(bed)

    return bed_list