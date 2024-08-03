#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Symbolic expression 3

    Copyright (C) 2021 Gien van den Enden - swvandenenden@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


    MathMl: https://www.mathjax.org/
            https://elsenaju.eu/mathml/MathML-Examples.htm
            https://www.w3.org/TR/MathML3/mathml.pdf

    Math html editor:
            http://mathquill.com/

    Python documentation tools:
            https://wiki.python.org/moin/DocumentationTools
            https://pdoc3.github.io/pdoc/
            https://pylint.readthedocs.io/en/stable/

    PrimeFac:
            https://pypi.org/project/primefac/               (orginal)
            https://github.com/elliptic-shiho/primefac-fork  (python3 version)

            https://stackoverflow.com/questions/32871539/integer-factorization-in-python


    Example documentenion:
            pdoc3 --html symexpress3

    Sin/Cos information:
             https://en.wikipedia.org/wiki/Trigonometric_functions
             https://en.wikipedia.org/wiki/Sine
             https://en.wikipedia.org/wiki/Inverse_trigonometric_functions
             https://en.wikipedia.org/wiki/List_of_trigonometric_identities
             https://de.wikipedia.org/wiki/Formelsammlung_Trigonometrie
             https://en.wikipedia.org/wiki/Atan2
             https://www.rapidtables.com/math/trigonometry/arctan.html
             https://brilliant.org/wiki/triple-angle-identities/
             https://mathworld.wolfram.com/Multiple-AngleFormulas.html
             https://www.wolframalpha.com/

             https://www.quora.com/Is-there-a-method-to-calculate-cos-%CF%80-7-and-sin-%CF%80-7
             https://www.quora.com/What-is-the-formula-for-sin-x-3-one-third-angle-formula

    Online calculators:
             https://www.wolframalpha.com/
             https://www.calculatorsoup.com/calculators/algebra/
             https://live.sympy.org/

    Cubic root equation
             https://en.wikipedia.org/wiki/Cubic_equation

    Square root complex number:
             https://math.stackexchange.com/questions/44406/how-do-i-get-the-square-root-of-a-complex-number

    Radicals complex number explained
             https://people.math.wisc.edu/~angenent/Free-Lecture-Notes/freecomplexnumbers.pdf

    Principal root
             https://math.stackexchange.com/questions/1385255/properties-of-the-principal-square-root-of-a-complex-number
