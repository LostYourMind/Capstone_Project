import sys
import os
from API.Youtube_Call import test_recommend_music as trm

sys.path.append("../")  # 상위 디렉터리 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


temp = trm()
print(f"temp_data = {temp}")
