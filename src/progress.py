import asyncio
import json
from typing import AsyncGenerator

class TranslationProgress:
    _instance = None
    _lock = asyncio.Lock()

    def __init__(self):
        self.progress = 0
        self.translated_chunks = 0
        self.total_chunks = 0
        self.status = "准备中..."
        self._subscribers = set()
        self.start_time = None
        self.chunk_times = []  # 存储每个块的处理时间

    @classmethod
    async def get_instance(cls):
        if not cls._instance:
            async with cls._lock:
                if not cls._instance:
                    cls._instance = cls()
        return cls._instance

    async def subscribe(self):
        queue = asyncio.Queue()
        self._subscribers.add(queue)
        return queue

    async def unsubscribe(self, queue):
        self._subscribers.remove(queue)

    def estimate_remaining_time(self) -> str:
        """估算剩余时间"""
        if not self.chunk_times or self.translated_chunks == 0:
            return "计算中..."
            
        # 计算平均每个块的处理时间（使用最近5个块的数据）
        recent_times = self.chunk_times[-5:]
        avg_time_per_chunk = sum(recent_times) / len(recent_times)
        
        # 计算剩余块数和预计剩余时间
        remaining_chunks = self.total_chunks - self.translated_chunks
        estimated_seconds = avg_time_per_chunk * remaining_chunks
        
        # 格式化时间
        if estimated_seconds < 60:
            return f"约 {int(estimated_seconds)} 秒"
        elif estimated_seconds < 3600:
            minutes = int(estimated_seconds / 60)
            return f"约 {minutes} 分钟"
        else:
            hours = int(estimated_seconds / 3600)
            minutes = int((estimated_seconds % 3600) / 60)
            return f"约 {hours} 小时 {minutes} 分钟"

    async def update(self, progress: int, translated_chunks: int, total_chunks: int, status: str):
        import time
        current_time = time.time()
        
        # 初始化开始时间
        if self.start_time is None:
            self.start_time = current_time
        
        # 记录这个块的处理时间
        if self.translated_chunks < translated_chunks:
            if self.chunk_times:
                chunk_time = current_time - (self.start_time + sum(self.chunk_times))
                self.chunk_times.append(chunk_time)
            else:
                # 第一个块的处理时间
                self.chunk_times.append(current_time - self.start_time)
        
        self.progress = progress
        self.translated_chunks = translated_chunks
        self.total_chunks = total_chunks
        
        # 添加预估剩余时间到状态信息
        remaining_time = self.estimate_remaining_time()
        self.status = f"{status} (预计剩余时间: {remaining_time})"

        # 通知所有订阅者
        for queue in self._subscribers:
            await queue.put({
                "progress": self.progress,
                "translated_chunks": self.translated_chunks,
                "total_chunks": self.total_chunks,
                "status": self.status
            })
