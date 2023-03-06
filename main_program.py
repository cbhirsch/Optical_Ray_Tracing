# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 09:46:58 2023

@author: Bryce
"""

import numpy as np
import matplotlib.pyplot as plt
from plano_convex import *

n = 1.5168  #Index of refraction of lens
radius = 20 # Radius of spherical surface
thickness = 2 #Central thickness of lens
dz = 0.01 #step size for computation purposes
aperture = 5
number_rays = 11

#Generate ray starting heights
dy = (2*aperture + 1)/number_rays
print("dy:", dy)
y = np.arange(-aperture, aperture + 1, dy)
print("y", y)

#Ray Matrix
[raymatrix, x_front, x_optaxis, zmax] = plano_convex(n,radius,thickness,dz,y)

#Figure
#front_lens = np.sqrt(radius**2 - np.power((x_front-radius),2))
fig, ray_tracing = plt.subplots()
ray_tracing.set(xlim=(min(x_optaxis)-1,max(x_optaxis)),ylim=(min(y)-1,max(y)+1))
for i in range(0,len(y)):
    ray_tracing.plot(x_optaxis, raymatrix[i],'r') #Rays

# Lens back surface
#ray_tracing.plot(x_front, front_lens,'b', linewidth = 5.0)
plt.show()