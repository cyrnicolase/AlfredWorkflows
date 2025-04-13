# -*- coding: utf-8 -*-
# time_switcher.py
# 根据时间切换不同的时间格式
# 当输入的内容为纯数字的时候,就将其作为unix时间戳使用，并且转换为年月日时分秒格式
# 当输入的内容为年月日时分秒格式的时候,就将其转换为unix时间戳格式
# 这里使用的是python3 的语法来实现该功能

import sys
import re
import json
from datetime import datetime

def is_timestamp(input_str):
    """判断输入是否为时间戳格式"""
    return input_str.isdigit()

def is_datetime_format(input_str):
    """判断输入是否为日期时间格式"""
    # 支持多种常见的日期时间格式
    patterns = [
        r'\d{4}[-/]\d{1,2}[-/]\d{1,2}( \d{1,2}:\d{1,2}(:\d{1,2})?)?',  # YYYY-MM-DD HH:MM:SS 或 YYYY/MM/DD HH:MM:SS
        r'\d{1,2}[-/]\d{1,2}[-/]\d{4}( \d{1,2}:\d{1,2}(:\d{1,2})?)?',  # DD-MM-YYYY HH:MM:SS 或 MM/DD/YYYY HH:MM:SS
    ]
    
    for pattern in patterns:
        if re.match(pattern, input_str):
            return True
    return False

def parse_datetime(input_str):
    """解析日期时间字符串为datetime对象"""
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d',
        '%Y/%m/%d %H:%M:%S',
        '%Y/%m/%d %H:%M',
        '%Y/%m/%d',
        '%d-%m-%Y %H:%M:%S',
        '%d-%m-%Y %H:%M',
        '%d-%m-%Y',
        '%m/%d/%Y %H:%M:%S',
        '%m/%d/%Y %H:%M',
        '%m/%d/%Y'
    ]
    
    for fmt in formats:
        try:
            # 使用strptime解析日期时间字符串
            dt = datetime.strptime(input_str, fmt)
            return dt
        except ValueError:
            continue
    
    raise ValueError(f"无法解析日期时间格式: {input_str}")

def timestamp_to_datetime(timestamp):
    """将时间戳转换为日期时间"""
    # 如果时间戳长度超过10位，认为是毫秒级时间戳
    if len(timestamp) > 10:
        timestamp = int(timestamp) / 1000
    else:
        timestamp = int(timestamp)
    
    return datetime.fromtimestamp(timestamp)

def datetime_to_timestamp(dt):
    """将日期时间转换为时间戳"""
    return int(dt.timestamp())

def format_output(timestamp_sec, dt):
    """格式化输出为Alfred JSON格式"""
    timestamp_ms = timestamp_sec * 1000
    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
    
    items = [
        {
            "title": f"Unix时间戳(秒): {timestamp_sec}",
            "subtitle": "复制到剪贴板",
            "arg": str(timestamp_sec),
            "icon": {"type": "default", "path": "icon.png"}
        },
        {
            "title": f"Unix时间戳(毫秒): {timestamp_ms}",
            "subtitle": "复制到剪贴板",
            "arg": str(timestamp_ms),
            "icon": {"type": "default", "path": "icon.png"}
        },
        {
            "title": f"格式化时间: {formatted_time}",
            "subtitle": "复制到剪贴板",
            "arg": formatted_time,
            "icon": {"type": "default", "path": "icon.png"}
        }
    ]
    
    return json.dumps({"items": items}, ensure_ascii=False)

def main():
    # 获取输入参数
    if len(sys.argv) > 1:
        input_str = ' '.join(sys.argv[1:]).strip()  # 合并所有参数，处理带空格的输入
    else:
        # 如果没有参数，使用当前时间
        dt = datetime.now()
        timestamp_sec = int(dt.timestamp())
        print(format_output(timestamp_sec, dt))
        return
    
    try:
        if is_timestamp(input_str):
            # 输入是时间戳
            dt = timestamp_to_datetime(input_str)
            timestamp_sec = int(dt.timestamp())
        elif is_datetime_format(input_str):
            # 输入是日期时间格式
            dt = parse_datetime(input_str)
            timestamp_sec = datetime_to_timestamp(dt)
        else:
            # 无法识别的格式，使用当前时间
            dt = datetime.now()
            timestamp_sec = int(dt.timestamp())
        
        print(format_output(timestamp_sec, dt))
    except Exception as e:
        # 发生错误时，输出错误信息
        error_output = json.dumps({
            "items": [{
                "title": f"错误: {str(e)}",
                "subtitle": "请检查输入格式",
                "arg": "",
                "icon": {"type": "default", "path": "icon.png"}
            }]
        }, ensure_ascii=False)
        print(error_output)

if __name__ == "__main__":
    main()
