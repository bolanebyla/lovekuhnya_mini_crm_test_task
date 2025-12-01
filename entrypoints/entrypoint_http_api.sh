#!/usr/bin/env bash
set -e
if [ -z "$API_LOG_LEVEL" ]; then
  API_LOG_LEVEL=info
fi
if [ -z "$API_PORT" ]; then
  API_PORT=8080
fi

uvicorn mini_crm.run.http_api:app --proxy-headers --host 0.0.0.0 --port "$API_PORT" --log-level "$API_LOG_LEVEL" --forwarded-allow-ips '*'
