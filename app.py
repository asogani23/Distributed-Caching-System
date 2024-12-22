from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

@app.route("/cache", methods=["POST"])
def set_cache():
    data = request.get_json()
    key = data["key"]
    value = data["value"]
    redis_client.set(key, value)
    return jsonify({"message": "Cache set successfully!"})

@app.route("/cache/<key>", methods=["GET"])
def get_cache(key):
    value = redis_client.get(key)
    if value is None:
        return jsonify({"error": "Key not found"}), 404
    return jsonify({"key": key, "value": value})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


