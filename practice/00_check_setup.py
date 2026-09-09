"""
practice/00_check_setup.py
------------------------------------------------------
설치 확인 + Gemini API KEY 연결 확인 테스트

이 파일의 목적
- .env에 넣어둔 GOOGLE_API_KEY가 제대로 읽히는지 확인
- GEMINI모델에 실제로 요청을 보내고, 응답을 받아오는지 확인
- 여기서 에러가 나면 이후 모든 실습이 진행되지 않으므로 꼭 통과시킬 것!

"""

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise SystemExit("GOOGLE_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

from langchain_google_genai import ChatGoogleGenerativeAI

# 가벼운 모델 설정 --> gemini-3.6-flash
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

response = llm.invoke("한 문장으로 자기 소개 해줘.")

print("연결 성공. 모델 응답 : ")
print(response.content[0]["text"])