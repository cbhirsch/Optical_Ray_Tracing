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
    print("zmax:", zmax)
    z_front = np.arange(0,thickness,dz)
    print("z_front:", '\n', "min:", min(z_front),"\n", "max:", max(z_front))
    z_back = np.arange(thickness,zmax+2*dz,dz)
    print("z_back:", z_back, '\n', "min:", min(z_back),"\n", "max:", max(z_back))
    z_optaxis = np.concatenate((z_front, z_back))
    print("z_optaxis:", '\n',"shape:",z_optaxis.shape,"\n", "min:", min(z_optaxis),"\n", "max:", max(z_optaxis))
    
    y[y==0]=10**(-10)
    print("this is the shape of y:", y.shape)
    print("this is the value of y:", y)
    raymatrix = np.zeros((len(y), len(z_optaxis)), dtype=int, order='C')
    
    #Ray Tracing
    for i in range(0,len(y)):
        print("\n increment:", i)
        print("y:",y[i])
        #Refraction at spherical surface
        [ray_lens, slope, x_lens] = sphere_refract_ray(y[i], radius, thickness, n, dz)
        #print(f"output: \n ray_lens:{ray_lens} \n slope: {slope} \n x_lens: {x_lens}" )
        print("ray_lens shape:", ray_lens.shape)
        print("ray_air range:",min(ray_lens),max(ray_lens))
        print("x_lens shape:", x_lens.shape)
        
        #Refraction at plane surface
        ray_air = plane_refract_ray(ray_lens[-1], slope, thickness, n, z_back, i)
        print("ray_air shape:", ray_air.shape)
        print("ray_air range:",min(ray_air),max(ray_air))
        
        #Incoming ray
        x_front_air = np.arange(0, x_lens[0],dz)
        print("x_front_air shape:", x_front_air.shape)
        if i != 5:
            print("x_front_air range:",min(x_front_air),max(x_front_air))
        ray_front_air = y[i]*np.ones((len(x_front_air)))
        print("ray_front_air shape:", ray_front_air.shape)
        
                                     
        #Create matrix of rays (adjust length if necessary)
        
        ray_length = len(ray_lens) + len(ray_air) + len(x_front_air)
        optic_axis_length = len(z_optaxis)

        print('raymatrix before:',raymatrix[i])
        print('raymatrix type', type(raymatrix[i]))
        print('raymatrix shape', raymatrix[i].shape)
        
        if ray_length <= optic_axis_length:
            print("string front:", ray_front_air)
            print("ray lens:", ray_lens)
            print("ray air:", ray_air )
            print("concatenated:",np.concatenate((ray_front_air,ray_lens, ray_air)))
            print("concatenated:",(np.concatenate((ray_front_air,ray_lens, ray_air))).shape)
            raymatrix[i] = raymatrix[i]+ np.concatenate((ray_front_air,ray_lens, ray_air))
        else:
            print("string front:", ray_front_air)
            print("ray lens:", ray_lens[0: len(ray_lens)-1])
            print("ray air:", ray_air )
            print("concatenated:",np.concatenate((ray_front_air, ray_lens[0: len(ray_lens)-1], ray_air)))
            print("concatenated:",(np.concatenate((ray_front_air, ray_lens[0: len(ray_lens)-1], ray_air))).shape)
            concatenated_string = np.concatenate((ray_front_air, ray_lens[0: len(ray_lens)-1], ray_air))
            raymatrix[i] = raymatrix[i] + concatenated_string
        print('raymatrix after:', raymatrix[i])
        print('raymatrix type', type(raymatrix[i]))
        print('raymatrix shape', raymatrix[i].shape)

        if y[i] == 5: 
            fig, ind_ray_plot = plt.subplots()
            ind_ray_plot.set(xlim=(0,42),ylim=(-7,7))
            ind_ray_plot.plot(z_optaxis,raymatrix[i],'r') #Rays
            plt.show()                                   
    print("raymatrix: \n", "shape:", raymatrix.shape)
    print(raymatrix)                                      
    return raymatrix, z_front, z_optaxis, zmax

