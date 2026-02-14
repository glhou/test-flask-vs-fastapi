from flask import Flask, jsonify
import asyncio

app = Flask(__name__)


async def worker_task(task_id):
    """
    Simulated I/O-bound task
    """
    await asyncio.sleep(2)  # simulate async I/O
    return {"task_id": task_id, "status": "done"}


@app.route("/test", methods=["GET"])
async def test():
    tasks = [worker_task(i) for i in range(5)]
    results = await asyncio.gather(*tasks)

    return jsonify({"results": results}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
