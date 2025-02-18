import streamlit as st
import pandas as pd
import os
import requests

# 파일 다운로드 경로
file_path = "./인천 개인별 대시보드.xlsm"
file_url = "https://raw.githubusercontent.com/YOUR_GITHUB_REPO/main/인천%20개인별%20대시보드.xlsm"

# 파일이 없거나 손상된 경우 다운로드
if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
    with st.spinner("데이터 파일 다운로드 중..."):
        response = requests.get(file_url)
        with open(file_path, "wb") as f:
            f.write(response.content)
        st.success("파일 다운로드 완료!")

# 엑셀 파일 확인 및 로드
def load_excel(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        df_final = pd.read_excel(xls, sheet_name="최종(개인별)", header=None)
        return df_final
    except Exception as e:
        st.error(f"엑셀 파일을 불러오는 중 오류 발생: {e}")
        return None

df_final = load_excel(file_path)

# Streamlit UI 구성
st.title("운전자별 대시보드")
company_input = st.text_input("운수사를 입력하세요")
user_id_input = st.text_input("운전자 ID를 입력하세요")
user_name_input = st.text_input("운전자 이름을 입력하세요")

if df_final is not None and company_input and user_id_input and user_name_input:
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
