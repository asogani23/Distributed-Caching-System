app = Flask(__name__)

# Connect to Redis
redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

@app.route('/cache', methods=['POST'])
def set_cache():
    data = request.json
    key = data.get('key')
    value = data.get('value')
    if not key or not value:
        return jsonify({"error": "Key and value are required"}), 400
    redis_client.set(key, value)
    return jsonify({"message": "Cache set successfully!"}), 201

@app.route('/cache/<key>', methods=['GET'])
def get_cache(key):
    value = redis_client.get(key)
    if value:
        return jsonify({"key": key, "value": value}), 200
    else:
        return jsonify({"error": "Key not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
