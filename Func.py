"""
Func.py

A class for defining a mathematics function that can be called similar to mathematics notation
This allows user to define and evaluate the mathematics function at given time interval in a more convenient way

Written by S. P. Lam
"""

import numpy as np
from numpy import sin, cos, tan, arcsin, arccos, arctan, sqrt, array
# from numpy import *  # note that this may waste computer resources


class Environment:
    """
    A class for setting an environment of the interested situation
    Allow "sharing" of the same environment with multiple functions
    This makes the code more reusable & scalable
    by setting an environment of a particular situation with multiple functions etc.
    
    Note that any updates to the constants can be seen by the Func() class associated to respective Environment() class
    ie. Func() class can use the updated value of constant from its parent Environment() class
        if the constants in parent class is being updated
    
    If some constants depend on other constants, simply pass a string instead
    ie. env.setConstants(a = 1, b = "2*a + 1")
    Note that the value of constants is evaluated only when Func() is being called
    
    Usage :
    env = Environment(
            F0 = 1,
            theta = 3.14,
            m = 1
    )  # create environment with known constants
    
    f1 = env.newF("F0*cos(theta*t)/sqrt(m)", "f1")  # new function in the env
    f2 = env.newF("-F0*sin(theta*t)/sqrt(m)", "f2")  # new function in the env
    
    # evaluate the function at t = 0
    print( f1(array([0])) )
    print( f2(array([0])) )
    
    
    env2 = Environment(
            g = 9.81,
            m = 3,
            omega = 2
    )  # new environment
    
    g1 = env2.newF("m*g*sin(omega*t)", "g1")  # new function in the env2
    print(g1.getConstants())  # get constants of env2. should use env2.getConstants()
    print( g1(np.array([0, 1, 2])) )  # evaluate the function at t = 0, 1, 2
    
    
    ##### Copy of constants from existing environment : #####
    env = Environment(
            F0 = 1,
            theta = 3.14,
            m = 1
    )
    
    env2 = Environment(  # new environment
            constants = env.getConstants(),  # same constants and values as env
            m = 3,  # update the value of m to be 3 ( m = 1 in env )
            g = 9.81  # new constant g = 9.81
    )
    print(env2.getConstants())  # get constants of env2
    
    
    ##### Constant that depends on other constants #####
    env3 = Environment(a = 1, b = "2*a")  # Environment with constant a = 1 and b = 2a, pass "2*a" as string
    # note that b = 2a should be defined only after a is defined
    # ie. first define "a" in Environment() , then define b = 2a
    f = env3.newF("a + b", "f")  # define function which return a + b
    print(f())  # 3
    
    env3.setConstants(a = 2)  # set a = 2 => b = 2*a = 4
    print(f())  # 6
    """
    
    def __init__(self, constants = None, name = None, **kwargs):
        self.constants = {}  # dict
        
        if constants:
            self.constants.update(constants)
            
        if kwargs:
            self.constants.update(kwargs)
            
        self.functions = {}  # dict of class Func() instance
        self.name = name  # name of the environment
        
        
    def getConstants(self):
        """
        Get all constants
        
        :return: type dict
        """
        return self.constants
    
    
    def setConstants(self, constants = None, **kwargs):
        """
        Define constants and its value
        If you wish to define constant that depends on other constants,
        pass the expression as string instead (see example below).
        Note that "independent constant" should be defined before related "dependent constant" is defined
        
        Usage :
        env = Environment()  # define environment
        env.setConstant(a = 1, b = 2)  # create new constant a = 1, b = 2
        env.setConstant(a = 3)  # update value of existing constant a to be 3
        env.setConstant(c = "2*a + 3*b")  # create new constant c = 2a + 3b which depends on a and b
        
        const = {
            "a": 4,
            "b": 5,
            "c": "2*a + 3*b"
        }
        env.setConstant(const)  # update / add constants from dict
        
        :param constants: type dict {name of constant: value, ...}
        :param kwargs: allow defining constants in a more natural manner by simply passing name and value as the parameter
        :return: None
        """
        if constants:
            self.constants.update(constants)
            
        self.constants.update(kwargs)
        
    
    def clearConstants(self):
        """
        Clear / empty all constants defined
        
        :return: None
        """
        self.constants.clear()
        
    
    def popConstants(self, *args):
        """
        Remove given constant from the self.constants
        e.g. popConstants("g", "c", "k")
        
        :param args: name of the constants of type str. Should be the key of dict in self.constants
        :return:
        """
        for i in args:
            self.constants.pop(i)
    
    
    def newF(self, func, name = None):
        """
        Create new function associated with this environment
        Only functions Func() created using this method with non-empty name will be added
        to the function list self.functions of Environment() class
        
        :param func: expression of the function of type str
        :param name: name of the function of type str
        :return: instance of class Func()
        """
        
        # check duplication of function
        for key, f in self.functions.items():
            
            if func == f.__str__():
                # duplication of function in same env
                # warn the user
                print(f"[Warning] Duplication of Function in the same Environment. Found at self.functions[{key}]")
                
        # store the Func() instance
        if name:
            self.functions.update({
                name: Func(func, env = self)
            })
        
        # return the Func() class instance
        # should be pointing to the same Func() instance in the self.functions
        # i.e. same id / memory address
        return self.functions[name] if name else Func(func, env = self)
    
    
    def getF(self, name):
        """
        Get stored function by name ( dict key )
        
        :param name: name ( dict key ) of the function stored in self.functions
        :return: instance of class Func()
        """
        # should be pointing to the same Func() instance in the self.functions
        # i.e. same id / memory address
        return self.functions[name]
    
    
    def getAllFunc(self):
        """
        Get all the Func() class instance stored
        Only functions Func() created using this method with non-empty name will be added
        to the function list self.functions of Environment() class
        
        :return: dict of Func() class instance
        """
        return self.functions
    
    
    def printAllFunc(self):
        """
        Print all the Func() class instance stored to console
        Only functions Func() created using this method with non-empty name will be added
        to the function list self.functions of Environment() class
        
        :return: None
        """
        
        if self.name:
            # environment name exists
            print(f"All Stored Functions in Environment \"{self.name}\"")
        
        print(f"{'key':^5} |{'Function':^10}")
        
        for key, func in self.functions.items():
            # i : index of the function in self.func_list
            # func : __str__() of Func() class ( if defined )
            print(f"{key:^5} | {func}")
            
        print("\nTo get access, use Environment().getAllFunc() or Environment().functions")
        print("Only functions with name are stored.")
        print("To label the function, use Environment().newF(<function_str>, <function_name_str>)")
        
        
