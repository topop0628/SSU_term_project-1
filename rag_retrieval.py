# ============================================================
# rag_retrieval.py
# 레시피 RAG 파이프라인 — 학습 불필요(training-free), 추론 단계만.
#
# 논문 3개를 단계별로 결합 (전부 추론 단계, 모델 재학습 없음):
#   ① Searching for Best Practices in RAG
#        Wang et al. (2024), arXiv:2407.01219
#        → 하이브리드 검색(BM25 + dense) → 리랭킹. 검색은 에이전트가 아닌 파이프라인.
#        ※ 리랭킹(cross-encoder)은 "선택" — 시간 없으면 BM25+dense 융합만으로도 동작.
#   ② Corrective RAG / CRAG
#        Yan, Gu, Zhu, Ling (2024), arXiv:2401.15884
#        → 검색 품질 평가기로 부적합 문서 필터(Correct / Incorrect / Ambiguous)
#        ※ 원본 evaluator는 "학습된 T5" 모델. 본 구현은 CRAG에서 착안하여
#          evaluator를 EEVE 프롬프트 1회 호출("재료에 맞나? 1~5점")로 "단순화".
#   ③ Real-Time Evaluation Models for RAG: Who Detects Hallucinations Best?
#        Sardana (2025), arXiv:2503.21157
#        → 정답 라벨 없이(reference-free) RAG 응답의 환각을 잡는 평가법 비교
#          (LLM-as-a-Judge, Lynx, HHEM 등). 본 구현은 LLM-as-a-Judge를 채택:
#          EEVE에 "생성 레시피의 각 단계가 검색 근거에 부합하나?"를 1회 질의.
#        ※ 생성 후 '외부 심사'라 기존 Self-verification(자가검토) 루프와 역할이 분리됨.
#
# 의존성(Kaggle에서 설치): pip install -q sentence-transformers rank_bm25
# ============================================================

import json
import re
from pathlib import Path


def _tokenize(text: str) -> list:
    """BM25용 간단 토크나이저 — 한글/영문/숫자 단위로 분리."""
    return re.findall(r"[가-힣]+|[a-zA-Z]+|\d+", text.lower())


class RecipeRetriever:
    """레시피 DB에 대한 하이브리드 검색 + 리랭킹 (논문 ①)."""

    def __init__(
        self,
        db_path: str = "recipe_db.json",
        embed_model: str = "jhgan/ko-sroberta-multitask",
        reranker_model: str = "BAAI/bge-reranker-v2-m3",
    ):
        self.docs = json.loads(Path(db_path).read_text(encoding="utf-8"))
        # 검색 대상 텍스트(요리명 + 재료 + 조리법)를 doc마다 1개로 구성
        self.corpus = [self._doc_to_text(d) for d in self.docs]

        # ── 1) BM25 (sparse) ─────────────────────────────────
        from rank_bm25 import BM25Okapi
        self.bm25 = BM25Okapi([_tokenize(c) for c in self.corpus])

        # ── 2) Dense 임베딩 (한국어 sentence-transformer) ─────
        from sentence_transformers import SentenceTransformer
        self.embedder = SentenceTransformer(embed_model)
        self.doc_emb = self.embedder.encode(
            self.corpus, convert_to_tensor=True, normalize_embeddings=True
        )

        # ── 3) Cross-encoder 리랭커 (선택) — 실제 사용 시 지연 로딩 ──
        self._reranker_model = reranker_model
        self.reranker = None

    @staticmethod
    def _doc_to_text(d: dict) -> str:
        return f"{d['dish_name']} | 재료: {', '.join(d['ingredients'])} | 조리법: {' '.join(d['steps'])}"

    def hybrid_search(self, query: str, top_k: int = 8) -> list:
        """BM25 순위 + dense 순위를 RRF(Reciprocal Rank Fusion)로 결합."""
        from sentence_transformers import util

        # BM25 점수 → 순위
        bm25_scores = self.bm25.get_scores(_tokenize(query))
        bm25_rank = {i: r for r, i in enumerate(
            sorted(range(len(self.corpus)), key=lambda i: -bm25_scores[i]))}

        # dense 코사인 → 순위
        q_emb = self.embedder.encode(query, convert_to_tensor=True, normalize_embeddings=True)
        cos = util.cos_sim(q_emb, self.doc_emb)[0].cpu().tolist()
        dense_rank = {i: r for r, i in enumerate(
            sorted(range(len(self.corpus)), key=lambda i: -cos[i]))}

        # RRF 융합 (k=60은 관례적 상수)
        k = 60
        rrf = {i: 1 / (k + bm25_rank[i]) + 1 / (k + dense_rank[i])
               for i in range(len(self.corpus))}
        ranked = sorted(rrf, key=lambda i: -rrf[i])[:top_k]
        return ranked  # doc 인덱스 리스트

    def rerank(self, query: str, cand_idx: list, top_n: int = 3) -> list:
        """cross-encoder로 (query, doc) 쌍을 재채점해 상위 top_n 선별 (논문 ①, 선택)."""
        if self.reranker is None:
            from sentence_transformers import CrossEncoder
            self.reranker = CrossEncoder(self._reranker_model)
        pairs = [[query, self.corpus[i]] for i in cand_idx]
        scores = self.reranker.predict(pairs)
        order = sorted(range(len(cand_idx)), key=lambda j: -scores[j])
        return [cand_idx[j] for j in order[:top_n]]

    def retrieve(self, ingredients: str, hated: str, top_n: int = 3,
                 use_rerank: bool = True) -> list:
        """재료 기반 쿼리 → 하이브리드 검색 → (선택)리랭킹 → 상위 레시피 dict 반환."""
        query = f"{ingredients} 재료로 {hated}를 숨기는 유아식 레시피"
        cand = self.hybrid_search(query, top_k=8)
        if use_rerank:
            top = self.rerank(query, cand, top_n=top_n)
        else:
            top = cand[:top_n]   # 리랭킹 생략(선택) — BM25+dense 융합 순위만 사용
        return [self.docs[i] for i in top]


