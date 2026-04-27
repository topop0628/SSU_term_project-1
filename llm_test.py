
from kaggle_secrets import UserSecretsClient
from huggingface_hub import login

user_secrets = UserSecretsClient()
secret_value_0 = user_secrets.get_secret("HF_TOKEN")
login(token=secret_value_0)  # ← secret_value_0 그대로 넣으면 됩니다
# ============================================================
# Korean LLM Structured Output Experiment
# 4 Models x 2 Prompt Libraries (RECIPE + STORY)
# Kaggle GPU 환경에서 실행 (T4 x2 or P100)
# ============================================================

# ── 0. 설치 (첫 실행 시 주석 해제) ───────────────────────────
# !pip install -q transformers accelerate bitsandbytes

# ── 1. 임포트 ────────────────────────────────────────────────
import json
import re
import os
import time
import gc
import shutil
from datetime import datetime
from pathlib import Path

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline,
)

# ── 2. 실험 설정 ─────────────────────────────────────────────

OUTPUT_DIR = Path("/kaggle/working/results")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODELS = [
    # 완료된 모델 (결과 저장됨):
    # "yanolja/EEVE-Korean-Instruct-10.8B-v1.0",
    # "MLP-KTLim/llama-3-Korean-Bllossom-8B",
    # 완료된 모델 (결과 저장됨):
    # "rtzr/ko-gemma-2-9b-it",
    "allganize/Llama-3-Alpha-Ko-8B-Instruct",
    "trillionlabs/Trillion-7B-preview",
]
MODELS = [
    # ── 완료 (결과 저장됨) ────────────────────────────────────────
    # "yanolja/EEVE-Korean-Instruct-10.8B-v1.0",        # ✅ 완료
    # "MLP-KTLim/llama-3-Korean-Bllossom-8B",           # ✅ 완료
    # "rtzr/ko-gemma-2-9b-it",                          # ✅ 완료
    # "Upstage/SOLAR-10.7B-Instruct-v1.0",              # ✅ 완료 
    # ── 실패 / 제외 ───────────────────────────────────────────────
    # "LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct",           # ❌ AttributeError (get_interface, transformers 버전 호환 불가)
    # "LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct",           # ❌ 동일 호환성 에러
    # "beomi/Llama-3-Open-Ko-8B",                       # ❌ 베이스 모델 (instruction following 없음)
    # "beomi/Llama-3-Open-Ko-8B-Instruct-preview",      # ❌ Korean instruction fine-tune 없음 → parse_error
    # "maywell/Llama-3-Ko-8B-Instruct",                 # ❌ JSON 포맷 미준수 → parse_error
 
    # ── 현재 실험 중 ──────────────────────────────────────────────
    "allganize/Llama-3-Alpha-Ko-8B-Instruct",           # 🔄 Llama3 기반, ORPO fine-tune, LogicKor 6.62  ✅ 완료
    "trillionlabs/Trillion-7B-preview",                 # 🔄 koIFEval 벤치마크, 한국어 instruction 특화 ✅ 완료
]

# ── 3. 템플릿 변수 ────────────────────────────────────────────

RECIPE_INPUTS = [
    {"ingredients": "당근, 계란, 치즈", "hated": "당근"},
]

# dish_name은 RECIPE 결과에서 동적으로 채워짐
STORY_INPUTS = [
    {"interest": "우주"},
]

# ── 4. 프롬프트 라이브러리 ────────────────────────────────────

# RECIPE_LIBRARY, STORY_LIBRARY 여기에 삽입
# (기존 라이브러리 코드를 그대로 붙여넣으세요)

# ── 5. 유틸리티 함수 ─────────────────────────────────────────

def fill_template(template: str, variables: dict) -> str:
    """프롬프트 템플릿에 변수를 채워 넣습니다."""
    result = template
    for key, val in variables.items():
        result = result.replace(f"{{{key}}}", str(val))
    return result


