from typing import List, Optional, Tuple
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentFormatter:
    """
    文档格式化器，负责处理文档的预处理和后处理
    """
    
    @staticmethod
    def preprocess_text(text: str) -> str:
        """
        预处理文本，清理和标准化可能影响翻译的格式问题
        """
        # 移除多余的空白字符
        text = re.sub(r'[ \t]+', ' ', text)
        
        # 标准化换行符
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'\r', '\n', text)
        
        # 移除行首行尾的多余空格
        lines = text.split('\n')
        cleaned_lines = [line.strip() for line in lines]
        text = '\n'.join(cleaned_lines)
        
        # 修复分段的单词（行尾有连字符的情况）
        text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2\n', text)
        
        return text

    @staticmethod
    def postprocess_translation(text: str) -> str:
        """
        后处理翻译结果，优化格式
        """
        # 清理多余的空格
        text = re.sub(r'[ \t]+', ' ', text)
        
        # 确保标题前后有空行并移除标题中的格式
        text = DocumentFormatter._normalize_headers(text)
        
        # 修复可能的段落分隔问题
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # 确保文档开头和结尾没有多余的空行
        text = text.strip()
        
        return text

    @staticmethod
    def _normalize_headers(text: str) -> str:
        """
        标准化标题格式：
        1. 确保标题前后有空行
        2. 移除标题中的加粗、斜体等格式
        """
        # 匹配标题行（以1-6个#开头的行）
        def clean_header(match):
            header_prefix = match.group(1)  # #, ##, ### 等
            header_content = match.group(2)  # 标题内容
            
            # 移除标题内的格式标记（如 **bold** 或 *italic*）
            # 移除加粗格式 **text**
            header_content = re.sub(r'\*\*(.*?)\*\*', r'\1', header_content)
            # 移除斜体格式 *text* 或 _text_
            header_content = re.sub(r'(?<!\*)\*(?!\*)(.*?) (?<!\*)\*(?!\*)', r'\1', header_content)
            header_content = re.sub(r'(?<!_)_(?!_)(.*?) (?<!_)_(?!_)', r'\1', header_content)
            # 移除行内代码格式 `code`
            header_content = re.sub(r'`(.*?)`', r'\1', header_content)
            
            # 确保标题前后有空行
            return f"\n\n{header_prefix} {header_content.strip()}\n\n"
        
        # 应用标题清理函数
        text = re.sub(r'\n?(#{1,6})\s+(.+?)\n', clean_header, text)
        
        # 确保文档开头是标题时也正确处理
        text = re.sub(r'^(#{1,6})\s+(.+?)\n', clean_header, text)
        
        # 清理重复的空行
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()