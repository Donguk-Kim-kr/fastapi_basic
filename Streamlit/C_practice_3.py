import streamlit as st

st.header('간단 설문')

string1 = st.text_input(
    '이름을 입력하세요.',
    placeholder='예) 홍길동',
    max_chars=32
)

year = st.slider("나이를 입력하세요.", 0, 100, 0)



badge = st.multiselect(
    "획득한 배지를 입력하세요. : ",
    ["회색배지", "블루배지", "오렌지배지", "무지개배지", "핑크배지", "골드배지", "진홍색배지", "그린배지"]
)

level = st.slider("체감 난이도를 적어주세요. : ", 1, 10, 1)

st.write("---")

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

def button_write():
    st.session_state.submitted = True

st.button('제출하기', on_click=button_write)

if st.session_state.submitted:
    if string1:
        st.text(f'이름 : {string1}')
        if year >= 1:
            st.text(f"나이 : {year}세")
            if badge:
                st.text(f"획득한 배지 : {', '.join(badge)}")
                if level:
                    st.text(f"체감 난이도 : {level}")
    st.text("참여해주셔서 감사합니다.")