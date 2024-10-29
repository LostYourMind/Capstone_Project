### Main.py

import logging
import sys
import os
from typing import List, Dict, Optional
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

sys.path.append("../")  # Add parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from Control.Control import Control
from Control.DBcontrol import dbControl 
from DataModel.DataModel import HeartRateData
from Config import Loger  # 로그 설정 모듈 임포트


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
    db_state = db_con.initialize_db_connection() 
    if(db_state == None) : logger.info("failed to DB StartUp")
    else : Loger.setup_logging()
    

@app.on_event("shutdown")
async def shutdown():
    db_state = db_con.close_db_connection()
    if(db_state == None) : logger.info("failed to DB Shutdown")
    else : logger.info("데이터베이스 연결이 성공적으로 종료되었습니다.")


@app.get("/")
async def something():
    return "API is Work"


@app.post("/")
async def Insert_Infomation():
    return None

# 심박수 데이터를 받는 POST 엔드포인트
@app.post("/heart-rate")
async def receive_heart_rate(data: HeartRateData):
    # 심박수 데이터가 성공적으로 전달되면 로그 출력
    logging.info(f"Received valid heart rate: {data.heart_rate}")
    
    return {"status": "success", "received_heart_rate": data.heart_rate}



# 날씨 정보 호출
@app.get("/WeatherCall")
async def WeatherCall():
    logger.info("Call Weather EndPoint")
    weather_Result, airCondition_Result = con.Weather_API_CALL()
    return weather_Result, airCondition_Result
    # return "asd"  # ECHO 용 함수


# 전역 예외 처리기: RequestValidationError를 처리
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # 서버에 자세한 오류 로그 출력
    logging.error(f"Validation error at {request.url}: {exc}")
    
    # 클라이언트에게 간결한 오류 메시지 반환
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "잘못된 요청"}
    )
