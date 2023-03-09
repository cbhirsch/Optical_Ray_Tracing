# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:19:24 2023

@author: Bryce
"""

import numpy as np
from sphere_refract_ray import *
from plane_refract_ray import *


def plano_convex(n, radius, thickness, dz, y):
    
    power = (n-1)/radius #lens power
    f = 1/power #paraxial focal length
    
    #Setting up the Z-Axis
    zmax = np.floor(f+.1*f)
    z_front = np.arange(0,thickness,dz)
    z_back = np.arange(thickness,zmax+2*dz,dz)
    z_optaxis = np.concatenate((z_front, z_back))
    
    #y[y==0]=10**(-10)
    raymatrix = np.zeros((len(y), len(z_optaxis)), dtype=float, order='C')
    
    #Ray Tracing
    for i in range(0,len(y)):
        #Refraction at spherical surface
        [ray_lens, slope, x_lens] = sphere_refract_ray(y[i], radius, thickness, n, dz)
        
        #Refraction at plane surface
        ray_air = plane_refract_ray(ray_lens[-1], slope, thickness, n, z_back, i)
        
        #Incoming ray
        x_front_air = np.arange(0, x_lens[0],dz)
        ray_front_air = y[i]*np.ones((len(x_front_air)))
        
                                     
        #Create matrix of rays (adjust length if necessary)
        ray_length = len(ray_lens) + len(ray_air) + len(x_front_air)
        optic_axis_length = len(z_optaxis)
        
        if ray_length <= optic_axis_length:
            raymatrix[i] = raymatrix[i]+ np.concatenate((ray_front_air,ray_lens, ray_air))
        else:
            concatenated_string = np.concatenate((ray_front_air, ray_lens[0: len(ray_lens)-1], ray_air))
            raymatrix[i] = raymatrix[i] + concatenated_string
                                     
    return raymatrix, z_front, z_optaxis, zmax

