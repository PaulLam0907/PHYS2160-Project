"""
ODE2.py

A class dedicated for solving second order differential equation.
ax" + bx' + cx = d * f(t)

Reference :
https://stackoverflow.com/questions/19779217/need-help-solving-a-second-order-non-linear-ode-in-python
https://cmps-people.ok.ubc.ca/jbobowsk/Python/html/Jupyter%20Second%20Order%20ODEs.html

Written by S. P. Lam
"""

# import numpy as np
from scipy.integrate import odeint


class ODE2:
    
    def __init__(self, a, b, c, d, x0, x_dot0, f = 1):
        """
        A class dedicated for solving second order differential equation.
        ax" + bx' + cx = d * f(t)
        
        Usage:
        f = ODE(1, 2, 3, 4, 5, 6)  # 1x" + 2x' + 3x = 4 * 1; x(0) = 5; x'(0) = 6
        x, v = f([1])  # solving for f at t=1
        
        :param a: coefficient for x"
        :param b: coefficient for x'
        :param c: coefficient for x
        :param d: constant term
        :param x0: initial condition for x at t = t0
        :param x_dot0: initial condition of x' at t = t0
        :param f: (optional) a callable function of time t with d as its coefficient
        """
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.x0 = x0
        self.x_dot0 = x_dot0
        self.f = f
        
    def __call__(self, t, *args, **kwargs):
        """
        Get the result of the solved ODE at given time t
        
        :param t: time, must be at least 1D array e.g. np.arange(0, 10, 1e-3)
        :param args:
        :param kwargs:
        :return: tuple of (position, velocity)
        """
        x, v = odeint(self.ddotX, (self.x0, self.x_dot0), t).T  # .T --> transpose
        
        return x, v
        
    def ddotX(self, x, t):
        """
        Helper function for odeint() to solve the differential equation
        
        ax" + bx' + cx = d * f(t)
        let v = x'  --(1)
        av' + bv + cx = d * f(t)
        v' = -(b/a)v - (c/a)x + (d/a) * f(t)  --(2)
        
        :param x:
        :param t:
        :return:
        """
        # x = x[0]
        v = x[1]
        
        if callable(self.f):
            # f is a callable function
            ddot_x = -(self.b/self.a)*v - (self.c/self.a)*x[0] + self.d*self.f(t)/self.a
        
        else:
            # f is not a callable function
            ddot_x = -(self.b/self.a)*v - (self.c/self.a)*x[0] + self.d*self.f/self.a
        
        return v, ddot_x
