STORY_LIBRARY = {
    "EXP_1": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 문학 작가야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "아이의 관심사인 {interest}와 셰프가 만든 {dish_name}을 창의적으로 연결하세요. 아이가 이 요리를 먹고 싶게 만드는 매력적인 한 문장을 만드세요.", "reasoning_instruction": "단계별로 논리적으로 생각하세요 (Let's think step-by-step).", "verification_instruction": "단판 생성", "input_data": { "dish_name": "{dish_name}", "interest": "{interest}" } },
  "in_context_learning": { "mode": "zero", "examples": [] },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[절대 주의] 너의 'identity'나 'persona' 등을 답변에 포함하지 마세요. 오직 아래 schema 구조의 JSON 데이터만 출력하고, 아이에게 들려줄 이야기는 'content' 필드에만 담으세요.",
    "style_guide": "아이에게 들려줄 설명 문장",
    "schema": "{\"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",

    "EXP_2": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 문학 작가야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "아이의 관심사인 {interest}와 셰프가 만든 {dish_name}을 창의적으로 연결하세요. 아이가 이 요리를 먹고 싶게 만드는 매력적인 한 문장을 만드세요.", "reasoning_instruction": "단계별로 논리적으로 생각하세요 (Let's think step-by-step).", "verification_instruction": "결과 생성 후 스스로 검토하여 {hated}가 잘 숨겨졌는지 확인하고 부족하면 수정하세요 (최대 3회).", "input_data": { "dish_name": "{dish_name}", "interest": "{interest}" } },
  "in_context_learning": { "mode": "zero", "examples": [] },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[절대 주의] 프롬프트의 지침 내용을 복사하지 마세요. 오직 지정된 JSON 형식만 출력하세요.",
    "style_guide": "아이에게 들려줄 설명 문장",
    "schema": "{\"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",

    "EXP_3": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 문학 작가야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "아이의 관심사인 {interest}와 셰프가 만든 {dish_name}을 창의적으로 연결하세요. 아이가 이 요리를 먹고 싶게 만드는 매력적인 한 문장을 만드세요.", "reasoning_instruction": "전략 수립 -> 세부 계획 -> 최종 생성 순으로 작업을 분리하세요.", "verification_instruction": "단판 생성", "input_data": { "dish_name": "{dish_name}", "interest": "{interest}" } },
  "in_context_learning": { "mode": "zero", "examples": [] },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[절대 주의] 프롬프트의 지침 내용을 복사하지 마세요. 오직 지정된 JSON 형식만 출력하세요.",
    "style_guide": "아이에게 들려줄 설명 문장",
    "schema": "{\"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",

    "EXP_4": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 문학 작가야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "아이의 관심사인 {interest}와 셰프가 만든 {dish_name}을 창의적으로 연결하세요. 아이가 이 요리를 먹고 싶게 만드는 매력적인 한 문장을 만드세요.", "reasoning_instruction": "전략 수립 -> 세부 계획 -> 최종 생성 순으로 작업을 분리하세요.", "verification_instruction": "결과 생성 후 스스로 검토하여 {hated}가 잘 숨겨졌는지 확인하고 부족하면 수정하세요 (최대 3회).", "input_data": { "dish_name": "{dish_name}", "interest": "{interest}" } },
  "in_context_learning": { "mode": "zero", "examples": [] },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[절대 주의] 프롬프트의 지침 내용을 복사하지 마세요. 오직 지정된 JSON 형식만 출력하세요.",
    "style_guide": "아이에게 들려줄 설명 문장",
    "schema": "{\"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",

    "EXP_5": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 문학 작가야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "아이의 관심사인 {interest}와 셰프가 만든 {dish_name}을 창의적으로 연결하세요. 아이가 이 요리를 먹고 싶게 만드는 매력적인 한 문장을 만드세요.", "reasoning_instruction": "단계별로 논리적으로 생각하세요 (Let's think step-by-step).", "verification_instruction": "단판 생성", "input_data": { "dish_name": "{dish_name}", "interest": "{interest}" } },
  "in_context_learning": { "mode": "few", "examples": [{"input": {"dish_name": "두부 된장국", "interest": "공룡"}, "output": {"strategy": "된장국의 구수한 향을 공룡 세계의 신비로운 마법 수프로 연결", "content": "이 수프를 마신 공룡들은 누구보다 강해졌대, 너도 한 숟가락 먹으면 트리케라톱스처럼 용감해질 수 있어!"}}] },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[절대 주의] 예시 형식을 따르되, 프롬프트 지침이나 너의 페르소나를 대답에 섞지 마세요.",
    "style_guide": "아이에게 들려줄 설명 문장",
    "schema": "{\"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",

    "EXP_6": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 문학 작가야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "아이의 관심사인 {interest}와 셰프가 만든 {dish_name}을 창의적으로 연결하세요. 아이가 이 요리를 먹고 싶게 만드는 매력적인 한 문장을 만드세요.", "reasoning_instruction": "단계별로 논리적으로 생각하세요 (Let's think step-by-step).", "verification_instruction": "결과 생성 후 스스로 검토하여 {hated}가 잘 숨겨졌는지 확인하고 부족하면 수정하세요 (최대 3회).", "input_data": { "dish_name": "{dish_name}", "interest": "{interest}" } },
  "in_context_learning": { "mode": "few", "examples": [{"input": {"dish_name": "두부 된장국", "interest": "공룡"}, "output": {"strategy": "된장국의 구수한 향을 공룡 세계의 신비로운 마법 수프로 연결", "content": "이 수프를 마신 공룡들은 누구보다 강해졌대, 너도 한 숟가락 먹으면 트리케라톱스처럼 용감해질 수 있어!"}}] },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[절대 주의] 지침 내용을 대답에 복사하지 마세요. JSON 데이터만 출력하세요.",
    "style_guide": "아이에게 들려줄 설명 문장",
    "schema": "{\"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",

    "EXP_7": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 문학 작가야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "아이의 관심사인 {interest}와 셰프가 만든 {dish_name}을 창의적으로 연결하세요. 아이가 이 요리를 먹고 싶게 만드는 매력적인 한 문장을 만드세요.", "reasoning_instruction": "전략 수립 -> 세부 계획 -> 최종 생성 순으로 작업을 분리하세요.", "verification_instruction": "단판 생성", "input_data": { "dish_name": "{dish_name}", "interest": "{interest}" } },
  "in_context_learning": { "mode": "few", "examples": [{"input": {"dish_name": "두부 된장국", "interest": "공룡"}, "output": {"strategy": "된장국의 구수한 향을 공룡 세계의 신비로운 마법 수프로 연결", "content": "이 수프를 마신 공룡들은 누구보다 강해졌대, 너도 한 숟가락 먹으면 트리케라톱스처럼 용감해질 수 있어!"}}] },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[절대 주의] 지침 내용을 대답에 복사하지 마세요. JSON 데이터만 출력하세요.",
    "style_guide": "아이에게 들려줄 설명 문장",
    "schema": "{\"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",

    "EXP_8": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 문학 작가야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "아이의 관심사인 {interest}와 셰프가 만든 {dish_name}을 창의적으로 연결하세요. 아이가 이 요리를 먹고 싶게 만드는 매력적인 한 문장을 만드세요.", "reasoning_instruction": "전략 수립 -> 세부 계획 -> 최종 생성 순으로 작업을 분리하세요.", "verification_instruction": "결과 생성 후 스스로 검토하여 {hated}가 잘 숨겨졌는지 확인하고 부족하면 수정하세요 (최대 3회).", "input_data": { "dish_name": "{dish_name}", "interest": "{interest}" } },
  "in_context_learning": { "mode": "few", "examples": [{"input": {"dish_name": "두부 된장국", "interest": "공룡"}, "output": {"strategy": "된장국의 구수한 향을 공룡 세계의 신비로운 마법 수프로 연결", "content": "이 수프를 마신 공룡들은 누구보다 강해졌대, 너도 한 숟가락 먹으면 트리케라톱스처럼 용감해질 수 있어!"}}] },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[절대 주의] 지침 내용을 대답에 복사하지 마세요. JSON 데이터만 출력하세요.",
    "style_guide": "아이에게 들려줄 설명 문장",
    "schema": "{\"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",

    "EXP_9": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 문학 작가야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "아이의 관심사인 {interest}와 셰프가 만든 {dish_name}을 창의적으로 연결하세요. 아이가 이 요리를 먹고 싶게 만드는 매력적인 한 문장을 만드세요.", "reasoning_instruction": "단계별로 논리적으로 생각하세요 (Let's think step-by-step).", "verification_instruction": "단판 생성", "input_data": { "dish_name": "{dish_name}", "interest": "{interest}" } },
  "in_context_learning": {
    "mode": "contrastive",
    "examples": [
      {
        "type": "bad",
        "input": {"dish_name": "두부 된장국", "interest": "공룡"},
        "output": {"strategy": "된장국이라고 설명함", "content": "이건 된장국이야, 한번 먹어봐."},
        "reason": "실패 이유: 아이의 관심사인 공룡과 전혀 연결되지 않음. 매력적이지 않고 아이의 흥미를 전혀 끌지 못함."
      },
      {
        "type": "good",
        "input": {"dish_name": "두부 된장국", "interest": "공룡"},
        "output": {"strategy": "된장국의 구수한 향을 공룡 세계의 신비로운 마법 수프로 연결", "content": "이 수프를 마신 공룡들은 누구보다 강해졌대, 너도 한 숟가락 먹으면 트리케라톱스처럼 용감해질 수 있어!"}
      }
    ]
  },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[절대 주의] 지침 내용을 대답에 복사하지 마세요. JSON 데이터만 출력하세요.",
    "style_guide": "아이에게 들려줄 설명 문장",
    "schema": "{\"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",

    "EXP_10": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 문학 작가야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "아이의 관심사인 {interest}와 셰프가 만든 {dish_name}을 창의적으로 연결하세요. 아이가 이 요리를 먹고 싶게 만드는 매력적인 한 문장을 만드세요.", "reasoning_instruction": "전략 수립 -> 세부 계획 -> 최종 생성 순으로 작업을 분리하세요.", "verification_instruction": "결과 생성 후 스스로 검토하여 아이의 관심사와 잘 연결되었는지 확인하고 부족하면 수정하세요 (최대 3회).", "input_data": { "dish_name": "{dish_name}", "interest": "{interest}" } },
  "in_context_learning": {
    "mode": "contrastive",
    "examples": [
      {
        "type": "bad",
        "input": {"dish_name": "두부 된장국", "interest": "공룡"},
        "output": {"strategy": "된장국이라고 설명함", "content": "이건 된장국이야, 한번 먹어봐."},
        "reason": "실패 이유: 아이의 관심사인 공룡과 전혀 연결되지 않음. 매력적이지 않고 아이의 흥미를 전혀 끌지 못함."
      },
      {
        "type": "good",
        "input": {"dish_name": "두부 된장국", "interest": "공룡"},
        "output": {"strategy": "된장국의 구수한 향을 공룡 세계의 신비로운 마법 수프로 연결", "content": "이 수프를 마신 공룡들은 누구보다 강해졌대, 너도 한 숟가락 먹으면 트리케라톱스처럼 용감해질 수 있어!"}
      }
    ]
  },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[절대 주의] 지침 내용을 대답에 복사하지 마세요. JSON 데이터만 출력하세요.",
    "style_guide": "아이에게 들려줄 설명 문장",
    "schema": "{\"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",

    "EXP_11": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 문학 작가야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "아이의 관심사인 {interest}와 셰프가 만든 {dish_name}을 창의적으로 연결하세요. 아이가 이 요리를 먹고 싶게 만드는 매력적인 한 문장을 만드세요.", "reasoning_instruction": "단계별로 논리적으로 생각하세요 (Let's think step-by-step).", "verification_instruction": "결과 생성 후 스스로 검토하여 아이의 관심사와 잘 연결되었는지 확인하고 부족하면 수정하세요 (최대 3회).", "input_data": { "dish_name": "{dish_name}", "interest": "{interest}" } },
  "in_context_learning": {
    "mode": "contrastive",
    "examples": [
      {
        "type": "bad",
        "input": {"dish_name": "두부 된장국", "interest": "공룡"},
        "output": {"strategy": "된장국이라고 설명함", "content": "이건 된장국이야, 한번 먹어봐."},
        "reason": "실패 이유: 아이의 관심사인 공룡과 전혀 연결되지 않음. 매력적이지 않고 아이의 흥미를 전혀 끌지 못함."
      },
      {
        "type": "good",
        "input": {"dish_name": "두부 된장국", "interest": "공룡"},
        "output": {"strategy": "된장국의 구수한 향을 공룡 세계의 신비로운 마법 수프로 연결", "content": "이 수프를 마신 공룡들은 누구보다 강해졌대, 너도 한 숟가락 먹으면 트리케라톱스처럼 용감해질 수 있어!"}
      }
    ]
  },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[절대 주의] 지침 내용을 대답에 복사하지 마세요. JSON 데이터만 출력하세요.",
    "style_guide": "아이에게 들려줄 설명 문장",
    "schema": "{\"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",

    "EXP_12": """아래 지침을 수행하세요:
{
  "identity": { "persona": "너는 아동 문학 작가야. 너의 생각을 결과에 담지마 혼자서만 생각해, 절대 영어로 말하지 마 모든 응답은 한글로 생성해", "target": "미취학 아동" },
  "task": { "goal": "아이의 관심사인 {interest}와 셰프가 만든 {dish_name}을 창의적으로 연결하세요. 아이가 이 요리를 먹고 싶게 만드는 매력적인 한 문장을 만드세요.", "reasoning_instruction": "전략 수립 -> 세부 계획 -> 최종 생성 순으로 작업을 분리하세요.", "verification_instruction": "결과 생성 후 스스로 검토하여 아이의 관심사와 잘 연결되었는지 확인하고 부족하면 수정하세요 (최대 3회).", "input_data": { "dish_name": "{dish_name}", "interest": "{interest}" } },
  "in_context_learning": {
    "mode": "contrastive",
    "examples": [
      {
        "type": "bad",
        "input": {"dish_name": "두부 된장국", "interest": "공룡"},
        "output": {"strategy": "된장국이라고 설명함", "content": "이건 된장국이야, 한번 먹어봐."},
        "reason": "실패 이유: 아이의 관심사인 공룡과 전혀 연결되지 않음. 매력적이지 않고 아이의 흥미를 전혀 끌지 못함."
      },
      {
        "type": "good",
        "input": {"dish_name": "두부 된장국", "interest": "공룡"},
        "output": {"strategy": "된장국의 구수한 향을 공룡 세계의 신비로운 마법 수프로 연결", "content": "이 수프를 마신 공룡들은 누구보다 강해졌대, 너도 한 숟가락 먹으면 트리케라톱스처럼 용감해질 수 있어!"}
      }
    ]
  },
  "output_format": {
    "type": "STRICT JSON ONLY",
    "instruction": "[절대 주의] 지침 내용을 대답에 복사하지 마세요. JSON 데이터만 출력하세요.",
    "style_guide": "아이에게 들려줄 설명 문장",
    "schema": "{\"strategy\": \"너만의 독창적인 전략 설명\", \"content\": \"실제 생성 내용\"}"
  }
}""",
}