"""

# internal build number, for version number see version.py
__buildnumber__ = "20240803001" # build number


import sys
import math
# import cmath

from abc       import ABC, abstractmethod
from threading import Thread
# multiprocess is not working with this solutions
# from multiprocessing import Process
# import multiprocessing as mp
# from queue     import Queue

from symexpress3 import symtables


# Classes:
# - SymNumber      : Number
# - SymVariable    : Variable
# - SymExpress     : The symbolic expression\
# - SymArray       : Array of SymExpress
#
# - SymBase        : Base class
# - SymBasePower   : Quotation handling for factor and power
# - SymBaseList    : List base


# mathml colors
colorposroot   = "#429e00"  # green, for roots with only one positve value
colorallroot   = "#000000"  # black, for roots with multiple values

fixedVariables      = {} # dictionary of fixed variables

# threads are slower then non-threads... to do (factor 9 for the test-script is len > 1)
globalUseThreads    = False # use thread, see _optSubThread()



def RegisterOptimzeActions():
  """
  Register all the optimize actions
  """
  # symRegisterFunctions.SymRegisterFunctions()
  # symRegisterOptimize.SymRegisterOptimize()
  # symRegisterOptSymNumber.SymRegisterOptimize()
  # symRegisterOptSymVariable.SymRegisterOptimize()
  # symRegisterOptSymFunction.SymRegisterOptimize()

def GetAllOptimizeActions():
  """
  Get all the optimize actions in a dictionary [key]=description
  """
  result = {}
  for key, value  in symtables.optSymAnyTable.items():
    result[ key ] = value.description

  for key, value  in symtables.optSymNumberTable.items():
    result[ key ] = value.description

  for key, value  in symtables.optSymVariableTable.items():
    result[ key ] = value.description

  for key, value  in symtables.optSymFunctionTable.items():
    result[ key ] = value.description

  for key, value  in symtables.optimizeTable.items():
    result[ key ] = value.description

  for key, value  in symtables.functionTable.items():
    result[ "functionToValue_" + key ] = value.description

  # fixed values
  result[ "functionToValues"        ] = 'Convert functions to values'
  # result[ "functionToComplexValues" ] = 'Convert functions to compex values'
  result[ "setOnlyOne"              ] = "All radcials are principal"


  return result

def GetAllFunctions():
  """
  Get all the functions in a dictionary [key]=description
  """
  result = {}
  for objFunc in symtables.functionTable.values():
    key = objFunc.syntax
    if key == None:
      key = objFunc.name
    result[ key ] = objFunc.description

  return result


def GetFixedVariables():
  """
  Get dictionary of fixed defined variables ( [variable name] = description
  """
  if len( fixedVariables) > 0:
    return fixedVariables

  fixedVariables[ "pi"       ] = "π"
  fixedVariables[ "i"        ] = "Imaginary number"
  fixedVariables[ "e"        ] = "Euler's number"
  fixedVariables[ "infinity" ] = "∞"

  return fixedVariables

#
# base class for the SymExpress2 module
#
class SymBase( ABC ):
  """
  Abstract class that is the base of all symexpress classes
  """
  # def __init__( self ):
  #  # self.elements = [] # pylint needed this


  @abstractmethod
  def optimize( self, cAction = None ):
    """
    Optimize the expression. cAction = None is the default optimization
    """
    # pass

  @abstractmethod
  def isEqual( self, elem, checkFactor = True, checkPower = True ):
    """
    Check if the given object is equal to this object.
    Return True for equal and False for not equal
    """
    # pass

  @abstractmethod
  def copy(self):
    """
    Make a copy of this expression
    """
    # pass

  @abstractmethod
  def mathMl( self ):
    """
    Give the expression in MathMl format
    """
    # pass

  @abstractmethod
  def getVariables( self ):
    """
    Get all the variables in and give it back in a dictionary &lt;variable&gt;:&lt;number of times found&gt;
    """
    # pass


  @abstractmethod
  def getFunctions( self ):
    """
    Get all the functions in and give it back in a dictionary &lt;function&gt;:&lt;number of times found&gt;
    """
    # pass

  @abstractmethod
  def replaceVariable( self, dDict ):
    """
    Replace variables in the given dictionary.
    \nkey = name variable, value = string for SymFormulaParser
    """
    # pass


  @abstractmethod
  def getValue( self, dDict = None):
    """
    Get the value of the expression
    \nkey = name variable, value = value of the variable
    \nThe follow variables are predefined: i, pi, e
    """
    # pass


  # check if this type is equal to an expression of type *, with 2 elements, 1 number and 1 type
  # def isEqualExpress( self, elem, checkFactor = True, checkPower = True  ):
  def isEqualExpress( self, elem, checkFactor = True  ):
    """
    Check if this type is equal to an expression of type *, with 2 elements, 1 number and 1 type
    """
    if checkFactor == True:
      return False

    # only a experssion of type * can has an expression and this type
    if not isinstance( elem, SymExpress ):
      return False
    if elem.symType != '*':
      return False
    if  elem.power != 1:
      return False
    # the expression must has 2 elements, 1 number and 1 variable
    if elem.numElements() != 2:
      return False
    elem1 = elem.elements[ 0 ]
    elem2 = elem.elements[ 1 ]

    # don't want to change this constuction, readable...
    # pylint: disable=no-else-return
    if isinstance( elem1, SymNumber ):
      if elem1.power != 1:
        return False
      return self.isEqual( elem2 )
    else:
      if not isinstance( elem2, SymNumber ):
        return False
      return self.isEqual( elem1 )
    # cannot come here, but to be sure
    return False

  #
  # get SymVariable and give a SymExpress back if the variable is in dDict, otherwise None is given
  #
  def _replaceVar( self, elem, dDict ):
    if not isinstance( elem, SymVariable ):
      return None

    if elem.name == '':
      return None

    cValue = dDict.get( elem.name, None )
    if cValue == None:
      return None

    expr = SymExpress( '*' )
    expr.powerSign        = elem.powerSign
    expr.powerCounter     = elem.powerCounter
    expr.powerDenominator = elem.powerDenominator
    expr.onlyOneRoot      = elem.onlyOneRoot

    addexpr = SymFormulaParser( cValue )
    expr.add( addexpr )

    # print( "elem was: {}, wordt: {}".format( str( elem ), str( expr )))

    return expr


  #
  # add the varname to the dictionary, varname can be a string or a dictionary
  #
  def _addVar( self, objDict, cVarName, iNumber = 1 ):
    # print( "dict type: {}".format( type( objDict )))
    if ( cVarName == '' or cVarName == None ):  # pylint: disable=consider-using-in
      return None

    if isinstance( cVarName, dict ):
      for key, var in cVarName.items():
        self._addVar( objDict, key, var )
      return cVarName

    if objDict == None:
      objDict = {}

    # print( "dict type: {}".format( type( objDict )))
    # print( "Var: {}, dict: {}".format( cVarName, objDict ))
    if cVarName in objDict:
      objDict[ cVarName ] += iNumber
    else:
      objDict[ cVarName ] = iNumber

    # print( "After Var: {}, dict: {}".format( cVarName, objDict ))
    return objDict


  #
  # convert a given function (elem) to a value (expression)
  # return None if elem is not a function or it cannot be converted
  # oterwhise the SymExpress will be returned
  #
  def _funcionToValue( self, elem, funcname = None ):
    if not isinstance( elem, SymFunction ):
      return None

    result = None

    # if function name is given, only convert that function
    if funcname != None and elem.name != funcname: # pylint: disable=consider-using-in
      return None

    funcDef = symtables.functionTable.get( elem.name )
    if funcDef == None:
      return None

    result = funcDef.functionToValue( elem )

    return result

  def existArray(self):
    """
    Exist there an array in this expression
    """
    return False

#
# standard handling power
#
class SymBasePower( SymBase ):
  """
  Base class for handling a power.
  """
  def __init__( self
               , inPowerSign        = 1
               , inPowerCounter     = 1
               , inPowerDenominator = 1
               , inOnlyOneRoot      = 1 # default principal root
               ):
    super().__init__()

    self.powerSign        = inPowerSign
    self.powerCounter     = inPowerCounter
    self.powerDenominator = inPowerDenominator
    self.onlyOneRoot      = inOnlyOneRoot

  @property
  def powerSign(self):
    """
    Get or set the sign of the power. Valid values are -1 and 1.
    """
    return self._powerSign

  @powerSign.setter
  def powerSign(self, val):
    if not isinstance( val, int ):
      raise NameError( f'powerSign is incorrect: {val}, expected integer value' )

    # if ( val != 1 and val != -1 ):
    if not val in (1, -1 ):
      raise NameError( f'powerSign is incorrect: {val}, expected 1 or -1' )

    self._powerSign = val


  @property
  def powerCounter(self):
    """
    Get or set the counter of the power. It is always positive and an integer.
    If a negative counter is set if will be make positive and the powerSign will be multiply with -1
    """
    return self._powerCounter

  @powerCounter.setter
  def powerCounter(self, val):
    if not isinstance( val, int):
      raise NameError( f'powerCounter is incorrect: {val}, expected integer value' )

    if val < 0:
      self.powerSign *= -1
      val            *= -1

    self._powerCounter = val


  @property
  def powerDenominator(self):
    """
    Get or set the denominator of the power, it is always positive and an integer.
    If a negative denominator is set if will be make positive and the powerSign will be multiply with -1
    """
    return self._powerDenominator

  @powerDenominator.setter
  def powerDenominator(self, val):
    if not isinstance( val, int):
      raise NameError( f'powerDenominator is incorrect: {val}, expected integer value' )

    if val == 0:
      raise NameError( f'powerDenominator is incorrect: {val}, value may not be zero' )

    if val < 0:
      self.powerSign *= -1
      val            *= -1

    self._powerDenominator = val

  @property
  def onlyOneRoot(self):
    """
    Get or set if this can only have one value if it is a root, 1=only one root, 0=many roots
    """
    return self._onlyOneRoot

  @onlyOneRoot.setter
  def onlyOneRoot(self, val):
    if not isinstance( val, int ):
      raise NameError( f'onlyOneRoot is incorrect: {val}, expected integer value' )

    # if ( val != 1 and val != 0 ):
    if not val in (1, 0 ):
      raise NameError( f'onlyOneRoot is incorrect: {val}, expected 0 or 1' )

    self._onlyOneRoot = val


  @property
  def power(self):
    """
    Get the power in decimal format (powerSign * powerCounter / powerDenominator )
    """
    if self.powerDenominator != 1:
      return self.powerSign * self.powerCounter / self.powerDenominator
    # else:
    return self.powerSign * self.powerCounter


  def valuePow( self, dValue ):
    """
    Pow the given value according the object
    """
    dResult = dValue

    if isinstance( dValue, list ):
      dResult = []
      # for iCnt in range( 0, len( dValue )):
      # for iCnt in enumerate( dValue ):
      # for iCnt, dValEnum in enumerate( dValue ):
      for dValEnum in dValue:
        # dValSub =  dValue[ iCnt ] ** self.power
        dValSub = dValEnum ** self.power
        if isinstance( dValSub, complex ):
          if round( abs( dValSub.imag ), 14 ) == 0:
            dValSub = dValSub.real
        dResult.append( dValSub )
    else:
      dResult = dValue ** self.power
      if isinstance( dResult, complex ):
        if round( abs( dResult.imag ), 14 ) == 0:
          dResult = dResult.real

    return dResult


  # set the only for if the denominator greater als 1 is
  def _setOnlyOne( self ):
    if self.powerDenominator > 1:
      self.onlyOneRoot = 1
      return True
    return False


  # power in string format
  def powerStr( self ):
    """
    Internal use, give the power in string format
    """
    output = ""
    if self.powerDenominator != 1:
      output += '(' + str( self.powerCounter * self.powerSign ) + '/' + str( self.powerDenominator ) + ')'
    else:
      output += str( self.power )
    return output

  def powerMathMlColor( self ):
    """
    Internal use, give mathml color string for root (one or multiple roots)
    """
    cResult = ''
    if self.onlyOneRoot == 0:
      cResult = colorallroot
    else:
      cResult = colorposroot

    return ' mathcolor= "' + cResult + '" '

  def powermathMl( self ):
    """
    Internal use, give the power in mathml format
    """
    output = ""
    if self.powerDenominator != 1:
      output += '<mfrac' + self.powerMathMlColor() + '>'
      if self.powerSign == -1:
        output += '<mrow>'
        output += '<mo>-</mo>'
      output += '<mn>' + str( self.powerCounter     ) + '</mn>'
      if self.powerSign == -1:
        output += '</mrow>'
      output += '<mn>' + str( self.powerDenominator ) + '</mn>'
      output += '</mfrac>'

    else:
      if self.powerSign == -1:
        output += '<mrow">'
        output += '<mo>-</mo>'
      output += '<mn>' + str( self.powerCounter     ) + '</mn>'
      if self.powerSign == -1:
        output += '</mrow>'
    return output + '\n'


  # optimize the unit
  def optimize( self, cAction = None ):
    """
    cAction = None: Optimize the factor and power so that they are in there lowest form
    \ncAction = 'setOnlyOne':  Set that this radicals can only has one solution
    """
    result = False

    if cAction == 'setOnlyOne':
      result |= self._setOnlyOne()

    if cAction == None:
      # no optimization, root first then powers

      # return result

      if ( self.powerDenominator > 1 and self.onlyOneRoot != 1 ) :
        return result

      # print( 'self.powerCounter: {}, self.powerDenominator: {}, self.onlyOneRoot: {}'.format( self.powerCounter, self.powerDenominator, self.onlyOneRoot ))

      iGcd = math.gcd( self.powerCounter, self.powerDenominator )
      if iGcd != 1:
        # print( "power before: {} - {}  fact: {} - {}".format( self.powerCounter, self.powerDenominator, self.factCounter, self.factDenominator  ))
        self.powerCounter     //= iGcd
        self.powerDenominator //= iGcd
        result = True
        # print( "power after: {} - {}".format( self.powerCounter, self.powerDenominator ))

    return result
#
# Number handling
#
class SymNumber( SymBasePower ):
  """
  Class for handling a factor and a power.
  """
  def __init__( self
               , in_factSign         = 1
               , in_factCounter      = 1
               , in_factDenominator  = 1
               , in_powerSign        = 1
               , in_powerCounter     = 1
               , in_powerDenominator = 1
               , in_onlyOneRoot      = 1 # default principal root
               ):
    super().__init__()

    self.factSign         = in_factSign
    self.factCounter      = in_factCounter
    self.factDenominator  = in_factDenominator
    self.powerSign        = in_powerSign
    self.powerCounter     = in_powerCounter
    self.powerDenominator = in_powerDenominator
    self.onlyOneRoot      = in_onlyOneRoot

  @property
  def factSign(self):
    """
    Get or set the sign of the factor. Valid values are -1 and 1.
    """
    return self._factSign

  @factSign.setter
  def factSign(self, val):
    if not isinstance( val, int):
      raise NameError( f'factSign is incorrect: {val}, expected integer value' )

    # if ( val != 1 and val != -1 ):
    if not val in ( 1, -1):
      raise NameError( f'factSign is incorrect: {val}, expected 1 or -1' )

    self._factSign = val


  @property
  def factCounter(self):
    """
    Get or set the counter of the factor. It is always positive and an integer.
    If a negative counter is set if will be make positive and the factSign will be multiply with -1
    """
    return self._factCounter

  @factCounter.setter
  def factCounter(self, val):
    if not isinstance( val, int):
      raise NameError( f'factCounter is incorrect: {val}, expected integer value({type(val)})' )

    if val < 0:
      self.factSign *= -1
      val           *=  -1

    self._factCounter = val


  @property
  def factDenominator(self):
    """
    Get or set the denominator of the factor, it is always positive and an integer.
    If a negative denominator is set if will be make positive and the factSign will be multiply with -1
    """
    return self._factDenominator

  @factDenominator.setter
  def factDenominator(self, val):
    if not isinstance( val, int):
      raise NameError( f'factDenominator is incorrect: {val}, expected integer value' )

    if val == 0:
      raise NameError( f'factDenominator is incorrect: {val}, value may not be zero' )

    if val < 0:
      self.factSign *= -1
      val           *=  -1

    self._factDenominator = val


  @property
  def factor(self):
    """
    Get the factor in decimal format (factSign * factCounter / factDenominator )
    """
    if self.factDenominator != 1:
      return self.factSign * self.factCounter / self.factDenominator
    # else:
    return self.factSign * self.factCounter

  # check if a given object is equal to this object
  def isEqual( self, elem, checkFactor = True, checkPower = True ):
    """
    Check if the given object is equal to this object.
    Return True for equal and False for not equal
    """
    if not isinstance( elem, SymNumber ):
      if ( self.factCounter == 0 and isinstance( elem, SymExpress ) == True ):
        if elem.numElements() == 0:
          return True

        if ( elem.numElements() == 1 and isinstance( elem.elements [ 0 ], SymNumber )):
          if elem.elements [ 0 ].factCounter == 0:
            return True

      return self.isEqualExpress( elem, checkFactor )

    if ( checkPower == True and self.power != elem.power ):
      return False

    if ( checkFactor == True and self.factor != elem.factor ):
      return False

    return True

  def getVariables( self ):
    dVar = {}
    return dVar

  def getFunctions( self ):
    dFunc = {}
    return dFunc

  def replaceVariable( self, dDict ):
    # you cannot replace your self, only subelements
    pass

  def getValue( self, dDict = None ):
    dValue = self.factor

    # print( "dValue before: {}".format( dValue ))
    dValue = dValue ** self.power
    # print( "dValue after: {}, factor: {}, power: {}".format( dValue, self.factor, self.power ))

    # print ( "getValue: {}, value: {}".format( str( self), dValue ))
    return dValue

  # factor in string format
  def factorStr( self ):
    """
    Internal use, give the factor in string format
    """
    output = ""
    if self.factDenominator != 1:
      if self.factSign == -1:
        output += '-'
      output += '(' + str( self.factCounter ) + '/' + str( self.factDenominator ) + ')'
    else:
      if self.factSign == -1:
        output += '-'
      output += str( self.factCounter )
    return output

  def factormathMl( self ):
    """
    Internal use, give the factor in mathml format
    """
    output = ""
    if self.factDenominator != 1:
      iCounter     = self.factCounter
      iDenominator = self.factDenominator
      iFact        = 0

      if iCounter > iDenominator:
        iCounter = self.factCounter  % iDenominator
        iFact    = self.factCounter // iDenominator

      if self.factSign == -1:
        output += '<mrow>'
        output += '<mo>-</mo>'

      if iFact > 0:
        output += '<mrow>'
        output += '<mn>' + str( iFact ) + '</mn>'

      output += '<mfrac>'
      # if ( self.factSign == -1 ):
      #   output += '<mrow>'
      #   output += '<mo>-</mo>'
      output += '<mn>' + str( iCounter ) + '</mn>'
      # if ( self.factSign == -1 ):
      #   output += '</mrow>'
      output += '<mn>' + str( iDenominator ) + '</mn>'
      output += '</mfrac>'

      if iFact > 0:
        output += '</mrow>'

      if self.factSign == -1:
        output += '</mrow>'

    else:
      if self.factSign == -1:
        output += '<mrow>'
        output += '<mo>-</mo>'
      output += '<mn>' + str( self.factCounter     ) + '</mn>'
      if self.factSign == -1:
        output += '</mrow>'

    return output + '\n'

  # optimize the unit
  def optimize( self, cAction = None ):
    """
    cAction = None: Optimize the factor and power so that they are in there lowest form
    \ncAction = 'setOnlyOne':  Set that this radicals can only has one solution
    \ncAction = 'power':  Write out the power
    """

    result = super().optimize( cAction )

    if cAction == 'setOnlyOne':
      result |= self._setOnlyOne()

    if cAction == None:
      iGcd = math.gcd( self.factCounter, self.factDenominator )
      # print ("factCounter: {}, factDenominator: {}, iGcd: {}".format(self.factCounter, self.factDenominator, iGcd ))
      if iGcd != 1:
        self.factCounter     //= iGcd
        self.factDenominator //= iGcd
        result = True
      if self.power == -1 and self.factCounter != 0:
        # 3^-1 = 1/3
        self.factCounter, self.factDenominator = self.factDenominator, self.factCounter
        self.powerSign = 1
        result = True
      if self.powerCounter == 0:
        self.factCounter      = 1
        self.factDenominator  = 1
        self.factSign         = 1
        self.powerCounter     = 1
        self.powerDenominator = 1
        self.powerSign        = 1
        result = True

    return result

  # output in MatMl format
  def mathMl( self ):
    """
    Give the unit in MathMl format
    """
    output = ''
    output += '<mrow>'

    if self.power != 1:
      if self.powerSign == -1:
        output += '<mfrac>'
        output += '<mn>1</mn>'
        output += '<mrow>'

      if self.powerDenominator != 1:
        output += '<mroot' + self.powerMathMlColor() + '>'
        output += '<mrow>'

      if self.powerCounter != 1:
        output += '<msup>'
        output += '<mrow>'

    output += self.factormathMl()

    if self.power != 1:
      if self.powerCounter != 1:
        output += '</mrow>'
        output += '<mn>' + str( self.powerCounter )  + '</mn>'
        output += '</msup>'

      if self.powerDenominator != 1:
        output += '</mrow>'
        if self.powerDenominator != 2:
          output += '<mn>' + str( self.powerDenominator ) + '</mn>'
        else:
          output += '<mn></mn>'
        output += '</mroot>'

      if self.powerSign == -1:
        output += '</mrow>'
        output += '</mfrac>'

    output += '</mrow>'
    return output + '\n'

  def __str__( self ):
    output = ''

    if self.factSign == -1:
      output += '(' + str( self.factCounter * self.factSign )
      if self.factDenominator != 1:
        output += '/' + str( self.factDenominator )
      output += ')'
    else:
      output += self.factorStr()

    if self.power != 1:
      if self.onlyOneRoot == 1:
        output += '^'
      output += '^' + self.powerStr()

    return output

  # give a copy of this object
  def copy(self):
    """
    Make a copy of this number
    """
    copyunit = SymNumber( self.factSign
                        , self.factCounter
                        , self.factDenominator
                        , self.powerSign
                        , self.powerCounter
                        , self.powerDenominator
                        , self.onlyOneRoot
                        )
    return copyunit

#
# SymVariable defintion, the basic block
# ( factor-sign factor-counter / factor-denominator ) ( <name> imaginary ) ^ ( power-sign power-counter / power-denominator )
# counter, denominator, power-counter power-denominator are all positive integers
# sign       = -1 or 1
# power-sign = -1 or 1
# name       = <empty> or filled
#
class SymVariable( SymBasePower ):
  """
  Handling a variable with power
  """
  def __init__( self
               , in_name             = ''
               , in_powerSign        = 1
               , in_powerCounter     = 1
               , in_powerDenominator = 1
               , in_onlyOneRoot      = 1 # default principal root

               ):

    super().__init__()

    self.name             = in_name
    self.powerSign        = in_powerSign
    self.powerCounter     = in_powerCounter
    self.powerDenominator = in_powerDenominator
    self.onlyOneRoot      = in_onlyOneRoot

  @property
  def name(self):
    """
    Get or set the name of the unit.
    \nSpecial names:
    \ni = imaginair number
    \npi = &pi; (3.1415...)
    \ne = Euler's number  (2.7182...)
    \ninfinity = &infin;
    """
    return self._name

  @name.setter
  def name(self, val):
    if not isinstance( val, str):
      raise NameError( f'name is incorrect: {val}, expected string value' )
    self._name = val

  # check if a given object is equal to this object
  def isEqual( self, elem, checkFactor = True, checkPower = True ):
    """
    Check if the given object is equal to this object.
    Return True for equal and False for not equal
    """
    if not isinstance( elem, SymVariable ):
      return self.isEqualExpress( elem, checkFactor )

    if (checkPower == True and elem.power != self.power  ):
      return False
    if elem.name != self.name:
      return False

    return True

  # optimize the unit
  def optimize( self, cAction = None ):
    """
    cAction = None: Optimize the unit, set the factor and power in there smallest form
    \ncAction = "i : Write out all the imaginary numbers (eliminate powers)
    """
    result = False

    if cAction == None:
      if self.powerCounter == 0:
        self.powerSign        = 1
        self.powerCounter     = 0
        self.powerDenominator = 1
        result = True

    result |= super().optimize( cAction )

    return result

  def getVariables( self ):
    dVar = {}
    return self._addVar( dVar, self.name )

  def getFunctions( self ):
    dFunc = {}
    return dFunc

  def replaceVariable( self, dDict ):
    # you cannot replace your self, only subelements
    pass

  def getValue( self, dDict = None ):
    dValue = None
    if dDict != None:
      dValue = dDict.get( self.name, None )

    # print( "GetValue: {}, value: {}".format( self.name, dValue ))
    if dValue == None:
      if self.name == 'pi':
        dValue = math.pi
      elif self.name == 'i':
        dValue = complex( 0, 1 )
      elif self.name == 'e':
        dValue = math.e
      else:
        raise NameError( f'getValue, for variable "{self.name}" is no value given.' )
    # print( "dValue before: {}".format( dValue ))
    dValue = dValue ** self.power
    # print( "dValue after: {}, factor: {}, power: {}".format( dValue, self.factor, self.power ))

    # print ( "getValue: {}, value: {}".format( str( self), dValue ))
    return dValue



  # output in MatMl format
  def mathMl( self ):
    """
    Give the unit in MathMl format
    """
    output = ''
    output += '<mrow>'

    if self.power != 1:
      if self.powerSign == -1:
        output += '<mfrac>'
        output += '<mn>1</mn>'
        output += '<mrow>'

      if self.powerDenominator != 1:
        output += '<mroot' + self.powerMathMlColor() + '>'
        output += '<mrow>'

      if self.powerCounter != 1:
        output += '<msup>'
        output += '<mrow>'

    if self.name == 'pi' :
      output += '<mi>' + '&pi;' + '</mi>'
    elif self.name == 'infinity':
      output += '<mi>' + '&infin;' + '</mi>'
    else:
      output += '<mi>' + self.name + '</mi>'

    if self.power != 1:
      if self.powerCounter != 1:
        output += '</mrow>'
        output += '<mn>' + str( self.powerCounter )  + '</mn>'
        output += '</msup>'

      if self.powerDenominator != 1:
        output += '</mrow>'
        if self.powerDenominator != 2:
          output += '<mn>' + str( self.powerDenominator ) + '</mn>'
        else:
          output += '<mn></mn>'
        output += '</mroot>'

      if self.powerSign == -1:
        # if ( self.name == '' ):
        #   output += self.factormathMl()
        output += '</mrow>'
        output += '</mfrac>'

    output += '</mrow>'
    return output + '\n'

  # the SymVariable in string format
  def __str__( self ):
    output = ''
    output += self.name

    if self.power != 1:
      if self.onlyOneRoot == 1:
        output += '^'
      output += '^' + self.powerStr()

    return output

  # give a copy of this object
  def copy(self):
    """
    Make a copy of this unit
    """
    copyunit = SymVariable( self.name
                          , self.powerSign
                          , self.powerCounter
                          , self.powerDenominator
                          , self.onlyOneRoot
                          )
    return copyunit


#
# SymBaseList, base for list handling
#
class SymBaseList( SymBasePower ):
  """
  Base class for list (array) support
  """
  def __init__( self
             , in_factSign         = 1
             , in_factCounter      = 1
             , in_factDenominator  = 1
             , in_powerSign        = 1
             , in_powerCounter     = 1
             , in_powerDenominator = 1
             , in_onlyOneRoot      = 1 # default principal root
             ):

    super().__init__()

    self.factSign         = in_factSign
    self.factCounter      = in_factCounter
    self.factDenominator  = in_factDenominator
    self.powerSign        = in_powerSign
    self.powerCounter     = in_powerCounter
    self.powerDenominator = in_powerDenominator
    self.onlyOneRoot      = in_onlyOneRoot
    self.elements         = []

  # add SymExpress or and SymVariable to the list
  def add( self, val ):
    """
    Make a copy of the given object (SymBase) and add it to this expression
    """
    if not isinstance( val, SymBase ):
      raise NameError( f'add is incorrect: {type( val )}, expected a class with inherents of SymBase' )
    self.elements.append( val.copy() )

  def numElements( self ):
    """
    Give the number if elements in this expression
    """
    return len( self.elements )

  def getVariables( self ):
    dVar = {}
    # for iCnt in range( 0, len( self.elements )):
    for elem in self.elements:
      # self._addVar( dVar, self.elements[ iCnt ].getVariables() )
      self._addVar( dVar, elem.getVariables() )
    return dVar

  def getFunctions( self ):
    dFunc = {}
    # for iCnt in range( 0, len( self.elements )):
    for elem in self.elements:
      # self._addVar( dFunc, self.elements[ iCnt ].getFunctions() )
      self._addVar( dFunc, elem.getFunctions() )
    return dFunc

  def replaceVariable( self, dDict ):
    # for iCnt in range( 0, len( self.elements )):
    for iCnt, elemSelect in enumerate( self.elements ):
      # elem = self._replaceVar( self.elements[ iCnt ], dDict )
      elem = self._replaceVar( elemSelect, dDict )
      if elem != None:
        self.elements[ iCnt ] = elem
      else:
        self.elements[ iCnt ].replaceVariable( dDict )

  def existArray(self):
    """
    Exist there an array in this expression
    """
    if isinstance( self, SymArray ):
      return True

    result = False
    for elem in self.elements:
      result |= elem.existArray()
      if result == True:
        break

    return result


  def _convertFunctionsToValues( self, funcname = None):
    """
    Convert functions to values
    If function name is given, only that function otherwise all functions
    """
    result = False
    # for iCnt in range( 0, len( self.elements )) :
    for iCnt, elemSelect in enumerate( self.elements ) :
      # elem = self.elements[ iCnt ]
      #
      elem = self._funcionToValue( elemSelect, funcname )
      if elem != None:
        self.elements[ iCnt ] = elem
        result = True
    return result

  # is sub element is a symexpress with 1 element, get it
  def _optGetOneExpressions(self):
    result = False
    # print( "Start _optGetOneExpressions: {}".format( str( self )))
    # for iCnt in range( 0, len( self.elements ) ) :
    for iCnt, elem in enumerate( self.elements ):
      # elem = self.elements[ iCnt ]

      # if ( elem.powerDenominator > 1 and elem.onlyOneRoot != 1 ):
      #   continue
      # print( "_optGetOneExpressions: {} , {}".format( iCnt, str( elem )))
      # if not ( isinstance( elem, SymExpress ) or isinstance( elem, SymArray ) ):
      if not isinstance( elem, (SymExpress, SymArray)):
        continue

      if elem.numElements() != 1:
        continue

      elem1 = elem.elements[0]

      # special zero case
      # if isinstance( elem1, SymNumber ):
      #  if elem1.factCounter == 0:
      #    print( "check number zero: " + str( elem1 ) )
      #
      #    self.elements[ iCnt ] = elem1
      #    return True

      # print( '_optGetOneExpressions  elem  : {}'.format( elem  ))
      # print( '_optGetOneExpressions  elem1 : {}'.format( elem1 ))

      # must be the same type
      if elem1.onlyOneRoot != elem.onlyOneRoot:
        if elem.powerDenominator == 1:
          # if parent has no denominator it can always put together
          pass
        elif elem1.powerCounter > 1:
          # parent has a denominator and the child a power
          # first write out the power
          continue
        elif elem1.powerDenominator == 1 and elem.powerDenominator == 1:
          # is there no denominator then onlyOneRoot as no meaning
          pass
        else:
          if (elem1.powerCounter == elem.powerCounter ) and (elem1.powerDenominator == elem.powerDenominator):
            # if the roots are the same you can add them together
            pass
          else:
            # print( "elem1.powerDenominator: " + str( elem1.powerDenominator ))
            # print( "elem.powerDenominator : " + str( elem.powerDenominator  ))
            # print( "elem1.powerCounter    : " + str( elem1.powerCounter     ))
            # print( "elem.powerCounter     : " + str( elem.powerCounter      ))

            # print( "Failed" )
            continue

      # first do the power then you can put then together
      if elem1.powerCounter > 1 and elem.powerDenominator > 1:
        # print( "Failed 1" )
        continue

      #
      # if sub element has a denominator and the parent and no counter
      # you can always combine because denominator must be done first before counter
      #

      # print( 'elem  : {}'.format( elem  ))
      # print( 'elem1 : {}'.format( elem1 ))

      iCounter     = elem1.powerCounter     * elem.powerCounter     * elem1.powerSign * elem.powerSign
      iDenominator = elem1.powerDenominator * elem.powerDenominator

      # print( 'iDenominator: {}, iCounter: {}'.format( iDenominator,iCounter ))

      # first write root out then make it smaller
      # if (       ( iDenominator == 1 or iDenominator == iCounter )                # pylint: disable=consider-using-in
      #     and (    ( elem1.powerDenominator > 1 and elem1.onlyOneRoot != 1  )
      #           or ( elem.powerDenominator  > 1 and elem.onlyOneRoot  != 1  )
      #          )
      #  ):
      #  continue


      # print( '_optGetOneExpressions  elem  : {}'.format( elem  ))
      # print( '_optGetOneExpressions  elem1 : {}'.format( elem1 ))


      # default is onylOneRoot = 1
      # elem1.onlyOneRoot      = max( elem1.onlyOneRoot, elem.onlyOneRoot )
      elem1.onlyOneRoot      = min( elem1.onlyOneRoot, elem.onlyOneRoot )
      elem1.powerSign        = 1
      elem1.powerCounter     = iCounter
      elem1.powerDenominator = iDenominator

      # print( '_optGetOneExpressions  elem1 new: {}'.format( elem1 ))

      self.elements[ iCnt ] = elem1

      result = True

    return result

  def _optimzeSymSubs( self, cAction ):
    result = False
    if cAction == None:
      return result

    if cAction == "functionToValues":
      result |= self._convertFunctionsToValues()
      return result

    if ( cAction != None and cAction.startswith( "functionToValue_") == True ):
      result |= self._convertFunctionsToValues( cAction.split("_",1)[1] ) # get the function name
      return result

    optFunc = symtables.optSymFunctionTable.get( cAction )
    optVar  = symtables.optSymVariableTable.get( cAction )
    optNum  = symtables.optSymNumberTable.get(   cAction )
    optAny  = symtables.optSymAnyTable.get(      cAction )

    # check nothing to do
    if optFunc == None and optVar == None and optNum == None and optAny == None:
      return result

    # for iCnt in range( 0, len( self.elements )) :
    for iCnt, elemSelect in enumerate( self.elements ) :
      if optFunc != None:
        elem = optFunc.optimize( elemSelect, cAction )
        # elem = self._optimzeSymFunction( self.elements[ iCnt ], cAction )
        if elem != None:
          self.elements[ iCnt ] = elem
          result = True
          continue

      if optVar != None:
        elem = optVar.optimize( elemSelect, cAction )
        # elem = self._optimzeSymVariable( self.elements[ iCnt ], cAction )
        if elem != None:
          self.elements[ iCnt ] = elem
          result = True
          continue

      if optNum != None:
        elem = optNum.optimize( elemSelect, cAction )
        # elem = self._optimzeSymNumber( self.elements[ iCnt ], cAction )
        if elem != None:
          self.elements[ iCnt ] = elem
          result = True
          continue

      if optAny != None:
        elem = optAny.optimize( elemSelect, cAction )
        if elem != None:
          self.elements[ iCnt ] = elem
          result = True
          continue

    return result
#
# SymArray, an array of expressions
#
class SymArray( SymBaseList ):
  """
  An array of expressions
  """
  def __init__( self
             , in_powerSign        = 1
             , in_powerCounter     = 1
             , in_powerDenominator = 1
             , in_onlyOneRoot      = 1 # default principal root
             ):

    super().__init__()

    self.powerSign        = in_powerSign
    self.powerCounter     = in_powerCounter
    self.powerDenominator = in_powerDenominator
    self.onlyOneRoot      = in_onlyOneRoot


  def optimize( self, cAction = None ):

    """
    Optimize the expression, but do no calculations
    \ncAction = None: Optimize the expression
    \ncAction = "functionToValues" : Convert functions to values
    \ncAction = "functionToValue_<functionName>" : Convert the given function into value
    """
    result = False
    if cAction == None:
      #  factor zero is no elements at all, and no elements is factor 0
      if len( self.elements ) == 0:
        self.elements          = []
        self.powerSign         = 1
        self.powerCounter      = 1
        self.powerDenominator  = 1
        result                 = True

      # power zero give always 1, is 1 element with value 1, factor is not changed
      if self.power == 0:
        self.elements          = []
        self.powerSign         = 1
        self.powerCounter      = 1
        self.powerDenominator  = 1
        self.add ( SymVariable() )
        result                 = True

    result |= super().optimize( cAction )

    for elem in self.elements:
      result |= elem.optimize( cAction )

    result |= self._optimzeSymSubs( cAction )

    if cAction == None:
      result |= self._optGetOneExpressions()

    return result


  def isEqual( self, elem, checkFactor = True, checkPower = True ):
    """
    Check if the given object is equal to this object.
    Return True for equal and False for not equal
    """
    if not isinstance( elem, SymArray ):
      return self.isEqualExpress( elem, checkFactor )

    if (checkPower == True and elem.power != self.power  ):
      return False

    if elem.numElements() != self.numElements():
      return False

    # array to remember if element is already used
    checkArr = []
    for iCnt in range( 0, self.numElements()):
      checkArr.append( False )

    for iCnt in range( 0, self.numElements()):
      elem1  = self.elements[ iCnt ]
      lFound = False
      for iCnt2 in range( 0, elem.numElements()) :
        if checkArr[ iCnt2 ] == True:
          continue
        elem2 = elem.elements[ iCnt2 ]
        # must the exact class
        if type( elem2 ) != type( elem1 ):  # pylint: disable=unidiomatic-typecheck
          continue
        if elem1.isEqual( elem2 ) != True:
          continue

        checkArr[ iCnt2 ] = True
        lFound = True
        break
      if lFound == False:
        return False

    return True

  def existArray(self):
    """
    Exist there an array in this expression
    """
    return True

  def getValue( self, dDict = None ):
    arrValues = []
    # for iCnt in range( 0, len( self.elements )):
    for elem in self.elements:
      # dValue = self.elements[ iCnt ].getValue( dDict )
      dValue = elem.getValue( dDict )
      if isinstance( dValue , list ):
        # for iCnt2 in range( 0, len( dValue )):
        for dValElem in dValue:
          # arrValues.append( dValue[ iCnt2 ] )
          arrValues.append( dValElem )
      else:
        arrValues.append( dValue )
    arrValues = self.valuePow( arrValues )

    return arrValues

  def copy(self):
    """
    Make a copy of this expression
    """
    copyArray = SymArray( self.powerSign
                        , self.powerCounter
                        , self.powerDenominator
                        , self.onlyOneRoot
                        )
    # for iCnt in range( 0, len( self.elements )) :
    for elem in self.elements:
      # copyArray.add( self.elements[ iCnt ] )
      copyArray.add( elem )
    return copyArray

  def mathMl( self ):
    output = ''
    output += '<mrow>'

    if self.power != 1:
      if self.powerDenominator != 1:
        output += '<mroot' + self.powerMathMlColor() + '>'
        output += '<mrow>'

      if self.powerSign == -1:
        output += '<mfrac>'
        output += '<mn>1</mn>'
        output += '<mrow>'

      if self.powerCounter != 1:
        output += '<msup>'
        output += '<mrow>'

    output += "<mfenced open='[' close=']'>"
    output += '<mtable>'
    # for iCnt in range( 0, len( self.elements )) :
    for elem in self.elements:
      output += '<mtr>'
      output += '<mtd>'
      # output += self.elements[ iCnt ].mathMl()
      output += elem.mathMl()
      output += '</mtd>'
      output += '</mtr>'

    output += '</mtable>'
    output += '</mfenced>'

    if self.power != 1:
      if self.powerCounter != 1:
        output += '</mrow>'
        output += '<mn>' + str( self.powerCounter )  + '</mn>'
        output += '</msup>'

      if self.powerSign == -1:
        output += '</mrow>'
        output += '</mfrac>'

      if self.powerDenominator != 1:
        output += '</mrow>'
        if self.powerDenominator != 2:
          output += '<mn>' + str( self.powerDenominator ) + '</mn>'
        else:
          output += '<mn></mn>'
        output += '</mroot>'

    output += '</mrow>'
    return output + '\n'


  def __str__( self ):
    output = ''
    output += '[ '

    # for iCnt in range( 0, len( self.elements )) :
    for iCnt, elem in enumerate( self.elements ):
      if iCnt > 0:
        output += ' | '
      # output += str( self.elements[ iCnt ] )
      output += str( elem )

    output += ' ]'

    if self.power != 1:
      if self.onlyOneRoot == 1:
        output += '^'
      output += '^' + self.powerStr()

    return output

#
# Sym function, name + symexpression
#
class SymFunction( SymBaseList ):
  """
  Handling of a function

  Supported functions for calculation and optimization:
  \nsin(x), cos(x), tan(x)
  \natan2(x,y), atan(x)
  \nabs(x)
  \nfloor(x), ceil(x)
  \nfactorial(n) = n!
  \nbinomial(n,k) = n!/(n! ( n - k )!)
  \nexp(x [,y]) = y^x, default is e (e^x)
  \nsum(&lt;variable&gt;,&lt;lower&gt;,&lt;upper&gt;,&lt;function&gt;) = sum function, from lower to upper,
  \nexample: sum(n,0,100,exp(x,n))
  """
  def __init__( self
               , in_name             = ""
               , in_powerSign        = 1
               , in_powerCounter     = 1
               , in_powerDenominator = 1
               , in_onlyOneRoot      = 1 # default principal root
               ):

    super().__init__()

    self.name             = in_name
    self.powerSign        = in_powerSign
    self.powerCounter     = in_powerCounter
    self.powerDenominator = in_powerDenominator
    self.onlyOneRoot      = in_onlyOneRoot

  @property
  def name(self):
    """
    Get or set the name of the function.
    """
    return self._name

  @name.setter
  def name(self, val):
    if not isinstance( val, str ):
      raise NameError( f'name is incorrect: {val}, expected string value' )
    self._name = val

  def getFunctions( self ):
    dFunc = super().getFunctions()
    self._addVar( dFunc, self.name )
    return dFunc

  def getValue( self, dDict = None ):
    dValue = None

    # SymFillFunctionTable()

    # print( "Test functiontable: {}".format( len(functionTable) ) )

    funcDef = symtables.functionTable.get( self.name )
    if funcDef != None:
      dValue = funcDef.getValue( self, dDict )

    # for funcDef in functionTable:
    #   if (funcDef.name == self.name):
    #      dValue = funcDef.getValue( self, dDict )
    #      if (dValue == None): # there can be more then 1 function with the same name
    #         continue
    #      break

    if dValue != None:
      return dValue

    raise NameError( f'getValue for function {self.name} is not implemented' )


  def optimize( self, cAction = None ):
    """
    Optimize the expression, but do no calculations
    \ncAction = None: Optimize the expression
    \ncAction = "functionToValues" : Convert functions to values
    \ncAction = "functionToValue_<functionName>" : Convert the given function into value
    """
    result = super().optimize( cAction )

    for elem in self.elements:
      result |= elem.optimize( cAction )

    result |= self._optimzeSymSubs( cAction )

    if cAction != None:
      return result

    # is sub element is a symexpress with 1 element, get it
    for iCnt, elem in enumerate( self.elements ):
      # elem.optimize( cAction )

      if ( isinstance( elem, SymExpress ) and elem.numElements() == 1 ):
        elem1 = elem.elements[0]
        if ( elem.power  == 1 and ( elem1.power == 1 )):
          self.elements[ iCnt ]  = elem1
          result = True

        elif ( isinstance( elem1 , SymVariable ) and elem1.power == 1):
          elem1.powerSign        *= elem.powerSign
          elem1.powerCounter     *= elem.powerCounter
          elem1.powerDenominator *= elem.powerDenominator

          self.elements[ iCnt ]   = elem1
          result = True

        elif ( isinstance( elem1, SymNumber ) and elem.power > 0 and elem1.power == -1):
          elem1.powerCounter     = elem.powerCounter
          elem1.powerDenominator = elem.powerDenominator

          self.elements[ iCnt ]  = elem1
          result = True

      # need always 1 element in a symexpression
      if ( isinstance( elem, SymExpress ) and elem.numElements() == 0 ):
        self.elements[ iCnt ] = SymNumber( 1, 0, 1, 1, 1, 1 )
        result = True

    return result

  def isEqual( self, elem, checkFactor = True, checkPower = True ):
    """
    Check if the given object is equal to this object.
    Return True for equal and False for not equal
    """
    if not isinstance( elem, SymFunction ):
      return self.isEqualExpress( elem, checkFactor )

    if self.name != elem.name:
      return False

    if (checkPower == True and elem.power != self.power ):
      return False

    if elem.numElements() != self.numElements():
      return False

    # if ( self.expression == None and elem.expression != None ):
    #    return False
    # if ( self.expression != None and elem.expression == None ):
    #   return False

    for iCnt in range( 0, self.numElements()):
      elem1 = self.elements[ iCnt ]
      elem2 = elem.elements[ iCnt ]

      if not elem1.isEqual( elem2 ):
        return False

    return True

    # return self.expression.isEqual( elem.expression )

  def copy(self):
    """
    Make a copy of this expression
    """
    copyFunc = SymFunction(  self.name
                          , self.powerSign
                          , self.powerCounter
                          , self.powerDenominator
                          , self.onlyOneRoot
                          )
    # for iCnt in range( 0, len( self.elements )) :
    for elem in self.elements:
      # copyFunc.add( self.elements[ iCnt ] )
      copyFunc.add( elem )

    return copyFunc

  def mathMl( self ):
    isFactorial  = False
    isExp        = False
    isExtraClose = False
    isSum        = False
    isBinomial   = False
    isFloor      = False
    isCeil       = False

    if (self.name == "factorial" and self.numElements() == 1 ):
      isFactorial = True

    if (self.name == "exp" and ( self.numElements() == 1 or self.numElements() == 2)):
      isExp = True

    if (self.name == "sum" and ( self.numElements() == 4 )):
      isSum = True

    if (self.name == "binomial" and ( self.numElements() == 2 )):
      isBinomial = True

    if (self.name == "floor" and ( self.numElements() == 1 )):
      isFloor = True

    if (self.name == "ceil" and ( self.numElements() == 1 )):
      isCeil = True

    output = ''
    output += "<mrow>"

    if isFactorial == True:
      # output += '<apply><factorial/><ci>'
      # output += '<apply><factorial/><apply>'
      pass

    if self.power != 1:
      if ( isFactorial == True or isExp == True or isSum == True):
        output += '<mo>(</mo>'

      if self.powerDenominator != 1:
        output += '<mroot' + self.powerMathMlColor() + '>'
        output += '<mrow>'

      if self.powerSign == -1:
        output += '<mfrac>'
        output += '<mn>1</mn>'
        output += '<mrow>'

      if self.powerCounter != 1:
        output += '<msup>'
        output += '<mrow>'

    if (isFactorial == False and isExp == False and isSum == False and isBinomial == False and isFloor == False and isCeil == False):
      output += '<mi>' + self.name + '</mi>'
      output += "<mfenced separators=''>"

    if self.numElements() == 0:
      output += '<mn>0</mn>'

    if isCeil == True:
      output += "<mfenced  open='&lceil;' close='&rceil;'>"
      output += "<mtable>"

      output += "<mtr>"
      output += "<mtd>"
      output += self.elements[ 0 ].mathMl()
      output += "</mtd>"
      output += "</mtr>"

      output += "</mtable>"
      output += "</mfenced>"

    elif isFloor == True:
      output += "<mfenced  open='&lfloor;' close='&rfloor;'>"
      output += "<mtable>"

      output += "<mtr>"
      output += "<mtd>"
      output += self.elements[ 0 ].mathMl()
      output += "</mtd>"
      output += "</mtr>"

      output += "</mtable>"
      output += "</mfenced>"

    elif isBinomial == True:
      output += "<mfenced>"
      output += "<mtable>"

      output += "<mtr>"
      output += "<mtd>"
      output += self.elements[ 0 ].mathMl()
      output += "</mtd>"
      output += "</mtr>"

      output += "<mtr>"
      output += "<mtd>"
      output += self.elements[ 1 ].mathMl()
      output += "</mtd>"
      output += "</mtr>"

      output += "</mtable>"
      output += "</mfenced>"

    elif isSum == True:
      output += "<munderover>"
      # output += '<mo>&sum;</mo>'
      # output += '<mo>&#x2211;</mo>'
      # output += '<mo>&int;</mo>'
      output += '<mn>&#x2211;</mn>'  # this give a sum with above and lower the range

      output += '<mrow>'
      output += '<mi>'
      output += self.elements[ 0 ].mathMl()
      output += '</mi>'
      output += '<mo>=</mo>'
      output += '<mi>'
      output += self.elements[ 1 ].mathMl()
      output += '</mi>'
      output += '</mrow>'

      output += '<mi>'
      output += self.elements[ 2 ].mathMl()
      output += '</mi>'

      output += '</munderover>'

      output += '<mi>'
      output += '<mo>(</mo>'
      output += self.elements[ 3 ].mathMl()
      output += '<mo>)</mo>'
      output += '</mi>'

    elif isExp == True:
      output += '<msup>'

      output += '<mi>'
      if self.numElements() == 2:

        isExtraClose = True
        if (     isinstance( self.elements[ 1 ], SymNumber )
           and self.elements[ 1 ].power           == 1
           and self.elements[ 1 ].factDenominator == 1
           and self.elements[ 1 ].factSign        == 1 ):
          isExtraClose = False

        if (     isinstance( self.elements[ 1 ], SymVariable )
           and self.elements[ 1 ].power           == 1         ):
          isExtraClose = False

        if isExtraClose == True:
          output += '<mo>(</mo>'

        output += self.elements[ 1 ].mathMl()

        if isExtraClose == True:
          output += '<mo>)</mo>'
      else:
        output += 'e'
      output += '</mi>'

      output += '<mi>'
      output += self.elements[ 0 ].mathMl()
      output += '</mi>'

      output += '</msup>'
    else:
      # for iCnt in range( 0, len( self.elements )):
      for iCnt, elem in enumerate( self.elements ):
        if iCnt > 0:
          output += '<mo>,</mo>'

        if isFactorial == True:
          # if self.elements[ iCnt ]
          isExtraClose = True
          # if (     isinstance( self.elements[ iCnt ], SymNumber )
          #    and self.elements[ iCnt ].power           == 1
          #    and self.elements[ iCnt ].factDenominator == 1
          #    and self.elements[ iCnt ].factSign        == 1 ):
          if (   isinstance( elem, SymNumber )
             and elem.power           == 1
             and elem.factDenominator == 1
             and elem.factSign        == 1 ):
            isExtraClose = False

        if isExtraClose == True:
          output += '<mo>(</mo>'

        # output += self.elements[ iCnt ].mathMl()
        output += elem.mathMl()

        if isExtraClose == True:
          output += '<mo>)</mo>'

    if (isFactorial == False and isExp == False and isSum == False and isBinomial == False and isFloor == False and isCeil == False):
      output += "</mfenced>"

    if isFactorial == True:
      # output += '<mn>)!</mn>'
      # output += '</ci></apply>'
      # output += '</apply></apply>'
      output += '<mo>!</mo>'

    if self.power != 1:

      if self.powerCounter != 1:
        output += '</mrow>'
        output += '<mn>' + str( self.powerCounter )  + '</mn>'
        output += '</msup>'

      if self.powerSign == -1:
        output += '</mrow>'
        output += '</mfrac>'

      if ( isFactorial == True or isExp == True or isSum == True):
        output += '<mo>)</mo>'

      if self.powerDenominator != 1:
        output += '</mrow>'
        if self.powerDenominator != 2:
          output += '<mn>' + str( self.powerDenominator ) + '</mn>'
        else:
          output += '<mn></mn>'
        output += '</mroot>'

    output += '</mrow>'
    return output + '\n'

  def __str__( self ):
    output = ' '
    output += self.name + '( '

    # if ( self.expression != None ):
    #   output += str( self.expression )
    # else:
    #   output += '0'

    if self.numElements() == 0:
      output += '0'

    # for iCnt in range( 0, len( self.elements )):
    for iCnt, elem in enumerate( self.elements ):
      if iCnt > 0:
        output += ','
      # output += str( self.elements[ iCnt ] )
      output += str( elem )

    output += ' )'

    if self.power != 1:
      if self.onlyOneRoot == 1:
        output += '^'
      output += '^' + self.powerStr()

    return output

#
# symbolic expression
#
# 2 types:
# + = adding
# * = multiplying
#
# Indirect types:
# - = substracting = adding with factor = -1
# / = dividing     = multiplying with power = -1
#
class SymExpress( SymBaseList ):
  """
  A symbolic expression
  """
  def __init__( self
               , in_symType          = "+"
               , in_powerSign        = 1
               , in_powerCounter     = 1
               , in_powerDenominator = 1
               , in_onlyOneRoot      = 1 # default principal root
               ):

    # SymBasePower.__init__(self)
    super().__init__()

    self.symType          = in_symType
    self.powerSign        = in_powerSign
    self.powerCounter     = in_powerCounter
    self.powerDenominator = in_powerDenominator
    self.onlyOneRoot      = in_onlyOneRoot

  @property
  def symType(self):
    """
    Get or set the type of the expression, valid values are + and *.
    \n For a negative number use a negative factor
    \n For division use a negative power
    """
    return self._symType

  @symType.setter
  def symType(self, val):
    if not isinstance( val, str ):
      raise NameError( f'symType is incorrect: {val}, expected string value' )

    # if ( val != '+' and val != '*' ):
    if not val in ( '+', '*' ):
      raise NameError( f'symType is incorrect: {val}, expected + or *' )

    self._symType = val

  # check if a given object is equal to this object
  def isEqual( self, elem, checkFactor = True, checkPower = True ):
    """
    Check if the given object is equal to this object.
    Return True for equal and False for not equal
    """
    if not isinstance( elem, SymExpress ):
      # elem is not an expression
      return elem.isEqualExpress( self, checkFactor )

    if elem.power != self.power:
      if checkFactor == False:
        lElemFactor = False
        lSelfFactor = False

        # elemFact = None
        elemExpr = None

        # selfFact = None
        selfExpr = None

        if ( elem.symType == '*'  and elem.numElements() == 2 ):
          elem1 = elem.elements[ 0 ]
          elem2 = elem.elements[ 1 ]

          # if ( isinstance( elem1, SymNumber ) or isinstance( elem2, SymNumber )):
          #  # ok 1 is number
          #  lElemFactor = True
          #else:
          #  lElemFactor = False
          lElemFactor = isinstance( elem1, SymNumber ) or isinstance( elem2, SymNumber )

          if ( lElemFactor == True and ( isinstance( elem1, SymExpress ) or isinstance( elem2, SymExpress ))):
            # ok 1 is SymExpress
            pass
          else:
            lElemFactor = False

          if lElemFactor == True:
            if isinstance( elem1, SymNumber ):
              # elemFact = elem1
              elemExpr = elem2
            else:
              # elemFact = elem2
              elemExpr = elem1
          # elemFact & elemExpr contains the elements or None if no factor * expression
          #


        if ( self.symType == '*'  and self.numElements() == 2 ):
          self1 = self.elements[ 0 ]
          self2 = self.elements[ 1 ]

          #if ( isinstance( self1, SymNumber ) or isinstance( self2, SymNumber )):
          #  # ok 1 is number
          #  lSelfFactor = True
          #else:
          #  lSelfFactor = False
          lSelfFactor = isinstance( self1, SymNumber ) or isinstance( self2, SymNumber )

          if ( lSelfFactor == True and ( isinstance( self1, SymExpress ) or isinstance( self2, SymExpress ))):
            # ok 1 is SymExpress
            pass
          else:
            lSelfFactor = False

          if lSelfFactor == True:
            if isinstance( self1, SymNumber ):
              # selfFact = self1
              selfExpr = self2
            else:
              # selfFact = self2
              selfExpr = self1

        if ( lElemFactor == True or lSelfFactor == True ):
          if ( lElemFactor == True and lSelfFactor == True ):
            return selfExpr.isEqual ( elemExpr )

          if ( lElemFactor == False and lSelfFactor == True ):
            return selfExpr.isEqual ( elem )

          if ( lElemFactor == True and lSelfFactor == False ):
            return self.isEqual ( elemExpr )

      return False

    # only power of 1 can have a factor
    if ( checkFactor == False and (self.power != 1 or elem.power != 1 )):
      checkFactor = True

    # skip factor for 1 unit expressions or multieply (*) expressions
    if ( self.symType == '+' and self.numElements() > 1 ):
      checkFactor = True

    if ( elem.symType == '+' and elem.numElements() > 1 ):
      checkFactor = True

    if ( checkFactor == True and elem.numElements() != self.numElements() ):
      return False

    # print( "isequal self: {}, elem: {}, checkFactor: {}, self.power: {}, elem.power: {}".format( str( self ), str( elem ), checkFactor, self.power, elem.power ))


    # array to remember if element is already used
    checkArr = []
    # iMax = max( self.numElements(), elem.numElements() )
    for iCnt in range( 0, elem.numElements() ):
      checkArr.append( False )

    # print( "before check loop number of elements: " +str( self.numElements() ) )

    for iCnt in range( 0, self.numElements()):
      elem1  = self.elements[ iCnt ]

      if ( checkFactor == False and isinstance( elem1, SymNumber ) and elem1.power == 1 ):
        continue

      lFound = False
      for iCnt2 in range( 0, elem.numElements()) :
        if checkArr[ iCnt2 ] == True:
          continue
        elem2 = elem.elements[ iCnt2 ]

        if ( checkFactor == False and isinstance( elem2, SymNumber ) and elem2.power == 1 ):
          checkArr[ iCnt2 ] = True
          continue

        # print( "Check elem1: " + str( elem1 ) )
        # print( "Check elem2: " + str( elem2 ) )

        if elem1.isEqual( elem2 ) != True:
          continue
        checkArr[ iCnt2 ] = True
        lFound = True
        break

      if lFound == False:
        return False

    # print( "check all used" )

    # now check off all the elem units are used
    for iCnt2 in range( 0, elem.numElements()):
      if checkArr[ iCnt2 ] == True:
        continue
      elem2 = elem.elements[ iCnt2 ]
      if ( checkFactor == False and isinstance( elem2, SymNumber ) and elem2.power == 1 ):
        checkArr[ iCnt2 ] = True
        continue

      return False

    # print( "True ??" )
    return True

  def getValue( self, dDict = None ):
    dValue = 0

    # for iCnt in range( 0, len( self.elements )):
    for iCnt, elem1 in enumerate( self.elements ):
    # for elem1 in self.elements:
      # dValSub = self.elements[ iCnt ].getValue( dDict )
      # print( "getValue" )
      # print( type( elem1 ) )
      # print( dDict )
      dValSub = elem1.getValue( dDict )
      if iCnt == 0:
        dValue = dValSub
      else:
        if ( isinstance( dValue, list ) and isinstance( dValSub, list )):
          dResult = []
          # for iCnt1 in range( 0, len( dValue )):
          for dVal1 in dValue:
            # for iCnt2 in range( 0, len( dValSub )):
            for dValSub2 in dValSub:
              if self.symType == '+':
                # dNew = dValue[ iCnt1 ] + dValSub[ iCnt2 ]
                dNew = dVal1 + dValSub2
              else:
                # dNew = dValue[ iCnt1 ] * dValSub[ iCnt2 ]
                dNew = dVal1 * dValSub2
              dResult.append( dNew )
          dValue = dResult
        elif ( not isinstance( dValue, list ) and isinstance( dValSub, list )):
          dResult = []
          # for iCnt2 in range( 0, len( dValSub )):
          for dValSub2 in dValSub:
            if self.symType == '+':
              # dNew = dValue + dValSub[ iCnt2 ]
              dNew = dValue + dValSub2
            else:
              # dNew = dValue * dValSub[ iCnt2 ]
              dNew = dValue * dValSub2
            dResult.append( dNew )
          dValue = dResult

        elif ( isinstance( dValue, list ) and not isinstance( dValSub, list )):
          dResult = []
          # for iCnt1 in range( 0, len( dValue )):
          for dVal1 in dValue:
            if self.symType == '+':
              # dNew = dValue[ iCnt1 ] + dValSub
              dNew = dVal1 + dValSub
            else:
              # dNew = dValue[ iCnt1 ] * dValSub
              dNew = dVal1 * dValSub
            dResult.append( dNew )
          dValue = dResult

        else:
          if self.symType == '+':
            dValue += dValSub
          else:
            dValue *= dValSub

    dValue = self.valuePow( dValue  )

    return dValue

  # optimize the symExpression, but do not add or multple elements together
  def optimize( self, cAction = None ):
    """
    Optimize the expression and all the sub-units and sub-expressions.
    \ncAction = None: Optimize the expression
    \ncAction = "power" : Write out all the powers greater then one so that they become one.
    \ncAction = "onlyOneRoot" : Simply the root to lowest form [27^^(1/2) = ((3^2)*3)^^(1/2) = 3 * 3^^(1/2)].
    \ncAction = "multiply" : Multiply the elements of this expressions and his sub-expressions
    \ncAction = "i" : Write out all the imaginary numbers (eliminate powers)
    \ncAction = "add" : Adding up elements in this expression and his sub-expression.
    \ncAction = "radicals" : Write out the radicals in there lowest form
    \ncAction = "functionToValues" : Convert functions to values
    \n. . . . . . . . . `exp, binomial, factorial, floor, ceil, abs, sin, cos, tan, atan2, atan`
    \ncAction = "expandArrays" : Expand arrays
    \ncAction = "setOnlyOne" : The radicals can only have one solution
    \ncAction = "nestedRadicals" : Disassemble nested radicals
    \ncAction = "imaginairDenominator" : Remove imagiar number in the denominator,\n
    \n. . . . . . . . . `1 / ( a + bi )` into `( a + bi ) / ( a + bi )^2`
    \ncAction = "splitDenominator" : Split denominator in seperated elements,
    \n. . . . . . . . . `1 / ( a * b *c )` into `1/a * 1/b * 1/c`
    \ncAction = "sinTwoCosTwo" : `sin^2 + cos^2 = 1`
    \ncAction = "unnestingRadicals" : Unnest radicals
    """

    # print( "Optimze before super: {}".format( str( self )))

    result = super().optimize( cAction )

    # print( "Optimze after super: {}".format( str( self )))
    # print ( "Express head optimize: action:{}, self: {}".format( cAction, self ))

    result |= self._optSubThread( cAction )

    # print( "Optimze after subelements: {}".format( str( self )))
    # print( ' step start: {} {}'.format( cAction, str( self )))

    if cAction == None:
      result |= self._optimizeDefault()

    result |= self._optimzeSymSubs( cAction )

    optDef = symtables.optimizeTable.get( cAction )
    if optDef != None :
      result |= optDef.optimize( self, cAction )
      # optDef.optimize( self, cAction )

    # print( ' step end: {} {}'.format( cAction, str( self )))
    return result

  def _optSubThread(self, cAction):

    def SubThread( elem, cAction ):
      elem.optimize( cAction )

    result = False

    if globalUseThreads == False or len( self.elements ) <= 4: # was 1
      # for iCnt in range( 0, len( self.elements )) :
      for elem in self.elements:
        # print ( "Express sub optimize: action: {}, self: {}".format( cAction, self.elements[ iCnt ] ))
        # self.elements[ iCnt ].optimize( cAction )
        # print( f"_optSubThread action: {cAction} express: {str(elem)}" )
        result |= elem.optimize( cAction )
    else:
      # TODO, this does not work !!!!!!!!!!!!!!!!!!!!!!!!!!!
      arrThread = []
      # for iCnt in range( 0, len( self.elements )) :
      for elem in self.elements:
        # print ( "Express sub optimize: action: {}, self: {}".format( cAction, self.elements[ iCnt ] ))
        # elem = self.elements[ iCnt ]
        # self.elements[ iCnt ].optimize( cAction )
        thr = Thread(target=SubThread, args=(elem,cAction,))
        # thr = mp.Process(target=elem.optimize, args=(cAction,))
        # multiprocess is not working with this solutions
        # thr = Process(target=SubThread, args=(elem,cAction,))
        thr.start()
        arrThread.append( thr )

      # for iCnt in range( 0, len( arrThread )) :
      #   arrThread[ iCnt ].start()

      # for iCnt in range( 0, len( arrThread )) :
      for thrd in arrThread:
        # arrThread[ iCnt ].join()
        thrd.join()

    return result

  def _optimizeDefault( self ):
    """
    Default optimization
    """

    #  factor zero is no elements at all, and no elements is factor 0
    # power zero give always 1, is 1 element with value 1, factor is not changed
    def _optFactPowerZero():
      result = False

      #  factor zero is no elements at all, and no elements is factor 0
      if len( self.elements ) == 0:
        self.elements          = []
        self.powerSign         = 1
        self.powerCounter      = 1
        self.powerDenominator  = 1
        # result                 = True

      # print( "SymExpress optimize 3: {}".format( str( self )))

      # power zero give always 1, is 1 element with value 1, factor is not changed
      if self.power == 0:
        self.elements          = []
        self.powerSign         = 1
        self.powerCounter      = 1
        self.powerDenominator  = 1
        self.add ( SymNumber() )
        result                 = True

      # power of zero always give 1
      # for iCnt in range( 0, len( self.elements ) ) :
      for iCnt, elem in enumerate( self.elements ) :
        # elem = self.elements[ iCnt ]
        if elem.powerCounter == 0:
          self.elements[ iCnt ] = SymNumber()
          result                = True

      return result

    # if subexpression is zero delete it
    def _optMultiZero():
      result = False
      for iCnt in range( len( self.elements ) - 1, -1, -1 ) :
        elem = self.elements[ iCnt ]
        if (  ( isinstance( elem, SymNumber  ) and elem.factor        == 0 )
           or ( isinstance( elem, SymExpress ) and elem.numElements() == 0 )
           ):
          if self.symType == '*':
            # sys.stderr.write( "_optMultiZero before: "  + str( self ) + "\n"  )
            self.elements = []
            # sys.stderr.write( "_optMultiZero after: "  + str( self ) + "\n"  )
            result        = True
            return result

          # if ( self.symType == '+' ):
          del self.elements[ iCnt ]
          result = True

      # if result == True:
      #  sys.stderr.write( "_optMultiZero: "  + str( self ) + "\n"  )

      return result

    # delete all sympressesion with zero elements
    def _optDelZeroElements():
      result = False

      if self.symType != '+':
        return result

      #newElements = []
      ## for iCnt in range( 0, len( self.elements )) :
      #for elem in self.elements:
      #  # elem = self.elements[ iCnt ]
      #  if isinstance( elem, SymExpress ) and elem.numElements() == 0:
      #    continue

      #  if ( isinstance( elem, SymNumber ) and elem.factor == 0 ) :
      #    continue

      #  newElements.append( elem )
      #self.elements = newElements

      for iCnt in range( len( self.elements ) - 1, -1, -1 ) :
        elem = self.elements[ iCnt ]
        if isinstance( elem, SymExpress ) and elem.numElements() == 0:
          del self.elements[ iCnt ]
          result = True
          continue
        if ( isinstance( elem, SymNumber ) and elem.factor == 0 ) :
          del self.elements[ iCnt ]
          result = True
          continue

      return result



    # kill 1 units. but never the last one
    def _optKillOneUnits():
      result = False
      if ( self.symType == '*' and len( self.elements ) > 1 ):
        # print ( "Test 1 units" )
        for iCnt in range( len( self.elements ) - 1, -1, -1) :
          elem = self.elements[ iCnt ]

          if not isinstance( elem, SymNumber ):
            continue

          if elem.factor != 1:
            continue

          if len( self.elements ) != 1:
            del self.elements[ iCnt ]
            result = True

      return result

    # get lower symexpress with same type and factor and power of 1
    def _optGetLowerSameType():
      result = False
      lFound = True
      while lFound == True:
        lFound = False
        # for iCnt in range( 0, len( self.elements ) ) :
        for iCnt, elem in enumerate( self.elements ) :
          # elem = self.elements[ iCnt ]
          if not isinstance( elem, SymExpress ):
            continue
          if elem.symType != self.symType:
            continue
          if elem.power != 1:
            continue

          del self.elements[ iCnt ]
          lFound = True


          # for iCnt2 in range( 0, elem.numElements() ):
          for elem2 in elem.elements:
            # elem2 = elem.elements[ iCnt2 ]
            self.add( elem2 )

          break
      return result

    #
    # main default optimize
    # .....................
    result = False

    # print( "Optimze before: {}".format( str( self )))

    # factor zero is no elements at all, and no elements is factor 0
    # power zero give always 1, is 1 element with value 1, factor is not changed
    result |= _optFactPowerZero()

    # sys.stderr.write( f"optimze 1: {result}" + "\n"  )

    # print( "Optimze (1): {}".format( str( self )))

    # if subexpression is zero delete it
    result |= _optMultiZero()

    # sys.stderr.write( f"optimze 2: {result}" + "\n"  )


    # print( "Optimze (2): {}".format( str( self )))

    # delete all sympressesion with zero elements
    result |= _optDelZeroElements()

    # print( "Optimze (3): {}".format( str( self )))

    # sys.stderr.write( f"optimze 3: {result}" + "\n"  )


    # is sub element is a symexpress with 1 element, get it
    result |= self._optGetOneExpressions()

    # print( "Optimze (4): {}".format( str( self )))
    # sys.stderr.write( f"optimze 4: {result}" + "\n"  )

    # kill 1 units. but never the last one
    result |= _optKillOneUnits()

    # print( "Optimze (5): {}".format( str( self )))
    # sys.stderr.write( f"optimze 5: {result}" + "\n"  )


    # get lower symexpress with same type and factor and power of 1
    result |= _optGetLowerSameType()

    # print( "Optimze (6): {}".format( str( self )))

    # sys.stderr.write( f"optimze 6: {result}" + "\n"  )


    # print( "SymExpress optimize 7: {}".format( str( self )))
    return result


  def optimizeNormal( self , output = None, filehandle = None, extra = None, varDict = None ):
    """
    Normalize the expression, this is a combination of optimize(), multiply, i, power and add optimzie methodes
    \n output = SymToHtml class
    \n filehandle = file handle
    \n If output and/or a filehandle is given then all the sub-optimizations will be writen to it.
    """
    def _printCalc():
      if ( extra != None and "calculation" in extra ):
        dValue = self.getValue( varDict )
        if output != None:
          output.writeLine( f'Calculated: {str( dValue )}' )
        if filehandle != None:
          print( f'Calculated: {str( dValue )}', file=filehandle )


    def _optimzeAction( arrAction, cText, maxCount = 10 ):
      # cStart   = ''
      iCnt     = 0
      # cTest  = str( self )
      bChanged = True
      # while( iCnt < maxCount and cStart != cTest):
      while( iCnt < maxCount and bChanged == True ):
        # cStart  = cTest
        bChanged = False
        iCnt    += 1
        cCode    = 'None'

        for cAction in arrAction:
          # print( f"_optimzeAction: {cAction}" )
          bChanged |= self.optimize( cAction )

          # if output != None:
          #   output.writeLine( f"cAction: {cAction} bChanged: {bChanged} ")

          # bChanged = True
          cCode = cAction

        bChanged |= self.optimize( None )
        # self.optimize( None )
        # if output != None:
        #   output.writeLine( f"cAction: None bChanged: {bChanged} ")

        # max iteration reached and no output, leave
        if iCnt >= maxCount and output == None and filehandle == None:
          break

        # cTest = str( self )  # cost a lot of time
        # if cTest == cStart:
        #   break # nothing changed, leave loop
        if bChanged == False:
          break # nothing changed, leave loop


        if output != None:
          output.writeLine( '<br>' + cText + ' [' + cCode + '] ' + str( iCnt ) )
          output.writeSymExpress( self )
          output.writeLine( str( self ))
        if filehandle != None:
          print( cText + ' [' + cCode + '] ' + str( iCnt ), file=filehandle )
          print( self, file=filehandle )
          SymExpressTree( self, filehandle )

        _printCalc()


    if output != None:
      if not isinstance( output , SymToHtml ):
        raise NameError( f'optimizeNormal, output is incorrect: {type( output )}, expected SymToHtml object or None' )

    if output != None:
      output.writeLine( '<br>Orignal expression' )
      output.writeSymExpress( self )
      output.writeLine( str( self ))

    if filehandle != None:
      print( "Orignal expression", file=filehandle )
      print( self, file=filehandle )
      SymExpressTree( self, filehandle )
    _printCalc()

    cStartBig = ''
    iCntBig   = 0
    cTestBig  = str( self )
    maxBig    = 10
    while( iCntBig < maxBig and cStartBig != cTestBig):
      cStartBig  = cTestBig
      iCntBig   += 1

      _optimzeAction( []                  , "Optimize expression"    ,  1 )
      _optimzeAction( [ "power"          ], "Eliminate powers"       ,  1 )
      _optimzeAction( [ "onlyOneRoot"    ], "Simplify only one roots",  1 )
      _optimzeAction( [ "multiply"       ], "Multiply elements"      , 10 )
      # _optimzeAction( [ "i"  , "multiply"], "Write out i"            ,  1 )
      # _optimzeAction( [ "add", "multiply"], "Add elements"           , 10 )
      _optimzeAction( [ "i"              ], "Write out i"            ,  1 )
      _optimzeAction( [ "add"            ], "Add elements"           , 10 )

      if iCntBig < maxBig:
        cTestBig  = str( self )

    if output != None:
      output.writeLine( '<br>' )
    if filehandle != None:
      print( " ", file=filehandle )


  def optimizeSpecial( self , output = None, filehandle = None, extra = None, varDict = None ):
    """
    Optimize the expression in all the posibilities, this use the power, multiply, i , add, radicals, unnestingRadicals, nestedRadicals, imaginairDenominator, splitDenominator, sinTwoCosTwo and functionToValues optimizations
    \n output = SymToHtml class
    \n filehandle = file handle
    \n If output and/or a filehandle is given then all the sub-optimizations will be writen to it.
    \n extra = list of extra optimizations:
    \n .............[ "calculation" ] for calculate the value and put it in the given output

    """

    def _printCalc( cTekst, iCnt, iCntBig ):
      if ( extra != None and "calculation" in extra ):
        dValue = self.getValue( varDict )
        if output != None:
          output.writeLine( f'Calculated {cTekst} {iCnt}/{iCntBig}: value:{str( dValue )}' )
        if filehandle != None:
          print( f'Calculated {cTekst} {iCnt}/{iCntBig}: value:{str( dValue )}', file=filehandle )


    def _optimizeAction( arrAction, cText, iCntBig, iMaxCnt ):
      # cStart = ''
      iCnt      = 0
      # cTest = str( self )
      bChanged = True
      cCode    = 'None'
      # while( iCnt < iMaxCnt and cStart != cTest):
      while( iCnt < iMaxCnt and bChanged == True ):
        # cStart = str( self )
        bChanged = False
        iCnt += 1

        for cAction in arrAction:
          # self.optimize( "nestedRadicals" )
          bChanged |= self.optimize( cAction )
          cCode     = cAction

        # cTest = str( self )
        # if cTest == cStart:
        #  continue
        if bChanged == False:
          break


        if output != None:
          output.writeLine( '<br>' + cText + ' [' + cCode + '] ' + str( iCnt ) + '/' + str( iCntBig ) )
          output.writeSymExpress( self )
          output.writeLine( str( self ))
        if filehandle != None:
          print( cText + ' [' + cCode + '] ' + str( iCnt ) + '/' + str( iCntBig ), file=filehandle )
          print( self, file=filehandle )
          SymExpressTree( self, filehandle )

        self.optimizeNormal( output, filehandle, extra, varDict )
        # _printCalc( cText, iCnt, iCntBig )
        _printCalc( arrAction[0], iCnt, iCntBig )


    _printCalc( 'start', 0, 0 )

    self.optimizeNormal( output, filehandle, extra, varDict )

    cStartBig = ''
    iCntBig   = 0
    cTest     = str( self )
    iBigMax   = 8
    while( iCntBig < iBigMax and cStartBig != cTest  ):
      cStartBig = cTest
      iCntBig  += 1

      if output != None:
        output.writeLine( '<br>Big Loop '  + str( iCntBig ) )
      if filehandle != None:
        print( "Big Loop "  + str( iCntBig ), file=filehandle )

      _printCalc( 'start', 0, iCntBig )

      _optimizeAction( ["rootToPrincipalRoot"         ], 'Write out all roots into principal roots'    , iCntBig,  1 )
      _optimizeAction( ["powerArrays"                 ], 'Put the power of the array into the elements', iCntBig,  1 )
      _optimizeAction( ["arrayPower"                  ], 'Put the power of an array into his elements' , iCntBig, 10 )
      _optimizeAction( ["functionToValues"            ], 'Function to values'                          , iCntBig, 10 )
      _optimizeAction( ["negRootToI"                  ], 'Negative root to i'                          , iCntBig,  1 )
      _optimizeAction( ["functionToValues"            ], 'Function to values'                          , iCntBig, 10 )
      _optimizeAction( ["unnestingRadicals"           ], 'Unnesting Radicals'                          , iCntBig,  1 ) # unnesting radicals
      _optimizeAction( ["functionToValues"            ], 'Function to values'                          , iCntBig, 10 )
      _optimizeAction( ["radicalDenominatorToCounter" ], 'Radical denominator to counter'              , iCntBig,  1 )
      _optimizeAction( ["rootIToSinCos"               ], 'Root i to cos + i sin'                       , iCntBig,  1 )
      _optimizeAction( ["functionToValues"            ], 'Function to values'                          , iCntBig, 10 )
      _optimizeAction( ["imaginairDenominator"        ], 'Imaginair Denominator'                       , iCntBig,  1 ) # get imaginair denominator into the counter
      _optimizeAction( ["rootOfImagNumToCosISin"      ], 'Root of imaginaire number to cos + i sin'    , iCntBig,  1 )
      _optimizeAction( ["functionToValues"            ], 'Function to values'                          , iCntBig, 10 )
      _optimizeAction( ["nestedRadicals"              ], 'Nested radicals'                             , iCntBig, 10 )
      _optimizeAction( ["sinTwoCosTwo"                ], 'Sin^2 + Cos^2'                               , iCntBig,  1 ) # sin(x)^2 + cos(x)^2 = 1
      _optimizeAction( ["cosXplusYtoSinCos"           ], 'cos(x+y) = cos(x)cos(y) - sin(x)sin(y)'      , iCntBig, 10 )
      _optimizeAction( ["sinXplusYtoSinCos"           ], 'sin(x+y) = sin(x)cos(y) + cos(x)sin(y)'      , iCntBig, 10 )
      _optimizeAction( ["splitDenominator"            ], 'Split Denominator'                           , iCntBig,  1 ) # get 1 ( a * b * c )  as 1/a * 1/b * 1/b
      _optimizeAction( ["expandArrays"                ], 'Expand arrays'                               , iCntBig, 10 )
      # _optimizeAction( ["cosAtanDiv3"                 ], 'cos( atan(x)/3)'                             , iCntBig,  1 )


      if iCntBig >= iBigMax:
        break
      cTest = str( self ) # cost a lot of time

    if output != None:
      output.writeLine( '<br>' )
    if filehandle != None:
      print( " ", file=filehandle )


  # copy the expression (sort of deepcopy)
  def copy( self ):
    """
    Make a copy of this expression.
    """
    copySymExpress = SymExpress( self.symType
                               , self.powerSign
                               , self.powerCounter
                               , self.powerDenominator
                               , self.onlyOneRoot
                               )
    # for iCnt in range( 0, len( self.elements )) :
    for elem in self.elements:
      # copySymExpress.add( self.elements[ iCnt ] )
      copySymExpress.add( elem )
    return copySymExpress

  # output in MatMl format
  def mathMl( self ):
    """
    Give the expression in MatMl format.
    """
    output = ''

    output += '<mrow>'

    # lCloseFactor = False

    if self.power != 1:
      if self.powerDenominator != 1:
        output += '<mroot' + self.powerMathMlColor() + '>'
        output += '<mrow>'

      if self.powerSign == -1:
        output += '<mfrac>'
        output += '<mn>1</mn>'
        output += '<mrow>'

      if self.powerCounter != 1:
        output += '<msup>'
        output += '<mrow>'

    # if ( self.power != 1 or self.factor != 1 ):
    # if ( self.symType != '*' and ( self.power != 1 or self.factor != 1 ) ):
    # if ( self.symType != '*' and ( self.powerCounter != 1 or ( self.factor != 1 and self.powerDenominator == 1 ) ) ):
    # if ( self.symType != '*' and self.powerCounter != 1 ):
    if self.powerCounter != 1:
      output += "<mfenced separators=''>"

    if len( self.elements ) == 0:
      output += '<mn>0</mn>'

    specicalVar = False
    if (self.symType == "*" and self.power == 1 and len( self.elements ) == 2 ):
      elem1 = self.elements[ 0 ]
      elem2 = self.elements[ 1 ]
      if  ( ( isinstance( elem1, SymNumber ) and isinstance( elem2, SymVariable )) or
             ( isinstance( elem2, SymNumber ) and isinstance( elem1, SymVariable ))   ):
        if not isinstance( elem1, SymNumber ):
          elem1 = self.elements[ 1 ]
          elem2 = self.elements[ 0 ]
        if ( elem1.power == 1 and elem1.factor == -1 and elem2.power == 1 ):
          specicalVar = True
          output += '<mi>-</mi>' + elem2.mathMl()

    if specicalVar == False:
      # for iCnt in range( 0, len( self.elements )) :
      for iCnt, elem in enumerate( self.elements ) :
        if iCnt > 0:
          # if ( self.symType == '+' and iCnt < len( self.elements ) and self.elements[ iCnt ].factSign == -1 and self.elements[ iCnt ].factDenominator == 1 and self.elements[ iCnt ].powerDenominator == 1 ):
          # if ( self.symType == '+' and iCnt < len( self.elements ) and self.elements[ iCnt ].factSign == -1 and self.elements[ iCnt ].powerDenominator == 1 ):
          # if ( False and self.symType == '+' and  self.elements[ iCnt ].hasNegativeSign() ):
          #   output += '<mspace width="4px" />'
          # else:
          if ( self.symType == '+'
              and iCnt < len( self.elements )
              # and isinstance( self.elements[ iCnt ], SymNumber )
              # and self.elements[ iCnt ].factSign        == -1
              # and self.elements[ iCnt ].factDenominator ==  1
              # and self.elements[ iCnt ].power           ==  1 ):
              and isinstance( elem, SymNumber )
              and elem.factSign        == -1
              and elem.factDenominator ==  1
              and elem.power           ==  1 ):
            output += '<mspace width="4px" />'
          else:
            output += '<mspace width="4px" />'
            output += '<mo>' + self.symType + '</mo> '
            output += '<mspace width="4px" />'


        # if ( self.elements[ iCnt ].power != 1 ):
        #   output += "<mfenced separators=''>"
        #   output += self.elements[ iCnt ].mathMl()
        #   output += "</mfenced>"
        #else:
        # if ( isinstance( self.elements[ iCnt ], SymExpress ) and self.elements[ iCnt ].symType != '*' and self.elements[ iCnt ].power == 1 ):
        if ( isinstance( elem, SymExpress ) and elem.symType != '*' and elem.power == 1 ):
          output += "<mfenced separators=''>"
          # output += self.elements[ iCnt ].mathMl()
          output += elem.mathMl()
          output += "</mfenced>"
        else:
          # output += self.elements[ iCnt ].mathMl()
          output += elem.mathMl()

        # if ( self.symType == '*' and isinstance( self.elements[ iCnt ] ,SymExpress ) and self.elements[ iCnt ].symType != '*' ) :
        #   # if ( self.elements[ iCnt ].IsFactorPowerOne() and ( self.elements[ iCnt ].numElements() ) > 1 ):
        #   # if ( self.elements[ iCnt ].factor == 1 and self.elements[ iCnt ].power == 1 and ( self.elements[ iCnt ].numElements() ) > 1 ):
        #   if ( self.elements[ iCnt ].power == 1 and ( self.elements[ iCnt ].numElements() ) > 1 ):
        #      output += "<mfenced separators=''>"
        #      output += self.elements[ iCnt ].mathMl()
        #      output += "</mfenced>"
        #   else:
        #      output += self.elements[ iCnt ].mathMl()
        #else:
        #   output += self.elements[ iCnt ].mathMl()

    # if ( self.symType != '*' and ( self.power != 1 or self.factor != 1 ) ):
    # if ( self.symType != '*' and ( self.powerCounter != 1 or ( self.factor != 1 and self.powerDenominator == 1 ) ) ):
    # if ( self.symType != '*' and self.powerCounter != 1  ):
    if self.powerCounter != 1:
      output += "</mfenced>"

    if self.power != 1:
      if self.powerCounter != 1:
        output += '</mrow>'
        output += '<mn>' + str( self.powerCounter )  + '</mn>'
        output += '</msup>'

      if self.powerSign == -1:
        output += '</mrow>'
        output += '</mfrac>'

      if self.powerDenominator != 1:
        output += '</mrow>'
        if self.powerDenominator != 2:
          output += '<mn>' + str( self.powerDenominator ) + '</mn>'
        else:
          output += '<mn></mn>'
        output += '</mroot>'

    # if ( lCloseFactor == True ):
    #   output += "</mfenced>"

    output += '</mrow>'
    return output + '\n'

  # the SymExpress in string format
  def __str__( self ):
    output = ''

    # if ( self.symType != '*' and ( self.power != 1 or self.factor != 1 ) ):
    # if ( self.power != 1 or self.factor != 1 ):
    if self.power != 1:
      output += '('

    if len( self.elements ) == 0:
      output += '0'

    #for iCnt in range( 0, len( self.elements )) :
    for iCnt, elem in enumerate( self.elements ) :
      if iCnt > 0:
        # if ( self.symType == '+' and self.elements[ iCnt ].hasNegativeSign() ):
        #   output += ' '
        # else:
        output += ' ' + self.symType + ' '

        # print ( "iCnt: {}, len: {}".format( iCnt, len( self.elements )))
        # if ( self.symType == '+' and ( iCnt ) < len( self.elements ) and self.elements[ iCnt ].factSign == -1 ):
        #   if ( isinstance( self.elements[ iCnt ] , SymVariable ) and self.elements[ iCnt ].name == '' and self.elements[ iCnt ].power != 1 ):
        #      output += ' ' + self.symType + ' '
        #   else:
        #      output += ' '
        #else:
        #   output += ' ' + self.symType + ' '

      # if ( type( self.elements[ iCnt ] ) is SymExpress ) :
      #   output += '( '
      # if ( self.symType == '*' and isinstance( self.elements[ iCnt ] , SymExpress ) and self.elements[ iCnt ].symType != '*' ) :
      if ( self.symType == '*' and isinstance( elem, SymExpress ) and elem.symType != '*' ) :
        # if ( self.elements[ iCnt ].IsFactorPowerOne() and ( self.elements[ iCnt ].numElements() ) > 1 ):
        # if ( self.elements[ iCnt ].factor == 1 and self.elements[ iCnt ].power == 1 and ( self.elements[ iCnt ].numElements() ) > 1 ):

        #if ( self.elements[ iCnt ].power == 1 and ( self.elements[ iCnt ].numElements() ) > 1 ):
        if ( elem.power == 1 and ( elem.numElements() ) > 1 ):
          # output += '(' + str( self.elements[ iCnt ] ) + ')'
          output += '(' + str( elem ) + ')'
        else:
          # output += str( self.elements[ iCnt ] )
          output += str( elem )
      else:
        # output += str( self.elements[ iCnt ] )
        output += str( elem )
      # if ( type( self.elements[ iCnt ] ) is SymExpress ) :
      #   output += ' )'

    # if ( self.symType != '*' and ( self.power != 1 or self.factor != 1 ) ):
    # if ( self.power != 1 or self.factor != 1 ):
    if self.power != 1:
      output += ')'

    if self.power != 1:
      if self.onlyOneRoot == 1:
        output += '^'
      output += '^' + self.powerStr()

    return output


# """
# Functions:
#  - SymToHtml        : write SymExpress to given (html) file in mathml format
#  - SymFormulaParser : Parse string to create a SymExpress object
#  - SymExpressTree   : Display the SymExpress tree (for debug)
# """

#
# write SymExpress formules too a html file
#
# class SymToHtml( object ):
class SymToHtml():
  """
  Write given SymExpress class in html (MathMl) format to a given file.
  """

  def __init__( self, inFilename = 'mathml.html', inTitle = 'SymToHtml' ):
    self._isOpen    = False
    self.isOpen     = False
    self._textFile  = None
    self.fileName   = inFilename
    self.title      = inTitle

  def __del__(self):
    self.isOpen = False

  @property
  def fileName(self):
    """
    Get or set the (html) filename (string)
    """
    return self._fileName

  @fileName.setter
  def fileName(self, val):
    # None = sys.stdout
    if val != None and not isinstance( val, str):
      raise NameError( f'fileName is incorrect: {val}, expected string value' )
    self.isOpen     = False
    self._fileName = val

  @property
  def isOpen(self):
    """
    Get of the file is open. If set and the file is not already open, it will open the file.
    \n type: boolean
    """
    return self._isOpen

  @isOpen.setter
  def isOpen(self, val):
    if not isinstance( val, bool):
      raise NameError( f'isOpen is incorrect: {val}, expected boolean value' )
    if ( val == False and self._isOpen == True ):
      self.writeFooter()
      if self.fileName != None :
        self._textFile.close()
      self._textFile = None
    self._isOpen = val


  def openFile(self):
    """
    Open the file if if is not already open. It will automatical write a html header (writeHeader) the the file.
    """
    if self.isOpen == True:
      return self.isOpen # is alreadu open
    if self.fileName == None:
      self._textFile = sys.stdout
    else:
      self._textFile = open( self.fileName, mode="w", encoding="utf-8")  # pylint: disable=consider-using-with
    self.isOpen    = True
    self.writeHeader()
    return self.isOpen

  def closeFile(self):
    """
    Close the file if it was open. If the file was open it write a html footer (writeFooter) too the file
    """
    self.isOpen = False
    return self.isOpen


  def writeLine( self, cLine, cTitle = None ):
    """
    Write the given text line to the file. If the file is not open, it will be opened.
    """
    if self.isOpen == False:
      self.openFile()
    if cTitle != None:
      self._textFile.write( cTitle )
      self._textFile.write( '<br>' )
    self._textFile.write( str( cLine ) + '\n' )
    self._textFile.write( '<br>' )

  def write( self, cData ):
    """
    Write the given text to the file. If the file is not open, it will be opened.
    """
    if self.isOpen == False:
      self.openFile()
    self._textFile.write( str( cData ) + '\n' )

  def writeHeader( self ):
    """
    Write the default html header to the file. Is called by opening the file (openFile).
    """
    self.write( '<!DOCTYPE html>' )
    self.write( '<html>' )
    self.write( '<head>' )
    self.write( '<meta charset="utf-8">' )
    self.write( '<title>' + self.title + '</title>' )
    self.write( '<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>' )
    self.write( '</head>' )
    self.write( '<body>' )

  def writeFooter( self ):
    """
    Write the default html footer to the file. Is called by closing (closeFile) the file.
    """
    self.write( '</body>' )
    self.write( '</html>' )

  def writeSymExpress( self, oSymExpress, cTitle = None ):
    """
    Write a SymExpress in MatmMl format to the file. If the file is not open, it will be opened.
    """
    cMath = oSymExpress.mathMl()
    if cTitle != None:
      self.writeLine( cTitle )
    self.write( "<math math-style='normal'>"  )
    self.write( cMath     )
    self.write( '</math>' )
    self.writeLine( '' )

  def writeGetValues( self, oFrm, dDictVars = None, cTitle = None ):
    """
    Write the values (getValue) from the expression
    """
    if cTitle != None:
      self.writeLine( cTitle )
    try:
      dValue = oFrm.getValue( dDictVars )

      if isinstance( dValue, list ):
        # for iCnt in range( 0, len( dValue )):
        for iCnt, dValSel in enumerate( dValue ):
          # self.writeLine( "Result (" + str( iCnt + 1 ) + ") : " + str( dValue[ iCnt ] ))
          self.writeLine( "Result (" + str( iCnt + 1 ) + ") : " + str( dValSel ))
      else:
        self.writeLine( "Result: " + str( dValue ))

    except NameError as exceptInfo:
      self.writeLine( "Error: " + str( exceptInfo ))
    except: # pylint: disable=bare-except
      self.writeLine( "Error: " + str( sys.exc_info()[0] ))


  def writeVariables( self, dVars, cTitle = None ):
    """
    Write the variables (dictonary)
    """
    if cTitle != None:
      self.writeLine( cTitle )
    for key, value in dVars.items() :
      self.writeLine( key + ' = ' + str( value ))

  def writeSymExpressComplete( self, oSymExpress, dVars = None, cTitle = None ):
    """
    Write the expression in MathMl and ascii format and calculate the value(s).
    """
    self.writeSymExpress( oSymExpress, cTitle )
    self.writeLine( str( oSymExpress ) )
    self.writeGetValues( oSymExpress , dVars )
    self.writeLine( '' )

#
# special for threads
#
# multiprocess is not working with this solutions
# def subThread( elem, cAction ):
#   elem.optimize( cAction )


#
# display the expression tree to the default output (for debug)
#
def SymExpressTree( symexpress, filehandle = None ):
  """
  Print all the elements of the given SymExpress class in tree format to the output. If not given the sys.stdout is used.

  Args:
     symexpress (SymExpress):  Expression to print the tree
     filehandle (file): Print the tree too this file, if not given the default output will be used.
  """
  def SymExpressTreeSub( symexpress, level ):
    sprint = ""
    # for iCnt in range( 1, level ):
    for _ in range( 1, level ):
      sprint += '  '

    if isinstance( symexpress, SymNumber ):
      # print( "{} lvl {} SymNumber  : f: {}, p: {}   expr: {}".format( sprint, level, symexpress.factor, symexpress.power, str( symexpress ) ), file=filehandle )
      print( f"{sprint} lvl {level} SymNumber  : f: {symexpress.factor}, p: {symexpress.power}   expr: {str( symexpress )}", file=filehandle )
    elif isinstance( symexpress, SymVariable ):
      # print( "{} lvl {} SymVariable: {} p: {}   expr: {}".format( sprint, level, symexpress.name, symexpress.power, str( symexpress ) ), file=filehandle )
      print( f"{sprint} lvl {level} SymVariable: {symexpress.name} p: {symexpress.power}   expr: {str( symexpress )}", file=filehandle )

    elif isinstance( symexpress, SymFunction ):
      # print( "{} lvl {} SymFunction: {} p: {} cnt: {}   expr: {}".format( sprint, level, symexpress.name, symexpress.power, symexpress.numElements(), str( symexpress ) ), file=filehandle )
      print( "{sprint} lvl {level} SymFunction: {symexpress.name} p: {symexpress.power} cnt: {symexpress.numElements()}   expr: {str( symexpress )}", file=filehandle )
    elif isinstance( symexpress, SymArray ):
      # print( "{} lvl {} SymArray   : p: {} cnt: {}   expr: {}".format( sprint, level, symexpress.power, symexpress.numElements(), str( symexpress ) ), file=filehandle )
      print( "{sprint} lvl {level} SymArray   : p: {symexpress.power} cnt: {symexpress.numElements()}   expr: {str( symexpress )}", file=filehandle )
    elif isinstance( symexpress, SymExpress ):
      # print( "{} lvl {} SymExpress : {} p: {} cnt: {}   expr: {}".format( sprint, level, symexpress.symType, symexpress.power, symexpress.numElements(), str( symexpress ) ), file=filehandle )
      print( "{sprint} lvl {level} SymExpress : {symexpress.symType} p: {symexpress.power} cnt: {symexpress.numElements()}   expr: {str( symexpress )}", file=filehandle )
    else:
      # print( "{} lvl {} Unnkwown type: {}    expr: {}".format( sprint, level, type( symexpress ), str( symexpress ) ), file=filehandle )
      print( "{sprint} lvl {level} Unnkwown type: {type( symexpress )}    expr: {str( symexpress )}", file=filehandle )

    if isinstance( symexpress , SymBaseList ):
      # for iCnt in range( 0, len( symexpress.elements ) ):
      for elem1 in symexpress.elements:
        # elem1 = symexpress.elements[ iCnt ]
        SymExpressTreeSub( elem1, level + 1 )

  if filehandle == None:
    filehandle = sys.stdout

  SymExpressTreeSub( symexpress, 1 )

# """
# String formule parser:
# nummer=0..9
# getal = <-><nummer>...
# letter=a..zA..Z
# name = <letter>...
# operator=+|-|*|/
# power=^|^^
# start subformule=(
# end subformule=)
# formule=<number|name><operator><number|name>|<start subformula><formula><end subformula>
# """

# iPosCur = 0    # Current position in the formula
# def SymFormulaParser ( cFormula, iStartPos = -1, cEndChar = None ) :
def SymFormulaParser ( cFormula ) :
  """
  Parse a given string and make a SymExpress from it.
  Returns a SymExpress class.
  \n digits           = 0..9
  \n number           = &lt;-&gt;&lt;digits&gt;...
  \n letter           = a..zA..Z
  \n name             = &lt;letter&gt;...
  \n operator         = +|-|*|/|^|^^  (^^=radical has only 1 solution)
  \n function         = &lt;name&gt;( &lt;formula>|, &lt;formula>|...
  \n end function     = )
  \n start subformule = (
  \n end subformule   = )
  \n formula          =&lt;number|name|function&gt;&lt;operator&gt;&lt;number|name|function&gt;|&lt;start subformula&gt;&lt;formula&gt;&lt;end subformula&gt;
  \n Example: (4+2^3) + y( 1 + 3 i x)^2 + sin( 2 pi )
  """
  # global iPosCur
  iPosCur = 0

  def _symFormulaParser ( cFormula, iStartPos = -1, cEndChar = None ) :

    oMul    = None
    oPlus   = None
    oUnit   = None
    oExpress= None

    # check input parameters
    # if not type( cFormula ) is str :
    if not isinstance( cFormula, str) :
      raise NameError( f'Formula must be a string, found: {cFormula}' )

    cFormula = cFormula.strip()
    if len( cFormula ) <= 0:
      raise NameError( 'No formula given' )

    # give current position in formula
    def GetCurPos():
      # global iPosCur
      nonlocal iPosCur
      return iPosCur

    # give next character
    def CharNext():
      # global iPosCur
      nonlocal iPosCur

      iPosCur += 1
      if iPosCur >= len( cFormula ):
        iPosCur -= 1
        return None

      return cFormula[ iPosCur:iPosCur + 1 ]

    # set last character back
    def CharBack():
      # global iPosCur
      nonlocal iPosCur

      if iPosCur >= 0:
        iPosCur -= 1

    # get current character
    def CharCurrent():
      # global iPosCur
      nonlocal iPosCur

      if iPosCur >= len( cFormula ):
        iPosCur -= 1
        return None

      return cFormula[ iPosCur:iPosCur + 1 ]


    # check if it is a skip character
    def IsSkipChar( cChar ):
      if ( cChar == ' ' or cChar == '\t' or cChar == '\n' ): # pylint: disable=consider-using-in
        return True
      return False


    # Skip with space, tab and newlines
    def SkipWithSpace():
      cChar = CharNext()
      if cChar == None:
        return
      while IsSkipChar( cChar ) == True:
        cChar = CharNext()
      if cChar != None:
        CharBack() # read 1 too many, put it back

    # get 1 parameter = number or name
    def GetParam():
      # global iPosCur
      nonlocal iPosCur

      SkipWithSpace()

      cChar = CharNext()
      if cChar == None:
        return None

      cResult = cChar

      # splting number of name
      if ( cResult == '-' or cResult.isdigit() ) :
        # numbers
        while cChar != None:
          cChar = CharNext()
          if cChar == None:
            break
          if IsSkipChar( cChar ) == True:
            CharBack()  # read 1 to many
            break
          if cChar.isdigit():
            cResult += cChar
          else:
            CharBack() # read 1 too many
            break
      elif cResult.isalpha():
        # names
        while cChar != None:
          cChar = CharNext()
          if cChar == None:
            break
          if IsSkipChar( cChar ) == True:
            CharBack()  # read 1 to many
            break
          if cChar.isdigit():
            # second pos, numbers are allowed
            cResult += cChar
          elif cChar.isalpha():
            # letters are allowd
            cResult += cChar
          else:
            CharBack() # read 1 too many
            break
      elif cResult == '(':
        # subformule
        return _symFormulaParser( cFormula, iPosCur, ')' )
      # elif ( cResult == cEndChar ):
      elif cResult == '[':
        exp   = SymArray()
        oElem = _symFormulaParser( cFormula, iPosCur, '|]' )
        exp.add( oElem )
        while CharCurrent() == '|':
          oElem = _symFormulaParser( cFormula, iPosCur, '|]' )
          exp.add( oElem )
        return exp
      elif ( cEndChar == cResult or ( cEndChar != None and cEndChar.find( cResult ) >= 0 ) ):
        CharBack() # read 1 too many
        return None
      else:
        # onbekend teken error
        raise NameError( f'Incorrect character {cChar} on position {GetCurPos()}' )

      # print ( "getParam, cResult: {}".format( cResult ))
      return cResult

    # check if cParam is een expression
    def IsSymExpress( cParam ):
      # if ( isinstance( cParam , SymExpress ) or isinstance( cParam, SymArray)):
      if isinstance( cParam , (SymExpress, SymArray )):
        return True
      return False

    # is string a numbers
    def IsNumber( cParam ):
      # if ( cParam == "infinity"):
      #   return False
      if cParam[0].isalpha():
        return False

      try:
        float( cParam )
        return True
      except ValueError:
        return False

    def IsInteger( cParam ):
      try:
        int( cParam )
        return True
      except ValueError:
        return False

    def GetNumber( cParam ):
      if IsInteger( cParam ):
        return int( cParam )
      # else:
      raise NameError( f'Incorrect number {cParam} on position {GetCurPos()}' )

    # Get an operator
    def GetOperator():
      SkipWithSpace()

      cChar = CharNext()
      if cChar == None:
        return None

      # if ( cChar == cEndChar ):
      if ( cEndChar == cChar or ( cEndChar != None and cEndChar.find( cChar ) >= 0 )):
        return None

      if cChar in [ '+', '-', '/', '*', '^' ]:
        cResult = cChar
      else:
        # operator is not need A X means A * X
        # 2A = 2 * A
        cResult = '**' # ** is implicit multiply
        CharBack() # read 1 too many

      return cResult


    # init vars
    nonlocal iPosCur

    iPosCur = iStartPos  # not yet started
    oMul    = SymExpress( '*' )
    oPlus   = SymExpress( '+' )
    iExpt   = 1

    cParam = GetParam()
    while True :
      #
      # check if cParam is an object -> subformule from ()
      # switchen between oUnit an oExpress
      #
      # print( "Before bepaling, iExpt: {}, cParam: {}".format( iExpt, str( cParam ) ) )
      if IsSymExpress( cParam ):
        # print( "IsSymExpress" )
        oUnit    = None
        if iExpt != 1:
          cParam2 = SymExpress()
          cParam2.powerCounter = iExpt
          cParam2.add( cParam )
          oExpress = cParam2
        else:
          oExpress = cParam
      elif IsNumber( cParam ):
        # print( "IsNumber" )
        oExpress = None
        oUnit    = SymNumber( 1, GetNumber( cParam ), 1, 1, iExpt, 1 )
      else:
        cChar = CharNext()
        # print( "Current char: {}, pos: {} ".format( CharCurrent(), iPosCur ))
        if ( cChar == '(' and len( cParam ) > 0 and cParam[ :1].isalpha() ):
        # if ( CharCurrent() == "(" ):
          # print( "Found function, char: {}, iPos: {}".format( cChar, iPosCur ))
          # formule
          oExt     = _symFormulaParser( cFormula, iPosCur, ',)' )
          # print ('oExt: {}'.format( str( oExt )))
          oExpress = SymFunction( cParam, 1, iExpt, 1 )
          oExpress.add( oExt )
          while CharCurrent() == ',':
            oExt     = _symFormulaParser( cFormula, iPosCur, ',)' )
            oExpress.add( oExt )
        else :
          # print ( "Found cChar: {}".format( cChar ))
          if cChar != None:
            CharBack() # read 1 too many

          # print( "Create SymVariable: {}".format( cParam ))
          oExpress = None
          if cParam == '-':
            oUnit = SymNumber( -1, 1, 1, 1, iExpt, 1 )
          else:
            oUnit = SymVariable( cParam, 1, iExpt, 1 )


      cOpt = GetOperator() # get an operator
      if cOpt == '^':
        lonlyOneRoot = 0

        cChar = CharNext()
        if cChar == '^':
          lonlyOneRoot = 1
        else:
          if cChar != None:
            CharBack() # read 1 too many

        # Get an exponent for the last parameter
        cParam2 = GetParam()
        iExpt2  = None
        if IsSymExpress( cParam2 ):
          iExpt = None
          # print( "SymExpress als parameter gevonden" )
          # make it simple
          # print( "cParam2 (1) : {}".format ( str( cParam2 )))
          # SymExpressTree( cParam2 )
          cParam2.optimizeNormal()
          # print( "cParam2 (2) : {}".format ( str( cParam2 )))
          # SymExpressTree( cParam2 )

          # if ( not cParam2.IsPowerOne() ):
          if not cParam2.power == 1:
            raise NameError( f'Incorrect power {cParam2} on position {GetCurPos()} power on power is not supported')
          # SymExpressTree( cParam2 )
          # need the factor, so no name and no factor on the expression, the factor is placed in the symunit
          if cParam2.numElements() == 1:
            cParam2 = cParam2.elements[ 0 ]
            # print( "cParam2 (3): {}".format ( str( cParam2 )))

            # if ( type( cParam2 ) is SymExpress and cParam2.numElements() == 1 ):
            if isinstance( cParam2 , SymNumber ):
              if cParam2.powerSign == -1:
                iExpt2  = cParam2.factCounter * cParam2.factSign
                iExpt   = cParam2.factDenominator
              else:
                iExpt   = cParam2.factCounter * cParam2.factSign
                iExpt2  = cParam2.factDenominator
          if iExpt == None:
            raise NameError( f'Incorrect power {cParam2} on position {GetCurPos()} it must be an integer' )
          # print ( "iExpt: {}, iExpt2: {}".format( iExpt, iExpt2 ))
        elif IsInteger( cParam2 ) == False:
          raise NameError( f'Incorrect power {cParam2} on position {GetCurPos()} it must be an integer' )

        if iExpt2 == None:
          iExpt = GetNumber( cParam2 )
          iExpt2 = 1

        if oExpress != None:
          oExpress.powerCounter     *= iExpt
          oExpress.powerDenominator *= iExpt2
          oExpress.onlyOneRoot       = lonlyOneRoot
        else:
          # unit with alone a number cannot have a power, only names and imaginary numbers
          # if ( oUnit.name == ''  ):
          #   oExpress = SymExpress( '*' )
          #   oExpress.add( oUnit )
          #   oExpress.powerCounter     *= iExpt
          #   oExpress.powerDenominator *= iExpt2
          #   oUnit = None
          # else:
          oUnit.powerCounter     *= iExpt
          oUnit.powerDenominator *= iExpt2
          oUnit.onlyOneRoot       = lonlyOneRoot

        cOpt  = GetOperator() # get an operator

      iExpt = 1
      if cOpt == '/':
        # dividing is exponent -1
        iExpt = -1

      if cOpt == None:
        # end of formule
        if oExpress != None:
          oMul.add( oExpress )
        else:
          oMul.add( oUnit )
        oPlus.add( oMul )
        break

      if cOpt == '^':
        raise NameError( f'Incorrect power {cOpt} on position {GetCurPos()}' )

      if cOpt in [ '+', '-' ]:
        # put current list in plus list
        if oExpress != None:
          oMul.add( oExpress )
        else:
          oMul.add( oUnit )

        oPlus.add( oMul )
        oMul = SymExpress( '*' )
        if cOpt == '-':
          oMul.add( SymNumber( -1, 1, 1, 1, 1, 1))
      else:
        if oExpress != None:
          oMul.add( oExpress )
        else:
          oMul.add( oUnit )

      cParam = GetParam()
      if cParam == None:
        if cOpt == '**':
          oPlus.add( oMul )
          break
        # else:
        raise NameError( 'Incorrect end of formula' )
      # else:
      #  pass

    # end of while( true )
    return oPlus

  iPosCur = 0    # Current position in the formula
  return _symFormulaParser ( cFormula )


# print( "Symexpress3 name: " + _name__ )

# .........
# Last line
# .........
