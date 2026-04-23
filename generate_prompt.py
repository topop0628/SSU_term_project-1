import json

# --- [1. 에이전트별 구체화된 목표(Goal)] ---
# '미취학 아동'의 발달 특성(질감, 색상 민감도)을 반영하여 목표를 설정했습니다.
RECIPE_GOAL = "{hated}의 맛, 향, 식감을 완벽하게 은폐하여, 식재료에 예민한 미취학 아동이 정체를 전혀 눈치채지 못하고 즐겁게 식사할 수 있는 최적의 조리법을 개발하는 것"
STORY_GOAL = "아이의 관심사인 {interest}와 {hated}를 창의적 서사로 연결하여, 미취학 아동이 싫어하는 음식을 먹고 싶은 마법의 도구나 특별한 에너지원으로 인식하게 만드는 매력적인 이야기를 만드는 것"

# --- [2. 시나리오 데이터 (예시용)] ---
RECIPE_INPUT = {"ingredients": "브로콜리, 계란, 치즈", "hated": "브로콜리"}
STORY_INPUT = {"ingredients": "브로콜리, 계란, 치즈", "hated": "브로콜리", "interest": "축구"}

# --- [3. 에이전트별 상세 예시 (Strategy + Content)] ---
RECIPE_EXAMPLE_OUTPUT = {
    "strategy": "브로콜리를 고온에서 볶아 수분과 향을 날린 뒤 계란과 치즈로 시각적/미각적 방어막을 형성하는 전략",
    "content": "recipe : 1. 브로콜리는 꽃 부분만 아주 곱게 다진 뒤, 마른 팬에 수분이 완전히 날아가 포슬포슬해질 때까지 충분히 볶아 특유의 풋내를 제거합니다. 2. 볼에 계란을 풀고 볶은 브로콜리를 섞어 입자가 뭉치지 않게 고르게 젓습니다. 3. 약불에서 계란말이를 만들되 속까지 완전히 익혀 미취학 아동이 싫어하는 특유의 아삭한 식감을 없앱니다. 4. 완성된 요리 위에 슬라이스 치즈를 넓게 펴 발라 잔열로 녹여줌으로써 초록색이 전혀 보이지 않도록 덮어줍니다."
}

STORY_EXAMPLE_OUTPUT = {
    "strategy": "브로콜리를 축구 선수의 에너지가 담긴 '파워 나무'로 비유하여 심리적 거부감을 도전 욕구로 전환하는 전략",
    "content": "이 초록색 작은 나무는 사실 국가대표 축구 선수들이 경기장에 나가기 전 비밀리에 챙겨 먹는 '무적의 파워 나무'란다! 우리 친구가 이 나무를 한 입 쏙 먹으면, 다리에 축구 공을 뻥 찰 수 있는 엄청난 에너지가 생겨서 누구보다 멋진 골을 넣을 수 있는 무적의 힘을 얻게 될 거야."
}

# --- [4. 전략 지시문 모듈] ---
STRATEGIES = {
    "cot": "단계별로 논리적으로 생각하세요 (Let's think step-by-step).",
    "chain": "전략 수립 -> 세부 계획 -> 최종 생성 순으로 작업을 분리하세요.",
    "refine": "결과 생성 후 스스로 검토하여 {hated}가 잘 숨겨졌는지 확인하고 부족하면 수정하세요 (최대 3회)."
}

def build_prompt(agent_type, icl, reasoning, refine):
    persona = "아동 영양 전문 셰프" if agent_type == "recipe" else "아동 문학 작가"
    format_guide = "recipe : 1. 2. 3. 순서 준수" if agent_type == "recipe" else "아이에게 들려줄 설명 문장"
    goal = RECIPE_GOAL if agent_type == "recipe" else STORY_GOAL
    
    # 에이전트에 따른 입력 데이터 구조 설정
    if agent_type == "recipe":
        example_data = [{"input": RECIPE_INPUT, "output": RECIPE_EXAMPLE_OUTPUT}]
        input_placeholder = {"ingredients": "{ingredients}", "hated": "{hated}"}
    else:
        example_data = [{"input": STORY_INPUT, "output": STORY_EXAMPLE_OUTPUT}]
        input_placeholder = {"ingredients": "{ingredients}", "hated": "{hated}", "interest": "{interest}"}
    
    prompt_packet = {
        "identity": {
            "persona": f"너는 {persona}야.",
            "target": "미취학 아동"
        },
        "task": {
            "goal": goal,
            "reasoning_instruction": STRATEGIES[reasoning],
            "verification_instruction": STRATEGIES["refine"] if refine == "refine" else "단판 생성",
            "input_data": input_placeholder
        },
        "in_context_learning": {
            "mode": icl,
            "examples": example_data if icl == "few" else []
        },
        "output_format": {
            "type": "JSON ONLY",
            "style_guide": format_guide,
            "schema": '{"strategy": "너만의 독창적인 전략 설명", "content": "실제 생성 내용"}'
        }
    }
    return "아래 지침을 수행하세요:\n" + json.dumps(prompt_packet, ensure_ascii=False, indent=2)

# --- [5. 파일 분리 저장] ---
for agent in ["recipe", "story"]:
    lib = {}
    idx = 1
    for icl in ["zero", "few"]:
        for reasoning in ["cot", "chain"]:
            for refine in ["none", "refine"]:
                lib[f"EXP_{idx}"] = build_prompt(agent, icl, reasoning, refine)
                idx += 1
    
    with open(f"{agent}_prompts.py", "w", encoding="utf-8") as f:
        f.write(f"{agent.upper()}_LIBRARY = " + json.dumps(lib, ensure_ascii=False, indent=4))

print("✅ '미취학 아동' 맞춤형 에이전트 프롬프트 라이브러리가 생성되었습니다!")