import requests


class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1"

    def get_weather_data(self, city):
        """현재 날씨 및 대기질 데이터를 요청하는 함수"""
        weather_url = (
            f"{self.base_url}/current.json?key={self.api_key}&q={city}&aqi=yes"
        )
        response = requests.get(weather_url)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Error: Unable to fetch data (Status code: {response.status_code})"
            )

    def parse_weather_data(self, data):
        """날씨 데이터를 파싱하는 함수"""
        current_weather = data["current"]
        weather_info = {
            "temperature": current_weather["temp_c"],
            "humidity": current_weather["humidity"],
            "wind_speed": current_weather["wind_kph"],
            "condition": current_weather["condition"]["text"],
        }

        return weather_info

    def parse_air_quality_data(self, data):
        """대기질 데이터를 파싱하는 함수"""
        air_quality = data["current"]["air_quality"]
        air_quality_info = {
            "pm2_5": air_quality.get("pm2_5", "N/A"),
            "pm10": air_quality.get("pm10", "N/A"),
            "co": air_quality.get("co", "N/A"),
            "no2": air_quality.get("no2", "N/A"),
            "o3": air_quality.get("o3", "N/A"),
        }

        return air_quality_info
