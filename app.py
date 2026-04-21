import streamlit as st
import requests

# 페이지 설정
st.set_page_config(page_title="시크릿 에이전트", layout="wide", page_icon="🍳")

# 사이드바: Kaggle 서버 주소 입력 및 사용자 정보 수집
with st.sidebar:
    st.header("🔗 서버 설정")
    # Kaggle에서 실행한 ngrok 주소를 여기에 입력합니다.
    api_url = st.text_input("Kaggle API URL", placeholder="https://passerby-blustery-magnolia.ngrok-free.dev")
    
    st.divider()
    
    st.header("📝 정보 입력")
    ingredients = st.text_input("냉장고 재료", "계란, 시금치")
    hated = st.text_input("아이가 싫어하는 재료", "시금치")
    interest = st.text_input("아이의 관심사", "요정")
    
    st.divider()
    submit = st.button("마법의 솔루션 생성 ✨")

# 메인 화면 구성
st.title("🍳 시크릿 에이전트: LLM 편식 교정")
st.write("사용자의 냉장고 상황과 아이의 기피 식재료를 실시간으로 반영한 '은폐 레시피'와 '맞춤형 동화'를 생성합니다.")

if submit:
    if not api_url:
        st.error("사이드바에 Kaggle API URL을 입력해주세요!")
    else:
        with st.spinner("LLM 에이전트가 최적의 솔루션을 찾는 중입니다..."):
            try:
                # Kaggle 백엔드 서버로 요청 전송
                payload = {
                    "ingredients": ingredients,
                    "hated": hated,
                    "interest": interest
                }
                # /generate 엔드포인트로 POST 요청
                response = requests.post(f"{api_url}/generate", json=payload, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("🧑‍🍳 Recipe Agent")
                        st.success("### 은폐 레시피")
                        st.write(result['recipe'])
                        
                    with col2:
                        st.subheader("📖 Story Agent")
                        st.info("### 맞춤형 동화")
                        st.write(result['story'])
                        
                    st.divider()
                    st.caption("실시간 언어 지능을 통해 부모의 심리적 안정과 자녀와의 유대 회복을 지원합니다.")
                else:
                    st.error(f"서버 오류: {response.status_code}")
            except Exception as e:
                st.error(f"연결 실패: {e}\nKaggle 서버가 켜져 있는지, URL이 맞는지 확인하세요.")
else:
    # 초기 안내 화면
    st.info("왼쪽 사이드바에서 재료와 아이의 정보를 입력하고 버튼을 눌러주세요.")
