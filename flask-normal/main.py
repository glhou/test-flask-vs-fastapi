from flask import Flask, jsonify
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

app = Flask(__name__)

# Thread pool (reuse threads instead of creating new ones each time)
executor = ThreadPoolExecutor(max_workers=5)


def worker_task(task_id):
    """
    Simulated I/O-bound task
    """
    thread_name = threading.current_thread().name
    time.sleep(2)  # simulate slow I/O (API call, DB, etc.)
    return {"task_id": task_id, "thread": thread_name, "status": "done"}


@app.route("/test", methods=["GET"])
def test():
    futures = [executor.submit(worker_task, i) for i in range(5)]

    results = []
    for future in as_completed(futures):
        results.append(future.result())

    return jsonify({"results": results}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
