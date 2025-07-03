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

import requests
import json 
import re
import os 
from unit import getUnitAndPrefixSymbol

# This class is obliged to use Stanford CoreNLP to get the NER and range representation of numbers
class NamedEntityRecognition():
       
    def __init__(self):
        self.url = "http://" + os.environ["TOPOSOID_CORENLP_HOST"] + ":9000"        
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
                prefix = ""
                if "normalizedNER" in nerElement:
                    range = nerElement["normalizedNER"]
                    quantitiy = re.sub(r"[^\d.]", "", range)
                    if ner == "DATE":
                        quantitiy = nerElement["normalizedNER"]
                    elif ner == "TIME":
                        #remove first T
                        range = nerElement["normalizedNER"][1:]
                        quantitiy = nerElement["normalizedNER"][1:]

                    prefix, unit = self.getPrefixAndUnit(range, quantitiy, tokens[int(nerElement["tokenEnd"])])                    
                nerResult.append({"word":word, "ner":ner, "begin":begin, "end":end, "quantity":quantitiy, "unit":unit, "range":range, "prefix": prefix})                                 
        return nerResult

    #Attempt to get the unit of quantity expression
    def getPrefixAndUnit(self, range, quantitiy, nextToken):
        unit = range.replace(quantitiy, "").replace("<", "").replace(">", "").replace("=", "").strip()
        if unit == "":
            #If the CoreNLP normalized NER does not contain a unit,
            #The next word pos in the quantification expression gets that of NNS.
            if nextToken["pos"] == "NNS" or nextToken["pos"] == "NN":
                unit = nextToken["word"]
            
        return getUnitAndPrefixSymbol(unit)
