# 📖 SSU_term_project-1: LLM 기반 편식 교정 앱

## 1. 환경별 작업 명세 (Workflow)

### 💻 Local (MacBook Air M2)
**목표: 사용자 인터페이스(UI) 구현 및 시스템 통합**
- **생성할 파일**:
  - `app.py`: Streamlit을 이용한 메인 앱 화면 코드.
  - `requirements.txt`: 필요한 라이브러리 목록 (streamlit, requests 등).
- **실행 방법**:
  ```bash
  pip install -r requirements.txt
  streamlit run app.py
  ```

### ☁️ Cloud (Kaggle / Colab GPU)
**목표: 고성능 LLM 구동 및 성능 비교 분석**
- **수행할 작업**:
  - **모델 로드**: Llama 3 8B 모델을 4-bit 양자화로 로드.
  - **프롬프트 실험**: '은폐 레시피'와 '동화'를 위한 최적의 프롬프트 구성 및 비교.
  - **LLM-as-a-Judge**: 상위 모델(GPT-4o 등)을 활용해 생성 결과물에 대한 정량적 점수 산출.
  - **API 서버 구축**: `FastAPI`와 `ngrok`을 사용하여 로컬 앱과 통신할 터널링 서버 가동.

---

## 2. 프로젝트 로드맵 (To-Do List)

- [ ] **Step 1 (Local)**: `app.py` 기본 레이아웃 제작 (재료 입력창, 결과 출력 탭).
- [ ] **Step 2 (Cloud)**: Kaggle에서 Llama 3 모델로 프롬프트별 출력 데이터 수집.
- [ ] **Step 3 (Judge)**: 수집된 데이터를 평가 모델에 넣어 '왜 이 프롬프트가 최적인지' 데이터 확보.
- [ ] **Step 4 (Integration)**: Cloud 서버 주소를 Local 앱에 연결하여 실시간 작동 테스트.
- [ ] **Step 5 (Final)**: 작동 영상 녹화 및 GitHub 최종 업데이트.

---

## 3. 에이전트 설계 개요 (Agent Architecture)
본 앱은 사용자 입력을 기반으로 두 개의 전문 에이전트가 작동합니다.
1. **Recipe Agent**: 영양소는 유지하되 식감을 숨기는 조리법 생성. [cite: 88]
2. **Story Agent**: 아이의 관심사를 반영한 식사 동기 부여 스토리 생성. [cite: 89]
