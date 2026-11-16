import os
from openai import OpenAI
from dotenv import load_dotenv, set_key

# 1. 환경 변수 로드 (.env 파일 탐색)
load_dotenv()

# 2. OpenAI 클라이언트 초기화 (조직 권한 자동 연동)
client = OpenAI()

def fetch_and_update_models():
    print("🔄 조직에서 사용 가능한 전체 OpenAI 모델 목록을 조회하는 중...")
    
    try:
        # 사용 가능한 모델 목록 조회
        models_response = client.models.list()
        model_ids = [model.id for model in models_response.data]
        
        # 보기 쉽게 정렬
        model_ids.sort()
        
        # 세부 카테고리별 분류 필터링 정의
        chat_models = [m for m in model_ids if any(k in m for k in ["gpt", "o1", "o3", "o4", "chatgpt"])]
        embedding_models = [m for m in model_ids if "embedding" in m]
        audio_models = [m for m in model_ids if any(k in m for k in ["whisper", "tts", "audio"])]
        image_models = [m for m in model_ids if any(k in m for k in ["dall-e", "image"])]
        moderation_models = [m for m in model_ids if "moderation" in m]
        realtime_models = [m for m in model_ids if "realtime" in m]
        
        # 그 외 분류되지 않은 모델들 (전체 목록 보존용)
        categorized_set = set(chat_models + embedding_models + audio_models + image_models + moderation_models + realtime_models)
        other_models = [m for m in model_ids if m not in categorized_set]
        
        print(f"\n[조회 완료] 총 {len(model_ids)}개의 모델을 불러왔습니다.")
        print(f"- 챗/추론 모델: {len(chat_models)}개")
        print(f"- 임베딩 모델: {len(embedding_models)}개")
        print(f"- 오디오/음성 모델: {len(audio_models)}개")
        print(f"- 이미지 모델: {len(image_models)}개")
        print(f"- 실시간(Realtime) 모델: {len(realtime_models)}개")
        print(f"- 모더레이션 모델: {len(moderation_models)}개")
        print(f"- 기타/파인튜닝 베이스 모델: {len(other_models)}개")
        
        # 3. .env 파일 경로 확인
        env_path = ".env"
        if not os.path.exists(env_path):
            print("⚠️ 경고: 루트 디렉토리에 .env 파일이 존재하지 않아 새로 생성합니다.")
            open(env_path, "w").close()
            
        # 4. .env 파일에 카테고리별 모델 리스트 저장
        set_key(env_path, "AVAILABLE_CHAT_MODELS", ",".join(chat_models))
        set_key(env_path, "AVAILABLE_EMBEDDING_MODELS", ",".join(embedding_models))
        set_key(env_path, "AVAILABLE_AUDIO_MODELS", ",".join(audio_models))
        set_key(env_path, "AVAILABLE_IMAGE_MODELS", ",".join(image_models))
        set_key(env_path, "AVAILABLE_REALTIME_MODELS", ",".join(realtime_models))
        set_key(env_path, "AVAILABLE_MODERATION_MODELS", ",".join(moderation_models))
        set_key(env_path, "AVAILABLE_ALL_MODELS", ",".join(model_ids)) # 전체 목록 필요 시 대비
        
        print("\n✅ 성공적으로 .env 파일에 카테고리별 모델 목록이 업데이트되었습니다!")
        
    except Exception as e:
        print(f"❌ 모델 목록을 불러오는 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    fetch_and_update_models()