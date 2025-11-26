# module/github.py

# ---------------------------------------------------
# Import module
# ---------------------------------------------------
import requests
from urllib.parse import urlparse

# ---------------------------------------------------
# Function
# ---------------------------------------------------
def url_branch_list(_url:str) -> list:
    pass

def url_check(_url:str) -> bool:
    parsed = urlparse(_url)
    paths = parsed.path.strip("/").split("/")
    if parsed.scheme not in ("https"):
        return False
    if parsed.netloc != "github.com":
        return False
    if len(paths) < 2:
        return False
    owner = paths[0]
    repo = paths[1]
    if not owner or not repo:
        return False
    return True

def url_tree_list(_url:str) -> list:
    tree_list = []
    parsed_url = urlparse(_url)

    paths = parsed_url.path.strip('/').split('/')
    owner, repo = str(paths[0]), str(paths[1])

    branches_to_try = ["main", "master"]
    commit_sha = None
    for branch in branches_to_try:
        branch_url = "https://api.github.com/repos/"+owner+"/"+repo+"/branches/"+branch
        response = requests.get(branch_url)
        if response.status_code == 200:
            commit_sha = str(response.json()["commit"]["sha"])
            break
    
    if not commit_sha:
        return None
    
    tree_url = "https://api.github.com/repos/"+owner+"/"+repo+"/git/trees/"+commit_sha+"?recursive=1"
    tree_response = requests.get(tree_url)

    if tree_response.status_code != 200:
        return None
    tree_list = tree_response.json()['tree']
    return tree_list

def url_tree_dict(_url:str) -> dict:
    tree_dict = {}
    file_list = url_tree_list(_url)

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

def url_tree_string(_url:str) -> str:
    tree_string = ""
    tree_dict = url_tree_dict(_url)

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

            for i in range(len(keys)-1, -1, -1):
                key = keys[i]
                is_last_child = (i == len(keys)-1)
                stack.append((node[key], key, depth_info + [is_last_child]))
    tree_string = "Root\n"+tree_string
    return tree_string

# ---------------------------------------------------
# Test
# ---------------------------------------------------
if __name__=="__main__":
    url = "https://github.com/minjunkim0205/Development-RepositorieRadar"
    tree = str(url_tree_dict(url))
    print(tree, end="")
