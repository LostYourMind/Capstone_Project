### Main.py


import logging
import sys
import os
from typing import List, Dict, Optional

sys.path.append("../")  # 상위 디렉터리 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from concurrent.futures import ThreadPoolExecutor
from pydantic import BaseModel
from Control.Control import Control


# FastAPI 앱 인스턴스를 생성
app = FastAPI()
con = Control()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Uvicorn")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처에서의 요청을 허용
    allow_credentials=False,  # 크로스 오리진 요청 시 쿠키를 지원
    allow_methods=["*"],  # 모든 HTTP 메소드를 허용
    allow_headers=["*"],  # 모든 헤더를 허용
)


@app.on_event("startup")
async def startup():
    logger.info("데이터베이스 연결이 성공적으로 시작되었습니다.")


@app.on_event("shutdown")
async def shutdown():
    logger.info("데이터베이스 연결이 성공적으로 종료되었습니다.")


@app.get("/")
async def something():
    # # temp = trm()
    # # logger.info(f"temp data : {temp}")
    # recomm_result = con.YT_CALL_RECOMM_MUSIC()
    # return "Test"  # ECHO용 코드

    return "밥 먹는 중 입니다"


# 날씨 정보 호출
@app.post("/WeatherCall")
async def WeatherCall():

    weather_Result, airCondition_Result = con.Weather_API_CALL()

    return "asd"  # ECHO 용 함수
