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

from fastapi.testclient import TestClient
from api import app
from model import AnalyzedSentenceObject, AnalyzedSentenceObjects, SurfaceInfo, TransversalState
import pytest
from functools import reduce
from fastapi.encoders import jsonable_encoder

#This is a unit test module
client = TestClient(app)
transversalState = str(jsonable_encoder(TransversalState(userId="test-user", username="guest", roleId=0, csrfToken = "")))

def test_PremiseAndClaimEmpty():
    try:
        response = client.post("/analyze",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": transversalState},
                            json={"premise": [], "claim": []})    
        assert response.status_code == 200
        asos = AnalyzedSentenceObjects.parse_obj(response.json())        
        assert len(asos.analyzedSentenceObjects) == 0
    except Exception:
        pytest.fail("Unexpected Error ..")


def test_PremiseOneSentenceAndClaimEmpty():
    response = client.post("/analyze",
                        headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": transversalState},
                        json={"premise": [{"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge":{"sentence": "The answer is blown'in the wind.", "lang": "en_US", "extentInfoJson": "{}", "isNegativeSentence":False, "knowledgeForImages": []}}], "claim": []})    
    assert response.status_code == 400
    assert "It is not possible to register only as a prerequisite. If you have any premises, please also register a claim." in str(response.json())


def test_PremiseEnmptyAndClaimOneSentence():
    response = client.post("/analyze",
                        headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": transversalState},
                        json={"premise": [], "claim": [{"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge":{"sentence": "The answer is blown'in the wind.","lang": "en_US", "extentInfoJson": "{}", "isNegativeSentence":False, "knowledgeForImages": []}}]})    
    assert response.status_code == 200
    asos = AnalyzedSentenceObjects.parse_obj(response.json())
    assert len(asos.analyzedSentenceObjects) == 1
    aso = asos.analyzedSentenceObjects[0]
    assert aso.knowledgeBaseSemiGlobalNode.sentenceType == 1
    scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.predicateArgumentStructure.currentId) 
    sentence =  reduce(lambda a, b: a + " " + b.predicateArgumentStructure.surface, scoresSorted, "")
    assert sentence.replace(" .", ".").strip() == "The answer is blown'in the wind."


def test_NegativeSimpleSentence():
    response = client.post("/analyze",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": transversalState},
                            json={"premise": [], "claim": [{"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge": {"sentence": "The problem does not seem soluble.", "lang":"en_US", "extentInfoJson": "{}", "isNegativeSentence":False, "knowledgeForImages": []}}]})    
    assert response.status_code == 200
    asos = AnalyzedSentenceObjects.parse_obj(response.json())
    for aso in asos.analyzedSentenceObjects:
        scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.predicateArgumentStructure.currentId)
        surfaces = []
        caseTypes = []
        denialIndex = -1
        for i, x in enumerate(scoresSorted):
            surfaces.append(x.predicateArgumentStructure.surface)
            caseTypes.append(x.predicateArgumentStructure.caseType)
            if x.predicateArgumentStructure.isDenialWord: denialIndex  = i
        sentence = " ".join(surfaces).replace(" .", ".")
        assert sentence == "The problem does not seem soluble."
        assert caseTypes == ['det', 'nsubj', 'aux', 'neg', 'ROOT', 'oprd', 'punct']
        assert denialIndex == 4 


def test_PremiseOneSentencetyAndClaimOneSentence():
    response = client.post("/analyze",
                        headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": transversalState},
                        json={"premise": [{"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge":{"sentence": "You may say I'm a dreamer, But I'm not the only one.","lang": "en_US", "extentInfoJson": "{}", "isNegativeSentence":False, "knowledgeForImages": []}}], "claim": [{"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge":{"sentence": "I hope someday you'll join us And the world will live as one.","lang":"en_US", "extentInfoJson": "{}", "isNegativeSentence":False, "knowledgeForImages": []}}]})    
    assert response.status_code == 200
    asos = AnalyzedSentenceObjects.parse_obj(response.json())
    assert len(asos.analyzedSentenceObjects) == 2
    for aso in asos.analyzedSentenceObjects:
        scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.predicateArgumentStructure.currentId) 
        sentence =  reduce(lambda a, b: a + " " + b.predicateArgumentStructure.surface, scoresSorted, "").replace(" .", ".").replace(" ,", ",").replace(" '", "'").strip()
        if aso.knowledgeBaseSemiGlobalNode.sentenceType == 0:
            assert sentence == "You may say I'm a dreamer, But I'm not the only one."
        elif aso.knowledgeBaseSemiGlobalNode.sentenceType == 1:
            assert sentence == "I hope someday you'll join us And the world will live as one."
        else:
            pytest.fail("Unexpected Error ..")

