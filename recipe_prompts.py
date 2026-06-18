RECIPE_LIBRARY = {
    "EXP_1": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 영양 전문 셰프야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "보편적인 요리명을 정하고 {hated}의 맛, 향, 식감을 완벽하게 은폐한 구체적인 요리법을 작성하세요.", "reasoning_instruction": "단계별로 논리적으로 생각하세요 (Let's think step-by-step).", "verification_instruction": "단판 생성", "input_data": { "ingredients": "{ingredients}", "hated": "{hated}" } },
  "in_context_learning": { "mode": "zero", "examples": [] },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[위험] 답변에 'identity'나 'task' 같은 프롬프트 지시사항을 절대로 포함하지 마세요. 오직 아래 schema 형식의 JSON 데이터만 출력하세요.",
    "style_guide": "recipe : 1. 2. 3. 순서 준수",
    "schema": "{\"dish_name\": \"요리 이름\", \"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",
    "EXP_2": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 영양 전문 셰프야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "보편적인 요리명을 정하고 {hated}의 맛, 향, 식감을 완벽하게 은폐한 구체적인 요리법을 작성하세요.", "reasoning_instruction": "단계별로 논리적으로 생각하세요 (Let's think step-by-step).", "verification_instruction": "결과 생성 후 스스로 검토하여 {hated}가 잘 숨겨졌는지 확인하고 부족하면 수정하세요 (최대 3회).", "input_data": { "ingredients": "{ingredients}", "hated": "{hated}" } },
  "in_context_learning": { "mode": "zero", "examples": [] },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[위험] 답변에 'identity'나 'task' 같은 프롬프트 지시사항을 절대로 포함하지 마세요. 오직 아래 schema 형식의 JSON 데이터만 출력하세요.",
    "style_guide": "recipe : 1. 2. 3. 순서 준수",
    "schema": "{\"dish_name\": \"요리 이름\", \"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",
    "EXP_3": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 영양 전문 셰프야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "보편적인 요리명을 정하고 {hated}의 맛, 향, 식감을 완벽하게 은폐한 구체적인 요리법을 작성하세요.", "reasoning_instruction": "전략 수립 -> 세부 계획 -> 최종 생성 순으로 작업을 분리하세요.", "verification_instruction": "단판 생성", "input_data": { "ingredients": "{ingredients}", "hated": "{hated}" } },
  "in_context_learning": { "mode": "zero", "examples": [] },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[위험] 답변에 'identity'나 'task' 같은 프롬프트 지시사항을 절대로 포함하지 마세요. 오직 아래 schema 형식의 JSON 데이터만 출력하세요.",
    "style_guide": "recipe : 1. 2. 3. 순서 준수",
    "schema": "{\"dish_name\": \"요리 이름\", \"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",
    "EXP_4": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 영양 전문 셰프야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "보편적인 요리명을 정하고 {hated}의 맛, 향, 식감을 완벽하게 은폐한 구체적인 요리법을 작성하세요.", "reasoning_instruction": "전략 수립 -> 세부 계획 -> 최종 생성 순으로 작업을 분리하세요.", "verification_instruction": "결과 생성 후 스스로 검토하여 {hated}가 잘 숨겨졌는지 확인하고 부족하면 수정하세요 (최대 3회).", "input_data": { "ingredients": "{ingredients}", "hated": "{hated}" } },
  "in_context_learning": { "mode": "zero", "examples": [] },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[위험] 답변에 'identity'나 'task' 같은 프롬프트 지시사항을 절대로 포함하지 마세요. 오직 아래 schema 형식의 JSON 데이터만 출력하세요.",
    "style_guide": "recipe : 1. 2. 3. 순서 준수",
    "schema": "{\"dish_name\": \"요리 이름\", \"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",
    "EXP_5": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 영양 전문 셰프야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "보편적인 요리명을 정하고 {hated}의 맛, 향, 식감을 완벽하게 은폐한 구체적인 요리법을 작성하세요.", "reasoning_instruction": "단계별로 논리적으로 생각하세요 (Let's think step-by-step).", "verification_instruction": "단판 생성", "input_data": { "ingredients": "{ingredients}", "hated": "{hated}" } },
  "in_context_learning": { "mode": "few", "examples": [{"input": {"ingredients": "시금치, 두부, 된장", "hated": "시금치"}, "output": {"dish_name": "두부 된장국", "strategy": "시금치를 잘게 다져 된장 향 속에 완전히 숨김", "content": "recipe : 1. 시금치를 최대한 잘게 다진다. 2. 두부와 된장을 넣고 끓인다. 3. 다진 시금치를 마지막에 넣고 한번 더 끓인다."}}] },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[위험] 답변에 'identity'나 'task' 같은 프롬프트 지시사항을 절대로 포함하지 마세요. 오직 아래 schema 형식의 JSON 데이터만 출력하세요.",
    "style_guide": "recipe : 1. 2. 3. 순서 준수",
    "schema": "{\"dish_name\": \"요리 이름\", \"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",
    "EXP_6": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 영양 전문 셰프야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "보편적인 요리명을 정하고 {hated}의 맛, 향, 식감을 완벽하게 은폐한 구체적인 요리법을 작성하세요.", "reasoning_instruction": "단계별로 논리적으로 생각하세요 (Let's think step-by-step).", "verification_instruction": "결과 생성 후 스스로 검토하여 {hated}가 잘 숨겨졌는지 확인하고 부족하면 수정하세요 (최대 3회).", "input_data": { "ingredients": "{ingredients}", "hated": "{hated}" } },
  "in_context_learning": { "mode": "few", "examples": [{"input": {"ingredients": "시금치, 두부, 된장", "hated": "시금치"}, "output": {"dish_name": "두부 된장국", "strategy": "시금치를 잘게 다져 된장 향 속에 완전히 숨김", "content": "recipe : 1. 시금치를 최대한 잘게 다진다. 2. 두부와 된장을 넣고 끓인다. 3. 다진 시금치를 마지막에 넣고 한번 더 끓인다."}}] },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[위험] 답변에 'identity'나 'task' 같은 프롬프트 지시사항을 절대로 포함하지 마세요. 오직 아래 schema 형식의 JSON 데이터만 출력하세요.",
    "style_guide": "recipe : 1. 2. 3. 순서 준수",
    "schema": "{\"dish_name\": \"요리 이름\", \"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",
    "EXP_7": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 영양 전문 셰프야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "보편적인 요리명을 정하고 {hated}의 맛, 향, 식감을 완벽하게 은폐한 구체적인 요리법을 작성하세요.", "reasoning_instruction": "전략 수립 -> 세부 계획 -> 최종 생성 순으로 작업을 분리하세요.", "verification_instruction": "단판 생성", "input_data": { "ingredients": "{ingredients}", "hated": "{hated}" } },
  "in_context_learning": { "mode": "few", "examples": [{"input": {"ingredients": "시금치, 두부, 된장", "hated": "시금치"}, "output": {"dish_name": "두부 된장국", "strategy": "시금치를 잘게 다져 된장 향 속에 완전히 숨김", "content": "recipe : 1. 시금치를 최대한 잘게 다진다. 2. 두부와 된장을 넣고 끓인다. 3. 다진 시금치를 마지막에 넣고 한번 더 끓인다."}}] },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[위험] 답변에 'identity'나 'task' 같은 프롬프트 지시사항을 절대로 포함하지 마세요. 오직 아래 schema 형식의 JSON 데이터만 출력하세요.",
    "style_guide": "recipe : 1. 2. 3. 순서 준수",
    "schema": "{\"dish_name\": \"요리 이름\", \"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",
    "EXP_8": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 영양 전문 셰프야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "보편적인 요리명을 정하고 {hated}의 맛, 향, 식감을 완벽하게 은폐한 구체적인 요리법을 작성하세요.", "reasoning_instruction": "전략 수립 -> 세부 계획 -> 최종 생성 순으로 작업을 분리하세요.", "verification_instruction": "결과 생성 후 스스로 검토하여 {hated}가 잘 숨겨졌는지 확인하고 부족하면 수정하세요 (최대 3회).", "input_data": { "ingredients": "{ingredients}", "hated": "{hated}" } },
  "in_context_learning": { "mode": "few", "examples": [{"input": {"ingredients": "시금치, 두부, 된장", "hated": "시금치"}, "output": {"dish_name": "두부 된장국", "strategy": "시금치를 잘게 다져 된장 향 속에 완전히 숨김", "content": "recipe : 1. 시금치를 최대한 잘게 다진다. 2. 두부와 된장을 넣고 끓인다. 3. 다진 시금치를 마지막에 넣고 한번 더 끓인다."}}] },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[위험] 답변에 'identity'나 'task' 같은 프롬프트 지시사항을 절대로 포함하지 마세요. 오직 아래 schema 형식의 JSON 데이터만 출력하세요.",
    "style_guide": "recipe : 1. 2. 3. 순서 준수",
    "schema": "{\"dish_name\": \"요리 이름\", \"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",
    "EXP_9": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 영양 전문 셰프야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "보편적인 요리명을 정하고 {hated}의 맛, 향, 식감을 완벽하게 은폐한 구체적인 요리법을 작성하세요.", "reasoning_instruction": "단계별로 논리적으로 생각하세요 (Let's think step-by-step).", "verification_instruction": "단판 생성", "input_data": { "ingredients": "{ingredients}", "hated": "{hated}" } },
  "in_context_learning": {
    "mode": "contrastive",
    "examples": [
      {
        "type": "bad",
        "input": {"ingredients": "시금치, 두부, 된장", "hated": "시금치"},
        "output": {"dish_name": "시금치 된장국", "strategy": "시금치를 넣고 끓임", "content": "recipe : 1. 시금치를 넣는다. 2. 된장을 푼다. 3. 두부를 넣는다."},
        "reason": "실패 이유: dish_name에 hated 재료가 그대로 노출됨. recipe에서도 hated를 숨기지 않고 첫 단계에 배치함."
      },
      {
        "type": "good",
        "input": {"ingredients": "시금치, 두부, 된장", "hated": "시금치"},
        "output": {"dish_name": "두부 된장국", "strategy": "시금치를 잘게 다져 된장 향 속에 완전히 숨김", "content": "recipe : 1. 시금치를 최대한 잘게 다진다. 2. 두부와 된장을 넣고 끓인다. 3. 다진 시금치를 마지막에 넣고 한번 더 끓인다."}
      }
    ]
  },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[위험] 답변에 'identity'나 'task' 같은 프롬프트 지시사항을 절대로 포함하지 마세요. 오직 아래 schema 형식의 JSON 데이터만 출력하세요.",
    "style_guide": "recipe : 1. 2. 3. 순서 준수",
    "schema": "{\"dish_name\": \"요리 이름\", \"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",
    "EXP_10": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 영양 전문 셰프야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "보편적인 요리명을 정하고 {hated}의 맛, 향, 식감을 완벽하게 은폐한 구체적인 요리법을 작성하세요.", "reasoning_instruction": "전략 수립 -> 세부 계획 -> 최종 생성 순으로 작업을 분리하세요.", "verification_instruction": "결과 생성 후 스스로 검토하여 {hated}가 잘 숨겨졌는지 확인하고 부족하면 수정하세요 (최대 3회).", "input_data": { "ingredients": "{ingredients}", "hated": "{hated}" } },
  "in_context_learning": {
    "mode": "contrastive",
    "examples": [
      {
        "type": "bad",
        "input": {"ingredients": "시금치, 두부, 된장", "hated": "시금치"},
        "output": {"dish_name": "시금치 된장국", "strategy": "시금치를 넣고 끓임", "content": "recipe : 1. 시금치를 넣는다. 2. 된장을 푼다. 3. 두부를 넣는다."},
        "reason": "실패 이유: dish_name에 hated 재료가 그대로 노출됨. recipe에서도 hated를 숨기지 않고 첫 단계에 배치함."
      },
      {
        "type": "good",
        "input": {"ingredients": "시금치, 두부, 된장", "hated": "시금치"},
        "output": {"dish_name": "두부 된장국", "strategy": "시금치를 잘게 다져 된장 향 속에 완전히 숨김", "content": "recipe : 1. 시금치를 최대한 잘게 다진다. 2. 두부와 된장을 넣고 끓인다. 3. 다진 시금치를 마지막에 넣고 한번 더 끓인다."}
      }
    ]
  },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[위험] 답변에 'identity'나 'task' 같은 프롬프트 지시사항을 절대로 포함하지 마세요. 오직 아래 schema 형식의 JSON 데이터만 출력하세요.",
    "style_guide": "recipe : 1. 2. 3. 순서 준수",
    "schema": "{\"dish_name\": \"요리 이름\", \"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",
    "EXP_11": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 영양 전문 셰프야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "보편적인 요리명을 정하고 {hated}의 맛, 향, 식감을 완벽하게 은폐한 구체적인 요리법을 작성하세요.", "reasoning_instruction": "단계별로 논리적으로 생각하세요 (Let's think step-by-step).", "verification_instruction": "결과 생성 후 스스로 검토하여 {hated}가 잘 숨겨졌는지 확인하고 부족하면 수정하세요 (최대 3회).", "input_data": { "ingredients": "{ingredients}", "hated": "{hated}" } },
  "in_context_learning": {
    "mode": "contrastive",
    "examples": [
      {
        "type": "bad",
        "input": {"ingredients": "시금치, 두부, 된장", "hated": "시금치"},
        "output": {"dish_name": "시금치 된장국", "strategy": "시금치를 넣고 끓임", "content": "recipe : 1. 시금치를 넣는다. 2. 된장을 푼다. 3. 두부를 넣는다."},
        "reason": "실패 이유: dish_name에 hated 재료가 그대로 노출됨. recipe에서도 hated를 숨기지 않고 첫 단계에 배치함."
      },
      {
        "type": "good",
        "input": {"ingredients": "시금치, 두부, 된장", "hated": "시금치"},
        "output": {"dish_name": "두부 된장국", "strategy": "시금치를 잘게 다져 된장 향 속에 완전히 숨김", "content": "recipe : 1. 시금치를 최대한 잘게 다진다. 2. 두부와 된장을 넣고 끓인다. 3. 다진 시금치를 마지막에 넣고 한번 더 끓인다."}
      }
    ]
  },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[위험] 답변에 'identity'나 'task' 같은 프롬프트 지시사항을 절대로 포함하지 마세요. 오직 아래 schema 형식의 JSON 데이터만 출력하세요.",
    "style_guide": "recipe : 1. 2. 3. 순서 준수",
    "schema": "{\"dish_name\": \"요리 이름\", \"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",
    "EXP_12": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 영양 전문 셰프야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "보편적인 요리명을 정하고 {hated}의 맛, 향, 식감을 완벽하게 은폐한 구체적인 요리법을 작성하세요.", "reasoning_instruction": "전략 수립 -> 세부 계획 -> 최종 생성 순으로 작업을 분리하세요.", "verification_instruction": "결과 생성 후 스스로 검토하여 {hated}가 잘 숨겨졌는지 확인하고 부족하면 수정하세요 (최대 3회).", "input_data": { "ingredients": "{ingredients}", "hated": "{hated}" } },
  "in_context_learning": {
    "mode": "contrastive",
    "examples": [
      {
        "type": "bad",
        "input": {"ingredients": "시금치, 두부, 된장", "hated": "시금치"},
        "output": {"dish_name": "시금치 된장국", "strategy": "시금치를 넣고 끓임", "content": "recipe : 1. 시금치를 넣는다. 2. 된장을 푼다. 3. 두부를 넣는다."},
        "reason": "실패 이유: dish_name에 hated 재료가 그대로 노출됨. recipe에서도 hated를 숨기지 않고 첫 단계에 배치함."
      },
      {
        "type": "good",
        "input": {"ingredients": "시금치, 두부, 된장", "hated": "시금치"},
        "output": {"dish_name": "두부 된장국", "strategy": "시금치를 잘게 다져 된장 향 속에 완전히 숨김", "content": "recipe : 1. 시금치를 최대한 잘게 다진다. 2. 두부와 된장을 넣고 끓인다. 3. 다진 시금치를 마지막에 넣고 한번 더 끓인다."}
      }
    ]
  },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[위험] 답변에 'identity'나 'task' 같은 프롬프트 지시사항을 절대로 포함하지 마세요. 오직 아래 schema 형식의 JSON 데이터만 출력하세요.",
    "style_guide": "recipe : 1. 2. 3. 순서 준수",
    "schema": "{\"dish_name\": \"요리 이름\", \"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",
}