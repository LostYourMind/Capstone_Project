# GPT_API.py
# GPT API를 활용한 코드들

import openai
import sys
import io
import os
import pytz

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 감정 상태와 검색어 쿼리를 딕셔너리로 정의
EMOTION_QUERIES = {
    "Calm","Exciting","Happy","Sad","Stress"
}

class USE_GPT:
    # api_key = os.environ.get("OPENAI_API_KEY")
    api_key = ""

    openai.api_key = api_key

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

    def generate_chat(prompt):
        """
        챗 모델을 이용한 텍스트 생성 함수.

        :param prompt: 모델에게 전달할 프롬프트.
        :param model: 사용할 모델의 이름.
        :param temperature: 생성된 텍스트의 창의성을 결정하는 온도 매개변수.
        :param max_tokens: 생성할 토큰(단어)의 최대 수.
        :return: 생성된 텍스트.
        """
        model = "gpt-4o"
        temperature = 0.7
        max_tokens = 300

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message["content"].strip()

    # GPT 호출
    def generate_Sentences(self, prompt):
        try:
            generated_text = USE_GPT.generate_chat(prompt)
            return generated_text
        except Exception as ex:
            print("오류 발생 :", ex)

    # 매뉴 추천 함수
    def TestModule(self, ibi, sdnn, rmssd, pnn50):
        temp_data = f"사용자의 IBI, SDNN,RMSSD,PNN50 값은 각 {ibi}, {sdnn}, {rmssd}, {pnn50} 이야. 해당 사용자의 현재 감정을 {EMOTION_QUERIES} 중에서 가장 가까운 감정을 선택해서 알려줘."
        try:
            generated_text = USE_GPT.generate_chat(temp_data)
            return generated_text
        except Exception as ex : 
            return f"Occur Exception : {ex}"
