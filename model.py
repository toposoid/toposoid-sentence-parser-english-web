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
class Knowledge(BaseModel):
    sentence:str
    lang:str
    extentInfoJson:str
    isNegativeSentence:bool

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
    logicType:str
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
    logicType:str
    lang:str

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
class KnowledgeFeatureNode(BaseModel):
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
class DeductionResult(BaseModel):
    status:bool 
    matchedPropositionInfoList:List[MatchedPropositionInfo]
    deductionUnit:str

'''
ref. https://github.com/toposoid/toposoid-deduction-protocol-model
com.ideal.linked.toposoid.protocol.model.base
'''
class AnalyzedSentenceObject(BaseModel):
    nodeMap:Dict[str, KnowledgeBaseNode]
    edgeList:List[KnowledgeBaseEdge]
    knowledgeFeatureNode:KnowledgeFeatureNode
    deductionResultMap:Dict[str, DeductionResult]

'''
ref. https://github.com/toposoid/toposoid-deduction-protocol-model
com.ideal.linked.toposoid.protocol.model.base
'''
class AnalyzedSentenceObjects(BaseModel):
    analyzedSentenceObjects:List[AnalyzedSentenceObject]