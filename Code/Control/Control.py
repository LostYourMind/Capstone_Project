### Control.py

import logging
from API.Youtube_Call import test_recommend_music as trm
from API.Weather import WeatherAPI


# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Control")

api_key = "08682524e061471b87b64659240104"

weather = WeatherAPI(api_key=api_key)


class Control:

    def YT_CALL_RECOMM_MUSIC():
        temp = trm()
        logger.info(f"Recommend : {temp}")
        return temp

    def Weather_API_CALL():
        rawResult = weather.get_weather_data(city="Seoul")
        weather_Result = weather.parse_weather_data(rawResult)
        airCondition_Result = weather.parse_air_quality_data(rawResult)

        return weather_Result, airCondition_Result
