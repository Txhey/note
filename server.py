import requests
import os
import glob
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


def get_file_patten(file_path):
    # 使用通配符查找文件夹中名为 cover 的文件
    matching_files = glob.glob(file_path)

    # 如果找到匹配的文件，返回第一个文件的名称
    if matching_files:
        return os.path.basename(matching_files[0])
    else:
        return None


def update_structure_json():
    file_info_list = []
    all_tag_set = set()
    for s in os.listdir('.\\main'):
        if s.startswith('.'):
            continue
        folder_path = os.path.join(".\\main", s)
        md_file_path = os.path.join(folder_path, "*.md")
        md_file_name = get_file_patten(md_file_path)
        print(md_file_path)
        md_file_path = os.path.join(folder_path, md_file_name)
        info_file_path = os.path.join(folder_path, 'info.json')
        cover_file_path = os.path.join(folder_path, 'img\\cover.*')
        # 获取title

        # 获取文件创建时间和最后修改时间
        create_time = os.path.getctime(md_file_path)
        last_modify = os.path.getmtime(md_file_path)
        create_time_str = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')
        last_modify_str = datetime.fromtimestamp(last_modify).strftime('%Y-%m-%d %H:%M:%S')
        # 获取文件的摘要
        title, abstract = get_title_and_extract_from_md(md_file_path)
        # 获取info(tag_list)
        tag_list = get_tag_info(info_file_path)
        # 获取cover图片名字
        img_cover_name = get_file_patten(cover_file_path)
        all_tag_set.update(tag_list)
        file_info = {
            "folderName": s,
            "fileName": md_file_name,
            "title": title,
            "abstract": abstract,
            "tagList": tag_list,
            "createTime": create_time_str,
            "lastModify": last_modify_str,
            "img": f"https://raw.githubusercontent.com/Txhey/note/main/main/{s}/img/{img_cover_name}",
            "view": 0  # 默认浏览量为0
        }
        file_info_list.append(file_info)
    json_data = {
        "main": file_info_list,
        "noteNum": len(file_info_list),
        "allTagList": list(all_tag_set)
    }
    print(json_data)
    # 将 JSON 数据写入文件
    with open("structure.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)


# 获取文件摘要（去除标题符号、代码块、表格、空白符）
def get_title_and_extract_from_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        # 获取title
        title = "title not found"
        for line in f:
            # 使用正则表达式匹配以#开头的行，并捕获标题内容
            match = re.match(r'^\s*#\s*(.+)', line)
            if match:
                title = match.group(1)
                break
        print(title)
        # 读取 Markdown 文件内容
        html = f.read()
        # 去掉列表
        html = re.sub(r'\* (.*?)[\r\n]', r' \1 ', html)
        # 标题去除#
        html = re.sub(r'#* (.*?)[\r\n]', r"\1", html)
        # 去除表格
        html = re.sub(r'\|.*?\|.*?\n', "", html)
        # 去除代码块
        html = re.sub(r'```.*?```|~~~.*?~~~', "", html, flags=re.DOTALL)
        # 去掉图片
        html = re.sub(r'!\[.*?\]\(.*?\)', " ", html, flags=re.DOTALL)
        # 去除换行、空行、制表符
        html = re.sub(r'\s+', " ", html)
        return title, html.strip()[:200]


# 获取tagInfo
def get_tag_info(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write('{"tagList": []}')
            return []
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            tags_list = json_data["tagList"]
            return tags_list


# 每天更新仓库所有的笔记
# 1. 更新structure的notes项
# 2. 更新structure的tree项
def updateRepository():
    print("update structure json file")
    update_structure_json()


updateRepository()
