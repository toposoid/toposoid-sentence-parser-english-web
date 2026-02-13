#!/bin/bash

cd /app/toposoid-sentence-parser-english-web
uv sync
uv run -- spacy download ${PIPELINES_MODEL}
uvicorn api:app --reload --host 0.0.0.0 --port 9007
