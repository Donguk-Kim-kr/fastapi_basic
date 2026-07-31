# ========================================================================
# ~/bigdata2026/fastapi/Streamlit/13_use_form2.py
#   
# 폼 위젯 : 입력값 검증
# ========================================================================
import streamlit as st

st.title("회원가입 (검증 포함)")

# "signup_form": 폼 이름은 폼을 구분하는 고유한 이름(key), 폼이 여러 개면 서로 다른 이름을 주어야 한다.
with st.form("signup_form"):
    name = st.text_input("이름")
    email = st.text_input("이메일")
    age = st.number_input("나이", min_value=0, max_value=150, value=20) # 기본값 20으로 설정
    agree = st.checkbox("이용약관에 동의합니다")

    # 일반 버튼 위젯이 아니고 폼 안에서만 사용할 수 있는 버튼 위젯을 사용해야 한다.
    submmited = st.form_submit_button("가입하기")

# 버튼을 클릭 -> 폼 제출 시점의 최종값을 그대로 가지고 있다. (with 블록 밖에서 해도 된다.)
if submmited:
    if not name:
        st.error("이름을 입력해주세요.")

    elif "@" not in email:
        st.error("올바른 이메일을 입력해주세요.")

    elif not agree:
        st.error("이용약관을 확인해주세요.")

    else:
        st.success(f"{name}님, 가입이 완료되었습니다. 이메일: {email}, 나이: {age}")