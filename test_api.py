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
from model import AnalyzedSentenceObject, AnalyzedSentenceObjects
import pytest
from functools import reduce

#This is a unit test module
client = TestClient(app)
def test_EmptySentence():
    try:
        response = client.post("/analyzeOneSentence",
                            headers={"Content-Type": "application/json"},
                            json={"sentence": "", "lang":"en_US", "extentInfoJson": "{}"})    
        assert response.status_code == 200
        aso = AnalyzedSentenceObject.parse_obj(response.json())        
    except Exception:
        pytest.fail("Unexpected Error ..")

def test_BasicSimpleSentence():
    response = client.post("/analyzeOneSentence",
                        headers={"Content-Type": "application/json"},
                        json={"sentence": "This is a simple test.", "lang":"en_US", "extentInfoJson": "{}"})    
    assert response.status_code == 200
    aso = AnalyzedSentenceObject.parse_obj(response.json())
    scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.currentId)
    surfaces = []
    caseTypes = []
    for x in scoresSorted:
        surfaces.append(x.surface)
        caseTypes.append(x.caseType)
    sentence = " ".join(surfaces).replace(" .", ".")
    assert sentence == "This is a simple test."
    assert caseTypes == ['nsubj', 'ROOT', 'det', 'amod', 'attr', 'punct']
    
def test_NegativeSimpleSentence():
    response = client.post("/analyzeOneSentence",
                            headers={"Content-Type": "application/json"},
                            json={"sentence": "The problem does not seem soluble.", "lang":"en_US", "extentInfoJson": "{}"})    
    assert response.status_code == 200
    aso = AnalyzedSentenceObject.parse_obj(response.json())
    scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.currentId)
    surfaces = []
    caseTypes = []
    denialIndex = -1
    for i, x in enumerate(scoresSorted):
        surfaces.append(x.surface)
        caseTypes.append(x.caseType)
        if x.isDenial: denialIndex  = i
    sentence = " ".join(surfaces).replace(" .", ".")
    assert sentence == "The problem does not seem soluble."
    assert caseTypes == ['det', 'nsubj', 'aux', 'neg', 'ROOT', 'oprd', 'punct']
    assert denialIndex == 4 


def test_SimpleSentenceWithConditionalClauses():
    response = client.post("/analyzeOneSentence",
                        headers={"Content-Type": "application/json"},
                        json={"sentence": "If you heat ice, it melts.", "lang":"en_US", "extentInfoJson": "{}"})    
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
                        json={"sentence": "If you heat ice it melts.", "lang":"en_US", "extentInfoJson": "{}"})    
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
                        json={"sentence": "I didn't bring an umbrella, as the wind is so strong today.", "lang":"en_US", "extentInfoJson": "{}"})    
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
    
def test_SimpleSentenceWithQuantitativeExpressions():
    response = client.post("/analyzeOneSentence",
                        headers={"Content-Type": "application/json"},
                        json={"sentence": "His weight is over 70kg.", "lang":"en_US", "extentInfoJson": "{}"})    
    assert response.status_code == 200
    aso = AnalyzedSentenceObject.parse_obj(response.json())
    scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.currentId)
    surfaces = []
    caseTypes = []
    quantity = ""
    unit = ""
    range  = ""    
    for x in scoresSorted:
        surfaces.append(x.surface)
        caseTypes.append(x.caseType)
        if "70" in x.rangeExpressions:
            quantity = x.rangeExpressions["70"]["quantity"]
            unit = x.rangeExpressions["70"]["unit"]
            range = x.rangeExpressions["70"]["range"]
             
    sentence = " ".join(surfaces).replace(" .", ".")
    assert sentence == "His weight is over 70 kg."
    assert quantity == "70.0"
    assert unit == "kg"
    assert range == ">70.0"


def test_SimpleSentenceWithQuantitativeExpressions():
    response = client.post("/analyzeOneSentence",
                        headers={"Content-Type": "application/json"},
                        json={"sentence": "His weight is over 70kg.", "lang":"en_US", "extentInfoJson": "{}"})    
    assert response.status_code == 200
    aso = AnalyzedSentenceObject.parse_obj(response.json())
    scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.currentId)
    surfaces = []
    caseTypes = []
    quantity = ""
    unit = ""
    range  = ""    
    for x in scoresSorted:
        surfaces.append(x.surface)
        caseTypes.append(x.caseType)
        if "70" in x.rangeExpressions:
            quantity = x.rangeExpressions["70"]["quantity"]
            unit = x.rangeExpressions["70"]["unit"]
            range = x.rangeExpressions["70"]["range"]
             
    sentence = " ".join(surfaces).replace(" .", ".")
    assert sentence == "His weight is over 70 kg."
    assert quantity == "70.0"
    assert unit == "kg"
    assert range == ">70.0"

def test_SimpleSentenceWithQuantitativeExpressions2():
    response = client.post("/analyzeOneSentence",
                        headers={"Content-Type": "application/json"},
                        json={"sentence": "Its stock price has risen by more than $ 10.", "lang":"en_US", "extentInfoJson": "{}"})    
    assert response.status_code == 200
    aso = AnalyzedSentenceObject.parse_obj(response.json())
    scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.currentId)
    surfaces = []
    caseTypes = []
    quantity = ""
    unit = ""
    range  = ""    
    for x in scoresSorted:
        surfaces.append(x.surface)
        caseTypes.append(x.caseType)
        if "$ 10" in x.rangeExpressions:
            quantity = x.rangeExpressions["$ 10"]["quantity"]
            unit = x.rangeExpressions["$ 10"]["unit"]
            range = x.rangeExpressions["$ 10"]["range"]
             
    sentence = " ".join(surfaces).replace(" .", ".")
    assert sentence == "Its stock price has risen by more than $ 10."
    assert quantity == "10.0"
    assert unit == "$"
    assert range == ">$10.0"