# ── 논문 ② CRAG(arXiv:2401.15884) 착안: 프롬프트 기반 검색 품질 평가기 ──
#    (원본 CRAG의 학습된 T5 evaluator를 LLM 프롬프트 평가로 단순화)
_CRAG_PROMPT = """다음 후보 레시피가 '참고 베이스'로 쓸 만한지 평가하세요.
사용자 재료: {ingredients}
숨겨야 할 재료: {hated}
후보 레시피: {doc}

※ 후보가 이미 {hated}를 숨기고 있을 필요는 없습니다. 재료가 일부 겹치거나
조리 방식을 응용해 {hated}를 숨기는 유아식의 '기반/출발점'으로 쓸 만하면 높은 점수입니다.
1~5점으로만 답하세요. 숫자 하나만 출력: """


def crag_filter(retriever_docs: list, ingredients: str, hated: str,
                generate_fn, threshold: int = 3) -> dict:
    """
    검색된 docs를 LLM으로 1~5점 평가해 부적합 문서를 거른다 (논문 ②).
    generate_fn(prompt:str)->str : 기존 추론 함수를 그대로 주입.
    반환: {"kept": [...], "label": "Correct|Ambiguous|Incorrect"}
    """
    kept = []
    for d in retriever_docs:
        prompt = _CRAG_PROMPT.format(
            ingredients=ingredients, hated=hated,
            doc=RecipeRetriever._doc_to_text(d))
        raw = generate_fn(prompt, max_new_tokens=8)   # 숫자(1~5)만 필요
        m = re.search(r"[1-5]", raw)
        score = int(m.group()) if m else 0
        if score >= threshold:
            kept.append(d)

    if len(kept) == len(retriever_docs) and kept:
        label = "Correct"        # 전부 관련 있음 → 그대로 사용
    elif kept:
        label = "Ambiguous"      # 일부만 통과 → 통과분만 사용
    else:
        label = "Incorrect"      # 전부 부적합 → 근거 없이 생성(폴백)
    return {"kept": kept, "label": label}


# ── 논문 ③ Sardana(2025, arXiv:2503.21157): reference-free LLM-as-a-Judge ──
#    (정답 라벨 없이 생성 응답이 검색 근거에 부합하는지 '외부 심사'로 환각 탐지.
#     생성 후 별도 judge라 기존 self-refine 자가검토 루프와 메커니즘이 겹치지 않음)
_GROUNDING_PROMPT = """[근거 심사 — LLM-as-a-Judge] 우리 과제는 싫어하는 재료를 '숨기는' 레시피이므로, 생성 레시피가 참고 레시피와 똑같을 필요는 없습니다.
참고 레시피의 실제 조리 방식에 '기반'하여 현실적으로 만들 수 있으면 높은 점수를 주세요.
- 숨기기 위한 변형·추가 단계(다지기, 볶아 향 날리기, 갈기, 덮기 등)는 감점하지 마세요.
- 참고에 근거가 전혀 없거나 비현실적인 단계(환각)만 감점하세요.
[참고 레시피]
{refs}

[생성된 레시피]
{generated}

생성 레시피가 참고에 '기반'해 현실적으로 실행 가능한 정도를 0~25점으로만 답하세요. 숫자 하나만 출력: """


def grounding_score(generated_text: str, kept_docs: list, generate_fn) -> int:
    """생성 레시피가 검색 근거에 부합하는지 외부 LLM-as-a-Judge로 채점 (Sardana 2025, reference-free)."""
    if not kept_docs:
        return 0
    refs = "\n".join(f"- {RecipeRetriever._doc_to_text(d)}" for d in kept_docs)
    raw = generate_fn(_GROUNDING_PROMPT.format(refs=refs, generated=generated_text),
                      max_new_tokens=8)   # 숫자(0~25)만 필요
    m = re.search(r"\d+", raw)
    return min(25, int(m.group())) if m else 0


# ── 프롬프트 증강: 검색 근거를 프롬프트에 주입 ──────────────
def build_reference_block(kept_docs: list, hated: str = "") -> str:
    """통과한 레시피를 '참고 전용' 근거 블록으로 직렬화.

    주의: 검색된 레시피 '이름'에는 보통 {hated}가 들어있어(예: '당근 시금치 계란말이'),
    모델이 그대로 따라 쓰면 요리명에서 은폐가 깨진다. → 제목 금지 지시를 함께 주입.
    이 블록은 RAG 조건에서만 붙으므로 Baseline 프롬프트(원본)는 그대로 보존됨.
    """
    if not kept_docs:
        return ""
    lines = ["\n\n[참고 레시피 — 근거로만 활용, 그대로 베끼지 말 것]"]
    for d in kept_docs:
        lines.append(f"- {d['dish_name']}: {' '.join(d['steps'])}")
    if hated:
        lines.append(
            f"\n[중요] 참고 레시피 이름에 '{hated}'가 들어있어도, 너의 요리명(dish_name)에는 "
            f"'{hated}'라는 단어를 절대 포함하지 마라. 정체를 숨긴 보편적인 요리명을 새로 지어라.")
    return "\n".join(lines)
