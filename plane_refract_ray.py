# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 12:07:07 2023

@author: Bryce
"""

import numpy as np
import matplotlib.pyplot as plt

def plane_refract_ray(y, slope, thickness,n, z):
    
    theta1 = np.arctan(slope)
    theta2 = np.arcsin(n*np.sin(theta1))
    slope2 = np.tan(theta2)
    ray_air = ((z-thickness)* slope2 + y)
    
    return ray_air