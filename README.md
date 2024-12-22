# Distributed Caching System

## Overview
This project implements a **distributed caching system** using **Flask** for the API layer and **Redis** for the caching backend. The system is containerized using **Docker**, making it scalable, portable, and easy to deploy in real-world environments.

---

## Key Features
- **Containerized Deployment**:
  The entire application runs inside Docker containers, ensuring consistency across environments.
- **Redis Integration**:
  Redis acts as the backend caching system, enabling low-latency data access.
- **RESTful API**:
  Provides endpoints for setting and retrieving cached key-value pairs.
- **Scalability**:
  Docker Compose allows seamless scaling of the app and Redis containers.
- **Performance Optimization**:
  Deployed a production-grade WSGI server (Gunicorn) to handle high-concurrency requests, reducing API response time by 17%.

---

## Setup Instructions

### Clone the Repository
```bash
git clone https://github.com/asogani23/Distributed-Caching-System.git
cd Distributed-Caching-System
Ensure Docker is Installed
Install Docker and Docker Compose: Docker Installation Guide
Build and Start Containers
bash
Copy code
docker-compose up --build
This will start the Flask app on localhost:5000 and Redis on localhost:6379.
Verify Containers are Running
bash
Copy code
docker ps
Ensure you see containers for the Flask app and Redis.
Example curl Commands
Set a Key-Value Pair
bash
Copy code
curl -X POST -H "Content-Type: application/json" \
-d '{"key": "test", "value": "123"}' \
http://localhost:5000/cache
Expected Response:

json
Copy code
{"message": "Cache set successfully!"}
Get a Value by Key
bash
Copy code
curl http://localhost:5000/cache/test
Expected Response:

json
Copy code
{"key": "test", "value": "123"}
Test Nonexistent Key
bash
Copy code
curl http://localhost:5000/cache/nonexistent
Expected Response:

json
Copy code
{"error": "Key not found"}
Performance Metrics
Initial Average Response Time (without Redis caching): 0.0288 seconds
Optimized Average Response Time (with Redis caching and Gunicorn): 0.0238 seconds
Performance Improvement: 17%
How It Was Achieved
Gunicorn Deployment:

Replaced Flask's development server with Gunicorn, a production-grade WSGI server, to handle high-concurrency requests.
Configured Gunicorn with 4 worker processes to optimize CPU utilization.
Redis Caching:

Integrated Redis to cache key-value pairs, reducing database query times for frequently accessed data.
Load Testing:

Conducted load testing with 1,000 requests to benchmark response times before and after optimization.
Technical Features Explained
Redis as a Caching Layer:
Redis stores key-value pairs for quick lookups, reducing the need for expensive database queries.
Flask API Layer:
Handles HTTP requests for setting and retrieving data, interacting with Redis as the backend.
Gunicorn Integration:
Used Gunicorn as a WSGI server to improve scalability and reduce response time under high load.
Dockerization:
Ensures the app and Redis run in isolated environments, removing dependencies on the host system.
Scalability:
The system can be scaled horizontally by increasing the number of app or Redis containers using Docker Compose.
Future Work
Add metrics monitoring for Redis and Flask using tools like Prometheus and Grafana.
Expand caching strategies for hierarchical or region-based cache partitioning.







