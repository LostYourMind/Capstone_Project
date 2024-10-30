from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime


# 심박수 데이터
class HeartRateData(BaseModel):
    heart_rate: str

class HeartRateResponse(BaseModel):
    heart_rate: int
    status: str

class AirCondition_Data(BaseModel) :
    airdata : str

class Arduino_Data(BaseModel) :
    Co : float
    Al : float
    Co2 : float
    Tolu : float
    Nh4 : float
    Acet : float
    Temp : int
    Humi : int
    heart_rate : int

# 데이터 모델 정의
class UserCreateResponse(BaseModel):
    user_id: str
    name: str
    created_at: datetime