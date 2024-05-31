import requests

# GitHub API 基础 URL
base_url = "https://api.github.com"

# 仓库所有者
owner = "Txhey"
# 仓库名称
repo = "note"
# 文件路径
file_path = "/disorder/git/Git.md"


# 每天更新仓库所有的笔记
# 1. 更新structure的notes项
# 2. 更新structure的tree项
def updateRepository:
    print("update notes")
    print("update tree")

updateRepository()

def test:
    # 获取文件的 commit 历史 URL
    commits_url = f"{base_url}/repos/{owner}/{repo}/commits?path={file_path}"

    # 获取文件的基本信息 URL
    file_info_url = f"{base_url}/repos/{owner}/{repo}/contents/{file_path}"

    print(commits_url)
    print(file_info_url)

    # 使用个人访问令牌进行身份验证（可选）
    headers = {'Authorization': 'token YOUR_PERSONAL_ACCESS_TOKEN'}

    # 发送 GET 请求获取文件的 commit 历史
    response = requests.get(commits_url, headers=headers)

    if response.status_code == 200:
        # 获取响应的 JSON 数据
        commits = response.json()

        if commits:
            # 获取第一个 commit（文件的创建时间）
            first_commit = commits[-1]
            creation_date = first_commit['commit']['committer']['date']

            # 获取最新的 commit（最近一次修改时间）
            latest_commit = commits[0]
            last_modified_date = latest_commit['commit']['committer']['date']
        else:
            creation_date = "N/A"
            last_modified_date = "N/A"
    else:
        print(f"Failed to retrieve commits: {response.status_code}")
        creation_date = "N/A"
        last_modified_date = "N/A"

    # 发送 GET 请求获取文件的基本信息
    response = requests.get(file_info_url, headers=headers)

    if response.status_code == 200:
        # 获取响应的 JSON 数据
        file_info = response.json()

        # 获取文件名
        file_name = file_info['name']
    else:
        print(f"Failed to retrieve file info: {response.status_code}")
        file_name = "N/A"

    print(f"File Name: {file_name}")
    print(f"Creation Date: {creation_date}")
    print(f"Last Modified Date: {last_modified_date}")