def test_IrregularSimpleSentence():
    try:
        response = client.post("/analyzeOneSentence",
                            headers={"Content-Type": "application/json"},
                            json={"sentence": "!#$%&Y'\"UIO\n strange =*+<H`OJWKFHgb", "lang":"en_US", "extentInfoJson": "{}"})    
        assert response.status_code == 200
        aso = AnalyzedSentenceObject.parse_obj(response.json())        
    except Exception:
        pytest.fail("Unexpected Error ..")


def test_PremiseAndClaimEmpty():
    try:
        response = client.post("/analyze",
                            headers={"Content-Type": "application/json"},
                            json={"premise": [], "claim": []})    
        assert response.status_code == 200
        asos = AnalyzedSentenceObjects.parse_obj(response.json())        
        assert len(asos.analyzedSentenceObjects) == 0
    except Exception:
        pytest.fail("Unexpected Error ..")


def test_PremiseOneSentenceAndClaimEmpty():
    response = client.post("/analyze",
                        headers={"Content-Type": "application/json"},
                        json={"premise": [{"sentence": "The answer is blown'in the wind.", "lang": "en_US", "extentInfoJson": "{}"}], "claim": []})    
    assert response.status_code == 200
    asos = AnalyzedSentenceObjects.parse_obj(response.json())
    assert len(asos.analyzedSentenceObjects) == 1
    aso = asos.analyzedSentenceObjects[0]
    assert aso.sentenceType == 0
    scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.currentId) 
    sentence =  reduce(lambda a, b: a + " " + b.surface, scoresSorted, "")
    assert sentence.replace(" .", ".").strip() == "The answer is blown'in the wind."


def test_PremiseEnmptyAndClaimOneSentence():
    response = client.post("/analyze",
                        headers={"Content-Type": "application/json"},
                        json={"premise": [], "claim": [{"sentence": "The answer is blown'in the wind.","lang": "en_US", "extentInfoJson": "{}"}]})    
    assert response.status_code == 200
    asos = AnalyzedSentenceObjects.parse_obj(response.json())
    assert len(asos.analyzedSentenceObjects) == 1
    aso = asos.analyzedSentenceObjects[0]
    assert aso.sentenceType == 1
    scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.currentId) 
    sentence =  reduce(lambda a, b: a + " " + b.surface, scoresSorted, "")
    assert sentence.replace(" .", ".").strip() == "The answer is blown'in the wind."

def test_PremiseOneSentencetyAndClaimOneSentence():
    response = client.post("/analyze",
                        headers={"Content-Type": "application/json"},
                        json={"premise": [{"sentence": "You may say I'm a dreamer, But I'm not the only one.","lang": "en_US", "extentInfoJson": "{}"}], "claim": [{"sentence": "I hope someday you'll join us And the world will live as one.","lang":"en_US", "extentInfoJson": "{}"}]})    
    assert response.status_code == 200
    asos = AnalyzedSentenceObjects.parse_obj(response.json())
    assert len(asos.analyzedSentenceObjects) == 2
    for aso in asos.analyzedSentenceObjects:
        scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.currentId) 
        sentence =  reduce(lambda a, b: a + " " + b.surface, scoresSorted, "").replace(" .", ".").replace(" ,", ",").replace(" '", "'").strip()
        if aso.sentenceType == 0:
            assert sentence == "You may say I'm a dreamer, But I'm not the only one."
        elif aso.sentenceType == 1:
            assert sentence == "I hope someday you'll join us And the world will live as one."
        else:
            pytest.fail("Unexpected Error ..")

def test_PremiseMultipleSentencetyAndClaimMultipleSentence():
    response = client.post("/analyze",
                        headers={"Content-Type": "application/json"},
                        json={"premise": [{"sentence": "Just The Way You Are!","lang": "en_US", "extentInfoJson": "{}"}, {"sentence": "The answer is blown'in the wind.","lang": "en_US", "extentInfoJson": "{}"}], "claim": [{"sentence": "You may say I'm a dreamer, But I'm not the only one.","lang": "en_US", "extentInfoJson": "{}"}, {"sentence": "I hope someday you'll join us And the world will live as one.","lang": "en_US", "extentInfoJson": "{}"}]})    
    assert response.status_code == 200
    asos = AnalyzedSentenceObjects.parse_obj(response.json())
    assert len(asos.analyzedSentenceObjects) == 4
    for aso in asos.analyzedSentenceObjects:
        scoresSorted = sorted(aso.nodeMap.values(), key=lambda x:x.currentId) 
        sentence =  reduce(lambda a, b: a + " " + b.surface, scoresSorted, "").replace(" .", ".").replace(" ,", ",").replace(" '", "'").strip()
        if aso.sentenceType == 0:
            assert sentence == "Just The Way You Are !" or sentence == "The answer is blown'in the wind."
        elif aso.sentenceType == 1:
            assert sentence == "You may say I'm a dreamer, But I'm not the only one." or sentence == "I hope someday you'll join us And the world will live as one."
        else:
            pytest.fail("Unexpected Error ..")
