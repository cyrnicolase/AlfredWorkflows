#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import urllib.parse
import urllib.request
import time
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

class IcibaAPI:
    """金山词霸API封装类"""
    
    BASE_URL = "https://dict.iciba.com/dictionary/word/suggestion"
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Referer': 'https://www.iciba.com/'
        }
    
    def _build_url(self, query):
        """构建API请求URL"""
        encoded_query = urllib.parse.quote(query)
        timestamp = int(time.time() * 1000)
        params = {
            'word': encoded_query,
            'nums': '5',
            'ck': '709a0db45332167b0e2ce1868b84773e',
            'timestamp': str(timestamp),
            'client': '6',
            'uid': '123123',
            'key': '1000006',
            'is_need_mean': '1',
            'signature': '14525899822c291c193c1a39ea893280'
        }
        query_string = urllib.parse.urlencode(params)
        return f"{self.BASE_URL}?{query_string}"
    
    def _make_request(self, url):
        """发送HTTP请求并获取响应"""
        try:
            request = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(request) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            logger.error(f"API请求失败: {e}")
            return None

class TranslationParser:
    """翻译结果解析器"""
    
    @staticmethod
    def parse_meanings(word_info):
        """解析单词释义"""
        meanings = []
        
        # 添加基本释义
        if word_info.get('paraphrase'):
            meanings.append({
                'part_of_speech': '',
                'definition': word_info['paraphrase']
            })
        
        # 添加详细释义
        if isinstance(word_info.get('means'), list):
            for mean in word_info['means']:
                part = mean.get('part', '')
                for definition in mean.get('means', []):
                    if definition:  # 确保定义不为空
                        meanings.append({
                            'part_of_speech': part,
                            'definition': definition
                        })
        
        return meanings

class TranslationService:
    """翻译服务类"""
    
    def __init__(self):
        self.api = IcibaAPI()
        self.parser = TranslationParser()
    
    def translate(self, query):
        """执行翻译"""
        if not query:
            return None
        
        # 构建并发送请求
        url = self.api._build_url(query)
        logger.info(f"查询URL: {url}")
        response = self.api._make_request(url)
        
        if not response:
            return None
        
        # 解析响应数据
        meanings = []
        examples = []
        
        if isinstance(response.get('message'), list):
            for word_info in response['message']:
                logger.info(f"处理单词: {word_info.get('key')}")
                meanings.extend(self.parser.parse_meanings(word_info))
                break  # 只处理第一个匹配结果
        
        return {
            'query': query,
            'meanings': meanings,
            'examples': examples
        }

class AlfredFormatter:
    """Alfred输出格式化器"""
    
    @staticmethod
    def format_empty_query():
        """格式化空查询提示"""
        return json.dumps({
            "items": [{
                "title": "请输入要翻译的文本",
                "subtitle": "输入中文或英文进行翻译",
                "icon": {"type": "default", "path": "icon.svg"}
            }]
        }, ensure_ascii=False)
    
    @staticmethod
    def format_no_result(query):
        """格式化无结果提示"""
        return json.dumps({
            "items": [{
                "title": "未找到翻译结果",
                "subtitle": f"无法获取 '{query}' 的翻译",
                "icon": {"type": "default", "path": "icon.svg"}
            }]
        }, ensure_ascii=False)
    
    @staticmethod
    def format_translation_result(result):
        """格式化翻译结果"""
        items = []
        
        # 添加词义条目
        for meaning in result['meanings']:
            pos = meaning['part_of_speech']
            definition = meaning['definition']
            items.append({
                "title": f"{pos} {definition}",
                "subtitle": "复制到剪贴板",
                "arg": definition,
                "icon": {"type": "default", "path": "icon.svg"}
            })
        
        # 添加例句条目
        for example in result.get('examples', []):
            items.append({
                "title": example['english'],
                "subtitle": example['chinese'],
                "arg": example['english'],
                "icon": {"type": "default", "path": "icon.svg"}
            })
        
        # 添加原始查询词条目
        items.append({
            "title": f"原始查询: {result['query']}",
            "subtitle": "复制到剪贴板",
            "arg": result['query'],
            "icon": {"type": "default", "path": "icon.svg"}
        })
        
        return json.dumps({"items": items}, ensure_ascii=False)

def main():
    # 获取输入参数
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    
    # 初始化服务
    translator = TranslationService()
    formatter = AlfredFormatter()
    
    # 处理空查询
    if not query:
        print(formatter.format_empty_query())
        return
    
    # 获取并格式化翻译结果
    result = translator.translate(query)
    if not result or not result.get('meanings'):
        print(formatter.format_no_result(query))
    else:
        print(formatter.format_translation_result(result))

if __name__ == "__main__":
    main()