def test_PremiseMultipleSentencetyAndClaimMultipleSentence():
    response = client.post("/analyze",
                        headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": transversalState},
                        json={"premise": [{"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge":{"sentence": "Just The Way You Are!","lang": "en_US", "extentInfoJson": "{}", "isNegativeSentence":False, "knowledgeForImages": []}}, {"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge":{"sentence": "The answer is blown'in the wind.","lang": "en_US", "extentInfoJson": "{}", "isNegativeSentence":False, "knowledgeForImages": []}}], "claim": [{"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge":{"sentence": "You may say I'm a dreamer, But I'm not the only one.","lang": "en_US", "extentInfoJson": "{}", "isNegativeSentence":False, "knowledgeForImages": []}}, {"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge":{"sentence": "I hope someday you'll join us And the world will live as one.","lang": "en_US", "extentInfoJson": "{}", "isNegativeSentence":False, "knowledgeForImages": []}}]})    
    assert response.status_code == 200
    asos = AnalyzedSentenceObjects.parse_obj(response.json())
    assert len(asos.analyzedSentenceObjects) == 4
    for aso in asos.analyzedSentenceObjects:
        scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.predicateArgumentStructure.currentId) 
        sentence =  reduce(lambda a, b: a + " " + b.predicateArgumentStructure.surface, scoresSorted, "").replace(" .", ".").replace(" ,", ",").replace(" '", "'").strip()
        if aso.knowledgeBaseSemiGlobalNode.sentenceType == 0:
            assert sentence == "Just The Way You Are !" or sentence == "The answer is blown'in the wind."
        elif aso.knowledgeBaseSemiGlobalNode.sentenceType == 1:
            assert sentence == "You may say I'm a dreamer, But I'm not the only one." or sentence == "I hope someday you'll join us And the world will live as one."
        else:
            pytest.fail("Unexpected Error ..")


def test_SimpleSentenceWithQuantitativeExpressions0():
    response = client.post("/analyze",
                        headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": transversalState},
                        json={"premise": [], "claim": [{"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge": {"sentence": "His weight is 70kg.", "lang":"en_US", "extentInfoJson": "{}", "isNegativeSentence":False, "knowledgeForImages": []}}]})    
    assert response.status_code == 200
    asos = AnalyzedSentenceObjects.parse_obj(response.json())
    for aso in asos.analyzedSentenceObjects:
        scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.predicateArgumentStructure.currentId)
        surfaces = []
        caseTypes = []
        quantity = ""
        unit = ""
        range  = ""  
        prefix = ""  
        for x in scoresSorted:
            surfaces.append(x.predicateArgumentStructure.surface)
            caseTypes.append(x.predicateArgumentStructure.caseType)
            if "70" in x.localContext.rangeExpressions:
                quantity = x.localContext.rangeExpressions["70"]["quantity"]
                unit = x.localContext.rangeExpressions["70"]["unit"]
                range = x.localContext.rangeExpressions["70"]["range"]
                prefix = x.localContext.rangeExpressions["70"]["prefix"]
        sentence = " ".join(surfaces).replace(" .", ".")
        assert sentence == "His weight is 70 kg."
        assert quantity == "70.0"
        assert unit == "GRAM"
        assert range == "70.0"
        assert prefix == "KILO"

def test_SimpleSentenceWithQuantitativeExpressions1():
    response = client.post("/analyze",
                        headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": transversalState},
                        json={"premise": [], "claim": [{"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge":{"sentence": "His weight is over 70kg.","lang": "en_US", "extentInfoJson": "{}", "isNegativeSentence":False, "knowledgeForImages": []}}]})                           
    assert response.status_code == 200
    asos = AnalyzedSentenceObjects.parse_obj(response.json())
    for aso in asos.analyzedSentenceObjects:
        scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.predicateArgumentStructure.currentId)
        surfaces = []
        caseTypes = []
        quantity = ""
        unit = ""
        range  = ""    
        prefix = ""
        for x in scoresSorted:
            surfaces.append(x.predicateArgumentStructure.surface)
            caseTypes.append(x.predicateArgumentStructure.caseType)
            if "70" in x.localContext.rangeExpressions:
                quantity = x.localContext.rangeExpressions["70"]["quantity"]
                unit = x.localContext.rangeExpressions["70"]["unit"]
                range = x.localContext.rangeExpressions["70"]["range"]
                prefix = x.localContext.rangeExpressions["70"]["prefix"]
                
        sentence = " ".join(surfaces).replace(" .", ".")
        assert sentence == "His weight is over 70 kg."
        assert quantity == "70.0"
        assert unit == "GRAM"
        assert range == ">70.0"
        assert prefix == "KILO"

