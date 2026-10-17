from src.core.serving.base_engine import BaseEngine
from src.utils.types import LLMInferRequest, LLMInferResponse, StreamChunk
from uuid import uuid4 
from collections.abc import AsyncGenerator

class BackendAdapter(BaseEngine):
    def __init__(self):
        self.store : dict[str,BaseEngine] = dict()

    def register_engine(self, model_name:str, engine: BaseEngine) ->None:
        self.store[model_name] = engine

    async def generate(self, request: LLMInferRequest) -> LLMInferResponse:
        if request.model not in self.store:
            raise ValueError(f"{request.model} not found in registry")
        chosen_engine = self.store[request.model]
        return await chosen_engine.generate(request)
    
    async def load_model(self, model_name:str) -> None:
        chosen_engine = self.store[model_name]
        await chosen_engine.load_model(model_name)
    
    async def unload_model(self, model_name:str) -> None:
        chosen_engine = self.store[model_name]
        await chosen_engine.unload_model(model_name)
        
    async def health_check(self) -> bool:
        all_healthy = True
        for engine in self.store.values():
            is_healthy = await engine.health_check()
            if is_healthy == False:
                return  False  
        return  all_healthy
    
    async def initialize(self) -> None: 
        for engine in self.store.values():
            await engine.initialize()
            
    async def shutdown(self) -> None: 
        for engine in self.store.values():
            await engine.shutdown()
    
    async def generate_stream(self,request: LLMInferRequest) -> AsyncGenerator[StreamChunk, None]:
        chosen_engine = self.store[request.model]
        async for chunk in chosen_engine.generate_stream(request):
            yield chunk 
                