# LLM Infra Gateway

> This project is a unified LLM scheduling gateway deployed on enterprise private servers. It connects front-end business systems with underlying LLM inference engines, exposing a unified standard API externally. It autonomously manages multiple large models: on-demand model startup, intelligent request dispatching, runtime status monitoring, and memory release for idle models. The design lowers operational overhead for maintaining multiple LLMs simultaneously.

## Background
Unlike simple OpenAI API wrappers, this project focuses on **underlying LLM inference engineering**: API gateway, adaptive routing, batched request scheduling, exact-match KV caching, cold start optimization, quantization pipelines, model version control, and end-to-end observability.

## Structure
- `src/api` - FastAPI and html routing
- `src/core/routing/` - model instances routing
-- `src/core/serving/` — batch_scheduler that combines multiple requests for batch inferences;kv_cache to enable fast inference when request prompt has been used before; backend_adapter that registers and calls for backend engine of a model based on instance. 
- `src/core/registry/` — Registers model with its stage and versions.
- `src/core/cold_start/` — manages warm up and cold start of models
- `src/monitoring/` — keeps track of performances such as latencies, cache hits/misses.

## How to run

本地：
```bash
python cli.py
```
By default it will run at 127.0.0.1:8000

Docker：
```bash
docker compose up
```

## Key design decisions


- Using batch execution when `max_batch_size` is reached or queue timeout hits, so that it can support future structure of processing multiple requests together to improve effiency with minimum impact on latency. (Currently it doesn't have vllm built in to batch inference, but as it currently stands it can support it in the future)
- Using kv_cache: Sometimes the same request prompts are being repeated used. To improve efficiency and reduce costs, kv_cache is implemented. So that when a new request prompt has been asked before, the system can use the same inference result without calling the LLM model again. It is using Least Recently Used (LRU) method and is limited with max_size of past requests and delete the least recently used ones. It is essentially an exact-match response caching with LRU eviction.