def test_SimpleSentenceWithQuantitativeExpressions2():
    response = client.post("/analyze",
                        headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": transversalState},
                        json={"premise": [], "claim": [{"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge":{"sentence": "Its stock price has risen by more than $ 10.", "lang":"en_US", "extentInfoJson": "{}", "isNegativeSentence":False, "knowledgeForImages": []}}]})    
    assert response.status_code == 200
    asos = AnalyzedSentenceObjects.parse_obj(response.json())
    for aso in asos.analyzedSentenceObjects:
        scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.predicateArgumentStructure.currentId)
        surfaces = []
        caseTypes = []
        quantity = ""
        unit = ""
        range  = ""    
        prefix = ""
        for x in scoresSorted:
            surfaces.append(x.predicateArgumentStructure.surface)
            caseTypes.append(x.predicateArgumentStructure.caseType)
            if "$ 10" in x.localContext.rangeExpressions:
                quantity = x.localContext.rangeExpressions["$ 10"]["quantity"]
                unit = x.localContext.rangeExpressions["$ 10"]["unit"]
                range = x.localContext.rangeExpressions["$ 10"]["range"]
                prefix = x.localContext.rangeExpressions["$ 10"]["prefix"]
                
        sentence = " ".join(surfaces).replace(" .", ".")
        assert sentence == "Its stock price has risen by more than $ 10."
        assert quantity == "10.0"
        assert unit == "DOLLER"
        assert range == ">$10.0"
        assert prefix == ""

def test_SimpleSentenceWithQuantitativeExpressions3():
    response = client.post("/analyze",
                        headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": transversalState},
                        json={"premise": [], "claim": [{"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge":{"sentence": "The height limit is 170cm.", "lang":"en_US", "extentInfoJson": "{}", "isNegativeSentence":False, "knowledgeForImages": []}}]})    
    assert response.status_code == 200
    asos = AnalyzedSentenceObjects.parse_obj(response.json())
    for aso in asos.analyzedSentenceObjects:
        scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.predicateArgumentStructure.currentId)
        surfaces = []
        caseTypes = []
        quantity = ""
        unit = ""
        range  = ""    
        prefix = ""
        for x in scoresSorted:
            surfaces.append(x.predicateArgumentStructure.surface)
            caseTypes.append(x.predicateArgumentStructure.caseType)
            if "170" in x.localContext.rangeExpressions:
                quantity = x.localContext.rangeExpressions["170"]["quantity"]
                unit = x.localContext.rangeExpressions["170"]["unit"]
                range = x.localContext.rangeExpressions["170"]["range"]
                prefix = x.localContext.rangeExpressions["170"]["prefix"]
                
        sentence = " ".join(surfaces).replace(" .", ".")
        assert sentence == "The height limit is 170 cm."
        assert quantity == "170.0"
        assert unit == "Metre"
        assert range == "170.0"
        assert prefix == "CENTI"
    
def test_SimpleSentenceWithQuantitativeExpressions4():
    response = client.post("/analyze",
                        headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": transversalState},
                        json={"premise": [], "claim": [{"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge":{"sentence": "The deadline was April 1, 2022.", "lang":"en_US", "extentInfoJson": "{}", "isNegativeSentence":False, "knowledgeForImages": []}}]})    
    #The deadline was April 1, 2022.
    #The deadline is from April 2022 to April 2023.
    assert response.status_code == 200
    asos = AnalyzedSentenceObjects.parse_obj(response.json())
    for aso in asos.analyzedSentenceObjects:
        scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.predicateArgumentStructure.currentId)
        surfaces = []
        caseTypes = []
        quantity = ""
        unit = ""
        range  = ""        
        for x in scoresSorted:
            surfaces.append(x.predicateArgumentStructure.surface)
            caseTypes.append(x.predicateArgumentStructure.caseType)
            if "April 1, 2022" in x.localContext.rangeExpressions:
                quantity = x.localContext.rangeExpressions["April 1, 2022"]["quantity"]
                unit = x.localContext.rangeExpressions["April 1, 2022"]["unit"]
                range = x.localContext.rangeExpressions["April 1, 2022"]["range"]
                
        sentence = " ".join(surfaces).replace(" .", ".")
        assert sentence == "The deadline was April 1 , 2022."
        assert quantity == "2022-04-01"
        assert unit == ""
        assert range == "2022-04-01"
    

def test_SimpleSentenceWithQuantitativeExpressions5():
    response = client.post("/analyze",
                        headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": transversalState},
                        json={"premise": [], "claim": [{"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge":{"sentence": "The deadline was 23:59:59.", "lang":"en_US", "extentInfoJson": "{}", "isNegativeSentence":False, "knowledgeForImages": []}}]})    
    assert response.status_code == 200
    asos = AnalyzedSentenceObjects.parse_obj(response.json())
    for aso in asos.analyzedSentenceObjects:
        scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.predicateArgumentStructure.currentId)
        surfaces = []
        caseTypes = []
        quantity = ""
        unit = ""
        range  = ""    
        
        for x in scoresSorted:
            surfaces.append(x.predicateArgumentStructure.surface)
            caseTypes.append(x.predicateArgumentStructure.caseType)
            if "23:59:59" in x.localContext.rangeExpressions:
                quantity = x.localContext.rangeExpressions["23:59:59"]["quantity"]
                unit = x.localContext.rangeExpressions["23:59:59"]["unit"]
                range = x.localContext.rangeExpressions["23:59:59"]["range"]
                
        sentence = " ".join(surfaces).replace(" .", ".")
        assert sentence == "The deadline was 23:59:59."
        assert quantity == "23:59:59"
        assert unit == ""
        assert range == "23:59:59"
        


