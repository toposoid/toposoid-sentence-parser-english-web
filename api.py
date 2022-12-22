'''
  Copyright 2021 Linked Ideal LLC.[https://linked-ideal.com/]
 
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
 
      http://www.apache.org/licenses/LICENSE-2.0
 
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
 '''

from fastapi import FastAPI
from model import InputSentenceForParser, KnowledgeForParser, AnalyzedSentenceObjects
from SentenceParser import SentenceParser
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from logging import config
config.fileConfig('logging.conf')
import logging
LOG = logging.getLogger(__name__)
import traceback


app = FastAPI(
    title="toposoid-sentence-parser-english-web",
    version="0.1-SNAPSHOT"
)
parser = SentenceParser()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# This API isfor building KnoledgeBase
@app.post("/analyzeOneSentence")
def analyzeOneSentence(knowledgeForParser:KnowledgeForParser):
    try:
        aso = parser.parse(knowledgeForParser, "-1")
        return JSONResponse(content=jsonable_encoder(aso))
    except Exception as e:
        LOG.error(traceback.format_exc())
        return JSONResponse({"status": "ERROR", "message": traceback.format_exc()})

#This API is for inference
@app.post("/analyze")
def analyze(inputSentenceForParser:InputSentenceForParser):
    try:
        asos = []
        for knowledgeForParser in inputSentenceForParser.premise:
            asos.append(parser.parse(knowledgeForParser, "0"))
        for knowledgeForParser in inputSentenceForParser.claim:
            asos.append(parser.parse(knowledgeForParser, "1"))
        return JSONResponse(content=jsonable_encoder(AnalyzedSentenceObjects(analyzedSentenceObjects = asos)))
    except Exception as e:
        LOG.error(traceback.format_exc())
        return JSONResponse({"status": "ERROR", "message": traceback.format_exc()})

    