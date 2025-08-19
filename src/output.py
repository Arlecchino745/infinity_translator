from pathlib import Path
import json
from datetime import datetime

class TranslationOutputFormatter:
    def __init__(self, provider_name: str, model_name: str):
        self.provider_name = provider_name
        self.model_name = model_name

    def format_translation(self, translated_text: str, original_filename: str) -> tuple[str, str]:
        """
        格式化翻译结果为markdown格式，并生成输出文件名
        
        Args:
            translated_text: 翻译后的文本
            original_filename: 原始文件名
        
        Returns:
            tuple: (格式化后的文本, 输出文件名)
        """
        # 添加翻译信息头
        header = f"Translate by {self.provider_name}|{self.model_name}\n\n"
        formatted_text = header + translated_text

        # 生成输出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"translated_{Path(original_filename).stem}_{timestamp}.md"
        
        return formatted_text, output_filename

def create_translation_response(translated_text: str, original_filename: str, provider_name: str, model_name: str) -> tuple[bytes, str]:
    """
    创建翻译响应
    
    Args:
        translated_text: 翻译后的文本
        original_filename: 原始文件名
        provider_name: 服务商名称
        model_name: 模型名称
    
    Returns:
        tuple: (文件内容的字节流, 输出文件名)
    """
    formatter = TranslationOutputFormatter(provider_name, model_name)
    formatted_text, output_filename = formatter.format_translation(translated_text, original_filename)
    
    return formatted_text.encode('utf-8'), output_filename