def test_IrregularSimpleSentence():
    try:
        response = client.post("/analyze",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": transversalState},
                            json={"premise": [], "claim": [{"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge": {"sentence": "!#$%&Y'\"UIO\n strange =*+<H`OJWKFHgb", "lang":"en_US", "extentInfoJson": "{}", "isNegativeSentence":False, "knowledgeForImages": []}}]})    
        assert response.status_code == 200
        asos = AnalyzedSentenceObjects.parse_obj(response.json())
    
    except Exception:
        pytest.fail("Unexpected Error ..")


def test_Sprit():
    try:
        response = client.post("/split",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": transversalState},
                            json={"sentence": "The GrandCanyon was registered as a national park in 1919."})
        assert response.status_code == 200
        print(response.json())
        correctJson = [{'surface': 'GrandCanyon', 'index': 1}, {'surface': 'park', 'index': 7}]        
        assert(response.json()==correctJson)
    except Exception:
        pytest.fail("Unexpected Error ..")


'''
def test_SimpleSentenceWithConditionalClauses():
    response = client.post("/analyzeOneSentence",
                        headers={"Content-Type": "application/json"},
                        json={"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge": {"sentence": "If you heat ice, it melts.", "lang":"en_US", "extentInfoJson": "{}", "isNegativeSentence":False}})    
    assert response.status_code == 200
    aso = AnalyzedSentenceObject.parse_obj(response.json())
    scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.currentId)
    surfaces = []
    caseTypes = []
    nodeTypes = []
    for x in scoresSorted:
        surfaces.append(x.surface)
        caseTypes.append(x.caseType)
        nodeTypes.append(x.nodeType)
    sentence = " ".join(surfaces).replace(" .", ".").replace(" ,", ",")
    assert sentence == "If you heat ice, it melts."
    assert caseTypes == ['mark', 'nsubj', 'advcl', 'dobj', 'punct', 'nsubj', 'ROOT', 'punct']
    assert nodeTypes ==  [0, 0, 0, 0, 1, 1, 1, 1]
    
def test_SimpleSentenceWithConditionalClauses2():
    response = client.post("/analyzeOneSentence",
                        headers={"Content-Type": "application/json"},
                        json={"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge": {"sentence": "If you heat ice it melts.", "lang":"en_US", "extentInfoJson": "{}", "isNegativeSentence":False}})    
    assert response.status_code == 200
    aso = AnalyzedSentenceObject.parse_obj(response.json())
    scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.currentId)
    surfaces = []
    caseTypes = []
    nodeTypes = []
    for x in scoresSorted:
        surfaces.append(x.surface)
        caseTypes.append(x.caseType)
        nodeTypes.append(x.nodeType)
    sentence = " ".join(surfaces).replace(" .", ".").replace(" ,", ",")
    assert sentence == "If you heat ice it melts."
    assert caseTypes == ['mark', 'nsubj', 'ROOT', 'dobj', 'nsubj', 'relcl', 'punct']
    assert nodeTypes ==  [0, 0, 0, 0, 1, 1, 0]

def test_SimpleSentenceWithConditionalClauses3():
    response = client.post("/analyzeOneSentence",
                        headers={"Content-Type": "application/json"},
                        json={"propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414", "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170", "knowledge": {"sentence": "I didn't bring an umbrella, as the wind is so strong today.", "lang":"en_US", "extentInfoJson": "{}", "isNegativeSentence":False}})    
    assert response.status_code == 200
    aso = AnalyzedSentenceObject.parse_obj(response.json())
    scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.currentId)
    surfaces = []
    caseTypes = []
    nodeTypes = []
    for x in scoresSorted:
        surfaces.append(x.surface)
        caseTypes.append(x.caseType)
        nodeTypes.append(x.nodeType)
    sentence = " ".join(surfaces).replace(" .", ".").replace(" ,", ",")
    assert sentence == "I did n't bring an umbrella, as the wind is so strong today."
    assert caseTypes == ['nsubj', 'aux', 'neg', 'ROOT', 'det', 'dobj', 'punct', 'mark', 'det', 'nsubj', 'advcl', 'advmod', 'acomp', 'npadvmod', 'punct']
    assert nodeTypes ==  [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]
    
'''