def extract_json(raw_text: str) -> dict:
    """
    모델 출력에서 JSON 블록을 추출합니다.
    1) ```json ... ``` 코드 블록 시도
    2) 첫 번째 { ... } 블록 시도
    3) 실패 시 raw_text 그대로 저장
    """
    code_block = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
    if code_block:
        try:
            return json.loads(code_block.group(1))
        except json.JSONDecodeError:
            pass

    brace_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if brace_match:
        try:
            return json.loads(brace_match.group())
        except json.JSONDecodeError:
            pass

    return {"parse_error": True, "raw": raw_text}


def extract_dish_name(parsed_output: dict) -> str | None:
    """RECIPE 결과의 parsed_output에서 dish_name을 추출합니다."""
    if "parse_error" in parsed_output or "error" in parsed_output:
        return None
    return parsed_output.get("dish_name", None)


def build_chat_messages(prompt_text: str) -> list[dict]:
    """Chat 형식 메시지를 구성합니다 (system + user)."""
    return [
        {
            "role": "system",
            "content": (
                "You must respond exclusively in Korean (한국어). "
                "Do NOT use English under any circumstances. "
                "영어 사용은 절대 금지입니다. 모든 응답은 반드시 한국어(한글)로만 작성하세요. "
                "출력은 오직 아래 JSON 스키마 형식만 허용됩니다: "
                "{\"strategy\": \"한글로 작성\", \"content\": \"한글로 작성\"}. "
                "JSON 외 다른 텍스트, 설명, 코드 블록(```)은 절대 포함하지 마세요. "
                "If you write even one word in English, your response is invalid."
            ),
        },
        {"role": "user", "content": prompt_text},
    ]


# ── 6. 모델 로딩 ─────────────────────────────────────────────

def load_model(model_id: str):
    """
    모델을 로드합니다. 전 모델 float16, 양자화 없음.
    pipeline은 generation_config 간섭을 막기 위해 여기서 생성합니다.
    """
    print(f"\n{'='*60}")
    print(f"  로딩 중: {model_id}")
    print(f"{'='*60}")

    os.environ["PYTORCH_ALLOC_CONF"] = "expandable_segments:True"

    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        trust_remote_code=True,
        padding_side="left",
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        device_map="auto",
        max_memory={0: "13GiB", 1: "13GiB"},
        trust_remote_code=True,
        low_cpu_mem_usage=True,
    )

    model.eval()

    if hasattr(model, "hf_device_map"):
        from collections import Counter
        gpu_usage = Counter(str(v) for v in model.hf_device_map.values())
        print(f"  ✓ 레이어 분배: {dict(gpu_usage)}")

    # pipeline 생성 — 모델 내장 generation_config를 빈 것으로 교체해서 간섭 차단
    # generation_config=None을 pipeline()에 직접 넘기면 내부 충돌 발생 → 이 방식으로 우회
    from transformers import GenerationConfig
    # GenerationConfig() 기본값 max_length=20이 max_new_tokens=512와 충돌 경고 유발
    # → max_length 필드를 명시적으로 제거해서 경고 차단
    # GenerationConfig에 max_new_tokens 직접 지정 → max_length 충돌 경고 원천 차단
    _gc = GenerationConfig()
    _gc.max_new_tokens = 512   # pipe() 호출 시 max_new_tokens 안 넘겨도 됨
    model.generation_config = _gc

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
    )

    return tokenizer, model, pipe


def unload_model(tokenizer, model, pipe, model_id):
    """GPU 메모리 + 다운로드 캐시 완전 삭제."""
    del pipe
    model.cpu()
    del model
    del tokenizer
    gc.collect()
    torch.cuda.synchronize()
    torch.cuda.empty_cache()

    cache_dir = f"/root/.cache/huggingface/hub/models--{model_id.replace('/', '--')}"
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
        print(f"  ✓ 캐시 삭제: {cache_dir}")
    else:
        print(f"  ℹ️ 캐시 없음: {cache_dir}")

    free = torch.cuda.mem_get_info()[0] / 1024**3
    print(f"  ✓ GPU 여유 메모리: {free:.2f} GB")


