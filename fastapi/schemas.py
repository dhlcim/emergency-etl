from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HospitalSchema(BaseModel):
    hpid: str
    duty_name: str
    duty_addr: Optional[str]
    duty_emcls: Optional[str]
    duty_emcls_name: Optional[str]
    duty_tel1: Optional[str]
    duty_tel3: Optional[str]
    wgs84_lat: Optional[float]
    wgs84_lon: Optional[float]

    class Config:
        from_attributes = True

class BedStatusSchema(BaseModel):
    id: int
    hpid: str
    hv_ec: Optional[int]
    hv_oc: Optional[int]
    hv_cc: Optional[int]
    hv_ncc: Optional[int]
    hv_gc: Optional[int]
    collected_at: Optional[datetime]

    class Config:
        from_attributes = True

class HospitalWithBedSchema(BaseModel):
    hpid: str
    duty_name: str
    duty_addr: Optional[str]
    duty_tel3: Optional[str]
    wgs84_lat: Optional[float]
    wgs84_lon: Optional[float]
    hv_ec: Optional[int]
    hv_oc: Optional[int]
    hv_cc: Optional[int]
    hv_ncc: Optional[int]
    hv_gc: Optional[int]
    collected_at: Optional[datetime]