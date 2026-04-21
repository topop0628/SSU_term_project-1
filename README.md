# 🍳 시크릿 에이전트 (Secret Agent): LLM 기반 편식 교정 솔루션

본 프로젝트는 에이전트 기술을 활용하여 아이가 기피하는 식재료를 조리법으로 숨기는 **'은폐 레시피 에이전트'**와 아이의 관심사를 반영한 **'맞춤형 동화 에이전트'**가 협업하는 멀티 에이전트 시스템입니다.

---

## 1. 시스템 아키텍처 (System Architecture)
본 프로젝트는 로컬의 개발 편의성과 클라우드의 강력한 GPU 성능을 결합한 **하이브리드 구조**로 설계되었습니다.

* **Frontend (Local)**: MacBook Air M2 / Streamlit UI
* **Backend (Cloud)**: Kaggle GPU T4 ×2 / FastAPI & uvicorn
* **Tunneling**: ngrok (로컬-클라우드 간의 보안 통로 구축)
* **Communication**: REST API (JSON) 기반 통신

---

## 2. 실험 모델 후보군 (Candidate Models)
성능과 효율성의 최적점을 찾기 위해 아래 모델들을 비교 분석합니다.

| 모델명 | 개발사 | 파라미터 | 특징 |
| :--- | :--- | :--- | :--- |
| **Llama-3-8B** | Meta | 8B | 우수한 오픈소스 모델, 창의적 스토리 생성에 강점 |
| **Gemma-2-9B** | Google | 9B | 논리적 추론 및 지시 이행 능력이 뛰어남 |
| **Phi-3-Mini** | Microsoft | 3.8B | 경량 모델 중 가장 효율적인 성능, 빠른 응답 속도 |
| **Gemma-2B-it** | Google | 2B | 초경량 모델, API 서버 구축 및 테스트용 (현재 사용 중) |

---

## 3. 평가 전략 (Evaluation Methodology)
단순 체감이 아닌 **'LLM-as-a-Judge'** 방식을 통해 정량 평가를 실시합니다.

### 🧪 실험 설계
1.  **모델 리스트**: [Llama-3-8B, Gemma-2-9B, Phi-3-Mini]
2.  **프롬프트 버전**:
    * **V1 (Zero-shot)**: 단순 명령 기반 생성
    * **V2 (Few-shot)**: 전문가 페르소나 및 예시 부여
    * **V3 (Chain-of-Thought)**: 단계별 추론 유도
3.  **평가 지표**: 은폐성(Recipe), 몰입도(Story), 생성 속도(Latency)

### 🤖 자동화 테스트 프로세스
* 모든 모델/프롬프트 조합을 반복문(Loop)으로 실행하여 결과 수집
* 수집된 데이터는 상위 모델(GPT-4o 등)에 전달하여 1~5점 척도로 평가 및 시각화

---

## 4. 설치 및 실행 방법 (Usage Guide)

### Step 1: 클라우드 서버 설정 (Kaggle)
1.  Kaggle Notebook에서 GPU 가속기(T4 x2)를 활성화합니다.
2.  `huggingface_hub`를 통해 모델 사용 권한을 인증합니다.
3.  백엔드 코드를 실행하여 생성된 **ngrok 주소**(`https://xxxx.ngrok-free.dev`)를 확인합니다.

### Step 2: 로컬 환경 설정 (MacBook)
1.  가상환경 생성 및 활성화:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2.  필수 라이브러리 설치:
    ```bash
    pip install streamlit requests
    ```
3.  앱 실행:
    ```bash
    streamlit run app.py
    ```

### Step 3: 서비스 연결
* 실행된 Streamlit 브라우저 사이드바에서 복사한 **Kaggle API URL**을 입력하고 '솔루션 생성'을 시도합니다.

---

## 5. 프로젝트 구조 (File Structure)
* `app.py`: Streamlit 기반 프론트엔드 UI 및 API 클라이언트
* `requirements.txt`: 프로젝트 의존성 라이브러리 목록
* `.venv/`: 로컬 독립 가상환경