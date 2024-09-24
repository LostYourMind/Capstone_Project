### Youtube_Call.py


from Module.Heart_Rate import get_heart_rate, get_user_emotion


# 감정 상태에 맞춰 음악을 추천하는 함수
def recommend_music_based_on_emotion(emotion, music_data):
    """
    감정 상태에 맞춰 음악을 추천하는 함수.
    - 차분한 음악: Classical, Jazz, Ballad 장르의 음악을 추천.
    - 활동적인 음악: Pop, Rock, EDM 장르의 음악을 추천.
    """
    # 차분한 음악 리스트
    calm_music = [
        song for song in music_data if song["genre"] in ["Classical", "Jazz", "Ballad"]
    ]

    # 활동적인 음악 리스트
    active_music = [
        song for song in music_data if song["genre"] in ["Pop", "Rock", "EDM"]
    ]

    # 감정 상태에 따른 추천 로직
    if emotion == "stressed":
        return calm_music  # 스트레스를 받았을 때는 차분한 음악 추천
    elif emotion == "calm":
        return active_music  # 차분할 때는 활동적인 음악도 추천 가능
    else:
        return music_data  # 중립적인 상태에서는 모든 음악을 추천


# 음악 데이터 (예시)
music_data = [
    {"title": "Calm Classical Song", "genre": "Classical"},
    {"title": "Energetic Pop Song", "genre": "Pop"},
    {"title": "Soothing Jazz Song", "genre": "Jazz"},
    {"title": "Upbeat Rock Song", "genre": "Rock"},
]

# 심박수 데이터 수집 및 감정 상태 추론, 음악 추천 실행
heart_rate = get_heart_rate()  # 심박수 데이터 수집
emotion = get_user_emotion(heart_rate)  # 감정 상태 추론
recommended_music = recommend_music_based_on_emotion(
    emotion, music_data
)  # 감정 상태에 맞는 음악 추천

# 결과 출력
print(f"User's heart rate: {heart_rate}")
print(f"User's emotion: {emotion}")
print("Recommended music:")
for music in recommended_music:
    print(f"Title: {music['title']}, Genre: {music['genre']}")


# 테스트 코드
def test_recommend_music():
    """
    감정 상태에 따른 음악 추천 시스템이 올바르게 동작하는지 테스트하는 함수.
    """
    music_data = [
        {"title": "Calm Classical Song", "genre": "Classical"},
        {"title": "Energetic Pop Song", "genre": "Pop"},
        {"title": "Soothing Jazz Song", "genre": "Jazz"},
        {"title": "Upbeat Rock Song", "genre": "Rock"},
    ]

    # 스트레스 상태 (심박수 110)일 때는 차분한 음악 추천
    heart_rate = 110  # 예: 스트레스 상태
    emotion = get_user_emotion(heart_rate)
    recommended_music = recommend_music_based_on_emotion(emotion, music_data)
    assert all(
        song["genre"] in ["Classical", "Jazz", "Ballad"] for song in recommended_music
    ), "Expected calm music"

    # 차분한 상태 (심박수 55)일 때는 활동적인 음악 추천
    heart_rate = 55  # 예: 차분한 상태
    emotion = get_user_emotion(heart_rate)
    recommended_music = recommend_music_based_on_emotion(emotion, music_data)
    assert all(
        song["genre"] in ["Pop", "Rock", "EDM"] for song in recommended_music
    ), "Expected active music"

    print("All tests passed.")


# 테스트 실행
test_recommend_music()
