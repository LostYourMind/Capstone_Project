### Main.py

# region Import 

import asyncio
import logging
import sys
import os
import pika
import json

from collections import defaultdict
from typing import List, Dict, Optional
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse

sys.path.append("../")  # Add parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


from Control.Control import Control
from Control.DBcontrol import dbControl
from DataModel.DataModel import HeartRateData, HeartRateResponse, UserCreateResponse
from Config import Loger  # 로그 설정 모듈 임포트


# endregion 

# region 맴버 필드

app = FastAPI()
con = Control()
db_connection = None  # 전역 데이터베이스 연결
db_con = None  # 전역 DBControl 인스턴스

call_counts = defaultdict(int)  # 디바이스 별 호출 횟수를 저장할 딕셔너리
device_ID_Contain = []

# endregion

# region 서버 설정 및 사용자 지정 메서드 & 로깅 설정

# 전체 로그 수준 설정
logging.basicConfig(
    level=logging.WARNING,  # 전체 로그를 WARNING 수준으로 설정
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 특정 모듈의 로깅 수준 설정
logging.getLogger("pika").setLevel(logging.WARNING)  # pika 모듈의 로그를 WARNING 이상만 출력
logging.getLogger("pika.adapters.utils.connection_workflow").setLevel(logging.ERROR)  # 연결 로그는 ERROR 수준으로 제한
logging.getLogger("pika.channel").setLevel(logging.ERROR)  # 채널 로그도 ERROR만 표시

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
        dbControl.close_db_connection(db_connection)
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



# # Android에서 보내는 데이터 받는 EndPoint
# @app.post("/heart-rate")
# async def heart_rate(data: dict):

#     # 받은 데이터를 RabbitMQ 큐로 전송
#     send_to_queue(data)
    
#     deviceId = data.get("deviceId")
#     result = db_con.Find_heart_rate(deviceId)

#     temp = con.YT_CALL_RECOMM_MUSIC(result)

#     # 호출 횟수 증가
#     call_counts[deviceId] += 1
#     logging.info(f"call Counts = {call_counts[deviceId]}")

#     temp_data = {
#                 "url" : temp
#             }
    
#     return temp_data
    
    #return {"status": "Data sent to RabbitMQ"}

# @app.post("/echo") # 디버깅용 Echo
# async def echo(request: Request):

#     logging.info("Call Echo")
#     try:
#         data = await request.body()  # 원본 요청 데이터 (바이트)
#         data_str = data.decode("utf-8")  # UTF-8로 디코딩하여 문자열로 변환
#         logging.info(f"Received data: {data_str}")
#         return {"url": "https://www.youtube.com/watch?v=Y8YCGVDCpNY"}
    
#     except Exception as e:
#         logging.error(f"Error reading request data: {e}")
#         return {"error": "Failed to read request data"}




# endregion


# Android에서 보내는 데이터 받는 EndPoint
@app.post("/heart-rate")
async def heart_rate(data: dict):

    # 받은 데이터를 RabbitMQ 큐로 전송
    send_to_queue(data)
    
    deviceId = data.get("deviceId")
    result = db_con.Find_heart_rate(deviceId)

    temp = con.YT_CALL_RECOMM_MUSIC(result)

    # 호출 횟수 증가
    call_counts[deviceId] += 1
    logging.info(f"call Counts = {call_counts[deviceId]}")

    temp_data = {
                "url" : temp
            }
    
    logger.info(f"temp_data = {temp_data}")
    return temp_data
    


@app.get("/echo") # 디버깅용 Echo
async def echo():
    logging.info("Echo Call")
    if device_ID_Contain:
            latest_device_id = device_ID_Contain[-1]
            deviceId = latest_device_id
            logging.info(f"device ID : {deviceId} \nlastest_deviceId : {latest_device_id}")
    else:
            return {"status": "No device IDs available"}

    result = db_con.Find_heart_rate(deviceId)

    temp = con.YT_CALL_RECOMM_MUSIC(result)

    # 호출 횟수 증가
    call_counts[deviceId] += 1
    logging.info(f"call Counts = {call_counts[deviceId]}")

    return {"url" : temp} 

    



    