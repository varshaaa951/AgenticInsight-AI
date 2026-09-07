import asyncio
import time
import httpx

# Worker function for fetching a single page
async def fetch_page(client: httpx.AsyncClient, url: str) -> str:
    start_time = time.perf_counter()
    
    # Await the async HTTP request without blocking the thread
    response = await client.get(url)
    
    elapsed = time.perf_counter() - start_time
    print(f"✓ Fetched {url} in {elapsed:.2f}s | Status Code: {response.status_code}")
    return response.text

# Main orchestrator function
async def main():
    urls = [
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/3"
    ]
    
    start_total = time.perf_counter()
    
    # Create a single persistent async client
    async with httpx.AsyncClient() as client:
        # Create a list of task coroutines
        tasks = [fetch_page(client, url) for url in urls]
        
        # Fire all requests concurrently
        await asyncio.gather(*tasks)
        
    total_time = time.perf_counter() - start_total
    print(f"\n⚡ Total execution time across all 5 requests: {total_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
    