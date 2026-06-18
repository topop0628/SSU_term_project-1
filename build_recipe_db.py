# ============================================================
# build_recipe_db.py
# KoreanRecipeGPT(skku-taehwan) 원본 데이터를 우리 RAG 스키마로 변환.
#
# 원본 형식(한 줄 = 한 레시피):
#   <unused0>요리명<unused1><unused2>재료1$재료2$...<unused3><unused4>조리법 문장들.<unused5>
# 출력: recipe_db.json  ({dish_name, ingredients[], steps[], tags[]} 리스트)
#
# 데이터 출처: https://github.com/skku-taehwan/KoreanRecipeGPT
#   (만개의레시피·해먹남녀·공공데이터포털·메뉴판 크롤링)
#
# 사용:
#   python build_recipe_db.py              # val 파일 다운로드해 3000개 변환
#   python build_recipe_db.py --all 50000  # train 파일에서 최대 50000개
# ============================================================

import argparse
import json
import re
import urllib.request
from pathlib import Path

RAW_BASE = "https://raw.githubusercontent.com/skku-taehwan/KoreanRecipeGPT/main/data/recipegpt"
SRC_VAL = "recipegpt_val.txt"      # 약 2.5MB, 빠른 구축용
SRC_TRAIN = "recipegpt_train.txt"  # 약 21MB, 대량 구축용

# 요리명 / 재료 / 조리법 3구간 추출
LINE_RE = re.compile(
    r"<unused0>(.*?)<unused1>.*?<unused2>(.*?)<unused3>.*?<unused4>(.*?)<unused5>",
    re.DOTALL,
)


def download(src_file: str) -> str:
    """원본 txt를 받아 로컬에 저장(이미 있으면 재사용)하고 경로 반환."""
    local = Path(src_file)
    if not local.exists():
        url = f"{RAW_BASE}/{src_file}"
        print(f"⬇️  다운로드: {url}")
        urllib.request.urlretrieve(url, local)
    print(f"✓ 원본: {local} ({local.stat().st_size//1024} KB)")
    return str(local)


def split_steps(text: str) -> list:
    """조리법 한 단락을 문장 단위 리스트로 분리."""
    parts = [s.strip() for s in re.split(r"(?<=다)[.\s]+|\.", text) if s.strip()]
    return parts or [text.strip()]


def parse(src_path: str, limit: int) -> list:
    raw = Path(src_path).read_text(encoding="utf-8")
    recipes, seen = [], set()

    for m in LINE_RE.finditer(raw):
        dish = re.sub(r"\s+", " ", m.group(1)).strip()
        if not dish or dish in seen:
            continue
        ingredients = [x.strip() for x in m.group(2).split("$") if x.strip()]
        steps = split_steps(m.group(3))
        if not ingredients or not steps:
            continue

        seen.add(dish)
        recipes.append({
            "dish_name": dish,
            "ingredients": ingredients,
            "steps": steps,
            "tags": [],
        })
        if len(recipes) >= limit:
            break

    return recipes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", type=int, metavar="N",
                    help="train 파일에서 최대 N개 (지정 시 train 사용)")
    ap.add_argument("--limit", type=int, default=3000,
                    help="val 파일에서 최대 개수 (기본 3000)")
    ap.add_argument("--out", default="recipe_db.json")
    args = ap.parse_args()

    if args.all:
        src, limit = download(SRC_TRAIN), args.all
    else:
        src, limit = download(SRC_VAL), args.limit

    recipes = parse(src, limit)
    Path(args.out).write_text(
        json.dumps(recipes, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ 변환 완료: {args.out} — {len(recipes)}개 레시피")
    if recipes:
        s = recipes[0]
        print(f"   예시: {s['dish_name']} | 재료 {len(s['ingredients'])}개 | 단계 {len(s['steps'])}개")


if __name__ == "__main__":
    main()
