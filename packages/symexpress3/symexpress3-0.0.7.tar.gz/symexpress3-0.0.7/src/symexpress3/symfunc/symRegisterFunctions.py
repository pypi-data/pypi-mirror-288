#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Registration of function classes for symexpress3

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


    Example documentenion:
            pdoc3 --html symFuncCeilFloor.py

"""

from symexpress3 import symtables

from symexpress3.symfunc import symFuncCeilFloor
from symexpress3.symfunc import symFuncExp
from symexpress3.symfunc import symFuncAbs
from symexpress3.symfunc import symFuncFactorial
from symexpress3.symfunc import symFuncBinomial
from symexpress3.symfunc import symFuncAtan2
from symexpress3.symfunc import symFuncAtan
from symexpress3.symfunc import symFuncSin
from symexpress3.symfunc import symFuncCos
from symexpress3.symfunc import symFuncTan
from symexpress3.symfunc import symFuncSum
#
# automatic called from symepxress3 too fill functionTable[]
#
def SymRegisterFunctions():
  """
  Register all the function classes
  """

  # symexpress3.symexpress3.functionTable = []

  # print( "fill funtiontable ")

  # symexpress3.symexpress3.functionTable.append( symFuncCeilFloor.SymFuncCeil()      )
  # symexpress3.symexpress3.functionTable.append( symFuncCeilFloor.SymFuncFloor()     )
  # symexpress3.symexpress3.functionTable.append( symFuncExp.SymFuncExp()             )
  # symexpress3.symexpress3.functionTable.append( symFuncAbs.SymFuncAbs()             )
  # symexpress3.symexpress3.functionTable.append( symFuncFactorial.SymFuncFactorial() )
  # symexpress3.symexpress3.functionTable.append( symFuncBinomial.SymFuncBinomial()   )
  # symexpress3.symexpress3.functionTable.append( symFuncAtan2.SymFuncAtan2()         )
  # symexpress3.symexpress3.functionTable.append( symFuncAtan.SymFuncAtan()           )
  # symexpress3.symexpress3.functionTable.append( symFuncSin.SymFuncSin()             )
  # symexpress3.symexpress3.functionTable.append( symFuncCos.SymFuncCos()             )
  # symexpress3.symexpress3.functionTable.append( symFuncTan.SymFuncTan()             )
  # symexpress3.symexpress3.functionTable.append( symFuncSum.SymFuncSum()             )

  # print( "len funtiontable: {}".format( len( symexpress3.symexpress3.functionTable )  ) )

  symtables.RegisterTableEntry( 'function', symFuncCeilFloor.SymFuncCeil()      )
  symtables.RegisterTableEntry( 'function', symFuncCeilFloor.SymFuncFloor()     )
  symtables.RegisterTableEntry( 'function', symFuncExp.SymFuncExp()             )
  symtables.RegisterTableEntry( 'function', symFuncAbs.SymFuncAbs()             )
  symtables.RegisterTableEntry( 'function', symFuncFactorial.SymFuncFactorial() )
  symtables.RegisterTableEntry( 'function', symFuncBinomial.SymFuncBinomial()   )
  symtables.RegisterTableEntry( 'function', symFuncAtan2.SymFuncAtan2()         )
  symtables.RegisterTableEntry( 'function', symFuncAtan.SymFuncAtan()           )
  symtables.RegisterTableEntry( 'function', symFuncSin.SymFuncSin()             )
  symtables.RegisterTableEntry( 'function', symFuncCos.SymFuncCos()             )
  symtables.RegisterTableEntry( 'function', symFuncTan.SymFuncTan()             )
  symtables.RegisterTableEntry( 'function', symFuncSum.SymFuncSum()             )


#
# Get all the modules from the functions, used in testsymexpress3.py
#
def SymRegisterGetModuleNames():
  """
  Get all the modules of the functions
  """

  # https://stackoverflow.com/questions/4858100/how-to-list-imported-modules
  # modulenames = set(sys.modules) & set(globals())
  # allmodules  = [sys.modules[name] for name in modulenames]

  # allmodules = set( globals() )
  # print( "globals(): " + str( globals() ))
  # print( "sys modules: " + str( sys.modules ))

  symModules = []
  # for key in allmodules:
  #  print("Name: " + str(key.__name__ ) )
  #  if not key.__name__.startswith( 'symexpress3.symfunc.symFunc' ):
  #     continue
  #  if not hasattr( key, 'Test' ):
  #     continue
  #  # symModules.append( key )

  symModules.append( symFuncCeilFloor )
  symModules.append( symFuncExp       )
  symModules.append( symFuncAbs       )
  symModules.append( symFuncFactorial )
  symModules.append( symFuncBinomial  )
  symModules.append( symFuncAtan2     )
  symModules.append( symFuncAtan      )
  symModules.append( symFuncSin       )
  symModules.append( symFuncCos       )
  symModules.append( symFuncTan       )
  symModules.append( symFuncSum       )


  # allmodules = [key for key in locals().keys()if isinstance(locals()[key], type(sys)) and not key.startswith('__')]
  # allmodules = [m.__name__ for m in sys.modules.values() if m]
  # return allmodules
  return symModules

if __name__ == '__main__':
  SymRegisterFunctions()
  print( "Modules: " + str( ( SymRegisterGetModuleNames() )))
  # print( "globals: " + str( globals() ))
