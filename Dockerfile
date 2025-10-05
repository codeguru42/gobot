FROM ghcr.io/astral-sh/uv:python3.12-trixie
LABEL authors="codeguru"

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev
COPY src .
