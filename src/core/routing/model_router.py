from uuid import uuid4

class ModelRouter:
    def __init__(self):
        self.instances: dict[str, list[str]] = {}
        self.index: dict[str, int] = {}
    
    def register(self, model_name: str, instance_id: str) -> None:
        if model_name not in self.instances:
            self.instances[model_name] = []
        self.instances[model_name].append(instance_id)
        
    def round_robin(self, model_name: str) -> str:
        names = self.instances[model_name]
        point = self.index.get(model_name,0)
        idx = point % len(names)
        self.index[model_name] = point+1
        return self.instances[model_name][idx]
