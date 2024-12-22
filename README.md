# Distributed Caching System

## Overview
This project implements a **distributed caching system** using **Flask** for the API layer and **Redis** for the caching backend. The system is containerized using **Docker**, making it scalable, portable, and easy to deploy.

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

---

## Setup Instructions

### Clone the Repository
```bash
git clone https://github.com/asogani23/Distributed-Caching-System.git
cd Distributed-Caching-System
Ensure Docker is Installed
Install Docker and Docker Compose:
Docker Installation Guide
Build and Start Containers
bash docker-compose up --build
This will start the Flask app on localhost:5000 and Redis on localhost:6379.

Verify Containers are Running
bash docker ps
Ensure you see containers for the Flask app and Redis.
