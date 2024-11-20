import os
import sys
import numpy as np
import schedule
import time
from scipy.signal import welch

sys.path.append("../")  # Add parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


def calculate_ibi(bpm):
    bpm = np.array(bpm)
    bpm = bpm[bpm > 0]  # 0보다 큰 값만 사용하여 IBI 계산
    if len(bpm) == 0:
        raise ValueError("유효한 BPM 값이 없습니다.")
    return 60000 / bpm

def calculate_sdnn(ibi_values):
    return np.std(ibi_values)

def calculate_rmssd(ibi_values):
    successive_diffs = np.diff(ibi_values)
    squared_diffs = successive_diffs ** 2
    mean_squared_diff = np.mean(squared_diffs)
    return np.sqrt(mean_squared_diff)

def calculate_pnn50(ibi_values):
    successive_diffs = np.abs(np.diff(ibi_values))  # 연속된 IBI 차이 계산
    count_above_50 = np.sum(successive_diffs > 0.05)  # 초 단위에서 0.05 이상 차이
    return (count_above_50 / len(successive_diffs)) * 100

def calculate_frequency_domain_features(ibi_values):
    ibi_values = np.array(ibi_values) / 1000.0
    fs = 4
    freqs, psd = welch(ibi_values, fs=fs, nperseg=len(ibi_values))
    lf_band = (0.04, 0.15)
    hf_band = (0.15, 0.4)
    
    lf_power = np.trapz([psd[i] for i, f in enumerate(freqs) if lf_band[0] <= f < lf_band[1]], dx=np.diff(freqs).mean())
    hf_power = np.trapz([psd[i] for i, f in enumerate(freqs) if hf_band[0] <= f < hf_band[1]], dx=np.diff(freqs).mean())
    lf_hf_ratio = lf_power / hf_power if hf_power != 0 else None

    return {
        "LF": lf_power,
        "HF": hf_power,
        "LF/HF Ratio": lf_hf_ratio
    }
