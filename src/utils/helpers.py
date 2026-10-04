import time 
import yaml 
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import structlog 

def get_ts_ms() -> int:
    start = time.time()
    return int(start*1000)

def safe_yaml_load(path: str):
    with open(path, "r", encoding='utf-8') as f:
        return yaml.safe_load(f)

def async_retry(max_attempts: int=3):
    return retry(
        stop = stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1,min=1,max=5),
        reraise=True 
    )

def init_logger():
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ]
    )
    return structlog.get_logger()