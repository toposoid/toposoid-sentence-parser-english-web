#!/bin/bash

cd /app/toposoid-sentence-parser-english-web
source /root/.local/bin/env
uv sync
uv run -- spacy download ${PIPELINES_MODEL}
uv run uvicorn api:app --reload --host 0.0.0.0 --port 9007
