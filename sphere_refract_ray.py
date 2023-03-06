# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 13:07:35 2023

@author: Bryce
"""

import numpy as np
import matplotlib.pyplot as plt

def sphere_refract_ray(y, radius, thickness,n,dz):
    
    sag = radius - np.sqrt(radius**2 - y**2) #lens sag at y
    z = np.arange(sag, thickness, dz)
    
    sin_phi1 = y/radius
    sin_phi2 = sin_phi1/n
    phi1 = np.arcsin(sin_phi1)
    phi2 = np.arcsin(sin_phi2)
    theta = phi2-phi1 
    slope = np.tan(theta)
    ray = np.round((slope*(z-sag)+y), 2)
    
    return ray, slope, z