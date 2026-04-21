import nest_asyncio
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import uvicorn
from pyngrok import ngrok
from huggingface_hub import login

# 1. 허깅페이스 로그인 (본인의 토큰을 따옴표 안에 넣으세요)
HF_TOKEN = "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"
login(token=HF_TOKEN)

# 2. 모델 설정 (가벼운 Gemma-2B-it 사용)
model_id = "google/gemma-2b-it" 

print(f"📡 모델 로딩 중: {model_id} (GPU 활용)...")
pipe = pipeline(
    "text-generation", 
    model=model_id, 
    model_kwargs={"torch_dtype": torch.bfloat16}, 
    device_map="auto"
)

# 3. FastAPI 앱 정의
app = FastAPI()

class Item(BaseModel):
    ingredients: str
    hated: str
    interest: str

@app.post("/generate")
async def generate(item: Item):
    # Recipe Agent 프롬프트 구성
    recipe_prompt = f"재료 {item.ingredients}를 사용해 {item.hated}의 맛과 식감을 완벽히 숨기는 20분 내외의 레시피를 알려줘."
    
    # Story Agent 프롬프트 구성
    story_prompt = f"아이의 관심사인 {item.interest}를 주제로, {item.hated}가 들어간 음식을 즐겁게 먹게 만드는 3문장 이내의 짧은 동화를 지어줘."
    
    # 결과 생성
    recipe_out = pipe(recipe_prompt, max_new_tokens=256, do_sample=True, temperature=0.7)[0]['generated_text']
    story_out = pipe(story_prompt, max_new_tokens=256, do_sample=True, temperature=0.7)[0]['generated_text']
    
    return {
        "recipe": recipe_out.replace(recipe_prompt, "").strip(),
        "story": story_out.replace(story_prompt, "").strip()
    }

# 4. ngrok 설정 (사진에서 확인된 오타 없는 토큰 적용)
NGROK_TOKEN = "3Cf7km4BvxnYUhCIp5lMFxUqA0Q_6hxaJ4Sd8qfwRAQNJXWYM" 
ngrok.set_auth_token(NGROK_TOKEN)

# 포트 8000으로 터널링 연결
public_url = ngrok.connect(8000)
print(f"\n" + "="*50)
print(f"✅ 서버 주소: {public_url}")
print(f"👉 위 주소를 맥북 Streamlit 앱 사이드바에 붙여넣으세요!")
print(f"="*50 + "\n")

# 5. 비동기 서버 실행 (Kaggle/Jupyter용)
nest_asyncio.apply()
config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
server = uvicorn.Server(config)

await server.serve()