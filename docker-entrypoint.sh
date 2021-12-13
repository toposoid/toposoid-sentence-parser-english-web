#!/bin/bash

cd /app/toposoid-sentence-parser-english-web
uvicorn main:app --reload --host 0.0.0.0 --port 9007
