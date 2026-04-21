import streamlit as st
import requests

# [중요] 캐글에서 복사한 주소를 여기에 한 번만 입력하세요!
# 캐글 세션을 새로 시작할 때마다 이 주소만 바꿔주면 됩니다.
KAGGLE_URL = "https://passerby-blustery-magnolia.ngrok-free.dev"

# 앱 페이지 설정
st.set_page_config(page_title="시크릿 에이전트", page_icon="🕵️‍♂️", layout="wide")

# 사이드바: 아이 정보 입력만 남기기
with st.sidebar:
    st.title("👶 아이 정보 입력")
    st.info("아이의 취향을 입력하면 에이전트가 작동합니다.")
    
    ingredients = st.text_input("냉장고 재료", placeholder="예: 시금치, 계란")
    hated = st.text_input("싫어하는 음식", placeholder="예: 시금치")
    interest = st.text_input("관심사 (주제)", placeholder="예: 공룡, 우주")
    
    st.divider()
    generate_btn = st.button("🪄 마법의 솔루션 생성", use_container_width=True)

# 메인 화면
st.title("🕵️‍♂️ 시크릿 에이전트: 우리 아이 편식 해결")

if generate_btn:
    if not ingredients or not hated or not interest:
        st.warning("아이 정보를 모두 입력해 주세요!")
    else:
        payload = {"ingredients": ingredients, "hated": hated, "interest": interest}
        
        try:
            with st.spinner('에이전트들이 비밀 작전을 수행 중입니다... 🕵️‍♂️🍳'):
                # 위에서 설정한 KAGGLE_URL을 바로 사용합니다.
                response = requests.post(f"{KAGGLE_URL}/generate", json=payload, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("솔루션 완성!")
                    st.balloons()
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("### 🧑‍🍳 에이전트 1: 비밀 레시피")
                        st.info(f"**{hated} 숨기기 작전**")
                        st.write(result.get("recipe", "레시피 생성 실패"))
                    with col2:
                        st.markdown("### 📖 에이전트 2: 맞춤형 동화")
                        st.info(f"**{interest}와 함께하는 식사**")
                        st.write(result.get("story", "동화 생성 실패"))
                else:
                    st.error(f"서버 응답 오류 (Status: {response.status_code})")
        except Exception as e:
            st.error("서버 연결에 실패했습니다. 코드 상단의 KAGGLE_URL이 최신인지 확인하세요!")

else:
    st.write("---")
    st.write("👈 왼쪽 사이드바에 정보를 입력하고 버튼을 눌러보세요!")