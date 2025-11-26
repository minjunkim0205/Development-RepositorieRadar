# ---------------------------------------------------
# Import module
# ---------------------------------------------------
# 먼저 설치 필요:  pip install google-genai
from google import genai


# ---------------------------------------------------
# Function
# ---------------------------------------------------
def api_check(api_key: str) -> bool:
    """
    Gemini API 키 유효성 검사 (아주 단순 버전)
    """
    try:
        client = genai.Client(api_key=api_key)
        client.models.generate_content(
            model="gemini-2.5-flash", #모델 오류 해결
            contents="hello"
        )
        return True
    except Exception:
        return False


# ---------------------------------------------------
# Test
# ---------------------------------------------------
if __name__ == "__main__":
    key = input("Gemini API Key를 입력하세요 :  >> ").strip()

    if api_check(key):
        print("API 키가 유효합니다.")
    else:
        print("유효하지 않은 API 키입니다.")
