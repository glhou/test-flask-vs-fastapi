from fastapi import FastAPI
import asyncio

app = FastAPI()


async def worker_task(task_id: int):
    """
    Simulated I/O-bound task
    """
    await asyncio.sleep(2)  # simulate async I/O
    return {"task_id": task_id, "status": "done"}


@app.get("/test")
async def test():
    tasks = [worker_task(i) for i in range(5)]
    results = await asyncio.gather(*tasks)

    return {"results": results}
