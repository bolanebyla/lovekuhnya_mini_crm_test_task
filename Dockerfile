FROM python:3.13-slim AS base

RUN pip install uv

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock README.md ./

RUN uv pip install --system . \
  && apt-get purge -y build-essential \
  && rm -rf /var/lib/apt/lists/*

FROM python:3.13-slim AS runtime

COPY ./entrypoints/entrypoint*.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint*.sh

COPY --from=base /usr/local /usr/local
COPY --from=base /app /app

WORKDIR /app
ENV PYTHONPATH=/app/src