class Func(Environment):
    """
    A class for defining a function that can be called similar to mathematics notation
    
    ##### Stand-alone Usage : #####
    f = Func(
          "F0*cos(theta*t)/sqrt(m)",  # function f = (F0)*(cos(theta * t))/sqrt(m)
          F0 = 1,  # constants
          theta = 1,
          m = 1
    )
    f0 = f(t = np.array([0]))  # evaluate the function at t = 0
    print(f0)  # print the numerical result
    
    ##### Usage with Environment() class : #####
    env = Environment(
        F0 = 1,
        theta = 3.14,
        m = 1
    )  # create environment with known constants
    
    f1 = env.newF("F0*cos(theta*t)/sqrt(m)")  # new function in the env
    f2 = env.newF("-F0*sin(theta*t)/sqrt(m)")  # new function in the env
    
    # evaluate the function at t = 0
    print( f1(np.array([0])) )
    print( f2(np.array([0])) )
    """
    
    def __init__(self, func, env = Environment(), **kwargs):
        super(Func, self).__init__(env.getConstants())
        # reference constants of this new Environment() class to the given existing Environment() class
        # note that dict is mutable
        
        self.func = func
        # self.constants = kwargs  # dict
        
        if kwargs:
            self.setConstants(kwargs)
            
        self.env = env
        
    
    def __str__(self):
        return self.func
    
    
    def __call__(self, t = array([0]), **kwargs):
        """
        Evaluate the self.func
        Simply call Func("sin(t)")(t = np.array([0, 1, 2]))
        Note that **kwargs passed here will override the value of existing constants
        
        :param t: default variable. Expected type of numpy.array
        :param kwargs: user-defined variables
        :return: the image of the given function
        """
        
        # update values of constants from environment
        self.constants.update(self.env.getConstants())
        
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
"""
env = Environment(
        F0 = 1,
        theta = 3.14,
        m = 1
)  # create environment with known constants

f1 = env.newF("F0*cos(theta*t)/sqrt(m)")  # new function in the env
f2 = env.newF("-F0*sin(theta*t)/sqrt(m)")  # new function in the env

# evaluate the function at t = 0
print( f1(array([0])) )
print( f2(array([0])) )


env2 = Environment(
        g = 9.81,
        m = 3,
        omega = 2
)  # new environment

g1 = env2.newF("m*g*sin(omega*t)")  # new function in the env2
print(g1.getConstants())  # get constants of env2
print( g1(array([0, 1, 2])) )  # evaluate the function at t = 0, 1, 2
"""
"""
env = Environment(
        F0 = 1,
        theta = 3.14,
        m = 1
)

env2 = Environment(  # new environment
        constants = env.getConstants(),  # same constants and values as env
        m = 3,  # update the value of m to be 3
        g = 9.81  # new constant g = 9.81
)
print(env2.getConstants())  # get constants of env2
"""
