FROM python:3.13-slim

ENV APP_PATH="/app"

WORKDIR $APP_PATH

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv==0.5.7

COPY pyproject.toml ./
COPY main.py ./
COPY src/ ./src

RUN uv venv .venv && uv sync --no-dev

EXPOSE 8000

ENTRYPOINT [".venv/bin/python", "main.py"]
