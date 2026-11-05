import asyncio
import time
import httpx 

async def send_one_request(client: httpx.AsyncClient) -> float:
    start = time.time()
    await client.post(
        "http://127.0.0.1:8000/v1/chat/completions",
        json={"model":"mock-7b","messages": [{"role":"user","content":"test"}]},
    )
    return (time.time() - start) *1000 

async def main(num_requests: int):
    async with httpx.AsyncClient() as client:
        tasks = [send_one_request(client) for _ in range(num_requests)]
        start = time.time()
        latencies = await asyncio.gather(*tasks)
        total_time = time.time() - start 
        
        if total_time == 0:
            QPS = 0
        else:
            QPS = num_requests/total_time
        if len(latencies) == 0 :
            avg_latency = 0
        else:
            avg_latency = sum(latencies)/len(latencies)
        print(f"QPS: {QPS}, Average Latency: {avg_latency}")

if __name__ == "__main__":
    asyncio.run(main(20))