import ctypes
import os
import time
from dataclasses import dataclass
from typing import List, Optional

import redis
from flask import Flask, jsonify, request

app = Flask(__name__)


@dataclass
class RedisShard:
    name: str
    client: redis.Redis


class DistributedCache:
    def __init__(self, shard_urls: List[str]):
        if not shard_urls:
            raise ValueError("At least one Redis shard URL is required")

        self._lib = self._load_hash_lib()
        self._shards: List[RedisShard] = []

        for idx, url in enumerate(shard_urls):
            client = redis.Redis.from_url(url, decode_responses=True)
            self._shards.append(RedisShard(name=f"shard-{idx}", client=client))

    @staticmethod
    def _load_hash_lib() -> Optional[ctypes.CDLL]:
        lib_path = os.getenv("HASH_LIB_PATH", "./libhashring.so")
        if not os.path.exists(lib_path):
            return None
        lib = ctypes.CDLL(lib_path)
        lib.shard_for_key.argtypes = [ctypes.c_char_p, ctypes.c_int]
        lib.shard_for_key.restype = ctypes.c_int
        return lib

    @property
    def shard_count(self) -> int:
        return len(self._shards)

    def _python_fallback_shard(self, key: str) -> int:
        # Stable fallback when native library isn't present.
        h = 1469598103934665603
        for b in key.encode("utf-8"):
            h ^= b
            h = (h * 1099511628211) & ((1 << 64) - 1)
        return h % self.shard_count

    def shard_index_for_key(self, key: str) -> int:
        if self._lib:
            idx = self._lib.shard_for_key(key.encode("utf-8"), self.shard_count)
            if idx >= 0:
                return idx
        return self._python_fallback_shard(key)

    def shard_for_key(self, key: str) -> RedisShard:
        return self._shards[self.shard_index_for_key(key)]

    def set(self, key: str, value: str, ttl_seconds: Optional[int] = None):
        shard = self.shard_for_key(key)
        if ttl_seconds is not None:
            shard.client.setex(key, ttl_seconds, value)
        else:
            shard.client.set(key, value)
        return shard

    def get(self, key: str):
        shard = self.shard_for_key(key)
        return shard, shard.client.get(key)

    def delete(self, key: str):
        shard = self.shard_for_key(key)
        deleted = shard.client.delete(key)
        return shard, deleted

    def stats(self):
        shard_stats = []
        for shard in self._shards:
            info = shard.client.info(section="stats")
            memory = shard.client.info(section="memory")
            shard_stats.append(
                {
                    "name": shard.name,
                    "keyspace_hits": info.get("keyspace_hits", 0),
                    "keyspace_misses": info.get("keyspace_misses", 0),
                    "used_memory_human": memory.get("used_memory_human", "unknown"),
                }
            )
        return shard_stats

    def health(self):
        health = []
        for shard in self._shards:
            start = time.perf_counter()
            try:
                pong = shard.client.ping()
                latency_ms = round((time.perf_counter() - start) * 1000, 2)
                health.append(
                    {
                        "name": shard.name,
                        "status": "ok" if pong else "degraded",
                        "latency_ms": latency_ms,
                    }
                )
            except redis.RedisError as exc:
                health.append({"name": shard.name, "status": "down", "error": str(exc)})
        return health


REDIS_SHARDS = os.getenv(
    "REDIS_SHARDS",
    "redis://redis-1:6379/0,redis://redis-2:6379/0,redis://redis-3:6379/0",
).split(",")
cache = DistributedCache([s.strip() for s in REDIS_SHARDS if s.strip()])


@app.route("/cache", methods=["POST"])
def set_cache():
    payload = request.get_json(silent=True) or {}
    key = payload.get("key")
    value = payload.get("value")
    ttl = payload.get("ttl_seconds")

    if not key or value is None:
        return jsonify({"error": "Both 'key' and 'value' are required"}), 400

    if ttl is not None:
        try:
            ttl = int(ttl)
            if ttl <= 0:
                raise ValueError
        except ValueError:
            return jsonify({"error": "ttl_seconds must be a positive integer"}), 400

    shard = cache.set(key=key, value=str(value), ttl_seconds=ttl)
    return jsonify({"message": "Cache set successfully", "shard": shard.name, "ttl_seconds": ttl}), 201


@app.route("/cache/<key>", methods=["GET"])
def get_cache(key: str):
    shard, value = cache.get(key)
    if value is None:
        return jsonify({"error": "Key not found", "key": key, "shard": shard.name}), 404
    return jsonify({"key": key, "value": value, "shard": shard.name}), 200


@app.route("/cache/<key>", methods=["DELETE"])
def delete_cache(key: str):
    shard, deleted = cache.delete(key)
    if not deleted:
        return jsonify({"error": "Key not found", "key": key, "shard": shard.name}), 404
    return jsonify({"message": "Key deleted", "key": key, "shard": shard.name}), 200


@app.route("/stats", methods=["GET"])
def stats():
    return jsonify({"shards": cache.stats(), "shard_count": cache.shard_count}), 200


@app.route("/health", methods=["GET"])
def health():
    data = cache.health()
    overall_ok = all(s.get("status") == "ok" for s in data)
    return jsonify({"status": "ok" if overall_ok else "degraded", "shards": data}), (200 if overall_ok else 503)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
