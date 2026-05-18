from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import models
import schemas

app = FastAPI(title="응급실 가용병상 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "응급실 가용병상 모니터링 API 서버 정상 작동 중"}

@app.get("/hospitals", response_model=List[schemas.HospitalSchema])
def get_hospitals():
    """전체 병원 목록 조회"""
    result = models.get_all_hospitals()
    if not result:
        raise HTTPException(status_code=404, detail="병원 정보 없음")
    return result

@app.get("/hospitals/{hpid}", response_model=schemas.HospitalSchema)
def get_hospital(hpid: str):
    """병원 단건 조회"""
    result = models.get_hospital_by_id(hpid)
    if not result:
        raise HTTPException(status_code=404, detail="해당 병원 없음")
    return result

@app.get("/beds", response_model=List[schemas.HospitalWithBedSchema])
def get_bed_status():
    """전체 병상현황 조회"""
    result = models.get_latest_bed_status()
    if not result:
        raise HTTPException(status_code=404, detail="병상 정보 없음")
    return result

@app.get("/beds/available", response_model=List[schemas.HospitalWithBedSchema])
def get_available_beds():
    """가용병상 있는 병원만 조회"""
    result = models.get_available_beds()
    if not result:
        raise HTTPException(status_code=404, detail="가용병상 있는 병원 없음")
    return result