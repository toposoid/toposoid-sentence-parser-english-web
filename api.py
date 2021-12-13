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
from model import InputSentence, Knowledge, AnalyzedSentenceObjects
from SentenceParser import SentenceParser
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware


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
def analyzeOneSentence(knoledge:Knowledge):
    aso = parser.parse(knoledge.sentence, "-1")
    return JSONResponse(content=jsonable_encoder(aso))

#This API is for inference
@app.post("/analyze")
def analyze(inputSentence:InputSentence):
    asos = []
    for sentence in inputSentence.premise:
        asos.append(parser.parse(sentence, 0))
    for sentence in inputSentence.claim:
        asos.append(parser.parse(sentence, 1))
    return JSONResponse(content=jsonable_encoder(AnalyzedSentenceObjects(analyzedSentenceObjects = asos)))
    