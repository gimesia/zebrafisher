# !!! TODO: UNFINISHED, but could use 'hiperfit'

import numpy as np

"""
fits a circle  in x,y plane in a more accurate (less prone to ill condition) 
procedure than circfit2 but using more memory x,y are column vector where 
(x(i),y(i)) is a measured point

result is center point (yc,xc) and radius R an optional output is the 
vector of coefficient a describing the circle's equation

x^2+y^2+a(1)*x+a(2)*y+a(3)=0
By:  Izhak bucher 25/oct /1991, 
"""

def circle_fit(x: np.ndarray, y: np.ndarray):
    """
    :param x: vector of x coordinates
    :param y: vector of y coordinates

    :returns c_x: X coordinate of the center
    :returns c_y: Y coordinate of the center
    :returns R: radius of the circle
    """

    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)

    a = []
