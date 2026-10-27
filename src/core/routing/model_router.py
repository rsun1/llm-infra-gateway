from uuid import uuid4

class ModelRouter:
    def __init__(self):
        self.instances: dict[str, list[str]] = {}
        self.index: dict[str, int] = {}
        self.latencies: dict[str, dict[str,float]] = {}
        self.costs: dict[str,dict[str,float]] = {}
        self.quality: dict[str,dict[str,float]] = {}
        self.health: dict[str,dict[str,bool]] = {}
        self.fallback_map: dict[str,str] = {}
    
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

    def record_latency(self,model_name:str, instance_id: str,latency_ms:float) -> None:
        if model_name not in self.latencies:
            self.latencies[model_name] = {}
        self.latencies[model_name][instance_id] = latency_ms 
        
    def latency_aware(self, model_name: str) -> str:
        names = self.instances[model_name]
        latencies_for_model = self.latencies.get(model_name,{})
        shortest = min(names, key= lambda name: latencies_for_model.get(name,float("inf")))
        return shortest
    
    def record_cost(self,model_name:str, instance_id:str,cost:float) -> None:
        if model_name not in self.costs:
            self.costs[model_name] = {}
        self.costs[model_name][instance_id] = cost 
    
    def cost_optimized(self,model_name:str,max_latency_ms: float) -> str:
        names=self.instances[model_name]
        latencies_for_model = self.latencies.get(model_name,{})
        costs_for_model =self.costs.get(model_name,{})
        candidates = []
        for n in names:
            if latencies_for_model.get(n,0)<= max_latency_ms:
                candidates.append(n)
        if not candidates:
            raise ValueError(f"no instance of {model_name} satisfies max_latency_ms={max_latency_ms}")
        else:
            cheapest = min(candidates,key=lambda c: costs_for_model.get(c,0))
        return cheapest
        
    def record_quality(self, model_name:str,instance_id:str,quality:float) -> None:
        if model_name not in self.quality:
            self.quality[model_name] = {}
        self.quality[model_name][instance_id] = quality
    
    def adaptive_weighted(
        self,
        model_name:str,
        w_latency:float = 0.4,
        w_cost:float = 0.3,
        w_quality: float = 0.3,
    ) -> str:
        names = self.instances[model_name]
        latencies_for_model = self.latencies.get(model_name,{})
        costs_for_model = self.costs.get(model_name,{})
        quality_for_model = self.quality.get(model_name,{})
        
        def score(name:str) -> float:
            name_latency = latencies_for_model.get(name,0)
            name_cost = costs_for_model.get(name,0)
            name_quality = quality_for_model.get(name,0)
        
            score = w_latency*name_latency + w_cost *name_cost - w_quality*name_quality
            return score 

        chosen = min(names,key=score)
        return chosen
    
    def record_health(self,model_name:str,instance_id:str,healthy:bool)->None:
        if model_name not in self.health:
            self.health[model_name] = {}
        self.health[model_name][instance_id] = healthy 
    
    def set_fallback(self,model_name:str,fallback_model_name:str) -> None:
        self.fallback_map[model_name] = fallback_model_name
        
    def get_healthy_instances(self, model_name:str) -> list[str]:
        names = self.instances.get(model_name,[])
        health_for_model = self.health.get(model_name,{})
        healthy_instances = []
        for n in names:
            if health_for_model.get(n,True):
                healthy_instances.append(n)
        return healthy_instances
    
    def route_with_fallback(self, model_name:str) -> str:
        healthy = self.get_healthy_instances(model_name)
        if healthy:
            point = self.index.get(model_name,0)
            idx = point % len(healthy)
            self.index[model_name] = point+1
            return healthy[idx]
        else:
            fallback_model = self.fallback_map.get(model_name)
            if fallback_model is not None:
                return self.route_with_fallback(fallback_model)
            else:
                raise ValueError(f"No available instances or models to use.")
            