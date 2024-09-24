### Heart_Rate.py


# 심박수 데이터를 수집하는 함수
def get_heart_rate():
    """
    심박수 데이터를 스마트워치 또는 다른 센서에서 가져오는 함수.
    실제 구현에서는 API 통신 또는 블루투스 통신을 사용해야 함.
    """
    # 예시 심박수 데이터 (실제 구현에서는 스마트워치 또는 센서에서 데이터를 가져옴)
    heart_rate = 85  # 예: 현재 심박수
    return heart_rate


# 심박수 데이터를 바탕으로 사용자의 감정 상태를 추론하는 함수
def get_user_emotion(heart_rate):
    """
    심박수 데이터를 기반으로 사용자의 감정 상태를 반환하는 함수.
    - 심박수 > 100: 스트레스를 받았거나 흥분한 상태 (stressed)
    - 심박수 < 60: 차분한 상태 (calm)
    - 그 외: 중립적인 상태 (neutral)
    """
    if heart_rate > 100:
        return "stressed"
    elif heart_rate < 60:
        return "calm"
    else:
        return "neutral"
