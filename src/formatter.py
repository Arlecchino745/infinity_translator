from typing import List, Optional, Tuple
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentFormatter:
    """
    Document formatter, responsible for preprocessing and postprocessing documents
    """
    
    @staticmethod
    def extract_code_blocks(text: str) -> Tuple[str, List[str]]:
        """提取代码块和行内代码，避免误处理"""
        code_blocks = []
        placeholder_text = text
        
        # 提取代码块和行内代码
        code_pattern = r'```[\s\S]*?```|`[^`\n]*`'
        for i, match in enumerate(re.finditer(code_pattern, text)):
            placeholder = f"__CODE_BLOCK_{i}__"
            code_blocks.append(match.group())
            placeholder_text = placeholder_text.replace(match.group(), placeholder, 1)
        
        return placeholder_text, code_blocks
    
    @staticmethod
    def restore_code_blocks(text: str, code_blocks: List[str]) -> str:
        """恢复代码块"""
        for i, code_block in enumerate(code_blocks):
            placeholder = f"__CODE_BLOCK_{i}__"
            text = text.replace(placeholder, code_block)
        return text
    
    @staticmethod
    def extract_links_and_images(text: str) -> Tuple[str, List[str]]:
        """提取链接和图片，避免翻译URL"""
        elements = []
        placeholder_text = text
        
        # 提取图片和链接
        link_pattern = r'!\[([^\]]*)\]\([^\)]+\)|\[([^\]]+)\]\([^\)]+\)'
        for i, match in enumerate(re.finditer(link_pattern, text)):
            placeholder = f"__LINK_ELEMENT_{i}__"
            elements.append(match.group())
            placeholder_text = placeholder_text.replace(match.group(), placeholder, 1)
        
        return placeholder_text, elements
    
    @staticmethod
    def restore_links_and_images(text: str, elements: List[str]) -> str:
        """恢复链接和图片"""
        for i, element in enumerate(elements):
            placeholder = f"__LINK_ELEMENT_{i}__"
            text = text.replace(placeholder, element)
        return text
    
    @staticmethod
    def preprocess_text(text: str) -> str:
        """
        Preprocess text, clean and normalize formatting issues that may affect translation
        """
        # Remove extra whitespace characters
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Normalize line breaks
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'\r', '\n', text)
        
        # Remove extra spaces at the beginning and end of lines
        lines = text.split('\n')
        cleaned_lines = [line.strip() for line in lines]
        text = '\n'.join(cleaned_lines)
        
        # Fix hyphenated words (cases where words are split with hyphens at line ends)
        text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2\n', text)
        
        return text

    @staticmethod
    def postprocess_translation(text: str) -> str:
        """
        Postprocess translation result, optimize formatting
        """
        # Clean up extra spaces
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Ensure headers have blank lines before and after and remove formatting from headers
        text = DocumentFormatter._normalize_headers(text)
        
        # Fix possible paragraph separation issues
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Ensure no extra blank lines at the beginning and end of the document
        text = text.strip()
        
        return text

    @staticmethod
    def _normalize_headers(text: str) -> str:
        """
        Normalize header formatting:
        1. Ensure headers have blank lines before and after
        2. Remove bold, italic, and other formatting from headers
        """
        # 先提取代码块，避免误处理
        placeholder_text, code_blocks = DocumentFormatter.extract_code_blocks(text)
        
        # Match header lines (lines starting with 1-6 # characters)
        def clean_header(match):
            header_prefix = match.group(1)  # #, ##, ###, etc.
            header_content = match.group(2)  # Header content
            
            # Remove formatting marks from headers (e.g., **bold** or *italic*)
            # Remove bold formatting **text**
            header_content = re.sub(r'\*\*(.*?)\*\*', r'\1', header_content)
            # Remove italic formatting *text* or _text_
            header_content = re.sub(r'\*(.*?)\*', r'\1', header_content)
            header_content = re.sub(r'_(.*?)_', r'\1', header_content)
            # Remove inline code formatting `code` (这里应该已经被提取了)
            header_content = re.sub(r'`(.*?)`', r'\1', header_content)
            
            # Ensure headers have blank lines before and after
            return f"\n\n{header_prefix} {header_content.strip()}\n\n"
        
        # Apply header cleaning function
        placeholder_text = re.sub(r'\n?(#{1,6})\s+(.+?)\n', clean_header, placeholder_text)
        
        # Ensure headers at the beginning of the document are handled correctly
        placeholder_text = re.sub(r'^(#{1,6})\s+(.+?)\n', clean_header, placeholder_text)
        
        # Clean up duplicate blank lines
        placeholder_text = re.sub(r'\n{3,}', '\n\n', placeholder_text)
        
        # 恢复代码块
        result = DocumentFormatter.restore_code_blocks(placeholder_text, code_blocks)
        
        return result.strip()