# ── 7. 추론 함수 ─────────────────────────────────────────────

def run_inference(
    tokenizer,
    model,
    pipe,
    prompt_text: str,
    max_new_tokens: int = 512,
) -> str:
    """
    pipeline + tokenize=False 방식으로 추론합니다.
    generation_config=None으로 이미 pipeline 생성 시 간섭 차단됨.
    약 2배 빠른 tok/s 달성 (12 tok/s vs 6.5 tok/s).
    """
    messages = build_chat_messages(prompt_text)

    # apply_chat_template으로 문자열 프롬프트 생성
    try:
        prompt_str = tokenizer.apply_chat_template(
            messages,
            tokenize=False,             # ← 문자열로만 반환
            add_generation_prompt=True,
        )
    except Exception:
        prompt_str = "\n".join(m["content"] for m in messages)

    # pipeline 추론 — max_new_tokens는 GenerationConfig에 설정되어 있으므로 여기서 제외
    outputs = pipe(
        prompt_str,
        do_sample=False,
        temperature=1.0,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
        return_full_text=False,
    )

    return outputs[0]["generated_text"].strip()


# ── 8. 실험 실행 루프 ─────────────────────────────────────────

def run_recipe_experiment(
    tokenizer,
    model,
    pipe,
    model_id: str,
    inputs_list: list[dict],
) -> tuple[list[dict], dict[str, dict[int, str | None]]]:
    """
    RECIPE 라이브러리 전체를 실행하고:
    - results: 결과 리스트
    - dish_name_map: {exp_key: {input_idx: dish_name}} 매핑 반환
    """
    results = []
    dish_name_map: dict[str, dict[int, str | None]] = {}

    for exp_key, template in RECIPE_LIBRARY.items():
        dish_name_map[exp_key] = {}
        for idx, inp in enumerate(inputs_list):
            prompt = fill_template(template, inp)
            print(f"  [RECIPE] {exp_key} | input_{idx+1} 추론 중...", end=" ")

            t0 = time.time()
            try:
                raw_output = run_inference(tokenizer, model, pipe, prompt)
                parsed = extract_json(raw_output)
                status = "success" if "parse_error" not in parsed else "parse_error"
                dish_name = extract_dish_name(parsed)
            except Exception as e:
                import traceback
                raw_output = ""
                tb = traceback.format_exc()
                parsed = {"error": str(e), "traceback": tb}
                status = "error"
                dish_name = None
                print(f"\n  ⚠️ 에러:\n{tb}")

            elapsed = round(time.time() - t0, 2)
            print(f"→ {status} ({elapsed}s) | dish_name: {dish_name}")

            dish_name_map[exp_key][idx + 1] = dish_name

            results.append({
                "model": model_id.split("/")[-1],
                "library": "RECIPE",
                "exp_key": exp_key,
                "input_idx": idx + 1,
                "input": inp,
                "status": status,
                "elapsed_sec": elapsed,
                "raw_output": raw_output,
                "parsed_output": parsed,
            })

    return results, dish_name_map


