#include <stdint.h>
#include <stdlib.h>
#include <string.h>

// 64-bit FNV-1a hash for stable cross-platform key hashing.
uint64_t fnv1a_hash(const char *str) {
    uint64_t hash = 1469598103934665603ULL;
    const unsigned char *p = (const unsigned char *)str;
    while (*p) {
        hash ^= (uint64_t)(*p++);
        hash *= 1099511628211ULL;
    }
    return hash;
}

// Jump Consistent Hash (Lamping & Veach) to assign a key to a shard.
int jump_consistent_hash(uint64_t key, int num_buckets) {
    if (num_buckets <= 0) {
        return -1;
    }

    int64_t b = -1, j = 0;
    while (j < num_buckets) {
        b = j;
        key = key * 2862933555777941757ULL + 1;
        j = (int64_t)((double)(b + 1) * ((double)(1LL << 31) / (double)((key >> 33) + 1)));
    }
    return (int)b;
}

int shard_for_key(const char *key, int num_buckets) {
    uint64_t h = fnv1a_hash(key);
    return jump_consistent_hash(h, num_buckets);
}
