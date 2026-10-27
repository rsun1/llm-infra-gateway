from src.core.serving.backend_adapter import BackendAdapter
from collections import OrderedDict

class ColdStartManager:
    def __init__(self, adapter: BackendAdapter, max_loaded:int):
        self.adapter = adapter
        self.max_loaded = max_loaded
        self.loaded: OrderedDict[str, bool] = OrderedDict()
        
    async def ensure_model_ready(self, model_name:str) -> None:
        if model_name in self.loaded:
            self.loaded.move_to_end(model_name)
            return 
        else:
            if len(self.loaded) >= self.max_loaded:
                oldest, _ = self.loaded.popitem(last=False)
                await self.adapter.unload_model(oldest)
            await self.adapter.load_model(model_name)
            self.loaded[model_name] = True 
    
    async def warmup(self, model_names:list[str]) -> None:
        for names in model_names:
            await self.ensure_model_ready(names)