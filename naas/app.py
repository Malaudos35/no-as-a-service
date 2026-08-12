import json
import os
import random
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template

API_ROOT = "/api"
DATA_DIRECTORY = Path(__file__).resolve().parent

app = Flask(__name__)

cache: dict[tuple[str, str], list[Any]] = {}


def load_items(category: str, language: str) -> list[Any]:
    """Load and cache the items for a category and language."""
    cache_key = (category, language)

    if cache_key not in cache:
        file_path = DATA_DIRECTORY / category / f"{language}.json"

        with file_path.open(encoding="utf-8") as file:
            cache[cache_key] = json.load(file)

    return cache[cache_key]


def random_response(category: str, language: str):
    """Return a random item from the requested category."""
    try:
        items = load_items(category, language)
        return jsonify(reason=random.choice(items))
    except FileNotFoundError:
        return jsonify(error="Language not supported"), 404
    except (json.JSONDecodeError, IndexError):
        return jsonify(error="No response available"), 500


@app.get("/")
def home():
    return render_template("reason.html", root=API_ROOT)


@app.get("/healthz")
def healthz():
    return jsonify(status="ok"), 200


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    if os.getenv("FORCE_HTTPS", "false").lower() in ("1", "true", "yes"):
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains; preload"
        )
    return response


@app.get(f"{API_ROOT}/no")
def no():
    return render_template("reason.html", root=API_ROOT)


@app.get(f"{API_ROOT}/no/<language>")
def get_random_reason(language: str):
    return random_response("reason", language)


@app.get(f"{API_ROOT}/hireme")
def hireme():
    return render_template("hireme.html", root=API_ROOT)


@app.get(f"{API_ROOT}/hireme/<language>")
def get_random_hireme(language: str):
    return random_response("hireme", language)


@app.get(f"{API_ROOT}/dateme")
def dateme():
    return render_template("dateme.html", root=API_ROOT)


@app.get(f"{API_ROOT}/dateme/<language>")
def get_random_dateme(language: str):
    return random_response("dateme", language)
