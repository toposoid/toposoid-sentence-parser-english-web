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

import const
const.YOTTA = "YOTTA"
const.ZETTA = "ZETTA"
const.EXA = "EXA"
const.PETA = "PETA"
const.TERA = "TERA"
const.GIGA = "GIGA"
const.MEGA = "MEGA"
const.KILO = "KILO"
const.HECTO = "HECTO"
const.DEKA = "DEKA"
const.DECI = "DECI"
const.CENTI = "CENTI"
const.MILLI = "MILLI"
const.MICRO = "MICRO"
const.NANO = "NANO"
const.PICO = "PICO"
const.FEMTO = "FEMTO"
const.ATTO = "ATTO"
const.ZEPTO = "ZEPTO"
const.YOCTO = "YOCTO"



def getPrefixSymbol(prefix):

    if prefix == "y":
      return const.YOCTO
    elif prefix == "z":
      return const.ZEPTO
    elif prefix == "a":
      return const.ATTO
    elif prefix == "f":
      return const.FEMTO
    elif prefix == "p":
      return const.PICO
    elif prefix == "n":
      return const.NANO
    elif prefix == "μ":
      return const.MICRO
    elif prefix == "c":
      return const.CENTI
    elif prefix == "da":
      return const.DEKA
    elif prefix == "d":
      return const.DECI
    elif prefix == "h":
      return const.HECTO
    elif prefix == "k":
      return const.KILO
    elif prefix == "M":
      return const.MEGA
    elif prefix == "G":
      return const.GIGA
    elif prefix == "T":
      return const.TERA
    elif prefix == "P":
      return const.PETA
    elif prefix == "E":
      return const.EXA
    elif prefix == "Z":
      return const.ZETTA
    elif prefix == "Y":
      return const.YOTTA
    else:
      return prefix
    
