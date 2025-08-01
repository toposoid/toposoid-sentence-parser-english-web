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

import spacy
#from _model import KnowledgeForParser, KnowledgeBaseNode, LocalContext, PredicateArgumentStructure, KnowledgeBaseEdge, AnalyzedSentenceObject, DeductionResult, LocalContextForFeature, KnowledgeBaseSemiGlobalNode, CoveredPropositionResult, CoveredPropositionEdge
from ToposoidCommon.model import KnowledgeForParser, KnowledgeBaseNode, LocalContext, PredicateArgumentStructure, KnowledgeBaseEdge, AnalyzedSentenceObject, DeductionResult, LocalContextForFeature, KnowledgeBaseSemiGlobalNode, CoveredPropositionResult, CoveredPropositionEdge
from NamedEntityRecognition import NamedEntityRecognition
import re
import os

#This module takes a sentence as input and returns the words of dependencies
class SentenceParser():

    nlp = None
    namedEntityRecognition = None

    def __init__(self):
        self.nlp = spacy.load(os.environ["TOPOSOID_PARSER_SPACY_MODEL_EN"])
        self.namedEntityRecognition = NamedEntityRecognition()

    #Get negative expressions and clause expressions in sentences
    def extractPreInfo(self, doc):
        result = {"isDenialWord":[], "isConditionalConnection":[], "premiseNode":set()}
        for token in doc:
            if token.dep_ == "neg" and token.head != None:
                result["isDenialWord"].append(token.head.i)
            if token.pos_ == "SCONJ" and token.head != None:
                result["isConditionalConnection"].append(token.head.i)
                try:
                    #Not used at the moment
                    result["premiseNode"] = self.getPremiseNode(doc, token.head, {token.head.i}, token.head)
                except:
                    pass
        return result

    #Specify the range of clauses that express the premise
    def getPremiseNode(self, doc, targetToken, result, conditilnalToken):
        premiseNodes = list(filter(lambda x: x.head.i == targetToken.i and x.i > conditilnalToken.i and not x.dep_ in ["advcl", "relcl"], doc))
        result = result.union(set(map(lambda y: y.i, premiseNodes)))
        for node in premiseNodes:
            #if len(list(node.children)) > 0:
            # and not x.dep_ in ["advcl", "relcl"]
            for child in node.children:
                if not child.i in result:
                    #If there is a children's nodes which parent is the node, 
                    # go to search for the node recursively and get information until it reaches the end.
                    result = result.union(self.getPremiseNode(doc, node, result,conditilnalToken))
        return result


    # main function
    def parse(self, knowledgeForParser:KnowledgeForParser, sentenceType:int):

        doc = self.nlp(knowledgeForParser.knowledge.sentence)
        extractInfo = self.extractPreInfo(doc)    
        nodeMap = {}
        edgeList = []
        propositionId = knowledgeForParser.propositionId
        sentenceId = knowledgeForParser.sentenceId
        documentId = knowledgeForParser.knowledge.knowledgeForDocument.id
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
                knowledgeFeatureReferences = []
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
                parallelType = "-",
                nodeType = nodeType,
                morphemes = [token.pos_]
            )

            node = KnowledgeBaseNode(
                nodeId = sentenceId + "-" + str(token.i),
                propositionId = propositionId,
                sentenceId = sentenceId,
                predicateArgumentStructure = predicateArgumentStructure,
                localContext = localContext,
            )
            nodeMap[sentenceId + "-" + str(token.i)] = node
            
            if token.i != token.head.i:
                edgeList.append(KnowledgeBaseEdge(
                    sourceId = sentenceId + "-" + str(token.i),
                    destinationId = sentenceId + "-" + str(token.head.i),
                    caseStr = token.dep_,
                    dependType = "-",
                    parallelType = "-",
                    hasInclusion = isConditionalConnection,
                    logicType = "-"                    
                ))
        localContextForFeature = LocalContextForFeature(lang=knowledgeForParser.knowledge.lang, knowledgeFeatureReferences=[])
        knowledgeBaseSemiGlobalNode = KnowledgeBaseSemiGlobalNode(
            sentenceId = sentenceId, 
            propositionId = propositionId,
            documentId = documentId,
            sentence = knowledgeForParser.knowledge.sentence,
            sentenceType = sentenceType,
            localContextForFeature = localContextForFeature,            
        )

        defaultDeductionResult = DeductionResult(status=False, coveredPropositionResults = [])
        aso = AnalyzedSentenceObject(nodeMap=nodeMap, edgeList=edgeList, knowledgeBaseSemiGlobalNode=knowledgeBaseSemiGlobalNode, deductionResult=defaultDeductionResult)
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

