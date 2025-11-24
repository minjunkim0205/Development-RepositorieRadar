## IntroductionToOpenSourceSoftware-Final-Team09
2025년 2학기 오픈소스SW의이해[01] - 기말 프로젝트 9팀


# BugRadar – 나에게 맞는 오픈소스 이슈 레이더

**BugRadar**는 GitHub의 이슈들을 자동으로 수집·분석해서  
**“내 기술 스택과 난이도에 맞는 오픈소스 이슈”**를 추천해주는 도구입니다.

- 오픈소스에 기여하고 싶지만 어디서, 무엇부터 해야 할지 모를 때
- `good first issue`, `help wanted` 같은 이슈를 한 번에 모아서 보고 싶을 때
- Python 기반으로 쉽게 실행할 수 있는 웹 대시보드 형태의 툴이 필요할 때

---

## ✨ 주요 기능

- 🔍 **기술 스택 기반 이슈 필터링**
  - 사용자의 관심 언어/프레임워크(예: `python`, `django`, `react`, `docker`)를 입력하면 관련도가 높은 이슈를 우선적으로 보여줍니다.

- 🏷️ **태그 기반 추천**
  - `good first issue`, `beginner`, `help wanted` 등 라벨을 가진 이슈를 우선 추천

- 🧠 **키워드 매칭 및 점수화 (scikit-learn 활용)**
  - 이슈 제목/본문과 사용자의 관심 키워드를 TF-IDF 벡터화
  - 코사인 유사도 기반으로 **추천 점수(0~1)** 계산

- 📊 **Streamlit 대시보드 UI**
  - 필터값(언어, 키워드, 레이블 등) 조정 → 즉시 결과 업데이트
  - 이슈 제목 클릭 시 GitHub 이슈 페이지로 바로 이동

- ⚙️ **GitHub API 기반 실시간 데이터**
  - GitHub REST API를 통해 최신 이슈를 가져와 분석
  - 저장된 데이터 없이도 바로 사용 가능 (캐시 기능은 선택)

---

## 🧱 기술 스택

- **언어**
  - Python 3.10+

- **주요 라이브러리**
  - [Streamlit] – 웹 대시보드/UI
  - [scikit-learn] – TF-IDF 기반 키워드 매칭, 유사도 계산
  - `requests` – GitHub API 호출
  - `pydantic` (선택) – 설정/데이터 모델링

- **외부 서비스**
  - GitHub REST API (토큰 기반 인증)

---

## 📦 설치 및 실행 방법
테스트 메세지 추가