# module/gpt.py

# ---------------------------------------------------
# Import module
# ---------------------------------------------------
from openai import OpenAI

# ---------------------------------------------------
# Function
# ---------------------------------------------------
def api_check(_key:str) -> bool:
    client = OpenAI(api_key=_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    # 반드시 영어로 대답 해야합니다.
                    "content": (
                        "You must answer in English."
                    )
                },
                {
                    "role": "user", 
                    # 핑
                    "content": (
                        "ping"
                    )
                }
            ]
        )
        # print(response.choices[0].message.content)
        return True
    except Exception as e:
        # print(e)
        return False

def api_repository_structure(_key:str, _file_tree:dict, _language:str="Korean") -> str:
    client = OpenAI(api_key=_key)
    parsed_file_tree = str(_file_tree)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    # 당신은 코드 분석을 도와주는 전문 어시스트 입니다.
                    # 반드시 {_language}로 대답 해야합니다.
                    "content": (
                        "You are an assistant who specializes in analyzing code."
                        "You must answer in "+_language+"."
                    )
                },
                {
                    "role": "user", 
                    # 저장소의 진입점, 사용 언어, ​​각 디렉토리에 대한 자세한 설명, 
                    # 파일이 잘 구성되어 있는지 여부를 정리해주세요.
                    "content": (
                        "Analyze this dictionary-type file tree."
                        "Please organize the repository's entry point, "
                        "language used, detailed description of each directory, "
                        "and whether the files are well organized."
                        ""+parsed_file_tree+""
                    )
                }
            ]
        )
        return str(response.choices[0].message.content)
    except Exception as e:
        return str(e)

# ---------------------------------------------------
# Test
# ---------------------------------------------------
if __name__=="__main__":
    key = str(input("Your GPT API key >> "))
    if api_check(key):
        print("Success", end="")
    else:
        print("Error", end="")
