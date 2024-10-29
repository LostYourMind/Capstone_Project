from pydantic import BaseModel
from typing import List, Dict, Optional


# 심박수 데이터
class HeartRateData(BaseModel):
    heart_rate: int  # 심박수 데이터는 정수형

class AirCondition_Data(BaseModel) :
    airdata : str
