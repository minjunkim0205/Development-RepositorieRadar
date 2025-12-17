# module/github.py

# ---------------------------------------------------
# Import module
# ---------------------------------------------------
import os
import requests
from urllib.parse import urlparse
import base64

# ---------------------------------------------------
# GitHub API 공통 설정 / 유틸
# ---------------------------------------------------
GITHUB_API_BASE = "https://api.github.com"


def parse_github_repo_url(_url: str):
    """
    GitHub 저장소 URL을 파싱해서 (owner, repo)를 반환.
    유효하지 않으면 (None, None) 반환.
    """
    parsed = urlparse(_url)
    paths = parsed.path.strip("/").split("/")

    if parsed.scheme != "https":
        return None, None
    if parsed.netloc != "github.com":
        return None, None
    if len(paths) < 2:
        return None, None

    owner, repo = paths[0], paths[1]
    if not owner or not repo:
        return None, None

    return owner, repo


def url_check(_url: str) -> bool:
    """
    GitHub 저장소 URL 유효성 검사
    """
    owner, repo = parse_github_repo_url(_url)
    return bool(owner and repo)


def github_api_get(endpoint: str, params: dict | None = None) -> requests.Response | None:
    """
    GitHub API GET 공통 함수.
    - endpoint: "/repos/{owner}/{repo}/branches" 같은 경로
    - params: querystring 파라미터
    - 필요 시 GITHUB_TOKEN 환경변수로 인증 헤더 추가
    """
    url = GITHUB_API_BASE + endpoint

    headers = {
        "Accept": "application/vnd.github+json",
    }

    # Optional: 토큰 있으면 rate limit 완화 / private repo 접근용
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    return response


# ---------------------------------------------------
# Public Function
# ---------------------------------------------------
def url_branch_list(_url: str) -> list:
    """
    GitHub 저장소 브랜치 목록 반환
    """
    if not url_check(_url):
        return []

    owner, repo = parse_github_repo_url(_url)
    endpoint = f"/repos/{owner}/{repo}/branches"

    response = github_api_get(endpoint)
    if response is None:
        return []

    branches = response.json()
    return [branch["name"] for branch in branches]


def url_readme_string(_url: str) -> str | None:
    """
    GitHub 저장소의 README 내용을 문자열로 반환
    """
    if not url_check(_url):
        return None

    owner, repo = parse_github_repo_url(_url)
    endpoint = f"/repos/{owner}/{repo}/readme"

    response = github_api_get(endpoint)
    if response is None:
        return None

    data = response.json()
    if "content" not in data:
        return None

    readme_bytes = base64.b64decode(data["content"])
    return readme_bytes.decode("utf-8", errors="ignore")


def url_tree_list(_url: str) -> list | None:
    """
    GitHub 저장소의 전체 트리(raw tree list)를 반환
    (main → master 순으로 브랜치 탐색)
    """
    if not url_check(_url):
        return None

    owner, repo = parse_github_repo_url(_url)

    branches_to_try = ["main", "master"]
    commit_sha = None

    # 브랜치 정보에서 커밋 SHA 가져오기
    for branch in branches_to_try:
        endpoint = f"/repos/{owner}/{repo}/branches/{branch}"
        response = github_api_get(endpoint)
        if response is not None:
            commit_sha = str(response.json()["commit"]["sha"])
            break

    if not commit_sha:
        return None

    # 트리 구조 가져오기 (recursive=1)
    endpoint = f"/repos/{owner}/{repo}/git/trees/{commit_sha}"
    response = github_api_get(endpoint, params={"recursive": "1"})
    if response is None:
        return None

    return response.json().get("tree", [])


def url_tree_dict(_url: str) -> dict | None:
    """
    트리 리스트를 계층적인 dict 구조로 변환
    """
    file_list = url_tree_list(_url)
    if file_list is None:
        return None

    tree_dict: dict = {}

    for item in file_list:
        parts = item["path"].split("/")
        node = tree_dict
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        if item["type"] == "tree":
            node.setdefault(parts[-1], {})
        else:
            node[parts[-1]] = None

    return tree_dict


def url_tree_string(_url: str) -> str | None:
    """
    dict 기반 트리를 사람이 읽기 쉬운 문자열 트리로 변환
    """
    tree_dict = url_tree_dict(_url)
    if tree_dict is None:
        return None

    tree_string = ""
    stack = [(tree_dict, None, [])]

    while stack:
        node, name, depth_info = stack.pop()

        if name is not None:
            indent = ""
            for is_last in depth_info[:-1]:
                indent += "    " if is_last else "│   "
            is_last = depth_info[-1]
            branch = "└── " if is_last else "├── "
            if isinstance(node, dict):
                tree_string += indent + branch + name + "/\n"
            else:
                tree_string += indent + branch + name + "\n"

        if isinstance(node, dict):
            folders = sorted([k for k, v in node.items() if isinstance(v, dict)])
            files = sorted([k for k, v in node.items() if v is None])
            keys = folders + files

            for i in range(len(keys) - 1, -1, -1):
                key = keys[i]
                is_last_child = (i == len(keys) - 1)
                stack.append((node[key], key, depth_info + [is_last_child]))

    return "Root\n" + tree_string


# ---------------------------------------------------
# Test
# ---------------------------------------------------
if __name__ == "__main__":
    url = "https://github.com/minjunkim0205/Development-RepositorieRadar"
    print("Valid URL? :", url_check(url))
    print("Branches   :", url_branch_list(url))
    print("Tree:\n", url_tree_string(url))
