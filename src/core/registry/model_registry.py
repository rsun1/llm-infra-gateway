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
        # key: model_name, value: 这个模型名下所有版本记录的列表
        self.versions: dict[str, list[ModelVersion]] = {}

    def register(self, model_name: str, version: str, stage: ModelStage) -> None:
        if model_name not in self.versions:
            self.versions[model_name] = []
        list_version = ModelVersion(model_name,version,stage)
        self.versions[model_name].append(list_version)

    def get_latest(self, model_name: str) -> ModelVersion:
        return self.versions[model_name][-1]

    def get_production_version(self, model_name: str) -> ModelVersion | None:
        # TODO 3: 从 self.versions[model_name] 里找 stage == ModelStage.PRODUCTION 的那个
        #   提示:可以用 for 循环遍历,找到就 return;循环结束还没找到就 return None
        for v in self.versions[model_name]:
            if v.stage == ModelStage.PRODUCTION:
                return v 
        return None

