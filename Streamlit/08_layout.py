"""
Streamlit 레이아웃 기초 실습
=============================
학습 포인트:
  1. 사이드바 (st.sidebar)
  2. 이미지 출력 (st.image)
  3. 컬럼 레이아웃 (st.columns)
  4. 탭 레이아웃 (st.tabs)
  5. seaborn + matplotlib 차트를 Streamlit에 삽입하는 방법

필요 파일 (./input/ 폴더 안에 있어야 함):
  - image2.jpg
  - image3.jpg
  - medical_cost.csv
"""

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image


# 1. 메인 페이지 제목
st.title('This is main page')


# 2. 사이드바 (with st.sidebar 블록 안 = 왼쪽 사이드바에 표시)
with st.sidebar:
    st.title('This is sidebar')

    # st.multiselect : 여러 항목을 동시에 선택할 수 있는 드롭다운 위젯
    # 반환값: 사용자가 선택한 항목들의 리스트 (미선택 시 빈 리스트 [])
    side_option = st.multiselect(
        label='your selection is',
        options=['Car', 'Airplane', 'Train', 'Ship', 'Bicycle'],
        placeholder='select transportation'
    )


# 3. 이미지 불러오기 (PIL)
img2 = Image.open('./input/image2.jpg')
img3 = Image.open('./input/image3.jpg')


# 4. 이미지 세로 나열 (컬럼 미사용 - 기본 레이아웃)
st.header('Lemonade')
st.image(img2, width=300, caption='Image from Unsplash')

st.header('Cocktail')
st.image(img3, width=300, caption='Image from Unsplash')


# 5. 컬럼 레이아웃 (st.columns(2) : 화면을 동일 너비 2열로 분할)
# 비율 지정 예시 → st.columns([2, 1])  : 2:1 비율로 분할
col1, col2 = st.columns(2)

with col1:
    st.header('Lemonade')
    st.image(img2, width=300, caption='Image from Unsplash')

with col2:
    st.header('Cocktail')
    st.image(img3, width=300, caption='Image from Unsplash')


# 6. 탭 레이아웃 (st.tabs() : 탭 레이블 리스트 → 탭 객체 리스트 반환)
tab1, tab2 = st.tabs(['Table', 'Graph'])

df = pd.read_csv('./input/medical_cost.csv')
df = df.query('region == "northwest"')   # .query() : SQL WHERE 절처럼 필터링

with tab1:
    # st.table : 정적 테이블 (정렬·스크롤 불가), .head(5) : 상위 5행
    st.table(df.head(5))

with tab2:
    # matplotlib Figure 객체 생성 후 seaborn으로 그리고 st.pyplot(fig)로 출력
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x='bmi', y='charges', ax=ax)
    st.pyplot(fig)