import requests
import time
import isodate

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
        # 각 감정에 대한 마지막 호출 시간과 기다려야 할 시간(초)을 추적하는 딕셔너리
        self.last_called = {emotion: 0 for emotion in EMOTION_QUERIES}
        self.wait_time = {emotion: 10 for emotion in EMOTION_QUERIES}  # 기본 대기 시간 10초로 설정

    def get_youtube_video(self, query: str) -> str:
        """YouTube API로 검색하여 첫 번째 동영상의 URL과 ID 반환."""
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&type=video&key={YOUTUBE_API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # 요청에 실패하면 예외 발생
            video_data = response.json()

            # 첫 번째 동영상의 videoId를 가져와 URL 생성
            if "items" in video_data and video_data["items"]:
                video_id = video_data["items"][0]["id"]["videoId"]
                video_url = BASE_YOUTUBE_URL + video_id
                return video_url, video_id
            else:
                return "No video found", None
        except requests.RequestException as e:
            return f"Error fetching video: {e}", None

    def get_video_duration(self, video_id: str) -> str:
        """동영상 ID를 사용하여 YouTube 동영상의 길이를 ISO 8601 형식으로 반환."""
        url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={video_id}&key={YOUTUBE_API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            video_data = response.json()

            # 동영상 길이 가져오기
            if "items" in video_data and video_data["items"]:
                duration = video_data["items"][0]["contentDetails"]["duration"]
                return duration  # ISO 8601 형식 반환 (예: PT4M13S)
            else:
                return "No duration found"
        except requests.RequestException as e:
            return f"Error fetching duration: {e}"

    def parse_iso8601_duration(self, duration_str: str) -> int:
        """ISO 8601 형식의 기간을 초 단위로 변환하여 반환"""
        duration = isodate.parse_duration(duration_str)
        return int(duration.total_seconds())  # 초 단위로 반환

    def recommend_music(self, emotion: str) -> str:
        """감정 상태에 맞는 추천 음악 URL과 길이 반환 (동영상 길이만큼 대기 후 호출 가능)."""
        current_time = time.time()  # 현재 시간을 초 단위로 가져옴
        last_time = self.last_called.get(emotion, 0)
        
        # 마지막 호출 이후 이전 동영상 길이(초)만큼 지나지 않았으면 호출 제한
        if current_time - last_time < self.wait_time[emotion]:
            remaining_time = int(self.wait_time[emotion] - (current_time - last_time))
            return f"Wait {remaining_time} seconds before requesting more music for emotion '{emotion}'."

        # 새로운 추천 URL 생성
        query = EMOTION_QUERIES.get(emotion, "music")  # 기본 검색어는 "music"
        video_url, video_id = self.get_youtube_video(query)

        if video_id:  # video_id가 유효한 경우에만 동영상 길이 조회
            video_duration = self.get_video_duration(video_id)
            video_duration_seconds = self.parse_iso8601_duration(video_duration)
            
            # 동영상 길이를 다음 호출 대기 시간으로 설정
            self.wait_time[emotion] = video_duration_seconds
            #self.last_called[emotion] = current_time
            self.last_called[emotion] = 1

            return video_url
        else:
            return video_url
