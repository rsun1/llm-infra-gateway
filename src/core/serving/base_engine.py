from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from src.utils.types import LLMInferRequest, LLMInferResponse, StreamChunk


class BaseEngine(ABC):
    @abstractmethod
    async def initialize(self):
        pass
    
    @abstractmethod
    async def generate(self, request: LLMInferRequest) -> LLMInferResponse:
        pass 
    
    @abstractmethod    
    async def generate_stream(self, request: LLMInferRequest) -> AsyncGenerator[StreamChunk, None]:
        pass
    
    @abstractmethod   
    async def load_model(self, model_name: str) -> None:
        pass 
 
    @abstractmethod    
    async def unload_model(self, model_name: str) -> None:
        pass 
    
    @abstractmethod
    async def health_check(self) -> bool:
        pass 

    @abstractmethod
    async def shutdown(self) -> None:
        pass 