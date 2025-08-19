from typing import List, Optional, Tuple
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
import logging
import re

from config.settings import get_provider_settings
from config.config import SILICONFLOW_API_KEY, OPENROUTER_API_KEY
from .output import create_translation_response
from .progress import TranslationProgress

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentTranslator:
    def __init__(self):

        self.active_provider, self.provider_settings = get_provider_settings()
        self.api_key = SILICONFLOW_API_KEY if self.active_provider == 'siliconflow' else OPENROUTER_API_KEY
        

        self.llm = ChatOpenAI(
            model_name=self.provider_settings['model_name'],
            openai_api_base=self.provider_settings['base_url'],
            openai_api_key=self.api_key,
            temperature=0.1,
        )
        
        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "header1"),
                ("##", "header2"),
                ("###", "header3"),
            ]
        )
        
        self.separators = [
            "# ",
            "## ",
            "### ",
            "\n\n",
            "。",
            "！",
            "？",
            ". ",
            "! ",
            "? ",
            "；",
            "; ",
        ]
        
        self.last_resort_punctuation = set([
            '。', '！', '？', '；', '.', '!', '?', ';'
        ])
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=0,
            length_function=len,
            separators=self.separators
        )

    def create_translation_prompt(self, text: str, previous_translation: Optional[str] = None) -> str:
        # 从配置中获取目标语言
        from config.settings import load_settings
        settings = load_settings()
        target_language = settings.get('target_language', 'zh')
        
        language_map = {
            'zh-Hans': 'fluent, professional Simplified Chinese that conforms to Chinese reading habits',
            'zh-Hant': 'fluent, professional Traditional Chinese that conforms to Traditional Chinese reading habits',
            'en': 'fluent, professional English that conforms to English writing conventions',
            'ja': 'fluent, professional Japanese that conforms to Japanese writing conventions',
            'ko': 'fluent, professional Korean that conforms to Korean writing conventions',
            'fr': 'fluent, professional French that conforms to French writing conventions',
            'de': 'fluent, professional German that conforms to German writing conventions',
            'es': 'fluent, professional Spanish that conforms to Spanish writing conventions',
            'pt': 'fluent, professional Portuguese that conforms to Portuguese writing conventions',
            'ru': 'fluent, professional Russian that conforms to Russian writing conventions',
            'ar': 'fluent, professional Arabic that conforms to Arabic writing conventions',
            'hi': 'fluent, professional Hindi that conforms to Hindi writing conventions',
            'it': 'fluent, professional Italian that conforms to Italian writing conventions',
            'tr': 'fluent, professional Turkish that conforms to Turkish writing conventions',
            'vi': 'fluent, professional Vietnamese that conforms to Vietnamese writing conventions',
            'th': 'fluent, professional Thai that conforms to Thai writing conventions',
            'id': 'fluent, professional Indonesian that conforms to Indonesian writing conventions',
            'fa': 'fluent, professional Persian that conforms to Persian writing conventions'
        }
        
        language_description = language_map.get(target_language, language_map['zh-Hans'])
        
        base_prompt = f"""Please translate the following text into {language_description}. Maintain the original markdown format, do not change the heading levels, and preserve code blocks and link formats. Only output the translated {target_language} content, do not include the original text.

Text to be translated:
{text}"""
        
        if previous_translation:
            context_prompt = """\n\nTo maintain contextual coherence, this is the translation of the previous paragraph for reference:
{previous_translation}

Also, FOLLOWING THESE INSTRUCTIONS:
1.There may be extra spaces between characters or words in the main text. Please remove them! 
2.Do not modify any links in the file, including image references or URLs! Do not modify them! They are completely correct. 
3.Pay attention to correcting the heading levels. For example, 1, 2, and 3 are generally first-level headings, and 1.1 and 1.2 are generally second-level headings, and so on. There may also be other forms of heading numbering, in which case please judge for yourself and ensure that their hierarchical relationship is correct. ATTENTION: Titles must have blank lines before and after them. If they don't, please add them.
4.Sometimes the text in the headers and footers may be mixed in the main text and interrupt the text, affecting reading. If it is like the journal or article title or page number mixed in, delete it; if it is nonsense such as "Project supported by..." or "These authors contributed equally to this work.", also delete it. If it is the author's email address, also delete it. In short, delete all headers, footers, and footnotes that commonly appear on the first page of the academic paper PDF.
\nPlease ensure that this translation is consistent with the above text in terms of terminology and style. Make sure you only output the translation result, without any other explanations or labels like "TRANSLATED TEXT". Again, do not output anything other than the translated text. 
"""
            return base_prompt + context_prompt
        
        return base_prompt

    def validate_chunk(self, chunk: str) -> bool:
        """验证文本块是否合适翻译
        1. 非空
        2. 长度适中（避免过短或过长）
        3. 尽量以完整句子结束
        """
        if not chunk or len(chunk) < 50:  # 过短的块没有必要单独翻译
            return False
        if len(chunk) > 2000:  # 过长的块需要继续分割
            return False
            
        # 检查是否以完整句子结束，但不强制要求
        valid_endings = [sep.strip() for sep in self.separators 
                        if sep.strip() and not sep.startswith('\n')]
        ends_with_separator = any(chunk.endswith(end) for end in valid_endings)
        
        # 如果长度合适（500-1500字符）且以分隔符结束，则为最优情况
        if 500 <= len(chunk) <= 1500 and ends_with_separator:
            return True
            
        # 如果长度在可接受范围内，即使不以分隔符结束也可以接受
        return 200 <= len(chunk) <= 1800

    def retry_split_chunk(self, chunk: str, max_retries: int = 3) -> List[str]:
        """尝试重新分割不合法的文本块"""
        if len(chunk) <= 2000 or max_retries <= 0:
            return [chunk]
        
        # 从后往前查找最近的合法分割点
        for sep in self.separators:
            sep = sep.strip()
            if not sep:
                continue
            
            last_pos = chunk.rfind(sep, 0, 2000)
            if last_pos > 0:
                first_part = chunk[:last_pos + len(sep)]
                second_part = chunk[last_pos + len(sep):]
                
                if self.validate_chunk(first_part):
                    # 递归处理剩余部分
                    return [first_part] + self.retry_split_chunk(second_part, max_retries - 1)
        
        # 如果实在找不到合适的分割点，返回原文本
        return [chunk]

    def _is_valid_chunk_size(self, chunk_size: int) -> bool:
        MIN_SIZE = 10
        MAX_SIZE = 2000
        
        if chunk_size < MIN_SIZE or chunk_size > MAX_SIZE:
            return False
        return True

    def _find_best_split_position(self, text: str, target_pos: int, search_range: int = 500) -> int:
        text_len = len(text)
        start_pos = max(0, target_pos - search_range)
        end_pos = min(text_len, target_pos + search_range)
        
        best_pos = -1
        min_distance = float('inf')
        
        for sep in self.separators:
            sep = sep.strip()
            if not sep:
                continue
                
            pos = text.find(sep, start_pos, end_pos)
            while pos != -1:
                distance = abs(pos - target_pos)
                if distance < min_distance:
                    min_distance = distance
                    best_pos = pos + len(sep)
                pos = text.find(sep, pos + 1, end_pos)
        
        if best_pos == -1:
            for i in range(start_pos, end_pos):
                if text[i] in self.last_resort_punctuation:
                    distance = abs(i - target_pos)
                    if distance < min_distance:
                        min_distance = distance
                        best_pos = i + 1
        
        return best_pos

    def split_text_chunk(self, chunk: str) -> List[str]:

        if self._is_valid_chunk_size(len(chunk)):
            return [chunk]
            
        split_pos = self._find_best_split_position(chunk, len(chunk) // 2)
        
        if split_pos == -1:
            split_pos = len(chunk) // 2
            
        first_part = chunk[:split_pos].strip()
        second_part = chunk[split_pos:].strip()
        
        result = []
        if first_part:
            result.extend(self.split_text_chunk(first_part))
        if second_part:
            result.extend(self.split_text_chunk(second_part))
            
        return result

    def translate_chunk(self, text: str, previous_translation: Optional[str] = None) -> str:
        try:
            if not self.validate_chunk(text):
                logger.warning(f"Illegal text block detected, attempting to re-split...")
                chunks = self.retry_split_chunk(text)
                if len(chunks) > 1:
                    translated_parts = []
                    for chunk in chunks:
                        translated_part = self.translate_chunk(chunk, previous_translation)
                        translated_parts.append(translated_part)
                        previous_translation = translated_part
                    return " ".join(translated_parts)
            
            prompt = self.create_translation_prompt(text, previous_translation)
            prompt_template = PromptTemplate(
                template=prompt,
                input_variables=["text"] if not previous_translation else ["text", "previous_translation"]
            )
            
            input_variables = {"text": text}
            if previous_translation:
                input_variables["previous_translation"] = previous_translation
            
            result = prompt_template.format(**input_variables)
            response = self.llm.predict(result)
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error occurred while translating chunk: {str(e)}")
            return f"[Translation Error] {str(e)}"

    async def translate_document(self, text: str, original_filename: str) -> Tuple[bytes, str]:

        logger.info(f"AI Provider: {self.active_provider}, Model: {self.provider_settings['model_name']}")
        
        try:
            provider_name = self.provider_settings.get('name', self.active_provider)
            model_name = self.provider_settings.get('model_name', 'unknown')
            markdown_docs = self.markdown_splitter.split_text(text)
            
            all_chunks = []
            for doc in markdown_docs:
                initial_chunks = self.text_splitter.split_text(doc.page_content)
                for chunk in initial_chunks:
                    processed_chunks = self.split_text_chunk(chunk)
                    all_chunks.extend(processed_chunks)
            
            logger.info(f"The document has been split into {len(all_chunks)} chunks")
            
            translated_chunks = []
            previous_translation = None
            progress_tracker = await TranslationProgress.get_instance()
            total_chunks = len(all_chunks)
            
            for i, chunk in enumerate(all_chunks):
                translated_text = self.translate_chunk(chunk, previous_translation)
                translated_chunks.append(translated_text)
                previous_translation = translated_text
                
                progress = int((i + 1) * 100 / total_chunks)
                await progress_tracker.update(
                    progress=progress,
                    translated_chunks=i + 1,
                    total_chunks=total_chunks,
                    status=f"Translating the {i + 1}/{total_chunks} chunk..."
                )
            
            final_translation = "\n\n".join(translated_chunks)
            
            final_translation = re.sub(r'\n{3,}', '\n\n', final_translation)
            
            return create_translation_response(
                translated_text=final_translation,
                original_filename=original_filename,
                provider_name=provider_name,
                model_name=model_name
            )
            
        except Exception as e:
            logger.error(f"Error occurred while translating the document: {str(e)}")
            raise