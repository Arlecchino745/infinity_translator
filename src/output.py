from pathlib import Path
import json
from datetime import datetime

class TranslationOutputFormatter:
    def __init__(self, provider_name: str, model_name: str):
        self.provider_name = provider_name
        self.model_name = model_name

    def format_translation(self, translated_text: str, original_filename: str) -> tuple[str, str]:
        """
        Format translation result as markdown and generate output filename
        
        Args:
            translated_text: Translated text
            original_filename: Original filename
        
        Returns:
            tuple: (Formatted text, Output filename)
        """
        # Add translation info header
        header = f"Translate by {self.provider_name}: {self.model_name}\n\n"
        formatted_text = header + translated_text

        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"translated_{Path(original_filename).stem}_{timestamp}.md"
        
        return formatted_text, output_filename

def create_translation_response(translated_text: str, original_filename: str, provider_name: str, model_name: str) -> tuple[bytes, str]:
    """
    Create translation response
    
    Args:
        translated_text: Translated text
        original_filename: Original filename
        provider_name: Provider name
        model_name: Model name
    
    Returns:
        tuple: (Byte stream of file content, Output filename)
    """
    formatter = TranslationOutputFormatter(provider_name, model_name)
    formatted_text, output_filename = formatter.format_translation(translated_text, original_filename)
    
    return formatted_text.encode('utf-8'), output_filename