# syntax=docker/dockerfile:1

FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/app/.venv/bin:$PATH" \
    UV_LINK_MODE=copy \
    FLASK_ENV=production \
    FLASK_DEBUG=0

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY naas/ ./naas/

RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app

USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/healthz')"

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "naas.wsgi:app"]
