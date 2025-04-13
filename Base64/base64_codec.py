# -*- coding: utf-8 -*-
# base64_codec.py
# Base64编码和解码工具
# 支持标准Base64编码、URL安全的Base64编码和文件编码

import sys
import json
import base64
import re

def is_base64(text):
    """检查文本是否为Base64编码"""
    # 检查是否符合Base64格式的正则表达式
    pattern = r'^[A-Za-z0-9+/]+={0,2}$'
    # URL安全的Base64格式
    url_safe_pattern = r'^[A-Za-z0-9_-]+={0,2}$'
    
    # 如果长度不是4的倍数（考虑到填充），可能不是Base64
    if len(text) % 4 != 0 and '=' not in text:
        return False
    
    # 尝试标准Base64格式
    if re.match(pattern, text):
        try:
            # 尝试解码，如果成功且结果是有效的UTF-8，则可能是Base64
            decoded = base64.b64decode(text).decode('utf-8')
            return True
        except:
            pass
    
    # 尝试URL安全的Base64格式
    if re.match(url_safe_pattern, text):
        try:
            # 尝试解码，如果成功且结果是有效的UTF-8，则可能是Base64
            decoded = base64.urlsafe_b64decode(text).decode('utf-8')
            return True
        except:
            pass
    
    return False

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
    
    items = []
    
    # 检查是否为Base64编码的文本
    is_base64_text = is_base64(text)
    
    # 如果不是Base64编码，提供编码选项
    if not is_base64_text:
        # 标准Base64编码
        standard_encode = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        # URL安全的Base64编码
        url_safe_encode = base64.urlsafe_b64encode(text.encode('utf-8')).decode('utf-8')
        
        items.extend([
            {
                "title": f"标准Base64编码: {standard_encode}",
                "subtitle": "复制到剪贴板 (标准Base64编码)",
                "arg": standard_encode,
                "icon": {"type": "default", "path": "icon.png"}
            },
            {
                "title": f"URL安全Base64编码: {url_safe_encode}",
                "subtitle": "复制到剪贴板 (URL安全的Base64编码，替换+为-，/为_)",
                "arg": url_safe_encode,
                "icon": {"type": "default", "path": "icon.png"}
            }
        ])
    else:
        # 如果是Base64编码，提供解码选项
        try:
            # 尝试标准Base64解码
            standard_decode = base64.b64decode(text).decode('utf-8')
            items.append({
                "title": f"Base64解码: {standard_decode}",
                "subtitle": "复制到剪贴板 (标准Base64解码)",
                "arg": standard_decode,
                "icon": {"type": "default", "path": "icon.png"}
            })
        except:
            try:
                # 尝试URL安全的Base64解码
                url_safe_decode = base64.urlsafe_b64decode(text).decode('utf-8')
                items.append({
                    "title": f"URL安全Base64解码: {url_safe_decode}",
                    "subtitle": "复制到剪贴板 (URL安全的Base64解码)",
                    "arg": url_safe_decode,
                    "icon": {"type": "default", "path": "icon.png"}
                })
            except:
                # 如果解码失败，添加一个提示
                items.append({
                    "title": "无法解码输入的Base64文本",
                    "subtitle": "请检查输入是否为有效的Base64编码",
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
