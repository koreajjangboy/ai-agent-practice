import os
from dotenv import load_dotenv, set_key

# 1. 환경 변수 로드 (.env 파일 탐색)
load_dotenv()

def fetch_and_update_gemini_models():
    print("🔄 Google Gemini API를 통해 사용 가능한 모델 목록을 조회하는 중...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ 오류: GEMINI_API_KEY가 설정되어 있지 않습니다. .env 파일을 확인해 주세요.")
        return

    try:
        from google import genai
        
        # Gemini 클라이언트 초기화
        client = genai.Client(api_key=api_key)
        
        # 사용 가능한 모델 목록 조회
        models_response = client.models.list()
        
        model_names = []
        for model in models_response:
            # model.name 형식은 'models/gemini-2.5-flash' 형태로 반환되므로 뒷부분 위주 또는 전체를 추출
            name = getattr(model, "name", str(model))
            model_names.append(name)
            
        model_names.sort()
        
        # 카테고리별 분류 필터링 (예: 텍스트/멀티모달 챗, 임베딩 등)
        chat_models = [m for m in model_names if "gemini" in m]
        embedding_models = [m for m in model_names if "embedding" in m]
        
        print(f"\n[조회 완료] 총 {len(model_names)}개의 모델을 불러왔습니다.")
        print(f"- Gemini 챗/멀티모달 모델: {len(chat_models)}개")
        print(f"- Gemini 임베딩 모델: {len(embedding_models)}개")
        
        # 3. .env 파일 경로 확인
        env_path = ".env"
        if not os.path.exists(env_path):
            print("⚠️ 경고: 루트 디렉토리에 .env 파일이 존재하지 않아 새로 생성합니다.")
            open(env_path, "w").close()
            
        # 4. .env 파일에 Gemini 모델 리스트 저장
        set_key(env_path, "AVAILABLE_GEMINI_CHAT_MODELS", ",".join(chat_models))
        set_key(env_path, "AVAILABLE_GEMINI_EMBEDDING_MODELS", ",".join(embedding_models))
        
        print("\n✅ 성공적으로 .env 파일에 Gemini 모델 목록이 업데이트되었습니다!")
        print("  - AVAILABLE_GEMINI_CHAT_MODELS")
        print("  - AVAILABLE_GEMINI_EMBEDDING_MODELS")
        
    except ImportError:
        print("❌ 오류: google-genai 패키지가 설치되어 있지 않습니다. 'pip install google-genai'를 실행해주세요.")
    except Exception as e:
        print(f"❌ 모델 목록을 불러오는 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    fetch_and_update_gemini_models()