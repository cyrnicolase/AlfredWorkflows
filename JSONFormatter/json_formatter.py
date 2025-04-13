#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

def format_json(text, indent=4):
    """格式化JSON文本"""
    try:
        # 尝试解析JSON文本
        if isinstance(text, str):
            # 如果输入是字符串，先解析成Python对象
            data = json.loads(text)
        else:
            data = text
        
        # 返回不同格式的JSON
        formats = {
            'pretty': json.dumps(data, indent=indent, ensure_ascii=False),
            'compact': json.dumps(data, separators=(',', ':'), ensure_ascii=False),
            'sorted': json.dumps(data, indent=indent, sort_keys=True, ensure_ascii=False)
        }
        return formats
    except json.JSONDecodeError:
        return None

def format_output(text):
    """格式化输出为Alfred JSON格式"""
    # 如果没有输入，提示用户输入
    if not text:
        return json.dumps({
            "items": [
                {
                    "title": "请输入要格式化的JSON文本",
                    "subtitle": "输入JSON文本后将显示不同的格式化选项",
                    "icon": {"type": "default", "path": "icon.svg"}
                }
            ]
        }, ensure_ascii=False)
    
    # 尝试格式化JSON
    formats = format_json(text)
    if formats is None:
        return json.dumps({
            "items": [
                {
                    "title": "无效的JSON格式",
                    "subtitle": "请检查输入的JSON文本是否正确",
                    "icon": {"type": "default", "path": "icon.svg"}
                }
            ]
        }, ensure_ascii=False)
    
    items = [
        {
            "title": "美化格式",
            "subtitle": "复制到剪贴板 (带缩进和换行)",
            "arg": formats['pretty'],
            "icon": {"type": "default", "path": "icon.svg"}
        },
        {
            "title": "紧凑格式",
            "subtitle": "复制到剪贴板 (无空格和换行)",
            "arg": formats['compact'],
            "icon": {"type": "default", "path": "icon.svg"}
        },
        {
            "title": "排序格式",
            "subtitle": "复制到剪贴板 (按键排序)",
            "arg": formats['sorted'],
            "icon": {"type": "default", "path": "icon.svg"}
        }
    ]
    
    return json.dumps({"items": items}, ensure_ascii=False)

def main():
    # 获取输入文本
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    # 输出结果
    print(format_output(query))

if __name__ == "__main__":
    main()
