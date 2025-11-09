#!/usr/bin/env sh
set -e

# Default values
: ${UVICORN_WORKERS:=2}
: ${HOST:=0.0.0.0}
: ${PORT:=8000}

echo "Starting uvicorn with ${UVICORN_WORKERS} workers on ${HOST}:${PORT}"

exec uvicorn main:app --host ${HOST} --port ${PORT} --workers ${UVICORN_WORKERS} --proxy-headers
