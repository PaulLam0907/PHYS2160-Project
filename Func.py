"""
Func.py

A class for defining a mathematics function that can be called similar to mathematics notation
This allows user to define and evaluate the mathematics function at given time interval in a more convenient way

Written by S. P. Lam
"""

import numpy as np
from numpy import sin, cos, tan, arcsin, arccos, arctan, sqrt, array
# from numpy import *  # note that this may waste computer resources


class Func:
    """
    A class for defining a function that can be called similar to mathematics notation
    
    Usage :
    f = Func(
          "F0*cos(theta*t)/sqrt(m)",  # function f = (F0)*(cos(theta * t))/sqrt(m)
          F0 = 1,  # constants
          theta = 1,
          m = 1
    )
    f0 = f(t = 0)  # evaluate the function at t = 0
    print(f0)  # print the numerical result
    """
    
    def __init__(self, func, **kwargs):
        self.func = func
        self.constants = kwargs  # dict
        
    
    def __call__(self, t = (0), **kwargs):
        
        # create variables for constants
        for const in self.constants.keys():
            exec(const + f" = {self.constants[const]}")
        
        # create user defined variables
        for i in kwargs:
            if type(kwargs[i]) == np.ndarray:
                exec(f"{i} = {list(kwargs[i])}")
                exec(f"{i} = array({i})")
            else:
                exec(f"{i} = {kwargs[i]}")
                
        
        # evaluate the function
        result = eval(self.func)
        
        # return result
        return result



"""
import numpy as np
f = Func("F0*cos(theta*t)/sqrt(m)",
         F0 = 1,
         theta = 1,
         m = 1
         )
f0 = f(np.arange(0, 10, 1e-3))
print(f0)
"""
