import requests
import time

YOUTUBE_API_KEY = "AIzaSyBcSKTR5Ls4U4cVp5ji_ZEjxXTL-_DBt2E"
BASE_YOUTUBE_URL = "https://www.youtube.com/watch?v="

# 감정 상태와 검색어 쿼리를 딕셔너리로 정의
EMOTION_QUERIES = {
    "C": "calm relaxing music",
    "E": "exciting upbeat music",
    "H": "happy music",
    "S": "sad emotional music",
    "F": "focus study music",
    "R": "romantic love songs",
    "M": "motivational workout music",
    "T": "stress relief music",
    "A": "adventure music",
}

class YouTubeMusicRecommender:
    def __init__(self):
        # 각 감정에 대한 마지막 호출 시간을 추적하는 딕셔너리
        self.last_called = {emotion: 0 for emotion in EMOTION_QUERIES}

    def get_youtube_video(self, query: str) -> str:
        """YouTube API로 검색하여 첫 번째 동영상의 URL 반환."""
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&type=video&key={YOUTUBE_API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # 요청에 실패하면 예외 발생
            video_data = response.json()

            # 첫 번째 동영상의 videoId를 가져와 URL 생성
            if "items" in video_data and video_data["items"]:
                video_id = video_data["items"][0]["id"]["videoId"]
                return BASE_YOUTUBE_URL + video_id
            else:
                return "No video found"
        except requests.RequestException as e:
            return f"Error fetching video: {e}"

    def recommend_music(self, emotion: str) -> str:
        """감정 상태에 맞는 추천 음악 URL 반환 (10초마다 호출 가능)."""
        current_time = time.time()  # 현재 시간을 초 단위로 가져옴
        last_time = self.last_called.get(emotion, 0)
        
        # 마지막 호출 이후 10초가 지나지 않았으면 호출 제한
        if current_time - last_time < 10:
            return f"Wait before requesting more music for emotion '{emotion}'."

        # 10초가 지난 경우, 새로운 추천 URL 생성
        query = EMOTION_QUERIES.get(emotion, "music")  # 기본 검색어는 "music"
        video_url = self.get_youtube_video(query)

        # 마지막 호출 시간을 현재 시간으로 업데이트
        self.last_called[emotion] = current_time

        return video_url