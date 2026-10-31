from enum import StrEnum
from datetime import datetime

class ModelStage(StrEnum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class ModelVersion:
    def __init__(self, model_name: str, version: str, stage: ModelStage):
        self.model_name = model_name
        self.version = version
        self.stage = stage
        self.registered_at = datetime.now()

class ModelRegistry:
    def __init__(self):
        self.versions: dict[str, list[ModelVersion]] = {}

    def register(self, model_name: str, version: str, stage: ModelStage) -> None:
        if model_name not in self.versions:
            self.versions[model_name] = []
        list_version = ModelVersion(model_name,version,stage)
        self.versions[model_name].append(list_version)

    def get_latest(self, model_name: str) -> ModelVersion:
        return self.versions[model_name][-1]

    def get_production_version(self, model_name: str) -> ModelVersion | None:
        for v in self.versions[model_name]:
            if v.stage == ModelStage.PRODUCTION:
                return v 
        return None

