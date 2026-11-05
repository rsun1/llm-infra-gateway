from src.core.serving.kv_cache import KVCacheManager 

def test_cache_miss_then_hit():
    cache = KVCacheManager(max_size=2)
    assert cache.get("key1") is None
    cache.put("key1","value1")
    assert cache.get("key1") == "value1"
    assert cache.hit_ratio() == 0.5 
    
def test_lru_eviction():
    cache = KVCacheManager(max_size=2)
    cache.put("a","1")
    cache.put("b","2")
    cache.put("c","3")
    assert cache.get("a") is None
    assert cache.get("b") == "2"
    assert cache.get("c") == "3"
    