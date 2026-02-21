import random
import statistics
import time
from concurrent.futures import ThreadPoolExecutor

import requests

BASE_URL = "http://127.0.0.1:5000"
NUM_REQUESTS = 2000
CONCURRENT_WORKERS = 100
WRITE_RATIO = 0.3


def timed_request(method, path, payload=None):
    start = time.perf_counter()
    if method == "POST":
        response = requests.post(f"{BASE_URL}{path}", json=payload, timeout=5)
    elif method == "GET":
        response = requests.get(f"{BASE_URL}{path}", timeout=5)
    else:
        raise ValueError("Unsupported method")
    elapsed = time.perf_counter() - start
    return response.status_code, elapsed


def worker(i):
    key = f"key-{random.randint(1, 500)}"
    if random.random() < WRITE_RATIO:
        return timed_request("POST", "/cache", {"key": key, "value": f"value-{i}", "ttl_seconds": 180})
    return timed_request("GET", f"/cache/{key}")


def run_load_test():
    latencies = []
    status_counts = {}

    with ThreadPoolExecutor(max_workers=CONCURRENT_WORKERS) as pool:
        for status, latency in pool.map(worker, range(NUM_REQUESTS)):
            latencies.append(latency)
            status_counts[status] = status_counts.get(status, 0) + 1

    p50 = statistics.median(latencies)
    p95 = statistics.quantiles(latencies, n=20)[18]
    p99 = statistics.quantiles(latencies, n=100)[98]

    print(f"Requests: {NUM_REQUESTS}")
    print(f"Status counts: {status_counts}")
    print(f"Latency p50: {p50 * 1000:.2f} ms")
    print(f"Latency p95: {p95 * 1000:.2f} ms")
    print(f"Latency p99: {p99 * 1000:.2f} ms")


if __name__ == "__main__":
    run_load_test()
