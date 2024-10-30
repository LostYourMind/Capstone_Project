### Main.py

import logging
import sys
import os
import json
import random
import string

from typing import List, Dict, Optional
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from uuid import uuid4
from datetime import datetime

sys.path.append("../")  # Add parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


#region 사용자 지정 Class import

from Control.Control import Control
from Control.DBcontrol import dbControl 
from DataModel.DataModel import HeartRateData, HeartRateResponse, UserCreateResponse
from Config import Loger  # 로그 설정 모듈 임포트

#endregion 


#region Instance

app = FastAPI()
con = Control()
db_con = dbControl()

#endregion


# 로깅 설정
logging.basicConfig(level=logging.INFO)

# 로그 설정 (포맷과 레벨 설정)
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("ExceptionLogger")

### CORS Setting
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_random_name(length=6):
    # 임의의 문자열을 생성하여 사용자 이름으로 사용
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))


@app.on_event("startup")
async def startup():
    db_state = db_con.initialize_db_connection() 
    if(db_state == None) : logger.info("failed to DB StartUp")
    else : Loger.setup_logging()
    

@app.on_event("shutdown")
async def shutdown():
    db_state = db_con.close_db_connection()
    if(db_state == None) : logger.info("failed to DB Shutdown")
    else : logger.info("데이터베이스 연결이 성공적으로 종료되었습니다.")


@app.get("/", status_code=200)
async def root():
    logger.info("Someone is Connect Root page")
    return JSONResponse(content={"message": "API is Working"}, status_code=200)


@app.post("/")
async def Insert_Infomation():
    return None



@app.post("/heart-rate")
async def heart_rate(data : HeartRateData):
    logging.info(f"Heart Rate : {data.heart_rate}")
    # return {"heart_rate": heart_rate, "status": "received"}
    return None


# 날씨 정보 호출
@app.get("/WeatherCall")
async def WeatherCall():
    logger.info("Call Weather EndPoint")
    weather_Result, airCondition_Result = con.Weather_API_CALL()
    return weather_Result, airCondition_Result
    # return "asd"  # ECHO 용 함수

@app.post("/echo")
async def echo(request: Request):
    # 요청 데이터를 가져옴
    try:
        data = await request.body()  # 원본 요청 데이터 (바이트)
        data_str = data.decode("utf-8")  # UTF-8로 디코딩하여 문자열로 변환

        # 요청 데이터를 로그에 출력
        logging.info(f"Received data: {data_str}")

        # 디코딩된 데이터를 그대로 반환
        return {"received_data": data_str}
    
    except Exception as e:
        # 오류가 발생한 경우 로그에 출력하고 에러 메시지를 반환
        logging.error(f"Error reading request data: {e}")
        return {"error": "Failed to read request data"}


# RequestValidationError 전역 예외 처리기
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # 요청 데이터 수집
    try:
        request_body = await request.json()
        request_data = json.dumps(request_body)  # JSON 문자열로 변환
    except Exception as e:
        request_data = f"Failed to retrieve request data: {str(e)}"

    # 서버에 자세한 오류 로그 출력
    logger.error(
        f"Validation error at {request.url} | "
        f"Request data: {request_data} | "
        f"Error: {exc}"
    )

    # 클라이언트에게 간결한 오류 메시지 반환
    return JSONResponse(
        status_code=422,
        content={"detail": "잘못된 요청"}
    )