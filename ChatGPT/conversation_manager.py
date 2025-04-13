#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime

class ConversationManager:
    def __init__(self, history_file):
        self.history_file = history_file
        self.current_conversation = []
        self.load_history()
    
    def load_history(self):
        """加载历史对话记录"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            else:
                self.history = []
        except Exception:
            self.history = []
    
    def start_new_conversation(self, agent_name):
        """开始新的对话"""
        self.current_conversation = []
        self.current_agent = agent_name
        self.conversation_start_time = datetime.now()
    
    def add_message(self, role, content):
        """添加新的对话消息"""
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.current_conversation.append(message)
    
    def get_conversation_messages(self):
        """获取当前对话的所有消息"""
        return [{'role': msg['role'], 'content': msg['content']} 
                for msg in self.current_conversation]
    
    def save_conversation(self):
        """保存当前对话到历史记录"""
        if not self.current_conversation:
            return
        
        conversation_record = {
            'agent': self.current_agent,
            'start_time': self.conversation_start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'messages': self.current_conversation
        }
        
        self.history.append(conversation_record)
        
        # 只保留最近100条对话记录
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存对话历史失败: {str(e)}")
    
    def clear_current_conversation(self):
        """清空当前对话"""
        self.current_conversation = []
