from pydantic import BaseModel
from typing import List, Dict, Optional


# 심박수 데이터
class Heart_Data(BaseModel):
    text: str
    sender: str
    id_Value: int
