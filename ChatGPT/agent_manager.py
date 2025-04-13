#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from conversation_manager import ConversationManager

class AgentManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.load_config()
        self.conversation_manager = None
    
    def load_config(self):
        """加载Agent配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                raise FileNotFoundError(f"配置文件不存在: {self.config_file}")
        except Exception as e:
            raise Exception(f"加载配置文件失败: {str(e)}")
    
    def get_agent(self, agent_name=None):
        """获取指定的Agent配置"""
        if not agent_name:
            agent_name = self.config.get('default_agent')
        
        for agent in self.config['agents']:
            if agent['name'] == agent_name:
                return agent
        
        return None
    
    def prepare_messages(self, agent, user_input):
        """准备发送给API的消息列表"""
        messages = []
        
        # 添加系统提示词
        messages.append({
            'role': 'system',
            'content': agent['system_prompt']
        })
        
        # 添加历史对话消息
        if self.conversation_manager:
            messages.extend(self.conversation_manager.get_conversation_messages())
        
        # 添加用户输入
        messages.append({
            'role': 'user',
            'content': user_input
        })
        
        return messages
    
    def start_conversation(self, agent_name=None, history_file=None):
        """开始新的对话"""
        agent = self.get_agent(agent_name)
        if not agent:
            raise ValueError(f"找不到指定的Agent: {agent_name}")
        
        if history_file:
            self.conversation_manager = ConversationManager(history_file)
            self.conversation_manager.start_new_conversation(agent['name'])
    
    def process_response(self, response_text):
        """处理API返回的响应"""
        if self.conversation_manager:
            self.conversation_manager.add_message('assistant', response_text)
        return response_text
    
    def end_conversation(self):
        """结束当前对话"""
        if self.conversation_manager:
            self.conversation_manager.save_conversation()
            self.conversation_manager.clear_current_conversation()
