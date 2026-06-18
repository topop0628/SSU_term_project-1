# ============================================================
# rag_experiment.py
# Baseline vs +RAG 비교 실험 (Kaggle GPU)
#
# 기존 6모델 비교에서 우승한 EEVE-10.8B + 최고 프롬프트 EXP_2 하나만 고정하고,
# "RAG 적용 여부"만 변수로 두는 controlled ablation.
#   - Baseline : 기존 방식 (검색 근거 없음)
#   - +RAG     : 하이브리드검색→(선택)리랭킹(①) → CRAG-착안 필터(②) → 근거 주입
#                → 생성 → LLM-as-a-Judge 근거 심사(③)
#
# 적용 논문 (전부 추론 단계·단일 모델·저비용, 모델 재학습 없음):
#   ① Wang et al. (2024), arXiv:2407.01219  — 하이브리드 검색 + (선택)리랭킹
#   ② Yan, Gu, Zhu, Ling (2024), arXiv:2401.15884 — CRAG 검색 품질 게이트
#        ※ 원본 학습된 T5 evaluator → EEVE 프롬프트 1회 호출로 단순화
#   ③ Sardana (2025), arXiv:2503.21157 — Real-Time Evaluation Models for RAG
#        ※ reference-free LLM-as-a-Judge로 근거 부합/환각 심사(외부 심사, 호출 1회)
#
# 설치: pip install -q transformers accelerate sentence-transformers rank_bm25
# ============================================================

import argparse
import json
import os
import re
import shutil
import time
from datetime import datetime
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, GenerationConfig

from recipe_prompts import RECIPE_LIBRARY
from story_prompts import STORY_LIBRARY
import rag_retrieval as rag

