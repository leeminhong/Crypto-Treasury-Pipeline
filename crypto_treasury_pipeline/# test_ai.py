# test_ai.py
import google.generativeai as genai
import yaml

# 🔴 [수정됨] encoding='utf-8'을 꼭 넣어줘야 한글 윈도우에서 에러가 안 납니다!
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

api_key = config.get('gemini_api_key')
genai.configure(api_key=api_key)

print("🔍 내 키로 사용 가능한 모델 목록:")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f" - {m.name}")
except Exception as e:
    print(f"❌ 목록 조회 실패: {e}")