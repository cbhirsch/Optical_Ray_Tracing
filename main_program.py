# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 09:46:58 2023

@author: Bryce
"""

import numpy as np
import matplotlib.pyplot as plt
from plano_convex import *
from safe_arange import *

n = 1.5168  #Index of refraction of lens
radius = 20 # Radius of spherical surface
thickness = 2 #Central thickness of lens
dz = 0.001 #step size for computation purposes
dec = 3 #decimal point accuracy
aperture = 5
number_rays = 11

#Generate ray starting heights
dy = (2*aperture + 1)/number_rays
y = safe_arange(-aperture, aperture, dy, dec)
print("y after safe arange:",y)

#Ray Matrix
[raymatrix, x_front, x_optaxis, zmax] = plano_convex(n,radius,thickness,dz,y, dec)

#Figure
front_lens = np.sqrt(radius**2 - np.power((x_front-radius),2))
fig, ray_tracing = plt.subplots()
ray_tracing.set(xlim=(min(x_optaxis)-1,max(x_optaxis)),ylim=(min(y)-6,max(y)+6))
for i in range(0,len(y)):
    ray_tracing.plot(x_optaxis, raymatrix[i],'r') #Rays

# Lens Front surface
ray_tracing.plot(x_front, front_lens,'b', x_front, -front_lens, 'b', linewidth = 3.0)

# Len Back Surface
x_back = [thickness, thickness]
y_back = [max(front_lens),-max(front_lens)]
ray_tracing.plot(x_back,y_back, 'b', linewidth = 3.0 )

#Optical axis
ray_tracing.plot(x_optaxis, np.zeros(len(x_optaxis)), 'k--')

ray_tracing.plot()
plt.show()

#Find where each ray crosses optical axis
ray_focus = np.zeros((1,len(y)), dtype = int, order = 'c')
for i in range(len(y)):
    ray_focus[0,i]=np.argmin(abs(raymatrix[i]))
    

#Find where paraxial ray crosses optical axis
paraxial_focus = int(ray_focus[0,int(np.ceil(len(y)/2))])

#Ray fan plot
fig, ray_fan_plot = plt.subplots()
ray_fan_plot.plot(y, raymatrix[:,paraxial_focus])
plt.show()

#Spherical Aberation
pos_y = np.transpose(np.argwhere(y>0))
spher_ab = x_optaxis[ray_focus[0,pos_y[0]]]
fig, spher_ab_plot = plt.subplots()
spher_ab_plot.plot(spher_ab - spher_ab[1],y[np.argwhere(y>0)])
plt.show()