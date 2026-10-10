from src.core.serving.mock_engine import MockEngine
from src.utils.types import LLMInferRequest, LLMInferResponse, StreamChunk

def __init__(self):
    self.store : {'model':str, 'engine': 'MockEngine'} = dict()

def generate(self, request: LLMInferRequest) -> LLMInferResponse:
    chosen_engine = generate
    return 