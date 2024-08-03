#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Write out roots in there lowest form for Sym Express 3

    Copyright (C) 2024 Gien van den Enden - swvandenenden@gmail.com

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



"""

from symexpress3          import symexpress3
from symexpress3.optimize import optimizeBase
from symexpress3          import primefactor  as primefac

class OptimizeOnlyOneRoot( optimizeBase.OptimizeBase ):
  """
  Write out roots in there lowest form
  \n 27^^(1/2) = ((3^2)*3)^^(1/2) = 3 * 3^^(1/2)
  """
  def __init__( self ):
    super().__init__()
    self._name         = "onlyOneRoot"
    self._symtype      = "all"
    self._desc         = "Write out roots in there lowest form"


  # 27^^(1/2) = ((3^2)*3)^^(1/2) = 3 * 3^^(1/2)
  def _numberOptimze( self, symExpr ):
    result = False

    # 27^^(1/2) = ((3^2)*3)^^(1/2) = 3 * 3^^(1/2)

    # print( "_writeOutOnlyOneRoot start" )

    # simplify the factCounter
    # 27^^(1/2) = ((3^2)*3)^^(1/2) = 3 * 3^^(1/2)
    # for iCnt in range( 0, len( symExpr.elements )):
    for iCnt, elem in enumerate( symExpr.elements ) :
      # elem = symExpr.elements[ iCnt ]

      if not isinstance( elem, symexpress3.SymNumber ):
        continue
      # print( "elem.onlyOneRoot: {} {}".format( elem.onlyOneRoot, elem ) )
      if elem.onlyOneRoot != 1:
        continue
      if elem.factSign != 1 :
        continue
      if elem.powerDenominator == 1 :
        continue
      if elem.factCounter == 1:
        if ( elem.powerSign == 1 and elem.powerCounter == 1 and elem.factDenominator == 1 ):
          elem.powerDenominator = 1
        continue

      # print( "OnlyOneRout: " + str( elem ))
      # symFact = SymExpress( '*', elem.powerSign, 1, 1, elem.onlyOneRoot )
      # symDeno = SymExpress( '*', elem.powerSign, elem.powerCounter, elem.powerDenominator, elem.onlyOneRoot)
      symFact = symexpress3.SymExpress( '*', 1, 1, 1, elem.onlyOneRoot )
      symDeno = symexpress3.SymExpress( '*', 1, elem.powerCounter, elem.powerDenominator, elem.onlyOneRoot)

      lFoundOne = False
      dPrimeSet = primefac.factorint( elem.factCounter )
      for iPrime, iCount in dPrimeSet.items():
        # print( "iPrime: {}, iCount: {}, elem.powerDenominator: {}".format( iPrime, iCount,elem.powerDenominator ))
        if iCount >= elem.powerDenominator :
          iFact = iCount // elem.powerDenominator
          iRad  = iCount % elem.powerDenominator
          lFoundOne = True

          elem1 = symexpress3.SymNumber( 1, int( iPrime ), 1, 1, iFact, 1, 1 )
          symFact.add ( elem1 )

          if iRad > 0 :
            elem1 = symexpress3.SymNumber( 1, int( iPrime ), 1, 1, iRad, 1, 1 )
            symDeno.add ( elem1 )
        else:
          elem1 = symexpress3.SymNumber( 1, int( iPrime ), 1, 1, iCount, 1, 1 )
          symDeno.add ( elem1 )

      if lFoundOne == True:
        result = True
        # print( "symExpr   : {}".format( str( symExpr)))
        # print( "Fact   : {}".format( str( symFact )))
        # print( "symDeno: {}".format( str( symDeno )))

        if elem.factDenominator > 1 :
          elem1 = symexpress3.SymNumber( 1, 1, elem.factDenominator, 1, 1, 1 )
          symDeno.add( elem1 )

        symReplace = symexpress3.SymExpress( '*', elem.powerSign, 1, 1, elem.onlyOneRoot )
        symReplace.add( symFact )
        if symDeno.numElements() > 0:
          symReplace.add( symDeno )

        # print( "fact old elem: {}".format( str( elem )))
        # print( "fact new elem: {}".format( str( symReplace)))

        symExpr.elements[ iCnt ] = symReplace

    # simplify the factDenominator
    # (1/27)^^(1/2) = (((1/3)^2)*3)^^(1/2) = 1/3 * 3^^(1/2)
    # for iCnt in range( 0, len( symExpr.elements )):
    for iCnt, elem in enumerate( symExpr.elements ):
      # elem = symExpr.elements[ iCnt ]

      # print( "check: {}".format( str( elem )))

      if not isinstance( elem, symexpress3.SymNumber ):
        continue
      if elem.onlyOneRoot != 1 :
        continue
      if elem.factSign != 1 :
        continue
      if elem.powerDenominator == 1 :
        continue
      if elem.factDenominator == 1 :
        continue

      # print( "check 2: deno:{}, elem: {}".format( elem.factDenominator, str( elem )))

      # symFact = SymExpress( '*', elem.powerSign, 1, 1, elem.onlyOneRoot )
      # symDeno = SymExpress( '*', elem.powerSign, elem.powerCounter, elem.powerDenominator, elem.onlyOneRoot)
      symFact = symexpress3.SymExpress( '*', 1, 1, 1, elem.onlyOneRoot )
      symDeno = symexpress3.SymExpress( '*', 1, elem.powerCounter, elem.powerDenominator, elem.onlyOneRoot)

      lFoundOne = False
      dPrimeSet = primefac.factorint( elem.factDenominator )

      # print ( "dPrimeSet factDenominator: {}".format( dPrimeSet ))
      for iPrime, iCount in dPrimeSet.items():
        # print( "iPrime: {}, iCount: {}, elem.powerDenominator: {}".format( iPrime, iCount,elem.powerDenominator ))
        if iCount >= elem.powerDenominator :
          iDenom    = iCount // elem.powerDenominator
          iRad      = iCount % elem.powerDenominator
          lFoundOne = True

          elem1 = symexpress3.SymNumber( 1, 1, int( iPrime ), 1, iDenom, 1, 1 )
          symFact.add ( elem1 )

          if iRad > 0 :
            elem1 = symexpress3.SymNumber( 1, 1, int( iPrime ), 1, iRad, 1, 1 )
            symDeno.add ( elem1 )
        else:
          elem1 = symexpress3.SymNumber( 1, 1, int( iPrime ), 1, iCount, 1, 1 )
          symDeno.add ( elem1 )

      if lFoundOne == True :
        result = True
        # print( "symExpr   : {}".format( str( symExpr)))
        # print( "Fact   : {}".format( str( symFact )))
        # print( "symDeno: {}".format( str( symDeno )))

        if elem.factCounter > 1 :
          elem1 = symexpress3.SymNumber( 1, elem.factCounter, 1, 1, 1, 1 )
          symDeno.add( elem1 )

        # symReplace = SymExpress( '*' )
        symReplace = symexpress3.SymExpress( '*', elem.powerSign, 1, 1, elem.onlyOneRoot )

        symReplace.add( symFact )
        if symDeno.numElements() > 0:
          symReplace.add( symDeno )

        # print( "deno old elem: {}".format( str( elem )))
        # print( "deno new elem: {}".format( str( symReplace)))
        symExpr.elements[ iCnt ] = symReplace

    # eliminate the factDenominator
    # (1/3)^(1/2) = 3 * 3^(1/2)

    # cBefore = str( symExpr )
    # dBefore = symExpr.getValue()
    # for iCnt in range( 0, len( symExpr.elements )):
    for iCnt, elem in enumerate( symExpr.elements ):
      # elem = symExpr.elements[ iCnt ]

      # print( "check: {}".format( str( elem )))

      if not isinstance( elem, symexpress3.SymNumber ):
        continue
      if elem.onlyOneRoot != 1 :
        continue
      if elem.factSign != 1 :
        continue
      if elem.powerDenominator == 1 :
        continue
      if elem.factDenominator == 1 :
        continue

      elemnew = elem.copy()
      elemnew.factDenominator = 1
      elemnew.powerSign       = 1
      elemfact = symexpress3.SymNumber( 1, 1, elem.factDenominator, 1, 1, 1 )

      iFactCounter = elem.factCounter
      # print( "iFactCounter: {}".format( iFactCounter ))
      for iFact in range( 1, elem.powerDenominator ):
        iFactCounter *= elem.factDenominator
        # print( "iFactCounter: {} = {}".format( iFact, iFactCounter ))
      elemnew.factCounter = iFactCounter

      symReplace = symexpress3.SymExpress( '*', elem.powerSign, 1, 1, elem.onlyOneRoot )
      symReplace.add( elemfact )
      symReplace.add( elemnew )

      #dValueElem = elem.getValue()
      #dValueRep  = symReplace.getValue()
      #if ( dValueElem != dValueRep ):
      #  print( "quotation old elem: {} = {}".format( dValueElem, str( elem )))
      #  print( "quotation new elem: {} = {}".format( dValueRep , str( symReplace)))

      symExpr.elements[ iCnt ] = symReplace
      result = True

    #cAfter = str( symExpr )
    #dAfter = symExpr.getValue()
    #if ( True or dAfter != dBefore ):
    #   print( "quotation before: {} = {}".format( dBefore, cBefore))
    #   print( "quotation after : {} = {}".format( dAfter , cAfter ))
    return result


  def _expressOptimze( self, symExpr ):
    # optimze expression (4   + 4 a  )^^(1/2) = 2  (1 + a)^^(1/2)
    #                    (1/4 + 1/4 a)^^(1/2) = 1/2(1 + a)^^(1/2)

    # prefered:  len(x) == 0


    def _cleanup( arrElem ):
      powerSearch = symExpr.powerDenominator
      firstElem   = True
      allEmpty    = False
      tebeRemoved = []
      for dPrimeSet in arrElem:
        # print( "Check: " + str( dPrimeSet ))
        if firstElem == True:
          firstElem = False
          if len( dPrimeSet ) == 0:  # pylint: disable=simplifiable-if-statement
            allEmpty = True
          else:
            allEmpty = False
        else:
          if len( dPrimeSet ) == 0:
            if allEmpty == False:
              return False
          else:
            if allEmpty == True:
              return False

        if allEmpty == False:
          # delete all power lower then powerSearch
          removeNumber = []
          for iPrime, iCount in dPrimeSet.items():
            if iCount < powerSearch:
              # del dPrimeSet[ iPrime ]
              removeNumber.append( iPrime )
            else:
              if iCount % powerSearch != 0:
                dPrimeSet[ iPrime ] = (iCount // powerSearch) * powerSearch
          for iRem in removeNumber:
            del dPrimeSet[ iRem ]
          if len( dPrimeSet ) == 0:
            return False
        else:
          # print( "Remove" )
          # arrElem.remove( dPrimeSet )
          tebeRemoved.append( dPrimeSet )

      for delElem in tebeRemoved:
        arrElem.remove( delElem )

      return True

    def _lowestPower( elemArr ):

      if len( elemArr ) == 0:
        return True

      firstElem = True
      firstSet  = {}
      for dPrimeSet in elemArr:
        if firstElem == True:
          firstSet = dPrimeSet
        else:
          # first walk firstElem
          for iPrime, iCount in firstSet.items():
            if iPrime in dPrimeSet:
              if iCount > dPrimeSet[ iPrime ]:
                firstSet[ iPrime ] = dPrimeSet[ iPrime ]
              else:
                dPrimeSet[ iPrime ] = iCount
            else:
              del firstSet[ iPrime ]
          # walk secon elem for missing
          for iPrime, iCount in dPrimeSet.items():
            if not iPrime in firstSet:
              return False
      return True



    result = False

    if not isinstance( symExpr, symexpress3.SymExpress):
      return result

    if symExpr.powerDenominator == 1:
      # print( "symexpress: " + str( symExpr ) )
      # symexpress3.SymExpressTree( symExpr )
      return result

    if symExpr.onlyOneRoot != 1:
      return result

    if symExpr.powerSign == -1:
      return result

    # print(" Start _expressOptimze" )

    # minNumber = 2 ** symExpr.powerDenominator  # min number 2^denominator, 2^2 = 4, 2^3 = 6
    arrFact  = []
    arrDenom = []
    found    = False
    if symExpr.symType == '*' :
      # search for first SymNumber with power of 1
      # get factCounter
      # get factDenominator
      found = False
      for elem in symExpr.elements :
        if not isinstance( elem, symexpress3.SymNumber ):
          continue
        # no powers
        if elem.power != 1:
          continue
        dPrimeSet = primefac.factorint( elem.factCounter )
        arrFact.append( dPrimeSet )

        dPrimeSet = primefac.factorint( elem.factDenominator )
        arrDenom.append( dPrimeSet )

        found = True
        # only 1 number supported
        break

      if found == False:
        # print( "Number invalid: " + str( symExpr ))
        return result

    else:
      # search in each element for a SymNumber with power of 1
      # get factCounter
      # get factDenominator
      found = False
      for elemplus in symExpr.elements:
        if isinstance( elemplus, symexpress3.SymNumber ):
          if elemplus.power != 1:
            return result

          dPrimeSet = primefac.factorint( elemplus.factCounter )
          arrFact.append( dPrimeSet )

          dPrimeSet = primefac.factorint( elemplus.factDenominator )
          arrDenom.append( dPrimeSet )

        elif isinstance( elemplus, symexpress3.SymExpress ):
          if elemplus.power != 1:
            return result

          if elemplus.symType == '+' and elemplus.numElements() != 1:
            return result

          found = False
          for elem in elemplus.elements:
            # print( "Check : " + str( elem ) + str( type( elem )))
            if not isinstance( elem, symexpress3.SymNumber ):
              continue
            # no powers
            if elem.power != 1:
              continue
            dPrimeSet = primefac.factorint( elem.factCounter )
            arrFact.append( dPrimeSet )

            dPrimeSet = primefac.factorint( elem.factDenominator )
            arrDenom.append( dPrimeSet )

            found = True
            # only 1 number supported
            break
          if found == False:
            return result

        else:
          return result # only numbers and symexpress supported

    # print( "Found: " + str( found ))

    if found == False:
      return result


    # print( "arrFact : " + str( arrFact  ))
    # print( "arrDemon: " + str( arrDenom ))

    # check if the powers are greater of equal expression power
    if _cleanup( arrFact  ) != True:
      return False

    if _cleanup( arrDenom ) != True:
      return False

    if len( arrFact ) == 0 and len( arrDenom ) == 0:
      return False

    # print( "arrFact 2: " + str( arrFact  ))
    # print( "arrDemon2: " + str( arrDenom ))

    # check all the bases and powers must be equal
    if _lowestPower( arrFact ) != True:
      return False

    if _lowestPower( arrDenom ) != True:
      return False

    # print( "arrFact 3: " + str( arrFact  ))
    # print( "arrDemon3: " + str( arrDenom ))

    if len( arrFact ) == 0 and len( arrDenom ) == 0:
      return False

    # make number (common factor)
    symNum = symexpress3.SymExpress( '*' )
    if len( arrFact ) > 0:
      # all powers are now the same
      for iPrime, iCount in arrFact[ 0 ].items():
        newNum = symexpress3.SymNumber()
        newNum.factCounter   = iPrime
        newNum.powerCounter  = iCount
        symNum.add( newNum )

    if len( arrDenom ) > 0:
      # all powers are now the same
      for iPrime, iCount in arrDenom[ 0 ].items():
        newNum = symexpress3.SymNumber()
        newNum.factDenominator = iPrime
        newNum.powerCounter    = iCount
        symNum.add( newNum )

    # print( "Common factor: " + str( symNum ))

    # copy symExpr
    copySymExpr = symExpr.copy()
    # create new SymExpress = *
    newSymExpr = symexpress3.SymExpress( '*' )
    # copy the power from symExpr to new
    newSymExpr.powerCounter     = symExpr.powerCounter
    newSymExpr.powerDenominator = symExpr.powerDenominator
    newSymExpr.powerSign        = symExpr.powerSign
    newSymExpr.onlyOneRoot      = symExpr.onlyOneRoot
    # set power of copy symExpress to 1
    copySymExpr.powerCounter     = 1
    copySymExpr.powerDenominator = 1
    copySymExpr.powerSign        = 1
    # add copy to new
    newSymExpr.add( copySymExpr )
    # add 1/fact to new
    # add 1/denom to new
    symNum.powerSign = -1
    newSymExpr.add( symNum )
    symNum.powerSign = 1

    # set org symexpres powerFactor & powerDenomotor to 1 (not sign)
    symExpr.powerCounter     = 1
    symExpr.powerDenominator = 1
    # make org empty
    symExpr.elements = []
    # set org to *
    symExpr.symType = '*'
    # add radical of fact
    # add radical of denom
    symNum.powerDenominator = newSymExpr.powerDenominator

    symNum1 = symexpress3.SymExpress( '*' )
    symNum1.add( symNum )

    # want whole number
    # otherwise optimze 'multiply' will put the radicals together (circle)
    symNum1.optimize()
    symNum1.optimize( "multiply" )
    symNum1.optimize()
    symNum1.optimize( "power" )
    symNum1.optimize()
    self._numberOptimze( symNum1 )
    symNum1.optimize()
    self._numberOptimze( symNum1 )
    symNum1.optimize()

    # print( " " )
    # symexpress3.SymExpressTree( symNum1 )

    # print( " " )
    # print( "symNum optimzed: " + str( symNum1 ))
    # print( " " )


    symExpr.add( symNum1 )
    # add new to org
    symExpr.add( newSymExpr )

    # print( "New symexpress: " + str( symExpr ))

    result = True

    return result

  def optimize( self, symExpr, action ):
    result = False
    if self.checkExpression( symExpr, action ) != True:
      # print( "Afgekeurd: " + symExpr.symType )
      return result

    result |= self._numberOptimze( symExpr )
    if result == True:
      return result

    # not wanted to get all the factors out of the radical
    result |= self._expressOptimze( symExpr )
    # if result == True:
    #   return result

    return result


#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """

  def _Check( testClass, symOrg, symTest, wanted ):
    if display == True :
      print( f"naam      : {testClass.name}" )
      print( f"orginal   : {str( symOrg  )}" )
      print( f"optimized : {str( symTest )}" )

    if str( symTest ).strip() != wanted:
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symOrg )}' )

  symTest = symexpress3.SymFormulaParser( '27^^(1/2)' )
  symTest.optimize()
  # symTest = symTest.elements[ 0 ]
  # symexpress3.SymExpressTree( symTest )
  symOrg = symTest.copy()

  testClass = OptimizeOnlyOneRoot()
  testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symOrg, symTest, "3 * (3)^^(1/2)" )


  symTest = symexpress3.SymFormulaParser( '(1/27)^^(1/2)' )
  symTest.optimize()
  symOrg = symTest.copy()
  testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symOrg, symTest, "(1/3) * ((1/3))^^(1/2)" )


  symTest = symexpress3.SymFormulaParser( '(1/3)^^(1/2)' )
  symTest.optimize()
  symTest.optimize( "multiply" )
  symTest.optimize()
  symOrg = symTest.copy()
  testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symOrg, symTest, "(1/3) * 3^^(1/2)" )


  symTest = symexpress3.SymFormulaParser( '(4 + 8 a)^^(1/2)' )
  symTest.optimize()
  symTest.optimize( "multiply" )
  symTest.optimize()
  symTest = symTest.elements [ 0 ]
  symOrg = symTest.copy()
  testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symOrg, symTest, "2 * ((4 + 8 * a) * (2^^2)^^-1)^^(1/2)" )

  symTest = symexpress3.SymFormulaParser( '(1/4 + 1/8 a)^^(1/2)' )
  symTest.optimize()
  symTest.optimize( "multiply" )
  symTest.optimize()
  symTest = symTest.elements [ 0 ]
  symOrg = symTest.copy()
  testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symOrg, symTest, "(1/2) * (((1/4) + (1/8) * a) * ((1/2)^^2)^^-1)^^(1/2)" )


  symTest = symexpress3.SymFormulaParser( '(4/27 + 8/9 a)^^(1/2)' )
  symTest.optimize()
  symTest.optimize( "multiply" )
  symTest.optimize()
  symTest = symTest.elements [ 0 ]
  symOrg = symTest.copy()
  testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symOrg, symTest, "2 * (1/3) * (((4/27) + (8/9) * a) * (2^^2 * (1/3)^^2)^^-1)^^(1/2)" )


if __name__ == '__main__':
  Test( True )
