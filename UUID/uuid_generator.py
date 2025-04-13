# -*- coding: utf-8 -*-
# uuid.py
# 生成多种格式的UUID
# 支持标准格式、无连字符格式、大写格式等

import sys
import json
import uuid as uuid_lib

def generate_uuid():
    """生成一个新的UUID"""
    return uuid_lib.uuid4()

def format_output(uuid_obj):
    """格式化输出为Alfred JSON格式"""
    # 标准格式
    standard_format = str(uuid_obj)
    # 无连字符格式
    no_hyphen_format = standard_format.replace('-', '')
    # 大写格式
    uppercase_format = standard_format.upper()
    # 大写无连字符格式
    uppercase_no_hyphen_format = no_hyphen_format.upper()
    # URN格式
    urn_format = f"urn:uuid:{standard_format}"
    
    items = [
        {
            "title": f"标准格式: {standard_format}",
            "subtitle": "复制到剪贴板 (8-4-4-4-12格式)",
            "arg": standard_format,
            "icon": {"type": "default", "path": "icon.png"}
        },
        {
            "title": f"无连字符: {no_hyphen_format}",
            "subtitle": "复制到剪贴板 (32个字符)",
            "arg": no_hyphen_format,
            "icon": {"type": "default", "path": "icon.png"}
        },
        {
            "title": f"大写格式: {uppercase_format}",
            "subtitle": "复制到剪贴板 (大写8-4-4-4-12格式)",
            "arg": uppercase_format,
            "icon": {"type": "default", "path": "icon.png"}
        },
        {
            "title": f"大写无连字符: {uppercase_no_hyphen_format}",
            "subtitle": "复制到剪贴板 (大写32个字符)",
            "arg": uppercase_no_hyphen_format,
            "icon": {"type": "default", "path": "icon.png"}
        },
        {
            "title": f"URN格式: {urn_format}",
            "subtitle": "复制到剪贴板 (URN格式)",
            "arg": urn_format,
            "icon": {"type": "default", "path": "icon.png"}
        }
    ]
    
    return json.dumps({"items": items}, ensure_ascii=False)

def main():
    # 无论是否有输入参数，都生成一个新的UUID
    uuid_obj = generate_uuid()
    print(format_output(uuid_obj))

if __name__ == "__main__":
    main()