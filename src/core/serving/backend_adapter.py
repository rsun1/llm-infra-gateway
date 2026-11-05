from src.core.serving.base_engine import BaseEngine
from src.utils.types import LLMInferRequest, LLMInferResponse, StreamChunk
from uuid import uuid4 
from collections.abc import AsyncGenerator
from src.core.serving.kv_cache import KVCacheManager
from src.core.routing.model_router import ModelRouter

class BackendAdapter(BaseEngine):
    def __init__(self):
        self.store : dict[str,dict[str, BaseEngine]] = dict()
        self.kv_cache: KVCacheManager | None = None
        self.model_router: ModelRouter | None = None
        

    def register_engine(self, model_name:str, instance_id:str,engine: BaseEngine) ->None:
        if model_name not in self.store:
            self.store[model_name] = {}
        self.store[model_name][instance_id] = engine

    def set_kv_cache(self, kv_cache: KVCacheManager) -> None:
        self.kv_cache = kv_cache

    def set_router(self, model_router:ModelRouter) ->None:
        self.model_router = model_router
        
    async def generate(self, request: LLMInferRequest) -> LLMInferResponse:
        if request.model not in self.store:
            raise ValueError(f"{request.model} not found in registry")
        instances = self.store[request.model]
        if self.model_router is not None:
            instance_id = self.model_router.round_robin(request.model)
            chosen_engine = instances[instance_id]
        else:
            chosen_engine = next(iter(instances.values()))
            
        key = request.model + str(request.messages)
        if self.kv_cache is not None:
            kv_cache = self.kv_cache
            cached = kv_cache.get(key)
            if cached is not None:
                return cached 
        
            response = await chosen_engine.generate(request)        
            kv_cache.put(key, response)
        else:
            response = await chosen_engine.generate(request)   
        return response
    
    async def load_model(self, model_name:str) -> None:
        instances = self.store[model_name]
        for engine in instances.values():
            await engine.load_model(model_name)
    
    async def unload_model(self, model_name:str) -> None:
        instances = self.store[model_name]
        for engine in instances.values():
            await engine.unload_model(model_name)
        
    async def health_check(self) -> bool:
        all_healthy = True
        for instances in self.store.values():
            for engine in instances.values():
                is_healthy = await engine.health_check()
                if is_healthy == False:
                    return  False  
        return  all_healthy
    
    async def initialize(self) -> None: 
        for instances in self.store.values():
            for engine in instances.values():
                await engine.initialize()
            
    async def shutdown(self) -> None: 
        for instances in self.store.values():
            for engine in instances.values():
                await engine.shutdown()
    
    async def generate_stream(self,request: LLMInferRequest) -> AsyncGenerator[StreamChunk, None]:
        instances = self.store[request.model]
        if self.model_router is not None:
            instance_id = self.model_router.round_robin(request.model)
            chosen_engine = instances[instance_id]
        else:
            chosen_engine = next(iter(instances.values()))
        async for chunk in chosen_engine.generate_stream(request):
            yield chunk 
                