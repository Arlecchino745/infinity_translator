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

    async def update(self, progress: int, translated_chunks: int, total_chunks: int, status: str):
        self.progress = progress
        self.translated_chunks = translated_chunks
        self.total_chunks = total_chunks
        self.status = status

        # 通知所有订阅者
        for queue in self._subscribers:
            await queue.put({
                "progress": self.progress,
                "translated_chunks": self.translated_chunks,
                "total_chunks": self.total_chunks,
                "status": self.status
            })
