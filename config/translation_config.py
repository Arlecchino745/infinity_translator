from dataclasses import dataclass
from typing import Dict, Any, Optional, List

@dataclass
class TranslationConfig:
    chunk_size: int = 2000
    chunk_overlap: int = 200
    temperature: float = 0.1
    context_window: int = 2  # 保持多少个前文段落作为上下文
    preserve_formatting: bool = True
    custom_separators: Optional[List[str]] = None
    glossary: Optional[Dict[str, str]] = None  # 术语表
    max_concurrent: int = 3  # 最大并发数
    max_retries: int = 3  # 最大重试次数
    retry_delay: float = 2.0  # 重试延迟
