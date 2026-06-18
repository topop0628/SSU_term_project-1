# 시크릿 에이전트 — LLM 기반 편식 교정 멀티 에이전트

아이가 싫어하는 재료를 숨긴 레시피와, 아이의 관심사를 엮은 짧은 동화를 함께 만들어 주는
멀티 에이전트 시스템입니다.

- **레시피 에이전트 (Chef)**: 싫어하는 재료의 맛·향·식감을 숨긴 조리법 생성
- **동화 에이전트 (Writer)**: 완성된 요리를 아이의 관심사와 연결한 이야기 생성

## 시스템 구조

- Frontend: Streamlit (`app.py`)
- Backend: FastAPI + ngrok, Kaggle/Colab GPU (`llmserver.py`)
- 서비스 모델: EEVE-Korean-Instruct-10.8B

## 실험 개요

1. **모델·프롬프트 선정** — 한국어 LLM 6종 × 프롬프트 12종을 LLM-as-a-Judge로 비교.
   EEVE-10.8B(85.33)와 EXP_2(Zero-shot + CoT + 자가검토, 85.67)가 가장 우수.
2. **RAG 업그레이드** — 실제 한국어 레시피를 검색해 근거로 주입(학습 없이 추론 단계만).
   프롬프트를 EXP_2로 고정하고 RAG on/off만 바꿔 4개 입력 케이스에서 비교.
   → 6모델 중 5모델 개선(평균 +10.8), 제목 은폐율 54%→83%.

### RAG 파이프라인

```
재료 입력
  → 하이브리드 검색(BM25 + 임베딩) + 리랭킹
  → CRAG 품질 필터 (검색 레시피가 쓸 만한지 평가)
  → 근거 주입 (참고용, 제목에 싫어하는 재료 금지)
  → 레시피 생성
  → LLM-as-a-Judge 근거 검증
```

## 주요 파일

| 파일 | 설명 |
|------|------|
| `app.py`, `llmserver.py` | Streamlit 프론트 / FastAPI 백엔드 |
| `recipe_prompts.py`, `story_prompts.py` | 에이전트 프롬프트 라이브러리 |
| `llm_test.py` | baseline 6모델 × 12프롬프트 실험 (Kaggle) |
| `llm_evaluation_prompt` | 평가 루브릭 |
| `build_recipe_db.py`, `recipe_db.json` | 레시피 DB 구축 / 레시피 2,147개 |
| `rag_retrieval.py` | 검색·필터·검증 코어 |
| `rag_experiment.py` | baseline vs RAG 실험 |
| `rag_colab.ipynb` | Colab 실행 노트북 |
| `rag_results/score_analysis` | 채점 결과 정리 |

## 실행

로컬 프론트엔드:

```bash
pip install streamlit requests
streamlit run app.py
```

GPU 실험 (Colab/Kaggle):

```bash
pip install transformers accelerate sentence-transformers rank_bm25
python rag_experiment.py
```

## 라이선스

학습/연구용 프로젝트입니다.
