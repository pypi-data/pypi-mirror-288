
# ------------------------------------------------------------------------------------#
#  Mesh Adaptive Direct Search - ORTHO-MADS (MADS)                                    #
#                                                                                     #
#  Author: Ahmed H. Bayoumy                                                           #
#  email: ahmed.bayoumy@mail.mcgill.ca                                                #
#                                                                                     #
#  This program is free software: you can redistribute it and/or modify it under the  #
#  terms of the GNU Lesser General Public License as published by the Free Software   #
#  Foundation, either version 3 of the License, or (at your option) any later         #
#  version.                                                                           #
#                                                                                     #
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY    #
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A    #
#  PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.   #
#                                                                                     #
#  You should have received a copy of the GNU Lesser General Public License along     #
#  with this program. If not, see <http://www.gnu.org/licenses/>.                     #
#                                                                                     #
#  You can find information on OMADS at                                               #
#  https://github.com/Ahmed-Bayoumy/OMADS                                             #
#  Copyright (C) 2022  Ahmed H. Bayoumy                                               #
# ------------------------------------------------------------------------------------#

from enum import Enum, auto
from dataclasses import dataclass, field
import warnings
import numpy as np
import platform
import pandas as pd

np.set_printoptions(legacy='1.21')

@dataclass
class DType:
  """A numpy data type delegator for decimal precision control

    :param prec: Default precision option can be set to "high", "medium" or "low" precision resolution, defaults to "medium"
    :type prec: str, optional
    :param dtype: Numpy double data type precision, defaults to np.float64
    :type dtype: np.dtype, optional
    :param itype: Numpy integer data type precision, defaults to np.int
    :type itype: np.dtype, optional
    :param zero: Zero value resolution, defaults to np.finfo(np.float64).resolution
    :type zero: float, optional
  """
  _prec: str = "medium"
  _dtype: np.dtype = np.float64
  _itype: np.dtype = np.int_
  _zero: float = (np.finfo(np.float64)).resolution
  _warned: bool = False


  @property
  def zero(self)->float:
    """This is the mantissa value of the machine zero

    :return: machine precision zero resolution
    :rtype: float
    """
    return self._zero

  @property
  def precision(self):
    """Set/get precision resolution level

    :return: float precision value
    :rtype: numpy float
    :note: MS Windows does not support precision with the {1e-18} high resolution of the python
            numerical library (numpy) so high precision will be
            changed to medium precision which supports {1e-15} resolution
            check: https://numpy.org/doc/stable/user/basics.types.html 
    """
    return self._prec

  @precision.setter
  def precision(self, val: str):
    self._prec = val
    self._prec = val
    isWin = platform.platform().split('-')[0] == 'Windows'
    if val == "high":
      if (not hasattr(np, 'float128')):
        'Warning: MS Windows does not support precision with the {1e-18} high resolution of the python numerical library (numpy) so high precision will be changed to medium precision which supports {1e-15} resolution check: https://numpy.org/doc/stable/user/basics.types.html '
        self.dtype = np.float64
        self._zero = np.finfo(np.float64).resolution
        self.itype = np.int_
        if not self._warned:
          warnings.warn("MS Windows does not support precision with the {1e-18} high resolution of the python numerical library (numpy) so high precision will be changed to medium precision which supports {1e-15} resolution check: https://numpy.org/doc/stable/user/basics.types.html")
        self._warned = True
      else:
        self.dtype = np.float128
        self._zero = np.finfo(np.float128).resolution
        self.itype = np.int_
    elif val == "medium":
      self.dtype = np.float64
      self._zero = np.finfo(np.float64).resolution
      self.itype = np.intc
    elif val == "low":
      self.dtype = np.float32
      self._zero = np.finfo(np.float32).resolution
      self.itype = np.short
    else:
      raise Exception("JASON parameters file; unrecognized textual"
              " input for the defined precision type. "
              "Please enter one of these textual values (high, medium, low)")

  @property
  def dtype(self):
    """Set/get the double formate type

    :return: float precision value
    :rtype: numpy float 
    """
    return self._dtype

  @dtype.setter
  def dtype(self, other: np.dtype):
    self._dtype = other

  @property
  def itype(self):
    """Set/Get for the integer formate type

    :return: integer precision value
    :rtype: numpy float 
    """
    return self._itype

  @itype.setter
  def itype(self, other: np.dtype):
    self._itype = other

