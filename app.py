import streamlit as st
import pandas as pd
import os
import requests

# 파일 다운로드 경로
file_path = "./인천 개인별 대시보드.xlsx"
file_url = "https://raw.githubusercontent.com/leejunghyunA/DASHBOARD/main/인천%20개인별%20대시보드.xlsx"

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
st.title("🚗 운전자별 대시보드")
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
    
    # 운전자 프로필 정보 출력
    st.subheader(f"🚙 {user_name_input}님의 운전 성향 분석")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://via.placeholder.com/100", width=100)  # 기본 프로필 이미지
        st.markdown(f"**{user_name_input}({user_id_input})**")
        st.markdown(f"소속: **{company_input}**")
    with col2:
        st.markdown("### <종합 평가>")
        st.write("✔ 연비등급: S 등급")
        st.write("✔ 목표달성율: 116%")
        st.write("✔ 급가속: 0.08회/100km, 급감속: 1.06회/100km")
    
    # 차량별 항목별 수치 테이블
    st.subheader("🚛 차량별 항목별 수치")
    st.dataframe(dashboard_data)
    
    # 노선 내 수치 비교 (바 차트 시각화)
    st.subheader("📊 노선 내 나의 수치")
    labels = ["달성율", "월업", "공회전", "급가속", "급감속"]
    values = [116, 4.1, 26.9, 0.08, 1.06]
    avg_values = [91, 2.0, 34.5, 0.18, 4.65]
    fig, ax = plt.subplots()
    ax.bar(labels, avg_values, label="노선 평균", alpha=0.5)
    ax.bar(labels, values, label="내 수치")
    ax.legend()
    st.pyplot(fig)
    
    # 12월 vs 1월 비교 (바 차트 시각화)
    st.subheader("📉 12월 vs 1월 비교")
    prev_values = [110, 2.8, 28.5, 0.08, 1.41]
    fig2, ax2 = plt.subplots()
    ax2.bar(labels, prev_values, label="12월 수치", alpha=0.5)
    ax2.bar(labels, values, label="1월 수치")
    ax2.legend()
    st.pyplot(fig2)
    
    # 등급 추이 시각화
    st.subheader("📅 나만의 등급 달력 & 등급 추이")
    st.markdown("11월: S (111%) → 12월: S (110%) → 1월: S (116%)")
    
else:
    st.warning("운수사, 운전자 ID, 운전자 이름을 입력하세요.")
