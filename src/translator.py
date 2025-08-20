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
                ("####", "header4"),
                ("#####", "header5"),
                ("######", "header6"),
            ]
        )
        
        self.separators = [
            "\n\n",  # 段落分隔
            "\n",    # 行分隔
            ". ",    # 句号
            "! ",    # 感叹号
            "? ",    # 问号
            "。",    # 中文句号
            "！",    # 中文感叹号
            "？",    # 中文问号
            "；",    # 中文分号
            "; ",    # 英文分号
        ]
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200,
            length_function=len,
            separators=self.separators
        )

    def preprocess_text(self, text: str) -> str:
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

    def postprocess_translation(self, text: str) -> str:
        """
        后处理翻译结果，优化格式
        """
        # 清理多余的空格
        text = re.sub(r'[ \t]+', ' ', text)
        
        # 确保标题前后有空行并移除标题中的格式
        text = self._normalize_headers(text)
        
        # 修复可能的段落分隔问题
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # 确保文档开头和结尾没有多余的空行
        text = text.strip()
        
        return text

    def _normalize_headers(self, text: str) -> str:
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
        
        base_prompt = f"""You are an expert academic translator and formatter. Your task is to translate academic papers while preserving and improving their formatting. 

Instructions:
1. Translate the following text into {language_description}.
2. Maintain all markdown formatting including headers, lists, code blocks, and links.
3. Keep the same header hierarchy.
4. Only output the translated {target_language} content, do not include the original text.

Text to be translated:
{text}"""
        
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
            # 预处理文本
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
            
            # 后处理翻译结果
            translated_text = DocumentFormatter.postprocess_translation(response.strip())
            
            return translated_text
            
        except Exception as e:
            logger.error(f"Error occurred while translating chunk: {str(e)}")
            return f"[Translation Error] {str(e)}"

    def translate_header(self, header_text: str) -> str:
        """
        翻译标题文本
        """
        try:
            # 为标题创建一个简化的提示
            prompt = self.create_translation_prompt(header_text)
            prompt_template = PromptTemplate(template=prompt, input_variables=["text"])
            result = prompt_template.format(text=header_text)
            response = self.llm.predict(result)
            return response.strip()
        except Exception as e:
            logger.error(f"Error occurred while translating header: {str(e)}")
            return header_text  # 如果翻译失败，返回原始标题

    async def translate_document(self, text: str, original_filename: str) -> Tuple[bytes, str]:

        logger.info(f"AI Provider: {self.active_provider}, Model: {self.provider_settings['model_name']}")
        
        try:
            provider_name = self.provider_settings.get('name', self.active_provider)
            model_name = self.provider_settings.get('model_name', 'unknown')
            
            # 预处理整个文档
            text = DocumentFormatter.preprocess_text(text)
            
            # 使用 MarkdownHeaderTextSplitter 分割文档以保留标题信息
            markdown_docs = self.markdown_splitter.split_text(text)
            
            # 处理每个分割后的文档块
            translated_sections = []
            previous_translation = None
            progress_tracker = await TranslationProgress.get_instance()
            total_sections = len(markdown_docs)
            
            for i, doc in enumerate(markdown_docs):
                # 对每个文档块使用 text_splitter 进一步分割（如果需要）
                chunks = self.text_splitter.split_text(doc.page_content)
                
                # 翻译每个块
                translated_chunks = []
                for chunk in chunks:
                    translated_chunk = self.translate_chunk(chunk, previous_translation)
                    translated_chunks.append(translated_chunk)
                    previous_translation = translated_chunk
                
                # 合并当前章节的翻译结果
                section_translation = "\n\n".join(translated_chunks)
                
                # 如果原文档块有标题元数据，添加标题上下文
                if doc.metadata:
                    # 构建标题上下文
                    header_context = ""
                    for header_level in ["header1", "header2", "header3", "header4", "header5", "header6"]:
                        if header_level in doc.metadata:
                            header_symbol = "#" * int(header_level[-1])
                            # 翻译标题文本
                            translated_header = self.translate_header(doc.metadata[header_level])
                            header_context += f"{header_symbol} {translated_header}\n\n"
                    
                    section_translation = header_context + section_translation
                
                translated_sections.append(section_translation)
                
                # 更新进度
                progress = int((i + 1) * 100 / total_sections)
                await progress_tracker.update(
                    progress=progress,
                    translated_chunks=i + 1,
                    total_chunks=total_sections,
                    status=f"Translating section {i + 1}/{total_sections}..."
                )
            
            # 合并所有章节的翻译结果
            final_translation = "\n\n".join(translated_sections)
            
            # 最终后处理
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