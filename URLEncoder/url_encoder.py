# -*- coding: utf-8 -*-
# url_encoder.py
# URL编码和解码工具
# 支持标准URL编码、组件编码和查询参数编码等

import sys
import json
import urllib.parse

def encode_url(text):
    """对输入文本进行URL编码"""
    # 如果没有输入，返回空字符串
    if not text:
        return ""
    return text

def format_output(text):
    """格式化输出为Alfred JSON格式"""
    # 如果没有输入，提示用户输入
    if not text:
        return json.dumps({
            "items": [
                {
                    "title": "请输入要编码或解码的文本",
                    "subtitle": "输入文本后将显示编码和解码结果",
                    "icon": {"type": "default", "path": "icon.png"}
                }
            ]
        }, ensure_ascii=False)
    
    # 标准URL编码
    standard_encode = urllib.parse.quote(text)
    # 完全URL编码（包括/等字符）
    full_encode = urllib.parse.quote_plus(text)
    # 组件编码
    component_encode = urllib.parse.quote(text, safe='')
    
    # 尝试解码（如果输入是已编码的文本）
    try:
        standard_decode = urllib.parse.unquote(text)
        # 只有当解码结果与原文本不同时才显示解码选项
        show_decode = standard_decode != text
    except:
        show_decode = False
        standard_decode = text
    
    items = [
        {
            "title": f"标准URL编码: {standard_encode}",
            "subtitle": "复制到剪贴板 (保留斜杠和部分特殊字符)",
            "arg": standard_encode,
            "icon": {"type": "default", "path": "icon.png"}
        },
        {
            "title": f"查询参数编码: {full_encode}",
            "subtitle": "复制到剪贴板 (将空格编码为+，适用于查询参数)",
            "arg": full_encode,
            "icon": {"type": "default", "path": "icon.png"}
        },
        {
            "title": f"完全URL编码: {component_encode}",
            "subtitle": "复制到剪贴板 (编码所有特殊字符)",
            "arg": component_encode,
            "icon": {"type": "default", "path": "icon.png"}
        }
    ]
    
    # 如果输入的是已编码的文本，添加解码选项
    if show_decode:
        items.append({
            "title": f"URL解码: {standard_decode}",
            "subtitle": "复制到剪贴板 (解码URL编码的文本)",
            "arg": standard_decode,
            "icon": {"type": "default", "path": "icon.png"}
        })
    
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
