# -*- coding: utf-8 -*-
# md5_hash.py
# MD5哈希计算工具
# 支持计算文本MD5和文件MD5

import sys
import json
import hashlib
import os.path

def calculate_md5(input_text):
    """计算输入文本或文件的MD5哈希值"""
    # 如果没有输入，返回空字符串
    if not input_text:
        return ""
    
    # 检查输入是否为文件路径
    if os.path.isfile(input_text):
        # 计算文件MD5
        return calculate_file_md5(input_text)
    else:
        # 计算文本MD5
        return calculate_text_md5(input_text)

def calculate_text_md5(text):
    """计算文本的MD5哈希值"""
    md5_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
    return md5_hash

def calculate_file_md5(file_path):
    """计算文件的MD5哈希值"""
    md5_hash = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            # 分块读取文件以处理大文件
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
    except Exception as e:
        return f"错误: {str(e)}"

def format_output(input_text):
    """格式化输出为Alfred JSON格式"""
    # 如果没有输入，提示用户输入
    if not input_text:
        return json.dumps({
            "items": [
                {
                    "title": "请输入要计算MD5的文本或文件路径",
                    "subtitle": "输入文本或拖拽文件到Alfred输入框",
                    "icon": {"type": "default", "path": "icon.svg"}
                }
            ]
        }, ensure_ascii=False)
    
    # 检查输入是否为文件路径
    is_file = os.path.isfile(input_text)
    
    # 计算MD5
    md5_result = calculate_md5(input_text)
    
    # 准备输出项
    if is_file:
        title = f"文件MD5: {md5_result}"
        subtitle = f"文件: {input_text}"
    else:
        title = f"文本MD5: {md5_result}"
        subtitle = f"文本: {input_text}"
    
    items = [
        {
            "title": title,
            "subtitle": subtitle,
            "arg": md5_result,
            "icon": {"type": "default", "path": "icon.svg"}
        },
        {
            "title": "复制MD5值到剪贴板",
            "subtitle": md5_result,
            "arg": md5_result,
            "icon": {"type": "default", "path": "icon.svg"}
        }
    ]
    
    return json.dumps({"items": items}, ensure_ascii=False)

def main():
    # 获取输入参数
    query = ""
    if len(sys.argv) > 1:
        query = sys.argv[1]
    
    # 输出结果
    print(format_output(query))

if __name__ == "__main__":
    main()
