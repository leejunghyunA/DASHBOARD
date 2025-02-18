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
    df_final.iloc[5, 33] = company_input  # AH6
    df_final.iloc[5, 34] = user_id_input  # AI6
    df_final.iloc[5, 35] = user_name_input  # AJ6
    
    # 데이터 가져오기
    user_grade = df_final.iloc[11, 33]  # AH12
    user_summary = df_final.iloc[15, 33]  # AH16
    vehicle_data = df_final.iloc[17:28, 39:50]  # AN18:AX28
    route_stats = df_final.iloc[5:7, 39:45]  # AN6:AT7
    monthly_comparison = df_final.iloc[10:12, 39:45]  # AN11:AT12
    calendar_data = df_final.iloc[6:16, 51:57]  # AZ7:AF16
    grade_trend = df_final.iloc[22:25, 51:57]  # AZ23:BB25
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("프로필.PNG", width=100)
        st.markdown(f"**{user_name_input}({user_id_input})**")
        st.markdown(f"소속: **{company_input}**")
        st.markdown(f"### {user_grade}")
        st.caption("이달의 등급")
    with col2:
        st.markdown("### <종합 평가>")
        st.write(user_summary)
    
    st.subheader("🚛 차량별 항목별 수치")
    vehicle_data.columns = ["운수사", "노선", "차량번호", "주행거리", "웜업", "공회전", "급가속", "연비", "달성율", "등급"]
    vehicle_data = vehicle_data.dropna(how='all')
    vehicle_data["웜업"] = vehicle_data["웜업"].apply(lambda x: f"{x:.2f}%")
    vehicle_data["공회전"] = vehicle_data["공회전"].apply(lambda x: f"{x:.2f}%")
    vehicle_data["급가속"] = vehicle_data["급가속"].apply(lambda x: f"{x:.2f}")
    vehicle_data["연비"] = vehicle_data["연비"].apply(lambda x: f"{x:.2f}")
    vehicle_data["달성율"] = vehicle_data["달성율"].apply(lambda x: f"{x:.0f}%")
    st.dataframe(vehicle_data)
    
    st.subheader("📊 노선 내 나의 수치")
    labels = ["달성율", "웜업", "공회전", "급가속", "급감속"]
    fig, ax = plt.subplots()
    ax.bar(labels, route_stats.iloc[0], label="노선 평균", alpha=0.5)
    ax.bar(labels, route_stats.iloc[1], label="내 수치")
    ax.legend()
    st.pyplot(fig)
    
    st.subheader("📉 12월 vs 1월 비교")
    fig2, ax2 = plt.subplots()
    ax2.bar(labels, monthly_comparison.iloc[0], label="12월 수치", alpha=0.5)
    ax2.bar(labels, monthly_comparison.iloc[1], label="1월 수치")
    ax2.legend()
    st.pyplot(fig2)
    
    st.subheader("📅 나만의 등급 달력")
    st.dataframe(calendar_data.dropna(how='all'))
    
    st.subheader("📊 월별 등급 추이")
    st.write(grade_trend)
else:
    st.warning("운수사, 운전자 ID, 운전자 이름을 입력하세요.")
