### Control.py

import sys
import os

sys.path.append("../")  # Add parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import logging
from API.Youtube_Call import YouTubeMusicRecommender
from API.Weather import get_weather_data, parse_air_quality_data, parse_weather_data
from Module.Heart_Rate import get_user_emotion
from Module.BPMtoHRV import calculate_sdnn, calculate_ibi

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Control")

ytapi_call = YouTubeMusicRecommender()

class Control:

    @staticmethod
    def YT_CALL_RECOMM_MUSIC(bpm_values):

        ibi_value = calculate_ibi(bpm_values)
        hrv_metrics = calculate_sdnn(ibi_value)
        #sdnn 연산 처리


        # 1. hrv_metrics 값을 이용해서 감정 판독 코드 추가



        # 2. 판독된 데이터를 이용한 음악 추천 로직 코드 추가


        # 3. 추천된 데이터 return 

        logging.info(f"hrv_metrics = {hrv_metrics}")
        return None
    
    @staticmethod
    def Weather_API_CALL():
        rawResult = get_weather_data()
        weather_Result = parse_weather_data(rawResult)
        airCondition_Result = parse_air_quality_data(rawResult)

        return weather_Result, airCondition_Result
