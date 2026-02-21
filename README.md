# Distributed Caching System (C + Python + Redis)

A production-style distributed caching service with:
- **C-powered consistent hashing** (Jump Hash + FNV-1a) for stable shard routing,
- **Flask API + Gunicorn** for scalable HTTP serving,
- **Redis sharding** across multiple nodes,
- **Operational endpoints** for health + stats,
- **Docker Compose orchestration** for local distributed deployment.

---

## Architecture

- `app.py` exposes API endpoints and orchestrates cache operations.
- `hash_ring.c` provides high-performance native shard selection via a compiled shared library.
- Three Redis instances (`redis-1`, `redis-2`, `redis-3`) serve as distributed cache shards.
- `load_test.py` performs concurrent mixed read/write load testing and reports p50/p95/p99 latency.

### Why this is stronger for SWE recruiting

This project now demonstrates:
- **Systems-level C programming** integrated into a higher-level service,
- **Distributed systems concepts** (sharding, deterministic routing, fault visibility),
- **Backend production practices** (Gunicorn, health checks, metrics endpoints),
- **Performance mindset** (latency distribution, not just average latency).

---

## API

### `POST /cache`
Set cache value with optional TTL.

Request:
```json
{
  "key": "session:123",
  "value": "payload",
  "ttl_seconds": 300
}
```

### `GET /cache/<key>`
Get value by key.

### `DELETE /cache/<key>`
Delete key.

### `GET /health`
Shard-level health and ping latency.

### `GET /stats`
Shard-level cache stats including keyspace hits/misses and memory usage.

---

## Run locally

```bash
docker-compose up --build
```

Service endpoints:
- App: `http://localhost:5000`
- Redis shards: `6379`, `6380`, `6381`

Example:

```bash
curl -X POST http://localhost:5000/cache \
  -H "Content-Type: application/json" \
  -d '{"key":"user:42","value":"gold","ttl_seconds":120}'

curl http://localhost:5000/cache/user:42
curl http://localhost:5000/health
curl http://localhost:5000/stats
```

---

## Load test

```bash
python load_test.py
```

Outputs:
- status-code distribution,
- latency p50/p95/p99.

---

## Resume-ready bullet options (ATS-friendly)

- Built a **distributed cache service** with **C-based consistent hashing** (Jump Hash + FNV-1a) to deterministically route keys across 3 Redis shards, improving key distribution and minimizing remapping during scaling events.
- Engineered a **low-latency caching API** (Flask + Gunicorn + Redis) with TTL support, delete semantics, and operational `/health` + `/stats` endpoints for shard-level observability.
- Containerized a multi-node cache stack with Docker Compose and stress-tested with 2,000 concurrent mixed R/W requests, reporting p50/p95/p99 to guide performance tuning.

---

## Tech stack

- **Languages**: C, Python
- **Infra/Runtime**: Docker, Docker Compose, Gunicorn
- **Data systems**: Redis
- **Testing**: Pytest
