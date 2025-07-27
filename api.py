'''
  Copyright (C) 2025  Linked Ideal LLC.[https://linked-ideal.com/]
 
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU Affero General Public License as
  published by the Free Software Foundation, version 3.
 
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Affero General Public License for more details.
 
  You should have received a copy of the GNU Affero General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from fastapi import FastAPI, Header
from ToposoidCommon.model import InputSentenceForParser, KnowledgeForParser, AnalyzedSentenceObjects, Knowledge, SingleSentence, SurfaceInfo, TransversalState
from SentenceParser import SentenceParser
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import ToposoidCommon as tc
from typing import Optional
LOG = tc.LogUtils(__name__)
import traceback


app = FastAPI(
    title="toposoid-sentence-parser-english-web",
    version="0.6-SNAPSHOT"
)
parser = SentenceParser()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#This API is for inference
@app.post("/analyze")
def analyze(inputSentenceForParser:InputSentenceForParser, X_TOPOSOID_TRANSVERSAL_STATE: Optional[str] = Header(None, convert_underscores=False)):
    transversalState = TransversalState.parse_raw(X_TOPOSOID_TRANSVERSAL_STATE.replace("'", "\""))
    try:                
        asos = []        
        if len(inputSentenceForParser.premise) > 0 and len(inputSentenceForParser.claim) == 0: return JSONResponse({"status": "ERROR", "message": "It is not possible to register only as a prerequisite. If you have any premises, please also register a claim."}, status_code = 400)        
        LOG.info("PREMISE:" + ",".join(list(map(lambda x: x.knowledge.sentence, inputSentenceForParser.premise))), transversalState)
        LOG.info("CLAIM:" + ",".join(list(map(lambda x: x.knowledge.sentence, inputSentenceForParser.claim))), transversalState)        

        for knowledgeForParser in inputSentenceForParser.premise:
            asos.append(parser.parse(knowledgeForParser, "0"))
        for knowledgeForParser in inputSentenceForParser.claim:
            asos.append(parser.parse(knowledgeForParser, "1"))
        response = JSONResponse(content=jsonable_encoder(AnalyzedSentenceObjects(analyzedSentenceObjects = asos)))
        LOG.info("Parsing completed.", transversalState)        
        return response
    except Exception as e:
        LOG.error(traceback.format_exc(), transversalState)
        return JSONResponse({"status": "ERROR", "message": traceback.format_exc()})

@app.post("/split")
def split(singleSentence:SingleSentence, X_TOPOSOID_TRANSVERSAL_STATE: Optional[str] = Header(None, convert_underscores=False)):
    transversalState = TransversalState.parse_raw(X_TOPOSOID_TRANSVERSAL_STATE.replace("'", "\""))    
    try:            
        LOG.info("SENTENCE:" + singleSentence.sentence, transversalState)
        if len(singleSentence.sentence) == 0 : return JSONResponse({"status": "ERROR", "message": "It is not possible to register only as a prerequisite. If you have any sentence."}, status_code = 400)
        knowledge = Knowledge(sentence=singleSentence.sentence, lang="", extentInfoJson="{}", isNegativeSentence=False)
        knowledgeForParser = KnowledgeForParser(propositionId = "", sentenceId="", knowledge=knowledge)        
        asos = parser.parse(knowledgeForParser, "1")
        predicateArgumentStructures = list(map(lambda x: x.predicateArgumentStructure, asos.nodeMap.values()))        
        candidates = list(filter(lambda x: "NOUN" in x.morphemes or "PROPN" in x.morphemes, predicateArgumentStructures))
        surfaceInfoList = list(map(lambda x: SurfaceInfo(surface=x.surface,index= x.currentId), candidates))
        response = JSONResponse(content=jsonable_encoder(surfaceInfoList))
        LOG.info("Splitting completed.", transversalState)
        return response
    except Exception as e:
        LOG.error(traceback.format_exc(), transversalState)
        return JSONResponse({"status": "ERROR", "message": traceback.format_exc()})
