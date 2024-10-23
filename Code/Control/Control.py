### Control.py

import sys
import os

sys.path.append("../")  # Add parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import logging
from API.Youtube_Call import test_recommend_music as trm
from API.Weather import get_weather_data, parse_air_quality_data, parse_weather_data

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Control")

class Control:

    @staticmethod
    def YT_CALL_RECOMM_MUSIC():
        temp = trm()
        logger.info(f"Recommend : {temp}")
        return temp
    
    @staticmethod
    def Weather_API_CALL():
        rawResult = get_weather_data()
        weather_Result = parse_weather_data(rawResult)
        airCondition_Result = parse_air_quality_data(rawResult)

        return weather_Result, airCondition_Result
