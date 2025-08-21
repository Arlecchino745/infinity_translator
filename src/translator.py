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
from .formatter import DocumentFormatter

from config.translation_config import TranslationConfig
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from tenacity import retry, stop_after_attempt, wait_exponential

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentTranslator:
    # 替换原来的 __init__ 方法
    def __init__(self, config: Optional[TranslationConfig] = None):
        self.config = config or TranslationConfig()
        self.glossary = self.config.glossary or {}
        self.context_buffer = []  # 保持上下文缓冲区
    
        self.active_provider, self.provider_settings = get_provider_settings()
        self.api_key = SILICONFLOW_API_KEY if self.active_provider == 'siliconflow' else OPENROUTER_API_KEY
    
        self.llm = ChatOpenAI(
        model_name=self.provider_settings['model_name'],
        openai_api_base=self.provider_settings['base_url'],
        openai_api_key=self.api_key,
        temperature=self.config.temperature,
        )
    
        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
            ("#", "header1"),
            ("##", "header2"),
            ("###", "header3"),
            ("####", "header4"),
            ("#####", "header5"),
            ("######", "header6"),
            ]
        )
    
        # 使用配置中的分隔符
        separators = self.config.custom_separators or [
            "\n\n",  # Paragraph separator
            "\n",    # Line separator
            ". ",    # Period
            "! ",    # Exclamation mark
            "? ",    # Question mark
            "。",    # Chinese period
            "！",    # Chinese exclamation mark
            "？",    # Chinese question mark
            "；",    # Chinese semicolon
            "; ",    # English semicolon
        ]
    
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
            length_function=len,
            separators=separators
        )
    
        # 添加信号量控制并发
        self.semaphore = asyncio.Semaphore(self.config.max_concurrent)


    def create_translation_prompt(self, text: str, previous_translation: Optional[str] = None) -> str:
        # Get target language from configuration
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
        
        base_prompt = f"""You are an expert academic translator and formatter. Your task is to translate academic papers while preserving and improving their formatting. 

Instructions:
1. Translate the following text into {language_description}.
2. Maintain all markdown formatting including headers, lists, code blocks, and links.
3. Keep the same header hierarchy.
4. Only output the translated {target_language} content, do not include the original text.

Text to be translated:
{{text}}"""
        
        if previous_translation:
            context_prompt = """\n\nTo maintain contextual coherence, here is the previous paragraph's translation for reference:
{previous_translation}

Additional formatting instructions:
1. Remove any extra spaces between characters or words in the main text.
2. Preserve all links, image references, and URLs exactly as they appear.
3. Correct any header levels if needed (e.g., 1, 2, 3 are first-level; 1.1, 1.2 are second-level).
4. Ensure headers are properly separated with blank lines before and after.
5. Maintain consistent terminology and writing style with the previous translation.
6. Output only the translated text without any additional labels or explanations.
"""
            return base_prompt + context_prompt
        
        return base_prompt

    def translate_chunk(self, text: str, previous_translation: Optional[str] = None) -> str:
        try:
            # Preprocess text
            text = DocumentFormatter.preprocess_text(text)
            
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
            
            # Post-process translation result
            translated_text = DocumentFormatter.postprocess_translation(response.strip())
            
            return translated_text
            
        except Exception as e:
            logger.error(f"Error occurred while translating chunk: {str(e)}")
            return f"[Translation Error] {str(e)}"

    def translate_header(self, header_text: str) -> str:
        """
        Translate header text
        """
        try:
            # Create a simplified prompt for headers
            prompt = self.create_translation_prompt(header_text)
            # Escape curly braces in header text to prevent formatting issues
            escaped_header_text = header_text.replace("{", "{{").replace("}", "}}")
            prompt_template = PromptTemplate(template=prompt, input_variables=["text"])
            result = prompt_template.format(text=escaped_header_text)
            response = self.llm.predict(result)
            return response.strip()
        except Exception as e:
            logger.error(f"Error occurred while translating header: {str(e)}")
            return header_text  # If translation fails, return original header

    # 完全替换 translate_document 方法
    async def translate_document(self, text: str, original_filename: str) -> Tuple[bytes, str]:
        logger.info(f"AI Provider: {self.active_provider}, Model: {self.provider_settings['model_name']}")
    
        try:
            provider_name = self.provider_settings.get('name', self.active_provider)
            model_name = self.provider_settings.get('model_name', 'unknown')
        
            # 重置上下文缓冲区
            self.context_buffer = []
        
            # Preprocess the entire document
            text = DocumentFormatter.preprocess_text(text)
        
            # Use MarkdownHeaderTextSplitter to split document while preserving header information
            markdown_docs = self.markdown_splitter.split_text(text)
        
            # Process each split document chunk
            translated_sections = []
            progress_tracker = await TranslationProgress.get_instance()
            progress_tracker.reset()  # 重置进度
            total_sections = len(markdown_docs)
        
            # Calculate total chunks for more accurate progress tracking
            total_chunks = 0
            section_chunk_counts = []
            for doc in markdown_docs:
                chunks = self.text_splitter.split_text(doc.page_content)
                section_chunk_counts.append(len(chunks))
                total_chunks += len(chunks)
        
            processed_chunks = 0
        
            for i, doc in enumerate(markdown_docs):
                # Further split each document chunk using text_splitter (if needed)
                chunks = self.text_splitter.split_text(doc.page_content)
            
                # Translate each chunk
                translated_chunks = []
                for j, chunk in enumerate(chunks):
                    chunk_start_time = time.time()
                
                    # 获取上下文
                    context = self.get_context_for_translation()
                
                    # 异步翻译
                    translated_chunk = await self.translate_chunk_async(chunk, context)
                    translated_chunks.append(translated_chunk)
                
                    # 更新上下文缓冲区
                    self.manage_context_buffer(translated_chunk)
                
                    # 计算处理时间
                    chunk_time = time.time() - chunk_start_time
                
                    # Update processed chunks count
                    processed_chunks += 1
                
                    # Update progress more frequently (per chunk rather than per section)
                    progress = round((processed_chunks / total_chunks) * 100, 1)
                    await progress_tracker.update(
                        progress=progress,
                        translated_chunks=processed_chunks,
                        total_chunks=total_chunks,
                        status=f"Translating section {i + 1}/{total_sections}, chunk {j + 1}/{len(chunks)}...",
                        chunk_time=chunk_time
                    )
            
                # Merge translation results for current section
                section_translation = "\n\n".join(translated_chunks)
            
                # If the original document chunk has header metadata, add header context
                if doc.metadata:
                    # Build header context
                    header_context = ""
                    for header_level in ["header1", "header2", "header3", "header4", "header5", "header6"]:
                        if header_level in doc.metadata:
                            header_symbol = "#" * int(header_level[-1])
                            # Translate header text
                            translated_header = self.translate_header(doc.metadata[header_level])
                            header_context += f"{header_symbol} {translated_header}\n\n"
                
                    section_translation = header_context + section_translation
            
                translated_sections.append(section_translation)
        
            # Merge translation results from all sections
            final_translation = "\n\n".join(translated_sections)
        
            # Final post-processing
            final_translation = DocumentFormatter.postprocess_translation(final_translation)
        
            return create_translation_response(
                translated_text=final_translation,
                original_filename=original_filename,
                provider_name=provider_name,
                model_name=model_name
            )
        
        except Exception as e:
            logger.error(f"Error occurred while translating the document: {str(e)}")
            raise

    def apply_glossary(self, text: str) -> str:
        """应用术语表"""
        if not self.glossary:
            return text
        
        for term, translation in self.glossary.items():
            # 使用词边界匹配，避免部分匹配
            pattern = r'\b' + re.escape(term) + r'\b'
            text = re.sub(pattern, translation, text, flags=re.IGNORECASE)
        return text
    def manage_context_buffer(self, new_translation: str):
        """管理上下文缓冲区"""
        self.context_buffer.append(new_translation)
        if len(self.context_buffer) > self.config.context_window:
            self.context_buffer.pop(0)

    def get_context_for_translation(self) -> Optional[str]:
        """获取用于翻译的上下文"""
        if not self.context_buffer:
            return None
        return "\n\n".join(self.context_buffer[-self.config.context_window:])
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8)
    )
    def translate_chunk_with_retry(self, text: str, context: Optional[str] = None) -> str:
        """带重试机制的翻译"""
        try:
            return self.translate_chunk_enhanced(text, context)
        except Exception as e:
            logger.warning(f"Translation attempt failed: {e}")
            raise

    def translate_chunk_enhanced(self, text: str, context: Optional[str] = None) -> str:
        """增强的翻译方法"""
        try:
            # 提取并保护代码块和链接
            text_without_code, code_blocks = DocumentFormatter.extract_code_blocks(text)
            text_without_links, link_elements = DocumentFormatter.extract_links_and_images(text_without_code)
        
            # 预处理文本
            processed_text = DocumentFormatter.preprocess_text(text_without_links)
        
            # 应用术语表
            processed_text = self.apply_glossary(processed_text)
        
            # 创建提示词
            prompt = self.create_translation_prompt(processed_text, context)
            prompt_template = PromptTemplate(
                template=prompt,
                input_variables=["text"] if not context else ["text", "previous_translation"]
            )
        
            input_variables = {"text": processed_text}
            if context:
                input_variables["previous_translation"] = context
        
            result = prompt_template.format(**input_variables)
            response = self.llm.predict(result)
        
            # 恢复代码块和链接
            translated_text = DocumentFormatter.restore_links_and_images(response.strip(), link_elements)
            translated_text = DocumentFormatter.restore_code_blocks(translated_text, code_blocks)
        
            # 后处理翻译结果
            translated_text = DocumentFormatter.postprocess_translation(translated_text)
        
            return translated_text
        
        except Exception as e:
            logger.error(f"Error occurred while translating chunk: {str(e)}")
            return f"[Translation Error] {str(e)}"

    async def translate_chunk_async(self, text: str, context: Optional[str] = None) -> str:
        """异步翻译块"""
        async with self.semaphore:
            # 在线程池中执行翻译以避免阻塞
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                return await loop.run_in_executor(
                    executor, 
                    self.translate_chunk_with_retry, 
                    text, 
                    context
                )


    
    