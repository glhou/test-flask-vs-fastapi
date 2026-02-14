import asyncio
import httpx
import time

URL = "http://0.0.0.0:5000/test"
RATE = 1000
DURATION = 10


async def worker(client: httpx.AsyncClient):
    try:
        response = await client.get(URL, timeout=20)
        return response.status_code
    except Exception as e:
        return str(e)


async def main():
    async with httpx.AsyncClient() as client:
        start = time.monotonic()
        total_requests = 0
        success_requests = 0

        while time.monotonic() - start < DURATION:
            tick_start = time.monotonic()

            tasks = [worker(client) for _ in range(RATE)]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            total_requests += len(results)
            success_requests += sum(1 for r in results if r == 200)

            elapsed = time.monotonic() - tick_start
            await asyncio.sleep(max(0, 1 - elapsed))

        print(
            f"Sent {success_requests}/{total_requests} successful requests in {DURATION} seconds"
        )


asyncio.run(main())
