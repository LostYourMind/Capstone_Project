import numpy as np

def calculate_hrv_from_bpm(bpm_values):
    ibi_values = [(60 / bpm) * 1000 for bpm in bpm_values]  # IBI를 ms 단위로 변환

    sdnn = np.std(ibi_values, ddof=1)

    ibi_diffs = np.diff(ibi_values)  # 연속된 IBI 간 차이 계산
    rmssd = np.sqrt(np.mean(ibi_diffs ** 2))  # 제곱 평균 제곱근 계산
    
    return {'SDNN': sdnn, 'RMSSD': rmssd}

def calculate_ibi(bpm):
    """
    BPM 값을 입력받아 IBI를 계산하는 함수
    """
    if bpm <= 0:
        raise ValueError("BPM 값은 0보다 커야 합니다.")
    ibi = 60000 / bpm  # BPM을 ms로 변환
    return ibi

def calculate_sdnn(ibi_values):
    return np.std(ibi_values)

def calculate_rmssd(ibi_values):
    successive_diffs = np.diff(ibi_values)
    squared_diffs = successive_diffs ** 2
    mean_squared_diff = np.mean(squared_diffs)
    return np.sqrt(mean_squared_diff)

def calculate_pnn50(ibi_values):
    successive_diffs = np.abs(np.diff(ibi_values))
    count_above_50 = np.sum(successive_diffs > 50)
    return (count_above_50 / (len(ibi_values) - 1)) * 100
