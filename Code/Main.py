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

# region 사용자 지정 Class import
from Control.Control import Control
from Control.DBcontrol import dbControl
from DataModel.DataModel import HeartRateData, HeartRateResponse, UserCreateResponse
from Config import Loger  # 로그 설정 모듈 임포트
# endregion 

# region Instance
app = FastAPI()
con = Control()
db_connection = None  # 전역 데이터베이스 연결
db_con = None  # 전역 DBControl 인스턴스
# endregion

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("ExceptionLogger")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    """서버 시작 시 데이터베이스 연결 초기화 및 DBControl 인스턴스 생성"""
    global db_connection, db_con
    db_connection = dbControl.initialize_db_connection()
    
    if db_connection is None:
        logger.error("Failed to connect to the database on startup.")
    else:
        logger.info("Database connected successfully on startup.")
        db_con = dbControl(db_connection)  # 전역 DBControl 인스턴스 생성
        Loger.setup_logging()  # 로그 설정

@app.on_event("shutdown")
async def shutdown():
    """서버 종료 시 데이터베이스 연결 종료"""
    global db_connection
    if db_connection:
        DBControl.close_db_connection(db_connection)
        logging.info("Database connection closed on shutdown.")

@app.get("/", status_code=200)
async def root():
    logger.info("Someone is connecting to the root page.")
    return JSONResponse(content={"message": "API is Working"}, status_code=200)

# Android에서 보내는 데이터 받는 EndPoint
@app.post("/heart-rate")
async def heart_rate(data: HeartRateData):
    # 로그에 데이터 각 필드를 출력
    logging.info("Start data received and processed in /heart-rate endpoint.")
    
    # 전역 db_con 인스턴스를 사용하여 데이터 저장
    try:
        result = db_con.save_data(data.dict())  # 데이터 저장
        logging.info("Data saved successfully in /heart-rate endpoint.")
        return result
    
    except Exception as e:
        logging.error(f"An error occurred in /heart-rate endpoint: {e}")
        return {"status": "Failed to process and save data", "error": str(e)}

# 날씨 정보 호출
@app.get("/WeatherCall")
async def WeatherCall():
    logger.info("Call Weather EndPoint")
    weather_Result, airCondition_Result = con.Weather_API_CALL()
    return weather_Result, airCondition_Result

# RequestValidationError 전역 예외 처리기
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if request.url.path == "/heart-rate":
        logging.error("Validation error on /heart-rate: 422 Unprocessable Entity")
        return {"error": "Invalid input for heart rate"}
    return await app.default_exception_handler(request, exc)

# region 디버깅 전용 ECHO 코드
@app.post("/echo")
async def echo(request: Request):
    logging.info("Call Echo")
    try:
        data = await request.body()  # 원본 요청 데이터 (바이트)
        data_str = data.decode("utf-8")  # UTF-8로 디코딩하여 문자열로 변환
        logging.info(f"Received data: {data_str}")
        return {"received_data": data_str}
    
    except Exception as e:
        logging.error(f"Error reading request data: {e}")
        return {"error": "Failed to read request data"}
# endregion
