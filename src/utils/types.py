from enum import StrEnum
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ModelStatus(StrEnum):
    IDLE = "idle"          
    LOADING = "loading"    
    STOPPED = "stopped"    
    ERROR = "error"        

class RoutingStrategy(StrEnum):
    ROUND_ROBIN = "round_robin"
    LEAST_LOAD = "least_load"
    PRIORITY = "priority"

class Message(BaseModel):
    role: str
    content: str

class LLMInferRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False
    extra_params: Dict[str, Any] = Field(default_factory=dict)

class StreamChunk(BaseModel):
    content: str
    finish_reason: Optional[str] = None

class LLMInferResponse(BaseModel):
    id: str
    model: str
    content: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ModelMetadata(BaseModel):
    model_name: str
    weight_path: str
    max_context_len: int
    required_gpu_mem_gb: float
    supported_backends: List[str]
    priority: int = 10
    auto_cold_start: bool = False
    idle_timeout_sec: int = 300