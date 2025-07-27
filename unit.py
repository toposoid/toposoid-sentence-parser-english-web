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

import const
import re
from prefixUnit import getPrefixSymbol

const.GRAM = "GRAM"
const.GRAIN = "GRAIN"
const.DRUM = "DRUM"
const.OUNCE = "OUNCE"
const.POUND = "POUND"
const.STONE = "STONE"
const.TONNE = "TONNE"
const.METRE = "Metre"
const.INCH = "INCH"
const.FEET = "FEET"
const.YARD = "YARD"
const.MILE = "MILE"
const.ANGSTROEM = "ANGSTROEM"
const.SQUARE_METRE = "SQUARE_METRE"
const.ARE = "ARE"
const.HECTARE = "HECTARE"
const.ACRE = "ACRE"
#const.TSUBO = "TSUBO"
const.CUBIC_METRE = "CUBIC_METRE"
const.LITRE = "Litre"
const.GALLON = "GALLON"
const.QUART = "QUART"
const.PINT = "PINT"
const.BARREL = "BARREL"
const.GAUSS = "GAUSS"
const.BIT = "BIT"
const.BYTE = "BYTE"
const.YEAR = "Year"
const.WEEK = "Week"
const.MONTH = "Month"
const.DAY = "Day"
const.HOUR = "Hour"
const.MINUTE = "Minute"
const.SECOND = "Second"
const.YEN = "YEN"
const.DOLLER = "DOLLER"
const.EURO = "EURO"
const.PERCENT = "Percent"


UNIT_PATTERN = re.compile(r"^(y|z|a|f|p|n|μ|m|c|d|da|h|k|M|G|T|P|E|Z|Y)((?i)g|gram|gr|grain|dr|drum|oz|ounce|lb|pound|st|stone|t|tone|m|metre|in|inch|ft|feet|yd|yard|mile||m\u00B2|a|are|ha|hectare|\u33A5|L|l|litre|gal|gallon|qt|quart|pt|pint|bbl|barrel|G|gauss|bit|b|B|byte|year|month|week|day|hour|month|min|minute|sec|second|yen|%)$")
CURRENCY_PATTERN = "^(\$|€|¥|JPY)$"

def getUnitAndPrefixSymbol(unit):  
  preixSymbol = ""
  unitSymbol = ""    
  c = re.match(CURRENCY_PATTERN, unit)
  m = re.match(UNIT_PATTERN, unit)  
  if c:
    preixSymbol = ""
    unitSymbol = getUnitSymbol(c.group(1))
  elif m:
    preixSymbol = getPrefixSymbol(m.group(1))
    unitSymbol = getUnitSymbol(m.group(2))    
  return (preixSymbol, unitSymbol)

def getUnitSymbol(unit):
  unit = unit.lower()
  #|sec|second|yen|$|€|%)$
  if unit == "g" or unit == "gram":
    return const.GRAM    
  elif unit == "gr" or unit == "grain":
    return const.GRAIN
  elif unit == "dr" or unit == "drum":  
    return const.DRUM
  elif unit == "oz" or unit == "ounce":
    return const.OUNCE
  elif unit == "lb" or unit == "pound":
    return const.POUND
  elif unit == "st" or unit == "stone":
    return const.STONE
  elif unit == "t" or unit == "tone":
    return const.TONNE
  elif unit == "m" or unit == "metre":
    return const.METRE
  elif unit == "in" or unit == "inch":
    return const.INCH
  elif unit == "ft" or unit == "feet":
    return const.FEET
  elif unit == "yd" or unit == "yard":
    return const.YARD
  elif unit == "mile":
    return const.MILE
  elif unit == "Å":
    return const.ANGSTROEM
  elif unit == "m\u00B2":
    return const.SQUARE_METRE
  elif unit == "a" or unit == "are":
    return const.ARE
  elif unit == "ha" or unit == "hectare":
    return const.HECTARE
  elif unit == "\u33A5":
    return const.CUBIC_METRE
  elif unit == "L" or unit == "l" or unit == "ℓ" or unit == "litre":
    return const.LITRE
  elif unit == "gal" or unit == "gallon":
    return const.GALLON
  elif unit == "qt" or unit == "quart":
    return const.QUART
  elif unit == "pt" or unit == "pint":
    return const.PINT
  elif unit == "bbl" or unit == "barrel":
    return const.BARREL
  elif unit == "G" or unit == "gauss":
    return const.GAUSS
  elif unit == "b" or unit == "bit":
    return const.BIT
  elif unit == "B" or unit == "byte":
    return const.BYTE
  elif unit == "year":
    return const.YEAR
  elif unit == "month":
    return const.MONTH
  elif unit == "week":
    return const.WEEK
  elif unit == "day":
    return const.DAY
  elif unit == "hour":
    return const.HOUR
  elif unit == "min" or unit == "minute":
    return const.MINUTE
  elif unit == "sec" or unit == "second":
    return const.SECOND
  elif unit == "%":
    return const.PERCENT
  elif unit == "yen" or unit == "¥" or unit == "JPY":
    return const.YEN
  elif unit == "doller" or unit == "$":
    return const.DOLLER
  elif unit == "euro" or unit == "€":
    return const.EURO
  else:
    return ""
  