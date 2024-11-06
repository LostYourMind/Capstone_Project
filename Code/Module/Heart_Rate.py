### Heart_Rate.py
### TETS CODE


# 심박수 데이터를 바탕으로 사용자의 감정 상태를 추론하는 함수
# 모델을 통한 심박수 데이터를 바탕으로 사용자 감정 상태를 추론 필요
def get_user_emotion(heart_rate: int):
    """
    심박수 데이터를 기반으로 사용자의 감정 상태를 반환하는 함수.
    """
    if heart_rate > 100:
        return "T" # stress relief music
    elif heart_rate < 85 and heart_rate > 60 :
        return "C" # calm relaxing music
    elif heart_rate < 60 :
        return "E" #exciting upbeat music
    else:
        return "H" #happy music
