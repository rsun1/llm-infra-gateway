from collections.abc import AsyncGenerator
from src.utils.types import LLMInferRequest, LLMInferResponse, StreamChunk
from src.core.serving.base_engine import BaseEngine
from uuid import uuid4 
import asyncio

class MockEngine(BaseEngine):
    def __init__(self):
        self.loaded_models: set[str] = set()
    
    async def initialize(self):
        pass         
    
    async def generate(self, request: LLMInferRequest) -> LLMInferResponse:
        request_id =  str(uuid4())
        model = request.model 
        content = f"This is mock response to {request.messages[-1].content}"
        prompt_tokens= sum(len(m.content) for m in request.messages)
        completion_tokens= len(content)
        total_tokens = prompt_tokens + completion_tokens 
        return LLMInferResponse(id = request_id,
                         model = model,
                         content = content,
                         prompt_tokens=prompt_tokens,
                         completion_tokens=completion_tokens,
                         total_tokens=total_tokens)
    
    async def generate_stream(self, request: LLMInferRequest) -> AsyncGenerator[StreamChunk, None]:
        content = f"This is mock response to {request.messages[-1].content}"
        chunk = content.split()
        for c in chunk:
            schunk = StreamChunk(content=c)
            await asyncio.sleep(0.05)
            yield schunk
        yield StreamChunk(content="",finish_reason= "stop")
        
    
    async def load_model(self, model_name: str) -> None:
        self.loaded_models.add(model_name) 
 
    async def unload_model(self, model_name: str) -> None:
        self.loaded_models.discard(model_name) 
    
    async def health_check(self) -> bool:
        return True  

    async def shutdown(self) -> None:
        pass
    