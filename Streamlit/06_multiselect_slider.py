# ========================================================================
# ~/bigdata2026/fastapi/Streamlit/06_multiselect_slider.py
#   
#   Streamlit 라이브러리 기초 실습
#
#       - 입력 위젯 (다중 선택 박스, 숫자 슬라이더 등)
# ========================================================================
import streamlit as st
from datetime import time

# 다중 선택 박스
st.title("Streamlit 입력 위젯 실습")
st.divider()

st.subheader("1. 다중 선택 박스 퀴즈")

fruits = st.multiselect(
    "Q1. 과일을 모두 선택하세요.(복수 정답 가능) : ",
    ["레몬", "키위", "파인애플", "딸기", "포도", "수박"]
)

correct = {"레몬", "키위", "파인애플", "딸기", "포도", "수박"} # set

if set(fruits) == correct:
    st.write("정답이다. 모두 과일이지.")
else:
    st.write("더 찾아보거라. 정답을 두고 왔으니.")

st.divider()
st.subheader("2. 숫자 슬라이더")

# 0부터 100까지의 점수를 슬라이더로 입력받는다.
score = st.slider("너의 점수는...", 0, 100, 50) # 기본값은 50

st.text(f"점수 : {score}")

st.divider()
st.subheader("3. 시간 범위 슬라이더")

start_time, end_time = st.slider(
    "근무시간은 ...",
    min_value=time(0),
    max_value=time(23),
    value=(time(9), time(18)),
    format="HH:mm"
)

st.text(f"근무시간 : {start_time}, {end_time}")


# 실습 1: 보기와 정답 바꾸기
animals = st.multiselect(
    "Q. 동물을 모두 선택하세요:",
    ["강아지", "자동차", "고양이", "책상"]
)
correct_animals = {"강아지", "고양이"}

# 실습 2: 점수에 따라 다른 메시지
if score >= 80:
    st.write("좋은 점수입니다.")
elif score >= 60:
    st.write("조금만 더 연습해 봅시다.")
else:
    st.write("기초부터 다시 복습해 봅시다.")

# 실습 3: 기본 근무 시간을 10시~17시로 변경
value=(time(10), time(17))