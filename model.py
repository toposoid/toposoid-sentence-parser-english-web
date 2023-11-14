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

from pydantic import BaseModel
from typing import Dict, List

'''
ref. https://github.com/toposoid/toposoid-knowledgebase-model
com.ideal.linked.toposoid.knowledgebase.regist.model
'''
class Reference(BaseModel):
    url:str
    surface:str 
    surfaceIndex:int 
    isWholeSentence:bool
    originalUrlOrReference:str

'''
ref. https://github.com/toposoid/toposoid-knowledgebase-model
com.ideal.linked.toposoid.knowledgebase.regist.model
'''
class ImageReference(BaseModel):
    reference:Reference
    x:int
    y:int
    weight:int 
    height:int

'''
ref. https://github.com/toposoid/toposoid-knowledgebase-model
com.ideal.linked.toposoid.knowledgebase.regist.model
'''
class KnowledgeForImage(BaseModel):
    id:str
    imageReference:ImageReference

'''
ref. https://github.com/toposoid/toposoid-knowledgebase-model
com.ideal.linked.toposoid.knowledgebase.regist.model
'''
class Knowledge(BaseModel):
    sentence:str
    lang:str
    extentInfoJson:str
    isNegativeSentence:bool
    knowledgeForImages:List[KnowledgeForImage] = []

'''
ref. https://github.com/toposoid/toposoid-deduction-protocol-model
com.ideal.linked.toposoid.protocol.model.parser
'''
class InputSentence(BaseModel):
    premise:List[Knowledge] 
    claim:List[Knowledge]

'''
ref. https://github.com/toposoid/toposoid-deduction-protocol-model
com.ideal.linked.toposoid.protocol.model.parser
'''
class KnowledgeForParser(BaseModel):
    propositionId:str
    sentenceId:str
    knowledge:Knowledge
'''
ref. https://github.com/toposoid/toposoid-deduction-protocol-model
com.ideal.linked.toposoid.protocol.model.parser
'''
class InputSentenceForParser(BaseModel):
    premise:List[KnowledgeForParser] 
    claim:List[KnowledgeForParser]

'''
ref. https://github.com/toposoid/toposoid-knowledgebase-model
com.ideal.linked.toposoid.knowledgebase.model
'''
class KnowledgeFeatureReference(BaseModel):
    id:str 
    featureType:int 
    url:str = ""
    source:str = ""
    featureInputType:int = 0    
    extentText:str = "{}"

'''
ref. https://github.com/toposoid/toposoid-knowledgebase-model
com.ideal.linked.toposoid.knowledgebase.model
'''
class LocalContext(BaseModel):
    lang: str
    namedEntity: str
    rangeExpressions: dict
    categories: dict
    domains: dict
    knowledgeFeatureReferences:List[KnowledgeFeatureReference]

'''
ref. https://github.com/toposoid/toposoid-knowledgebase-model
com.ideal.linked.toposoid.knowledgebase.model
'''
class PredicateArgumentStructure(BaseModel):
    currentId:int
    parentId:int
    isMainSection:bool
    surface:str
    normalizedName:str
    dependType:str
    caseType:str
    isDenialWord:bool
    isConditionalConnection:bool
    normalizedNameYomi:str
    surfaceYomi:str
    modalityType:str
    parallelType:str
    nodeType:int
    morphemes:List[str]

'''
ref. https://github.com/toposoid/toposoid-knowledgebase-model
com.ideal.linked.toposoid.knowledgebase.model
'''
class KnowledgeBaseNode(BaseModel):
    nodeId:str
    propositionId:str
    sentenceId:str
    predicateArgumentStructure:PredicateArgumentStructure
    localContext:LocalContext

'''
ref. https://github.com/toposoid/toposoid-knowledgebase-model
com.ideal.linked.toposoid.knowledgebase.model
'''
class KnowledgeBaseEdge(BaseModel):
    sourceId:str
    destinationId:str 
    caseStr:str
    dependType:str
    parallelType:str
    hasInclusion:bool
    logicType:str

'''
ref. https://github.com/toposoid/toposoid-knowledgebase-model
com.ideal.linked.toposoid.knowledgebase.model
'''
class LocalContextForFeature(BaseModel):
    lang: str
    knowledgeFeatureReferences:List[KnowledgeFeatureReference]

'''
ref. https://github.com/toposoid/toposoid-knowledgebase-model
com.ideal.linked.toposoid.knowledgebase.model
'''
class KnowledgeBaseSemiGlobalNode(BaseModel):
    nodeId: str
    propositionId: str
    sentenceId: str
    sentence: str
    sentenceType:int
    localContextForFeature: LocalContextForFeature

'''
ref. https://github.com/toposoid/toposoid-deduction-protocol-model
com.ideal.linked.toposoid.protocol.model.base
'''
class MatchedFeatureInfo(BaseModel):
    featureId:str
    similarity:float

'''
ref. https://github.com/toposoid/toposoid-deduction-protocol-model
com.ideal.linked.toposoid.protocol.model.base
'''
class MatchedPropositionInfo(BaseModel):
    propositionId:str 
    featureInfoList:List[MatchedFeatureInfo]

'''
ref. https://github.com/toposoid/toposoid-deduction-protocol-model
com.ideal.linked.toposoid.protocol.model.base
'''
class CoveredPropositionNode(BaseModel):    
    terminalId:str
    terminalSurface:str
    terminalUrl:str

'''
ref. https://github.com/toposoid/toposoid-deduction-protocol-model
com.ideal.linked.toposoid.protocol.model.base
'''
class CoveredPropositionEdge(BaseModel):
    sourceNode:CoveredPropositionNode
    destinationNode:CoveredPropositionNode

'''
ref. https://github.com/toposoid/toposoid-deduction-protocol-model
com.ideal.linked.toposoid.protocol.model.base
'''
class CoveredPropositionResult(BaseModel):
    deductionUnit:str
    propositionId:str 
    sentenceId:str
    coveredPropositionEdges:List[CoveredPropositionEdge]

'''
ref. https://github.com/toposoid/toposoid-deduction-protocol-model
com.ideal.linked.toposoid.protocol.model.base
'''
class DeductionResult(BaseModel):
    status:bool 
    matchedPropositionInfoList:List[MatchedPropositionInfo]
    deductionUnit:str
    coveredPropositionResult:CoveredPropositionResult
    havePremiseInGivenProposition:bool = False

'''
ref. https://github.com/toposoid/toposoid-deduction-protocol-model
com.ideal.linked.toposoid.protocol.model.base
'''
class AnalyzedSentenceObject(BaseModel):
    nodeMap:Dict[str, KnowledgeBaseNode]
    edgeList:List[KnowledgeBaseEdge]
    knowledgeBaseSemiGlobalNode:KnowledgeBaseSemiGlobalNode
    deductionResult:DeductionResult

'''
ref. https://github.com/toposoid/toposoid-deduction-protocol-model
com.ideal.linked.toposoid.protocol.model.base
'''
class AnalyzedSentenceObjects(BaseModel):
    analyzedSentenceObjects:List[AnalyzedSentenceObject]

'''
ref. https://github.com/toposoid/toposoid-knowledgebase-model
com.ideal.linked.toposoid.knowledgebase.nlp.model
'''
class SingleSentence(BaseModel):
    sentence: str

'''
ref. https://github.com/toposoid/toposoid-knowledgebase-model
com.ideal.linked.toposoid.knowledgebase.nlp.model
'''
class SurfaceInfo(BaseModel):
   surface: str
   index: int 