def run_story_experiment(
    tokenizer,
    model,
    pipe,
    model_id: str,
    story_inputs_list: list[dict],
    dish_name_map: dict[str, dict[int, str | None]],
) -> list[dict]:
    """
    STORY 라이브러리를 실행합니다.
    dish_name은 같은 EXP의 RECIPE 결과에서 동적으로 주입됩니다.
    dish_name 추출 실패 시 해당 케이스는 스킵합니다.
    """
    results = []

    for exp_key, template in STORY_LIBRARY.items():
        for idx, story_inp in enumerate(story_inputs_list):
            dish_name = dish_name_map.get(exp_key, {}).get(idx + 1, None)

            if dish_name is None:
                print(f"  [STORY] {exp_key} | input_{idx+1} → ⚠️ dish_name 없음, 스킵")
                results.append({
                    "model": model_id.split("/")[-1],
                    "library": "STORY",
                    "exp_key": exp_key,
                    "input_idx": idx + 1,
                    "input": {**story_inp, "dish_name": None},
                    "status": "skipped",
                    "elapsed_sec": 0,
                    "raw_output": "",
                    "parsed_output": {"skip_reason": "RECIPE dish_name 추출 실패"},
                })
                continue

            combined_inp = {**story_inp, "dish_name": dish_name}
            prompt = fill_template(template, combined_inp)
            print(f"  [STORY] {exp_key} | input_{idx+1} 추론 중... (dish_name: {dish_name})", end=" ")

            t0 = time.time()
            try:
                raw_output = run_inference(tokenizer, model, pipe, prompt)
                parsed = extract_json(raw_output)
                status = "success" if "parse_error" not in parsed else "parse_error"
            except Exception as e:
                import traceback
                raw_output = ""
                tb = traceback.format_exc()
                parsed = {"error": str(e), "traceback": tb}
                status = "error"
                print(f"\n  ⚠️ 에러:\n{tb}")

            elapsed = round(time.time() - t0, 2)
            print(f"→ {status} ({elapsed}s)")

            results.append({
                "model": model_id.split("/")[-1],
                "library": "STORY",
                "exp_key": exp_key,
                "input_idx": idx + 1,
                "input": combined_inp,
                "status": status,
                "elapsed_sec": elapsed,
                "raw_output": raw_output,
                "parsed_output": parsed,
            })

    return results


# ── 9. 메인 실행 ─────────────────────────────────────────────

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    all_results: dict[str, list] = {}

    for model_id in MODELS:
        model_short = model_id.split("/")[-1]
        print(f"\n{'#'*60}")
        print(f"  모델 실험 시작: {model_short}")
        print(f"{'#'*60}")

        tokenizer, model, pipe = load_model(model_id)
        model_results = []

        # ── RECIPE 실험 → dish_name_map 생성 ──────────────────
        recipe_results, dish_name_map = run_recipe_experiment(
            tokenizer, model, pipe, model_id,
            inputs_list=RECIPE_INPUTS,
        )
        model_results += recipe_results

        print(f"\n  [dish_name_map 요약]")
        for exp_key, idx_map in dish_name_map.items():
            for idx, dn in idx_map.items():
                print(f"    {exp_key} | input_{idx} → {dn}")

        # ── STORY 실험 (dish_name 동적 주입) ──────────────────
        story_results = run_story_experiment(
            tokenizer, model, pipe, model_id,
            story_inputs_list=STORY_INPUTS,
            dish_name_map=dish_name_map,
        )
        model_results += story_results

        all_results[model_short] = model_results

        # ── 모델별 중간 저장 ───────────────────────────────────
        per_model_path = OUTPUT_DIR / f"{model_short}_{timestamp}.json"
        with open(per_model_path, "w", encoding="utf-8") as f:
            json.dump(model_results, f, ensure_ascii=False, indent=2)
        print(f"\n  ✓ 저장 완료: {per_model_path}")

        unload_model(tokenizer, model, pipe, model_id)

    # ── 전체 결과 통합 저장 ───────────────────────────────────
    summary_path = OUTPUT_DIR / f"all_results_{timestamp}.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\n\n{'='*60}")
    print(f"  ✅ 모든 실험 완료!")
    print(f"  통합 결과: {summary_path}")
    print(f"{'='*60}")

    # ── 성공률 요약 ───────────────────────────────────────────
    print("\n[성공률 요약]")
    for model_short, results in all_results.items():
        for lib in ["RECIPE", "STORY"]:
            lib_results = [r for r in results if r["library"] == lib]
            total = len(lib_results)
            if total == 0:
                continue
            success = sum(1 for r in lib_results if r["status"] == "success")
            skipped = sum(1 for r in lib_results if r["status"] == "skipped")
            print(f"  {model_short:40s} [{lib}] : {success}/{total} 성공, {skipped} 스킵 ({100*success//total}%)")


if __name__ == "__main__":
    main()