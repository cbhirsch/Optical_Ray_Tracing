# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 13:07:35 2023

@author: Bryce
"""

import numpy as np
import matplotlib.pyplot as plt

def sphere_refract_ray(y, radius, thickness,n,dz):
    
    sag = radius - np.sqrt(radius**2 - y**2) #lens sag at y
    print("sag:", sag)
    z = np.arange(sag, thickness, dz)
    
    sin_phi1 = y/radius
    sin_phi2 = sin_phi1/n
    phi1 = np.arcsin(sin_phi1)
    phi2 = np.arcsin(sin_phi2)
    theta = phi2-phi1 
    slope = np.tan(theta)
    ray = np.round((slope*(z-sag)+y), 2)

    if y == 5:
# =============================================================================
#         print("slope:", slope)
#         print("z shape: ",z.shape)
#         print("z:", z)
#         print("ray shape:", ray.shape)
#         print("ray:", ray)
# =============================================================================
        fig, sphere_refract_check = plt.subplots()
        sphere_refract_check.set(xlim=(0,42),ylim=(-7,7))
        sphere_refract_check.plot(z,ray,'r') #Rays
        plt.show()
    
    return ray, slope, z