class VAR_TYPE(Enum):
  REAL = auto()
  INTEGER = auto()
  DISCRETE = auto()
  BINARY = auto()
  CATEGORICAL = auto()
  ORDINAL = auto()

class BARRIER_TYPES(Enum):
  EB = auto()
  PB = auto()
  PEB = auto()
  RB = auto()

class SUCCESS_TYPES(Enum):
  US = auto()
  PS = auto()
  FS = auto()
  
class MPP(Enum):
  LAMBDA = 0.
  RHO = 0.00005

class DESIGN_STATUS(Enum):
  FEASIBLE = auto()
  INFEASIBLE = auto()
  ERROR = auto()
  UNEVALUATED = auto()

class MSG_TYPE(Enum):
  DEBUG = auto()
  WARNING = auto()
  ERROR = auto()
  INFO = auto()
  CRITICAL = auto()

class SAMPLING_METHOD(Enum):
  FULLFACTORIAL: int = auto()
  LH: int = auto()
  RS: int = auto()
  HALTON: int = auto()
  ACTIVE: int = auto()

class SEARCH_TYPE(Enum):
  SAMPLING: int = auto()
  SURROGATE: int = auto()
  VNS: int = auto()
  BAYESIAN: int = auto()
  NM: int = auto()
  PSO: int = auto()

class DIST_TYPE(Enum):
  GAUSS: int = auto()
  GAMMA: int = auto()
  EXPONENTIAL: int = auto()
  BIONOMIAL: int = auto()
  POISSON: int = auto()

class STOP_TYPE(Enum):
  NO_STOP: int = auto()
  ERROR: int = auto()
  UNKNOWN_STOP_REASON: int = auto()
  CTRL_C: int = auto()
  USER_STOPPED: int = auto()
  MESH_PREC_REACHED: int = auto()
  X0_FAIL: int = auto()
  P1_FAIL: int = auto()
  DELTA_M_MIN_REACHED: int = auto()
  DELTA_P_MIN_REACHED: int = auto()
  MAX_TIME_REACHED: int = auto()
  MAX_BB_EVAL_REACHED: int = auto()
  MAX_SGTE_EVAL_REACHED: int = auto()
  F_TARGET_REACHED: int = auto()
  MAX_CACHE_MEMORY_REACHED: int = auto()
  GL_LIMITS_REACHED: int = auto()

class MESH_TYPE(Enum):
  ORTHO = auto()
  GMESH = auto()
  XMESH = auto()
  SMESH = auto()

class EVAL_TYPE(Enum):
  BB = auto()
  CALLABLE = auto()

class COMPARE_TYPE:
  EQUAL = auto() #///< Both points are feasible or infeasible, and their
                  # ///< objective values and h (where h is the squared sum
                  # ///< of violations of all constraints) are equal to
                  # ///< approximation tolerance rounding.
  INDIFFERENT = auto() # ///< Both point are non dominated relatively to each other.
  DOMINATED = auto() # ///< The first point is dominated by the other.
  DOMINATING = auto() # ///< The first point dominates the other.
  UNDEFINED = auto() # ///< May be used when comparing feasible and infeasible solutions for example.

HARD_MIN_MESH_INDEX: int = -300
# gmesh index constants
GL_LIMITS: int    = -50;         #< Limits for the gmesh index values
UNDEFINED_GL: int = GL_LIMITS-1;  #< Undefined value for the gmesh index

M_INF_INT = -2147483647 - 1
P_INF_INT = 2147483647
