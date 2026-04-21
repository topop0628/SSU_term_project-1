# 📖 SSU_term_project-1: LLM 기반 편식 교정 앱

## 1. 실험 모델 후보군 (Candidate Models)
본 프로젝트는 성능과 효율성의 최적점을 찾기 위해 아래 모델들을 비교 분석합니다.

| 모델명 | 개발사 | 파라미터 | 특징 |
| :--- | :--- | :--- | :--- |
| **Llama-3-8B** | Meta | 8B | 현재 가장 우수한 오픈소스 모델, 창의적 스토리 생성에 강점 |
| **Gemma-2-9B** | Google | 9B | 논리적 추론 및 지시 이행 능력이 뛰어남 |
| **Phi-3-Mini** | Microsoft | 3.8B | 경량 모델 중 가장 효율적인 성능, 빠른 응답 속도 |
| **Gemma-2B** | Google | 2B | 초경량 모델, 실시간 모바일 환경 적용 가능성 테스트용 |

---

## 2. 평가 전략 (Evaluation Methodology)
단순 체감이 아닌 **'LLM-as-a-Judge'** 방식을 통해 정량 평가를 실시합니다.

### 🧪 실험 설계
1. **모델 리스트**: [Llama-3-8B, Gemma-2-9B, Phi-3-Mini]
2. **프롬프트 버전**:
   - V1: 단순 명령 (Zero-shot)
   - V2: 페르소나 부여 (Few-shot)
   - V3: 단계별 추론 유도 (Chain-of-Thought)
3. **평가 지표**: 은폐성(Recipe), 몰입도(Story), 생성 속도(Latency)

### 🤖 자동화 테스트 프로세스
- 모든 모델과 프롬프트 조합을 루프(Loop)로 돌려 결과를 수집합니다.
- 수집된 결과는 상위 모델(GPT-4o 등)에게 전달되어 1~5점 척도로 점수화됩니다.

---

## 3. 개발 및 실행 환경
- **Local**: MacBook Air M2 (Streamlit UI 개발)
- **Cloud**: Kaggle/Colab GPU (모델 비교 및 추론 서버)
