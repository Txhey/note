import requests
import os
import json
import re
from datetime import datetime
import markdown
from bs4 import BeautifulSoup

# GitHub API 基础 URL
base_url = "https://api.github.com"
# 仓库所有者
owner = "Txhey"
# 仓库名称
repo = "note"


# 每天更新仓库所有的笔记
# 1. 更新structure的notes项
# 2. 更新structure的tree项
def updateRepository():
    print("update structure json file")
    update_structure_json()


def update_structure_json():
    file_info_list = []
    for s in os.listdir('.\\main'):
        folder_path = os.path.join(".\\main", s)
        md_file_path = os.path.join(folder_path, s + ".md")
        tag_file_path = os.path.join(folder_path, 'tag')
        # 获取title
        title = s
        # 获取文件创建时间和最后修改时间
        create_time = os.path.getctime(md_file_path)
        last_modify = os.path.getmtime(md_file_path)
        create_time_str = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')
        last_modify_str = datetime.fromtimestamp(last_modify).strftime('%Y-%m-%d %H:%M:%S')
        # 获取文件的摘要
        abstract = extract_text_from_md(md_file_path)
        # 获取tagList
        tag_list = get_tag_list(tag_file_path)
        file_info = {
            "title": title,
            "abstract": abstract,
            "tagList": tag_list,
            "createTime": create_time_str,
            "lastModify": last_modify_str,
            "view": 0  # 默认浏览量为0
        }
        file_info_list.append(file_info)
    json_data = {
        "main": file_info_list,
    }
    print(json_data)
    # 将 JSON 数据写入文件
    with open("structure.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)


# 获取文件摘要（去除标题符号、代码块、表格、空白符）
def extract_text_from_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        # 读取 Markdown 文件内容
        html = f.read()
        # 标题去除#
        html = re.sub(r'#* (.*?)[\r\n]', r"\1", html)
        # 去除表格
        html = re.sub(r'\|.*?\|.*?\n', "", html)
        # 去除代码块
        html = re.sub(r'```.*?```|~~~.*?~~~', "", html, flags=re.DOTALL)
        # 去除换行、空行、制表符
        html = re.sub(r'\s+', " ", html)

        return html.strip()[:200]


# 获取tagList
def get_tag_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        re.sub(r'\s*?,\s*?',",",content)
        return content.split(',')
