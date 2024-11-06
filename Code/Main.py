### Main.py

# region Import 

import logging
import sys
import os
import pika
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


from Control.Control import Control
from Control.DBcontrol import dbControl
from DataModel.DataModel import HeartRateData, HeartRateResponse, UserCreateResponse
from Config import Loger  # 로그 설정 모듈 임포트
from CRUD_FILE.UserDataFetcher import UserDataFetcher

# endregion 

# region Instance
app = FastAPI()
con = Control()
db_connection = None  # 전역 데이터베이스 연결
db_con = None  # 전역 DBControl 인스턴스
# endregion

# region 서버 설정 및 사용자 지정 메서드

# 전체 로그 수준 설정
logging.basicConfig(
    level=logging.WARNING,  # 전체 로그를 WARNING 수준으로 설정
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

def send_to_queue(data):
    """RabbitMQ 큐에 데이터를 전송하는 함수"""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='sensor_data')
    message = json.dumps(data)
    channel.basic_publish(exchange='', routing_key='sensor_data', body=message)
    connection.close()

# endregion 

#region 서버 시작 & 종료 연결 설정

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


# endregion 

#region EndPoint




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


@app.post("/echo") # 디버깅용 Echo
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



# Android에서 보내는 데이터 받는 EndPoint
@app.post("/heart-rate")
async def heart_rate(data: dict):

    # 받은 데이터를 RabbitMQ 큐로 전송
    send_to_queue(data)
    
    # 1. ID 값 추출
    heartrate = data.get("heartRate")
    temp = con.YT_CALL_RECOMM_MUSIC(heartrate)

    # 3. 추출된 BPM 값을 이용해서 예측 HRV 값 측정
    # 4. 해당 값을 이용해서 Model로 감정 판별
    # 5. 판별된 감정을 이용한 음악 추천 URL 흭득
    # 6. 흭득한 URL return 




    
    return {"status": "Data sent to RabbitMQ"}