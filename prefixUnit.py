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
    
