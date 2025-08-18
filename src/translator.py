# translator.py

from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from tqdm import tqdm
import logging
import re

# 导入配置管理
from config.settings import get_provider_settings
from config.config import SILICONFLOW_API_KEY, OPENROUTER_API_KEY

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentTranslator:
    def __init__(self):
        # 获取当前激活的服务商配置
        self.active_provider, self.provider_settings = get_provider_settings()
        self.api_key = SILICONFLOW_API_KEY if self.active_provider == 'siliconflow' else OPENROUTER_API_KEY
        
        # 初始化 LLM
        self.llm = ChatOpenAI(
            model_name=self.provider_settings['model_name'],
            openai_api_base=self.provider_settings['base_url'],
            openai_api_key=self.api_key,
            temperature=0.1,
            streaming=True,
        )
        
        # 初始化分割器
        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "header1"),
                ("##", "header2"),
                ("###", "header3"),
            ]
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,  # 减小chunk大小以提高翻译质量
            chunk_overlap=200,
            length_function=self.llm.get_num_tokens_from_messages,
            separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""]
        )

    def create_translation_prompt(self, text: str, previous_translation: Optional[str] = None) -> str:
        """创建带有上下文的翻译提示"""
        base_prompt = """请将以下文本翻译成流畅、专业、符合中文阅读习惯的简体中文。
保持原文的markdown格式，不要改变标题层级，保留代码块和链接格式。
只输出翻译后的中文内容，不要包含原文。

待翻译文本:
{text}"""
        
        if previous_translation:
            context_prompt = """\n\n为了保持上下文的连贯性，这是前一段的翻译结果作为参考:
{previous_translation}

请确保本次翻译与上文在术语使用和风格上保持一致。
"""
            return base_prompt + context_prompt
        
        return base_prompt

    def translate_chunk(self, text: str, previous_translation: Optional[str] = None) -> str:
        """翻译单个文本块"""
        try:
            prompt = self.create_translation_prompt(text, previous_translation)
            prompt_template = PromptTemplate(
                template=prompt,
                input_variables=["text"] if not previous_translation else ["text", "previous_translation"]
            )
            
            # 准备输入变量
            input_variables = {"text": text}
            if previous_translation:
                input_variables["previous_translation"] = previous_translation
            
            # 执行翻译
            result = prompt_template.format(**input_variables)
            response = self.llm.predict(result)
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"翻译chunk时发生错误: {str(e)}")
            return f"[翻译错误] {str(e)}"

    def translate_document(self, text: str) -> str:
        """
        使用配置好的 LLM 服务翻译长文档。
        采用顺序处理并保持上下文连贯性。
        """
        logger.info(f"正在使用服务: {self.active_provider}, 模型: {self.provider_settings['model_name']}")
        
        try:
            # 1. 先按markdown标题分割
            markdown_docs = self.markdown_splitter.split_text(text)
            
            # 2. 对每个部分进行进一步的分块
            all_chunks = []
            for doc in markdown_docs:
                chunks = self.text_splitter.split_text(doc.page_content)
                all_chunks.extend(chunks)
            
            logger.info(f"文档已分割成 {len(all_chunks)} 个块")
            
            # 3. 顺序翻译每个块，并保持上下文连贯
            translated_chunks = []
            previous_translation = None
            
            for chunk in tqdm(all_chunks, desc="翻译进度"):
                translated_text = self.translate_chunk(chunk, previous_translation)
                translated_chunks.append(translated_text)
                # 更新上下文，只保留上一个块的翻译
                previous_translation = translated_text
            
            # 4. 合并翻译结果
            final_translation = "\n\n".join(translated_chunks)
            
            # 5. 清理可能的重复内容
            final_translation = re.sub(r'\n{3,}', '\n\n', final_translation)
            
            return final_translation
            
        except Exception as e:
            logger.error(f"翻译文档时发生错误: {str(e)}")
            raise

def translate_document(text: str) -> str:
    """
    入口函数，保持与原接口兼容
    """
    translator = DocumentTranslator()
    return translator.translate_document(text)