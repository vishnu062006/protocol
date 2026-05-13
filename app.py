import os
from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

# Load API key from environment variable
API_KEY = os.environ.get("API_KEY", "dev-secret-key-123")


# ─── Auth Decorator ───────────────────────────────────────────────────────────

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-KEY")
        if not key:
            return jsonify({
                "error": "Unauthorized",
                "message": "Missing X-API-KEY header"
            }), 401
        if key != API_KEY:
            return jsonify({
                "error": "Forbidden",
                "message": "Invalid API key"
            }), 403
        return f(*args, **kwargs)
    return decorated


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/sum", methods=["POST"])
@require_api_key
def sequential_sum():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Bad Request",
            "message": "Request body must be valid JSON"
        }), 400

    numbers = data.get("numbers")

    if numbers is None:
        return jsonify({
            "error": "Bad Request",
            "message": "Missing required field: 'numbers'"
        }), 400

    if not isinstance(numbers, list):
        return jsonify({
            "error": "Bad Request",
            "message": "'numbers' must be a list"
        }), 400

    if not all(isinstance(n, (int, float)) for n in numbers):
        return jsonify({
            "error": "Bad Request",
            "message": "All elements in 'numbers' must be numeric (int or float)"
        }), 400

    # Sequential sum
    total = 0
    for n in numbers:
        total += n

    return jsonify({
        "input": numbers,
        "result": total,
        "count": len(numbers)
    }), 200


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
