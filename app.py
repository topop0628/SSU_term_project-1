import streamlit as st
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

KAGGLE_URL = "https://exponent-ungraded-related.ngrok-free.dev"

st.set_page_config(page_title="시크릿 에이전트", page_icon="🕵️‍♂️", layout="wide")

st.title("🕵️‍♂️ 시크릿 에이전트: 우리 아이 편식 해결")

with st.sidebar:
    st.title("👶 아이 정보 입력")

    ingredients = st.text_input("냉장고 재료", placeholder="예: 시금치, 계란")
    hated = st.text_input("싫어하는 음식", placeholder="예: 시금치")
    interest = st.text_input("관심사", placeholder="예: 공룡, 우주")

    generate_btn = st.button("🪄 생성")

if generate_btn:
    payload = {
        "ingredients": ingredients,
        "hated": hated,
        "interest": interest
    }

    try:
        with st.spinner("생성 중..."):
            response = requests.post(
                f"{KAGGLE_URL}/generate",
                json=payload,
                timeout=300,
                verify=False
            )

        st.write("status:", response.status_code)

        if response.status_code == 200:
            result = response.json()

            recipe = result.get("recipe", {})
            story = result.get("story", {})

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🧑‍🍳 레시피")
                st.write("요리명:", recipe.get("dish_name", "없음"))
                st.write("전략:", recipe.get("strategy", "없음"))
                st.write(recipe.get("content", "실패"))

            with col2:
                st.subheader("📖 스토리")
                st.write("전략:", story.get("strategy", "없음"))
                st.write(story.get("content", "실패"))

        else:
            st.error("서버 오류")
            st.write(response.text)

    except Exception as e:
        st.error("연결 실패")
        st.write(e)