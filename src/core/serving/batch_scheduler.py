from src.core.serving.backend_adapter import BackendAdapter
from src.utils.types import LLMInferRequest,LLMInferResponse
from src.core.cold_start.cold_start_mgr import ColdStartManager
import asyncio
from time import time 

class BatchScheduler:
    def __init__(self, adapter: BackendAdapter, max_batch_size: int, max_wait_ms: int):
        self.adapter = adapter
        self.max_batch_size = max_batch_size
        self.max_wait_ms = max_wait_ms
        self.queue : list[tuple[LLMInferRequest, asyncio.Future]]=[]
        self.first_queue_at: float | None = None 
        self.cold_start_mgr: ColdStartManager | None = None
        
    async def _timeout_watcher(self):
        while True:
            await asyncio.sleep(0.05)
            if self.queue and self.first_queue_at:
                wait_time_ms = 1000* (asyncio.get_event_loop().time() - self.first_queue_at)
                if wait_time_ms >= self.max_wait_ms:
                    await self._run_batch()
                    
    def set_cold_start_mgr(self, cold_start_mgr: ColdStartManager):
        self.cold_start_mgr = cold_start_mgr
    
    async def _run_batch(self):
        batch = self.queue[:self.max_batch_size]
        self.queue = self.queue[self.max_batch_size:]
        #print("number of requests this turn：", len(batch))
        for request, future in batch:
            try:
                await self.cold_start_mgr.ensure_model_ready(request.model) 
                response = await self.adapter.generate(request)
                future.set_result(response)
            except Exception as e:
                future.set_exception(e)
        
        
    async def submit(self,request:LLMInferRequest) -> LLMInferResponse:
        future = asyncio.Future()
        if not self.queue:
            self.first_queue_at = asyncio.get_event_loop().time()
        self.queue.append((request,future))
        if len(self.queue) >= self.max_batch_size:
            await self._run_batch()
        result = await future 
        return result