"""
Diff.py

Calculate differential of a given dataset numerically

Written by S. P. Lam
"""

from numpy import array


def dydx(y, x):
    """
    Calculate first order differential from given data numerically
    
    :param y: data points for y-coordinate
    :param x: data points for x-coordinate
    :return: type of numpy array
    """
    points = list(zip(x, y))
    dydx = []
    
    # calculate the slope for each point P_i and P_(i+1)
    for i in range(len(points) - 1):
        dy = points[i+1][1] - points[i][1]
        dx = points[i+1][0] - points[i][0]
        slope = dy/dx
        dydx.append(slope)
    
    # approximate the slope for last data point equals to the previous one
    dydx.append(dydx[-1])
    
    return array(dydx)
    
