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

import requests
import json 
import re
import os 

# This class is obliged to use Stanford CoreNLP to get the NER and range representation of numbers
class NamedEntityRecognition():
       
    def __init__(self):
        self.url = "http://" + os.environ["CORENLP_HOST"] + ":9000"        
        self.headers = {'content-type': 'text/plain'}

    def getNerAndSpanExpression(self, sentence):
        nerResult = []       
        response = requests.post(self.url , data=sentence, headers=self.headers)
        result = json.loads(response.text)
        for sentenceDict in result["sentences"]:
            tokens = sentenceDict["tokens"]
            for nerElement in sentenceDict["entitymentions"]:
                word = nerElement["text"]                
                ner = nerElement["ner"] 
                begin = int(nerElement["characterOffsetBegin"]) 
                end = int(nerElement["characterOffsetEnd"])
                unit = ""
                quantitiy = ""
                range = ""
                if "normalizedNER" in nerElement:
                    range = nerElement["normalizedNER"]
                    quantitiy = re.sub(r"[^\d.]", "", range)                    
                    unit = self.getUnit(range, quantitiy, tokens[int(nerElement["tokenEnd"])])                    
                nerResult.append({"word":word, "ner":ner, "begin":begin, "end":end, "quantity":quantitiy, "unit":unit, "range":range})                                 
        return nerResult

    #Attempt to get the unit of quantity expression
    def getUnit(self, range, quantitiy, nextToken):
        unit = range.replace(quantitiy, "").replace("<", "").replace(">", "").replace("=", "").strip()
        if unit == "":
            #If the CoreNLP normalized NER does not contain a unit,
            #The next word pos in the quantification expression gets that of NNS.
            if nextToken["pos"] == "NNS":
                unit = nextToken["word"]
        return unit