# ── 실험 설정 ────────────────────────────────────────────────
# 6모델 전체 (Colab에서는 모델당 1개 서브프로세스로 실행 → VRAM 완전 회수)
MODELS = [
    "yanolja/EEVE-Korean-Instruct-10.8B-v1.0",   # 1등
    "rtzr/ko-gemma-2-9b-it",                      # 2등
    "MLP-KTLim/llama-3-Korean-Bllossom-8B",
    "trillionlabs/Trillion-7B-preview",
    "allganize/Llama-3-Alpha-Ko-8B-Instruct",
    "Upstage/SOLAR-10.7B-Instruct-v1.0",
]
MODEL_ID = MODELS[0]                                     # --model 미지정 시 기본
EXP_KEY = "EXP_2"                                        # 최고 점수 프롬프트로 고정
# 다양한 입력 케이스 (일반화 + 평균±표준편차 측정용)
CASES = [
    {"ingredients": "당근, 계란, 치즈",   "hated": "당근",    "interest": "우주"},
    {"ingredients": "시금치, 두부, 계란", "hated": "시금치",  "interest": "공룡"},
    {"ingredients": "브로콜리, 감자, 치즈", "hated": "브로콜리", "interest": "공주"},
    {"ingredients": "가지, 계란, 양파",   "hated": "가지",    "interest": "바다"},
]
# Kaggle/Colab/로컬 어디서나 동작: 기본은 현재 폴더의 rag_results,
# 필요 시 환경변수 RAG_OUT_DIR로 덮어쓰기 가능.
OUTPUT_DIR = Path(os.environ.get("RAG_OUT_DIR", "rag_results"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ── 유틸 ─────────────────────────────────────────────────────
def fill_template(template: str, variables: dict) -> str:
    out = template
    for k, v in variables.items():
        out = out.replace(f"{{{k}}}", str(v))
    return out


def extract_json(raw: str) -> dict:
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            pass
    # 폴백: 출력이 잘려 JSON이 안 닫혀도 완성된 필드는 정규식으로 복구
    # (dish_name·strategy는 보통 앞쪽이라 살아있음 → 동화 생성 스킵 방지)
    out = {}
    for key in ("dish_name", "strategy", "content"):
        km = re.search(rf'"{key}"\s*:\s*"(.*?)"\s*[,}}]', raw, re.DOTALL)
        if km:
            out[key] = km.group(1).replace("\\n", "\n")
    if out:
        out["_recovered"] = True   # 부분 복구 표시
        return out
    return {"parse_error": True, "raw": raw}


def build_chat_messages(prompt_text: str) -> list:
    return [
        {"role": "system", "content":
            "모든 응답은 반드시 한국어(한글)로만 작성하세요. 영어 사용 금지. "
            "출력은 오직 JSON 스키마 {\"dish_name\":\"\",\"strategy\":\"\",\"content\":\"\"} 형식만 허용됩니다. "
            "JSON 외 다른 텍스트나 코드블록은 절대 포함하지 마세요."},
        {"role": "user", "content": prompt_text},
    ]


# ── 모델 로딩 / 추론 ─────────────────────────────────────────
def load_model(model_id: str):
    tok = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True, padding_side="left")
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    # GPU 개수에 맞춰 자동 적응. 단일 GPU(A100/H100 등)면 max_memory 제한 없이,
    # 멀티 GPU(예: Kaggle T4x2)면 카드별 상한을 둔다.
    n_gpu = torch.cuda.device_count()
    load_kwargs = dict(
        dtype=torch.float16, device_map="auto",
        trust_remote_code=True, low_cpu_mem_usage=True)
    if n_gpu > 1:
        load_kwargs["max_memory"] = {i: "13GiB" for i in range(n_gpu)}
    print(f"  GPU {n_gpu}개 감지 → device_map=auto"
          + (f", max_memory={load_kwargs['max_memory']}" if n_gpu > 1 else ""))

    model = AutoModelForCausalLM.from_pretrained(model_id, **load_kwargs)
    model.eval()
    gc = GenerationConfig()
    gc.max_new_tokens = 512
    model.generation_config = gc
    pipe = pipeline("text-generation", model=model, tokenizer=tok)
    return tok, pipe


def make_generate_fn(tok, pipe):
    """rag 모듈(CRAG 평가·근거검증)이 재사용할 단일 추론 함수."""
    def _gen(prompt_text: str, max_new_tokens: int = 768) -> str:
        # 생성(레시피/동화)은 768로 충분히 길게 → JSON이 잘리지 않게.
        # CRAG/Judge는 호출부에서 max_new_tokens=8로 짧게(숫자만) 받음.
        msgs = build_chat_messages(prompt_text)
        try:
            s = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        except Exception:
            s = "\n".join(m["content"] for m in msgs)
        out = pipe(s, do_sample=False, max_new_tokens=max_new_tokens,
                   pad_token_id=tok.pad_token_id,
                   eos_token_id=tok.eos_token_id, return_full_text=False)
        return out[0]["generated_text"].strip()
    return _gen


# ── 1회 실행(레시피→스토리) : RAG on/off 공통 ────────────────
def run_once(generate_fn, retriever, use_rag: bool, case: dict,
             case_idx: int = 0, model_short: str = "") -> dict:
    ingredients, hated, interest = case["ingredients"], case["hated"], case["interest"]
    rec_template = fill_template(RECIPE_LIBRARY[EXP_KEY], {"ingredients": ingredients, "hated": hated})

    rag_meta = {"use_rag": use_rag}
    if use_rag:
        # ① 하이브리드 검색 + 리랭킹
        docs = retriever.retrieve(ingredients, hated, top_n=3, use_rerank=True)
        # ② CRAG 품질 필터
        crag = rag.crag_filter(docs, ingredients, hated, generate_fn)
        rec_template += rag.build_reference_block(crag["kept"], hated=hated)
        rag_meta.update({
            "retrieved": [d["dish_name"] for d in docs],
            "kept": [d["dish_name"] for d in crag["kept"]],
            "crag_label": crag["label"],
        })

    # 레시피 생성
    t0 = time.time()
    recipe_raw = generate_fn(rec_template)
    recipe = extract_json(recipe_raw)
    rec_elapsed = round(time.time() - t0, 2)

    # ③ Sardana(2025) LLM-as-a-Judge: 근거 부합 외부 심사(평가 보조 지표)
    if use_rag and rag_meta.get("kept"):
        kept_docs = [d for d in docs if d["dish_name"] in rag_meta["kept"]]
        rag_meta["grounding_score"] = rag.grounding_score(recipe_raw, kept_docs, generate_fn)

    # 스토리 생성 (dish_name 동적 주입)
    dish = recipe.get("dish_name") if isinstance(recipe, dict) else None
    story = {"skipped": True}
    story_raw = ""
    if dish:
        story_template = fill_template(STORY_LIBRARY[EXP_KEY], {"interest": interest, "dish_name": dish})
        story_raw = generate_fn(story_template)
        story = extract_json(story_raw)

    return {
        "model": model_short,
        "case_idx": case_idx + 1,
        "case": {"ingredients": ingredients, "hated": hated, "interest": interest},
        "condition": "RAG" if use_rag else "Baseline",
        "exp_key": EXP_KEY,
        "rag_meta": rag_meta,
        "recipe_elapsed_sec": rec_elapsed,
        "recipe_raw": recipe_raw,
        "recipe": recipe,
        "story_raw": story_raw,
        "story": story,
    }


def purge_cache(model_id: str):
    """HF 다운로드 캐시 삭제(디스크 확보). 서브프로세스 종료로 VRAM은 OS가 회수."""
    cache_dir = os.path.expanduser(
        f"~/.cache/huggingface/hub/models--{model_id.replace('/', '--')}")
    if os.path.isdir(cache_dir):
        shutil.rmtree(cache_dir, ignore_errors=True)
        print(f"  🧹 캐시 삭제: {cache_dir}")


def run_model(model_id: str, retriever) -> list:
    """모델 1개에 대해 Baseline + RAG 실행 후 모델별 JSON 저장."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    short = model_id.split("/")[-1]
    print(f"\n{'#'*60}\n  모델: {short}\n{'#'*60}")
    tok, pipe = load_model(model_id)
    generate_fn = make_generate_fn(tok, pipe)

    results = []
    for ci, case in enumerate(CASES):
        for use_rag in [False, True]:
            print(f"\n=== {short} | case{ci+1}({case['hated']}) | "
                  f"{'RAG' if use_rag else 'Baseline'} ===")
            results.append(run_once(generate_fn, retriever, use_rag, case,
                                    case_idx=ci, model_short=short))

    out_path = OUTPUT_DIR / f"rag_ablation_{short}_{ts}.json"
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ 저장: {out_path}")
    for r in results:
        gs = r["rag_meta"].get("grounding_score", "-")
        d = r["recipe"].get("dish_name", "?") if isinstance(r["recipe"], dict) else "?"
        print(f"  case{r['case_idx']}({r['case']['hated']}) [{r['condition']}] "
              f"dish={d} | 근거={gs}")
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=None,
                    help="단일 모델 ID. 지정 시 그 모델만 실행(Colab 서브프로세스용).")
    ap.add_argument("--keep-cache", action="store_true",
                    help="실행 후 HF 캐시를 지우지 않음(재실행 시 재다운로드 방지).")
    args = ap.parse_args()

    print("📚 레시피 검색 인덱스 구축...")
    retriever = rag.RecipeRetriever(db_path="recipe_db.json")

    targets = [args.model] if args.model else MODELS
    for mid in targets:
        run_model(mid, retriever)
        if not args.keep_cache:
            purge_cache(mid)


if __name__ == "__main__":
    main()
