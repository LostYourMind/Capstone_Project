### Main.py


import logging
import sys
import os
from typing import List, Dict, Optional

sys.path.append("../")  # Add parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from concurrent.futures import ThreadPoolExecutor
from pydantic import BaseModel
from Control.Control import Control
from Control.DBcontrol import dbControl


# Create FastAPI App Instance, Control Class Instance
app = FastAPI()
con = Control()
db_con = dbControl()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Uvicorn")


### CORS Setting
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():

    logger.info("데이터베이스 연결이 성공적으로 시작되었습니다.")


@app.on_event("shutdown")
async def shutdown():
    logger.info("데이터베이스 연결이 성공적으로 종료되었습니다.")


@app.get("/")
async def something():
    return "API is Work"


@app.get("/")
async def Insert_Infomation():
    return None


# 날씨 정보 호출
@app.post("/WeatherCall")
async def WeatherCall():

    weather_Result, airCondition_Result = con.Weather_API_CALL()

    return "asd"  # ECHO 용 함수
