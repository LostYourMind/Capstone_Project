import asyncio
import sys
import os
import logging

sys.path.append("../")  # Add parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from API.Youtube_Call import YouTubeMusicRecommender
from API.Weather import get_weather_data, parse_air_quality_data, parse_weather_data
from Module.BPMtoHRV import calculate_ibi, calculate_sdnn, calculate_rmssd, calculate_pnn50, calculate_frequency_domain_features
from API.GPT_API import USE_GPT

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Control")

ytapi_call = YouTubeMusicRecommender()
gpt_api = USE_GPT()

class Control:
    scheduled_tasks = {}

    @staticmethod
    def YT_CALL_RECOMM_MUSIC(bpm_values):
        """
        BPM 배열을 받아 IBI와 HRV(Time Domain)를 계산하여 로그에 출력합니다.
        """
        try:
            
            # IBI 계산
            ibi_values = calculate_ibi(bpm_values)

            # Time Domain HRV Features
            sdnn = calculate_sdnn(ibi_values)
            rmssd = calculate_rmssd(ibi_values)
            pnn50 = calculate_pnn50(ibi_values)

            # Frequency Domain HRV Features
            freq_domain_features = calculate_frequency_domain_features(ibi_values)
        
            resultdata = gpt_api.TestModule(ibi_values, sdnn, rmssd, pnn50)
        
            if sdnn < 50:
                temp = ytapi_call.recommend_music("T")
            elif 50 <= sdnn <= 100:
                temp = ytapi_call.recommend_music("E")
            else:
                temp = ytapi_call.recommend_music("C")
            logging.info(f"GPT answer : {resultdata}")
            return temp
            
        except ValueError as e:
            logging.error(f"Invalid BPM values provided: {e}")
            return None

    @staticmethod
    def Weather_API_CALL():
        rawResult = get_weather_data()
        weather_Result = parse_weather_data(rawResult)
        airCondition_Result = parse_air_quality_data(rawResult)
        return weather_Result, airCondition_Result
