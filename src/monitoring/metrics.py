class MetricsCollector:
    def __init__(self):
        self.latencies: dict[str,list[float]] ={}
        self.cache_hits = 0
        self.cache_misses =0

        
    def record_request(self,model_name:str,latency_ms:float)->None:
        if model_name not in self.latencies:
            self.latencies[model_name] = []
        self.latencies[model_name].append(latency_ms)
    
    def get_request_count(self,model_name:str) -> int:
        return len(self.latencies[model_name])
    
    def get_avg_latency(self,model_name:str) -> float:
        if len(self.latencies[model_name]) ==0:
            avg_latency = 0.0
        else:
            avg_latency = sum(self.latencies[model_name])/len(self.latencies[model_name])
        return avg_latency
    
    def get_p95_latency(self,model_name:str)->float:
        sorted_latency = sorted(self.latencies[model_name])
        index = int(len(sorted_latency)*0.95)
        p95_latency = sorted_latency[index]
        return p95_latency
    
    def record_cache_hit(self)->None:
        self.cache_hits += 1
    
    def record_cache_miss(self) -> None:
        self.cache_misses += 1
        
    def get_cache_hit_ratio(self) -> float:
        if self.cache_hits + self.cache_misses == 0:
            return 0 
        ratio = self.cache_hits/(self.cache_hits+self.cache_misses)
        return ratio 