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

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Control")

ytapi_call = YouTubeMusicRecommender()

class Control:

    @staticmethod
    def YT_CALL_RECOMM_MUSIC(emotion: int):
        # 감정 상태에 따른 유튜브 추천 호출
        user_emotion = get_user_emotion(emotion)
        temp = ytapi_call.recommend_music(user_emotion)
        logger.info(f"Recommend : {temp}")
        return temp
    
    @staticmethod
    def Weather_API_CALL():
        rawResult = get_weather_data()
        weather_Result = parse_weather_data(rawResult)
        airCondition_Result = parse_air_quality_data(rawResult)

        return weather_Result, airCondition_Result
