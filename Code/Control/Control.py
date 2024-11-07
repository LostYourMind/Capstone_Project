### Control.py

import asyncio
import sys
import os
import time

sys.path.append("../")  # Add parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import logging
from API.Youtube_Call import YouTubeMusicRecommender
from API.Weather import get_weather_data, parse_air_quality_data, parse_weather_data
from Module.BPMtoHRV import calculate_ibi, calculate_sdnn, calculate_rmssd, calculate_pnn50, calculate_frequency_domain_features

# 완료 여부를 추적하기 위한 플래그
is_task_running = False

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Control")

ytapi_call = YouTubeMusicRecommender()

class Control:

    
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

            # HRV 결과를 통합하여 반환 (또는 로그 출력)
            hrv_results = {
                "Time Domain Features": {
                    "SDNN": sdnn,
                    "RMSSD": rmssd,
                    "pNN50": pnn50
                },
                "Frequency Domain Features": freq_domain_features
            }
            
            logging.info(f"HRV Results: {hrv_results}")
            return hrv_results

        except ValueError as e:
            logging.error(f"Invalid BPM values provided: {e}")
            return None
    

    @staticmethod
    def Weather_API_CALL():
        rawResult = get_weather_data()
        weather_Result = parse_weather_data(rawResult)
        airCondition_Result = parse_air_quality_data(rawResult)

        return weather_Result, airCondition_Result


    #region 스케줄링

    def scheduled_yt_call_recomm_music(bpm_values):
        Control.YT_CALL_RECOMM_MUSIC(bpm_values)

    async def start_scheduled_tasks(bpm_values):
        while True:
            await Control.scheduled_yt_call_recomm_music(bpm_values)
            await asyncio.sleep(10)  # 10초 주기 설정
    
    #endregion