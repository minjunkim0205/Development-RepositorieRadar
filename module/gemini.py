# module/gemini.py

# ---------------------------------------------------
# Import module
# ---------------------------------------------------
from google import genai

# ---------------------------------------------------
# Function
# ---------------------------------------------------
def api_check(_key: str) -> bool:
    client = genai.Client(api_key=_key)
    try:
        client.models.generate_content(
            model="gemini-2.5-flash",
            contents="hello"
        )
        # print("where is response msg?")
        return True
    except Exception as e:
        # print(e)
        return False

# ---------------------------------------------------
# Test
# ---------------------------------------------------
if __name__ == "__main__":
    key = str(input("Your Gemini API Key >> "))
    if api_check(key):
        print("Success", end="")
    else:
        print("Error", end="")
