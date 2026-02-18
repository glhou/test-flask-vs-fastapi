from typing import Callable
import asyncio
import httpx
import time

URL = "http://0.0.0.0:5000/test"
BATCH = 10
TIMES = 100


async def worker(client: httpx.AsyncClient):
    try:
        response = await client.get(URL, timeout=20)
        return response.status_code
    except Exception as e:
        return str(e)


async def worker_bad(client: httpx.AsyncClient):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(URL, timeout=20)
        return response.status_code
    except Exception as e:
        return str(e)


async def run(client: httpx.AsyncClient, fn: Callable[[httpx.AsyncClient], int | str]):
    tasks = [asyncio.create_task(fn(client)) for _ in range(BATCH)]
    results = []
    for coro in asyncio.as_completed(tasks):
        results.append(await coro)
    return results


async def main():
    async with httpx.AsyncClient(limits=httpx.Limits(max_connections=100)) as client:
        start = time.monotonic()
        success_requests = 0
        coros = [asyncio.create_task(run(client, worker)) for _ in range(TIMES)]

        for results in await asyncio.gather(*coros):
            success_requests += sum(1 for r in results if r == 200)

        finish = time.monotonic() - start

        print(
            f"Sent {success_requests}/{TIMES * BATCH} successful requests in {finish} seconds"
        )

        coros = [asyncio.create_task(run(client, worker_bad)) for _ in range(TIMES)]

        for results in await asyncio.gather(*coros):
            success_requests += sum(1 for r in results if r == 200)

        finish = time.monotonic() - start

        print(
            f"Sent {success_requests}/{TIMES * BATCH} successful requests in {finish} seconds"
        )
        # OUTPUTS:
        # Sent 1000/1000 successful requests in 44.45776169099986 seconds
        # Sent 2000/1000 successful requests in 78.44145470199987 seconds


asyncio.run(main())
