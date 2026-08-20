N8N_WEBHOOK_URL = "https://km2754.app.n8n.cloud/webhook-test/bus-arrival/webhook/bus-arrival"
import streamlit as st
import requests
import json
import time

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="실시간 스마트 버스 도착 비서",
    page_icon="🚌",
    layout="centered"
)

# 2. 커스텀 CSS 스타일링
st.markdown("""
<style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .arrival-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #2563EB;
        border-radius: 8px;
        padding: 16px;
        margin-top: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# 3. 헤더 섹션
st.markdown('<div class="main-title">🚌 실시간 스마트 버스 도착 비서</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">n8n 워크플로우 + 공공데이터포털 실시간 API 연동 데모</div>', unsafe_allow_html=True)

# n8n Webhook URL (나중에 실제 n8n 주소로 교체 가능)
N8N_WEBHOOK_URL = https://https://km2754.app.n8n.cloud/webhook-test/bus-arrival/webhook/bus-arrival

# 4. 빠른 테스트 샘플 버튼
st.markdown("##### ⚡ 빠른 테스트 (샘플 쿼리)")
sample_col1, sample_col2, sample_col3 = st.columns(3)

if "query_input" not in st.session_state:
    st.session_state.query_input = ""

with sample_col1:
    if st.button("📍 강남역 140번", use_container_width=True):
        st.session_state.query_input = "강남역 140번 버스 언제 와?"
with sample_col2:
    if st.button("📍 판교역 9007번", use_container_width=True):
        st.session_state.query_input = "판교역에서 9007번 버스 몇 분 남았어?"
with sample_col3:
    if st.button("📍 사당역 7770번", use_container_width=True):
        st.session_state.query_input = "사당역 4번출구 7770번 버스 도착 정보"

# 5. 사용자 입력 폼
user_query = st.text_input(
    "정류장과 버스 번호를 입력하세요",
    value=st.session_state.query_input,
    placeholder="예: 강남역에서 140번 버스 몇 분 뒤에 도착해?"
)

search_clicked = st.button("실시간 버스 도착 조회하기", type="primary", use_container_width=True)

# 6. n8n 통신 및 결과 표시
if search_clicked:
    if not user_query.strip():
        st.warning("⚠️ 정류장 또는 버스 번호를 입력해 주세요.")
    else:
        with st.spinner("🤖 n8n AI 에이전트가 실시간 공공데이터를 조회 중입니다..."):
            try:
                payload = {
                    "message": user_query,
                    "timestamp": time.time()
                }
                
                # n8n URL이 기본값인 경우 데모용 가상 데이터로 응답
                if "your-n8n-domain" in N8N_WEBHOOK_URL:
                    time.sleep(1.0)
                    result = {
                        "status": "success",
                        "station": "강남역",
                        "bus_number": "140번",
                        "first_bus": {
                            "arrival_time": "3분 20초 후",
                            "remaining_stops": "2개 전 정류장",
                            "congestion": "여유"
                        },
                        "second_bus": {
                            "arrival_time": "11분 후",
                            "remaining_stops": "7개 전 정류장",
                            "congestion": "보통"
                        },
                        "ai_summary": "현재 140번 버스가 약 3분 뒤 도착할 예정입니다. 좌석은 여유롭습니다."
                    }
                else:
                    response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=15)
                    if response.status_code == 200:
                        result = response.json()
                    else:
                        st.error(f"서버 통신 실패 (상태 코드: {response.status_code})")
                        st.stop()

                st.success("✅ 실시간 도착 정보 조회 성공!")
                
                if "ai_summary" in result:
                    st.markdown(f"**📢 실시간 브리핑:** {result['ai_summary']}")
                
                card_col1, card_col2 = st.columns(2)
                with card_col1:
                    fb = result.get("first_bus", {})
                    st.markdown(f"""
                    <div class="arrival-card">
                        <h4 style="margin:0 0 8px 0; color:#1E40AF;">🥇 첫 번째 버스</h4>
                        <p style="font-size:1.4rem; font-weight:700; color:#2563EB; margin:4px 0;">{fb.get('arrival_time', '도착 정보 없음')}</p>
                        <p style="margin:0; color:#475569;">📍 위치: {fb.get('remaining_stops', '-')}</p>
                        <p style="margin:0; color:#475569;">👥 혼잡도: {fb.get('congestion', '-')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                with card_col2:
                    sb = result.get("second_bus", {})
                    st.markdown(f"""
                    <div class="arrival-card" style="border-left-color: #64748B;">
                        <h4 style="margin:0 0 8px 0; color:#475569;">🥈 다음 버스</h4>
                        <p style="font-size:1.4rem; font-weight:700; color:#475569; margin:4px 0;">{sb.get('arrival_time', '도착 정보 없음')}</p>
                        <p style="margin:0; color:#475569;">📍 위치: {sb.get('remaining_stops', '-')}</p>
                        <p style="margin:0; color:#475569;">👥 혼잡도: {sb.get('congestion', '-')}</p>
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")

# 7. 아키텍처 토글
st.markdown("---")
with st.expander("🛠️ 시스템 아키텍처 및 기술 스택 보기"):
    st.markdown("""
    * **Frontend:** Streamlit Community Cloud
    * **Backend & Pipeline:** n8n (Webhook → LLM Parsing → Public API → Response)
    * **API:** 공공데이터포털 버스도착정보 실시간 API
    """)
