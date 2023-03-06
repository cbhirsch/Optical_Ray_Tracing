# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:19:24 2023

@author: Bryce
"""

import numpy as np
import sphere_refract_ray.sphere_refract_ray
import plane_refract_ray.plane_refract_ray

def plano_convex(n, radius, thickness, dz, y):
    
    power = (n-1)/radius
    f = 1/power
    
    zmax = np.floor(f+.1*f)
    z_front = np.arange(0,thickness-dz,dz)
    z_back = np.arange(thickness,zmax-dz,dz)
    z_optaxis = [z_front, z_back]
    print(z_optaxis)
    
    y[y==0]=10**(-10)
    raymatrix = np.zeros(len(y), len(z_optaxis))
    
    #Ray Tracing
    for i in np.arange(1,len(y)):
        
        #Refraction at spherical surface
        [ray_lens, slope, x_lens] = sphere_refract_ray(y(i), radius, thickness, n, dz)
        
        #Refraction at plane surface
        [ray_air] = plane_refract_ray(ray_lens(-1), slope, thickness, n, z_back)
        
        #Incoming ray
        x_front_air = np.arange(0, x_lens(1)-dz,dz)
        ray_front_air = y(i)*np.ones(1,len(x_front_air))
        
        #Create matrix of rays (adjust length if necessary)
        if len(ray_lens) + len(ray_air) + len(x_front_air) <= len(z_optaxis):
            raymatrix[i,:] = [ray_front_air,ray_lens, ray_air]
        else:
            raymatrix[i,:] = np.arange(ray_front_air, ray_lens(np.arange(1,len(ray_lens)-1)), ray_air)

    return raymatrix, z_front, z_optaxis, zmax