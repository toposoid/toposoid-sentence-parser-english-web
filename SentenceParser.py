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

import spacy
from model import KnowledgeForParser, KnowledgeBaseNode, LocalContext, PredicateArgumentStructure, KnowledgeBaseEdge, AnalyzedSentenceObject, DeductionResult
from NamedEntityRecognition import NamedEntityRecognition
import uuid

#This module takes a sentence as input and returns the words of dependencies
class SentenceParser():

    nlp = None
    namedEntityRecognition = None

    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')
        self.namedEntityRecognition = NamedEntityRecognition()

    #Get negative expressions and clause expressions in sentences
    def extractPreInfo(self, doc):
        result = {"isDenialWord":[], "isConditionalConnection":[], "premiseNode":set()}
        for token in doc:
            if token.dep_ == "neg" and token.head != None:
                result["isDenialWord"].append(token.head.i)
            if token.pos_ == "SCONJ" and token.head != None:
                result["isConditionalConnection"].append(token.head.i)
                result["premiseNode"] = self.getPremiseNode(doc, token.head, {token.head.i})
        return result

    #Specify the range of clauses that express the premise
    def getPremiseNode(self, doc, targetToken, result):
        premiseNodes = list(filter(lambda x: x.head.i == targetToken.i and not x.dep_ in ["advcl", "relcl"], doc))
        result = result.union(set(map(lambda y: y.i, premiseNodes)))
        for node in premiseNodes:
            #if len(list(node.children)) > 0:
            # and not x.dep_ in ["advcl", "relcl"]
            for child in node.children:
                if not child.i in result:
                    #If there is a children's nodes which parent is the node, 
                    # go to search for the node recursively and get information until it reaches the end.
                    result = result.union(self.getPremiseNode(doc, node, result))
        return result

    # main function
    def parse(self, knowledgeForParser:KnowledgeForParser, sentenceType:int):
        doc = self.nlp(knowledgeForParser.knowledge.sentence)
        extractInfo = self.extractPreInfo(doc)    
        nodeMap = {}
        edgeList = []
        propositionId = knowledgeForParser.propositionId
        sentenceId = knowledgeForParser.sentenceId
        beginIndex = 0        
        nerInfo = self.namedEntityRecognition.getNerAndSpanExpression(knowledgeForParser.knowledge.sentence)

        for token in doc:        
            if sentenceType == "-1": 
                #For registration
                nodeType = 1
                if "premiseNode" in  extractInfo and token.i in extractInfo["premiseNode"]:
                    nodeType = 0
            else:
                #For reasoning
                nodeType = sentenceType
            isDenial = False
            if "isDenialWord" in extractInfo and token.i in extractInfo["isDenialWord"]:
                isDenial = True
            isConditionalConnection = False
            if "isConditionalConnection" in extractInfo and token.i in extractInfo["isConditionalConnection"]:
                isConditionalConnection = True            
                        
            nerExp, rangeExp = self.extractNerAndRange(beginIndex, nerInfo)
            beginIndex = beginIndex + len(token.text) + 1

            localContext = LocalContext(
                lang = knowledgeForParser.knowledge.lang,
                namedEntity = nerExp,
                rangeExpressions = rangeExp,
                categories = {},
                domains = {},
                referenceIdMap = {}
            )
            
            predicateArgumentStructure = PredicateArgumentStructure(
                currentId = token.i,
                parentId = token.head.i,
                isMainSection = True,
                surface = token.text,
                normalizedName = token.lemma_,
                dependType = "-",
                caseType = token.dep_,
                isDenialWord = isDenial,
                isConditionalConnection = isConditionalConnection,
                surfaceYomi = "",
                normalizedNameYomi = "",
                modalityType =  "-",
                logicType = "-",
                nodeType = nodeType,
                morphemes = [token.pos_]
            )

            node = KnowledgeBaseNode(
                nodeId = sentenceId + "-" + str(token.i),
                propositionId = propositionId,
                sentenceId = sentenceId,
                predicateArgumentStructure = predicateArgumentStructure,
                localContext = localContext,
                extentText ="{}"
            )
            nodeMap[sentenceId + "-" + str(token.i)] = node
            
            if token.i != token.head.i:
                edgeList.append(KnowledgeBaseEdge(
                    sourceId = sentenceId + "-" + str(token.i),
                    destinationId = sentenceId + "-" + str(token.head.i),
                    caseStr = token.dep_,
                    dependType = "-",
                    logicType = "-",
                    lang = knowledgeForParser.knowledge.lang
                ))
            
        defaultDeductionResult = DeductionResult(status=False,matchedPropositionIds=[], deductionUnit="")
        aso = AnalyzedSentenceObject(nodeMap=nodeMap, edgeList=edgeList, sentenceType=sentenceType, sentenceId=knowledgeForParser.sentenceId, lang=knowledgeForParser.knowledge.lang, deductionResultMap={"0":defaultDeductionResult, "1":defaultDeductionResult})
        return aso

    #Get named entity and quantity range representation from words starting with a character index.
    def extractNerAndRange(self, beginIndex, nerInfo):
        nerExpression = ""
        rangeExpression = {"": {}}
        if len(nerInfo) == 0: return (nerExpression, rangeExpression)

        hitInfo = list(filter(lambda x: x["begin"] <= beginIndex and x['end'] >= beginIndex, nerInfo))
        if len(hitInfo) != 0:
            nerExpression = hitInfo[0]["ner"]
            rangeExpression = {hitInfo[0]["word"]:{"quantity":hitInfo[0]["quantity"], "unit":hitInfo[0]["unit"], "range":hitInfo[0]["range"],"prefix":hitInfo[0]["prefix"] }}        
        return (nerExpression, rangeExpression)

