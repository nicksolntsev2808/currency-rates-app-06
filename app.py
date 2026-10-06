import os

import requests
from flask import Flask, jsonify

from rates import build_url, format_rates, is_valid_code

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"service": "currency-rates", "usage": "/rates/<BASE>, например /rates/USD"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/rates/<base>")
def rates(base):
    base = base.upper()
    if not is_valid_code(base):
        return jsonify({"error": "base must be a 3-letter currency code"}), 400

    try:
        response = requests.get(build_url(base), timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        return jsonify({"error": "upstream request failed", "details": str(exc)}), 502

    return jsonify(format_rates(base, response.json()))


if __name__ == "__main__":
    host = os.environ.get("APP_HOST", "127.0.0.1")
    port = int(os.environ.get("APP_PORT", "6100"))
    app.run(host=host, port=port)
