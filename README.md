## Distributed Caching System

### Overview
This project implements a distributed caching system using Redis, Flask for API Gateway, and Nginx as a Load Balancer. It supports high-speed data caching for large-scale applications.

### Features
- Redis cluster with automatic load balancing.
- Flask-based REST API for caching operations.
- Scalable architecture deployed on AWS Lambda or EC2.

### How to Run
1. **Docker Setup**
   ```bash
   docker-compose up
   ```

2. **Start Flask API**
   ```bash
   python app.py
   ```

3. **Access Endpoints**:
   - `POST /cache` to set cache.
   - `GET /cache/<key>` to retrieve cache.
