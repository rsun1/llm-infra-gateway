from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os 
from ..utils.helpers import safe_yaml_load 
from pathlib import Path 


class ServerConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000 
    
class MonitoringConfig(BaseSettings):
    prometheus_port: int = 9090
    enable_tracing: bool = True 
    gpu_metric_interval_sec: int = 5 

class ColdStartConfig(BaseSettings):
    start_timeout_sec: int = 120
    warmup_prompt: str = 'hi'

class RoutingConfig(BaseSettings):
    default_strategy: str = "least_load"
    max_queue_size: int = 100 

class GlobalSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")
    
    server: ServerConfig = Field(default_factory=ServerConfig)
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)
    cold_start: ColdStartConfig = Field(default_factory=ColdStartConfig)
    routing: RoutingConfig = Field(default_factory=RoutingConfig)

    @classmethod
    def from_yaml(cls, path: str):
        if os.path.exists(path):
            data = safe_yaml_load(path)
            return cls(**data)
        return cls()

HERE = Path(__file__).parent
yaml_path = HERE / "settings.yaml"
settings = GlobalSettings.from_yaml(yaml_path)
