from types import SimpleNamespace

import app as app_module


class FakeCache:
    def __init__(self):
        self.store = {}
        self.shard_count = 3

    def set(self, key, value, ttl_seconds=None):
        self.store[key] = value
        return SimpleNamespace(name="shard-0")

    def get(self, key):
        return SimpleNamespace(name="shard-0"), self.store.get(key)

    def delete(self, key):
        exists = key in self.store
        if exists:
            del self.store[key]
        return SimpleNamespace(name="shard-0"), 1 if exists else 0

    def stats(self):
        return [{"name": "shard-0", "keyspace_hits": 1, "keyspace_misses": 0, "used_memory_human": "1M"}]

    def health(self):
        return [{"name": "shard-0", "status": "ok", "latency_ms": 1.0}]


def test_cache_endpoints():
    fake = FakeCache()
    app_module.cache = fake
    client = app_module.app.test_client()

    set_resp = client.post("/cache", json={"key": "a", "value": "1", "ttl_seconds": 20})
    assert set_resp.status_code == 201

    get_resp = client.get("/cache/a")
    assert get_resp.status_code == 200
    assert get_resp.get_json()["value"] == "1"

    delete_resp = client.delete("/cache/a")
    assert delete_resp.status_code == 200

    miss_resp = client.get("/cache/a")
    assert miss_resp.status_code == 404


def test_operational_endpoints():
    fake = FakeCache()
    app_module.cache = fake
    client = app_module.app.test_client()

    stats_resp = client.get("/stats")
    assert stats_resp.status_code == 200
    assert stats_resp.get_json()["shard_count"] == 3

    health_resp = client.get("/health")
    assert health_resp.status_code == 200
    assert health_resp.get_json()["status"] == "ok"
