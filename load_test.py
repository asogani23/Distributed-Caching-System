import requests
import time
from concurrent.futures import ThreadPoolExecutor

# Configuration
API_URL = "http://127.0.0.1:5000/cache"
NUM_REQUESTS = 1000
CONCURRENT_WORKERS = 50

def set_cache_request():
    """Send a POST request to set cache."""
    try:
        data = {"key": "test_key", "value": "test_value"}
        response = requests.post(API_URL, json=data)
        return response.elapsed.total_seconds()
    except Exception as e:
        print(f"Error: {e}")
        return None

def load_test():
    """Perform load testing with concurrent requests."""
    times = []
    with ThreadPoolExecutor(max_workers=CONCURRENT_WORKERS) as executor:
        results = list(executor.map(lambda _: set_cache_request(), range(NUM_REQUESTS)))
        times.extend([r for r in results if r is not None])
    # Calculate performance metrics
    total_requests = len(times)
    avg_response_time = sum(times) / total_requests
    print(f"Total Requests: {total_requests}")
    print(f"Average Response Time: {avg_response_time:.4f} seconds")
    return avg_response_time

if __name__ == "__main__":
    print("Starting load test...")
    avg_time = load_test()
    print(f"Average Response Time: {avg_time:.4f} seconds")

