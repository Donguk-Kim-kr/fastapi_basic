import streamlit as st

st.header('나만의 자기소개 카드')

name = st.text_input(
    '이름을 입력하세요.',
    placeholder='예) 홍길동',
    max_chars=32
)

year = st.slider("나이를 입력하세요.", 0, 100, 0)



skill = st.selectbox(
    "관심있는 문장을 선택하세요. : ",
    ["용기", "우정", "순수", "사랑", "지식", "성실", "희망", "빛"]
)

st.write("---")

if name:
    st.text(f"이름 : {name}")
    if year >= 1 :
        st.text(f"나이 : {year}세")
        if skill :
            st.text(f"문장 : {''.join(skill)}")
            if year >= 20:
                st.text(f"당신은 선택받은 '아이'가 될 수 없습니다.")
            else:
                st.text(f"당신은 {''.join(skill)}의 문장을 선택받았습니다.")