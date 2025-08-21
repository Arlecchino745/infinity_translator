import asyncio
import json
import time
from typing import AsyncGenerator, Set, Optional
from weakref import WeakSet

class TranslationProgress:
    _instance: Optional['TranslationProgress'] = None
    _lock = asyncio.Lock()

    def __init__(self):
        self.progress = 0
        self.translated_chunks = 0
        self.total_chunks = 0
        self.status = "Preparing..."
        self._subscribers: Set = set()  # 改为普通set，手动管理
        self.start_time = None
        self.chunk_times = []
        self._max_chunk_times = 10  # 限制记录的时间数量

    @classmethod
    async def get_instance(cls) -> 'TranslationProgress':
        if cls._instance is None:
            async with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    async def subscribe(self):
        queue = asyncio.Queue()
        self._subscribers.add(queue)
        return queue

    async def unsubscribe(self, queue):
        self._subscribers.discard(queue)  # 使用discard避免KeyError

    def add_chunk_time(self, time_taken: float):
        """添加处理时间，保持固定长度"""
        self.chunk_times.append(time_taken)
        if len(self.chunk_times) > self._max_chunk_times:
            self.chunk_times.pop(0)

    def estimate_remaining_time(self) -> str:
        """Estimate remaining time"""
        if not self.chunk_times or self.translated_chunks == 0:
            return "Calculating..."
            
        # Calculate average processing time per chunk (using data from the last 5 chunks)
        recent_times = self.chunk_times[-5:]
        avg_time_per_chunk = sum(recent_times) / len(recent_times)
        
        # Calculate remaining chunks and estimated time
        remaining_chunks = self.total_chunks - self.translated_chunks
        estimated_seconds = avg_time_per_chunk * remaining_chunks
        
        # Format time
        if estimated_seconds < 60:
            return f"About {int(estimated_seconds)} seconds"
        elif estimated_seconds < 3600:
            minutes = int(estimated_seconds / 60)
            return f"About {minutes} minutes"
        else:
            hours = int(estimated_seconds / 3600)
            minutes = int((estimated_seconds % 3600) / 60)
            return f"About {hours} hours {minutes} minutes"

    async def update(self, progress: int, translated_chunks: int, total_chunks: int, status: str, chunk_time: Optional[float] = None):
        current_time = time.time()
        
        # Initialize start time
        if self.start_time is None:
            self.start_time = current_time
        
        # Record processing time for this chunk
        if chunk_time is not None:
            self.add_chunk_time(chunk_time)
        
        self.progress = progress
        self.translated_chunks = translated_chunks
        self.total_chunks = total_chunks
        
        # Add estimated remaining time to status message
        remaining_time = self.estimate_remaining_time()
        self.status = f"{status} (Estimated time remaining: {remaining_time})"

        # Notify all subscribers, 移除失效的队列
        failed_queues = set()
        for queue in self._subscribers:
            try:
                await queue.put({
                    "progress": self.progress,
                    "translated_chunks": self.translated_chunks,
                    "total_chunks": self.total_chunks,
                    "status": self.status
                })
            except Exception:
                failed_queues.add(queue)
        
        # 清理失效的队列
        self._subscribers -= failed_queues

    def reset(self):
        """重置进度"""
        self.progress = 0
        self.translated_chunks = 0
        self.total_chunks = 0
        self.status = "Preparing..."
        self.start_time = None
        self.chunk_times = []
