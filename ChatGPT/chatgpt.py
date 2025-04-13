#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import os
import requests
from datetime import datetime
from agent_manager import AgentManager

# 配置文件路径
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')
AGENT_CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'agent_config.json')
HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'history.json')

def load_config():
    """加载配置文件"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'api_key': '', 'model': 'gpt-3.5-turbo'}
    except Exception as e:
        return {'api_key': '', 'model': 'gpt-3.5-turbo'}

def chat_with_agent(text):
    """与Agent进行对话"""
    config = load_config()
    
    if not config['api_key']:
        return json.dumps({
            "items": [{
                "title": "请先设置API Key",
                "subtitle": "在config.json中设置OpenAI API Key",
                "arg": "",
                "icon": {"path": "icon.svg"}
            }]
        }, ensure_ascii=False)
    
    if not text:
        return json.dumps({
            "items": [{
                "title": "请输入问题",
                "subtitle": "输入问题后AI助手会为您解答",
                "arg": "",
                "icon": {"path": "icon.svg"}
            }]
        }, ensure_ascii=False)
    
    try:
        # 初始化Agent管理器
        agent_manager = AgentManager(AGENT_CONFIG_FILE)
        
        # 开始新的对话
        agent_manager.start_conversation(history_file=HISTORY_FILE)
        
        # 获取当前Agent
        current_agent = agent_manager.get_agent()
        
        # 准备消息
        messages = agent_manager.prepare_messages(current_agent, text)
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {config["api_key"]}',
                'Content-Type': 'application/json'
            },
            json={
                'model': config['model'],
                'messages': messages,
                'temperature': current_agent.get('temperature', 0.7)
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content'].strip()
            
            # 处理响应
            agent_manager.process_response(answer)
            
            # 结束对话并保存历史
            agent_manager.end_conversation()
            
            return json.dumps({
                "items": [{
                    "title": answer,
                    "subtitle": f"当前Agent: {current_agent['name']} - 按Enter复制回答到剪贴板",
                    "arg": answer,
                    "icon": {"path": "icon.svg"}
                }]
            }, ensure_ascii=False)
        else:
            error_msg = f"API请求失败: {response.status_code}"
            return json.dumps({
                "items": [{
                    "title": error_msg,
                    "subtitle": "请检查API Key是否正确",
                    "arg": error_msg,
                    "icon": {"path": "icon.svg"}
                }]
            }, ensure_ascii=False)
            
    except requests.exceptions.Timeout:
        error_msg = "请求超时，请稍后重试"
        return json.dumps({
            "items": [{
                "title": error_msg,
                "subtitle": "网络连接超时",
                "arg": error_msg,
                "icon": {"path": "icon.svg"}
            }]
        }, ensure_ascii=False)
    except Exception as e:
        error_msg = f"发生错误: {str(e)}"
        return json.dumps({
            "items": [{
                "title": error_msg,
                "subtitle": "请检查网络连接和API配置",
                "arg": error_msg,
                "icon": {"path": "icon.svg"}
            }]
        }, ensure_ascii=False)

def main():
    # 获取输入文本
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    # 输出结果
    print(chat_with_agent(query))

if __name__ == "__main__":
    main()
