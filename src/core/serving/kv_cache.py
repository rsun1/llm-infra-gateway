from collections import OrderedDict
from src.utils.types import LLMInferResponse

class KVCacheManager:
    def __init__(self, max_size:int):
        self.max_size = max_size
        self.cache: OrderedDict[str, LLMInferResponse]=OrderedDict()
        self.hits = 0
        self.misses = 0
        
    def get(self,key:str) -> LLMInferResponse | None:
        if key in self.cache:
            self.hits += 1
            self.cache.move_to_end(key)
            return self.cache[key]
        else:
            self.misses += 1 
            return None 
    
    def put(self, key:str, value:LLMInferResponse) -> None: 
        self.cache[key] = value 
        self.cache.move_to_end(key)
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)
        
    def hit_ratio(self) -> float:
        if self.hits + self.misses == 0:
            return 0
        ratio = self.hits/(self.hits+self.misses)
        return ratio