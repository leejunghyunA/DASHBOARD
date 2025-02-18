import streamlit as st
import pandas as pd

# 엑셀 파일 로드
file_path = "인천 개인별 대시보드.xlsm"
xls = pd.ExcelFile(file_path)

def load_data():
    df_final = pd.read_excel(xls, sheet_name="최종(개인별)", header=None)
    return df_final

df_final = load_data()

# Streamlit UI 구성
st.title("운전자별 대시보드")
company_input = st.text_input("운수사를 입력하세요")
user_id_input = st.text_input("운전자 ID를 입력하세요")
user_name_input = st.text_input("운전자 이름을 입력하세요")

if company_input and user_id_input and user_name_input:
    # AH6:AJ6에 입력값을 반영 (엑셀 수식을 활용한 연산)
    df_final.iloc[5, 33] = company_input  # AH6
    df_final.iloc[5, 34] = user_id_input  # AI6
    df_final.iloc[5, 35] = user_name_input  # AJ6
    
    # AH5:BF25 범위의 데이터를 가져오기
    dashboard_data = df_final.iloc[4:25, 33:58]
    
    # A2:AF42에 최종 결과 데이터 반영
    final_dashboard = df_final.iloc[1:43, 0:32]
    
    st.subheader("대시보드 결과")
    st.write(final_dashboard)
    
    st.subheader("세부 계산 데이터")
    st.write(dashboard_data)
    
else:
    st.warning("운수사, 운전자 ID, 운전자 이름을 입력하세요.")