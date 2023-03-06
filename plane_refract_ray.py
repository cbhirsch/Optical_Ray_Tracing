# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 12:07:07 2023

@author: Bryce
"""

import numpy as np
import matplotlib.pyplot as plt

def plane_refract_ray(y, slope, thickness,n, z, i):
    
    theta1 = np.arctan(slope)
    theta2 = np.arcsin(n*np.sin(theta1))
    slope2 = np.tan(theta2)
    ray_air = np.round(((z-thickness)* slope2 + y),2)
    z = np.arange(2,42.02,.01)
    
    return ray_air