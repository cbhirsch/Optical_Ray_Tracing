import numpy as np
from exactraytrace.Functions import safe_arange

def sphere_refract_ray(y, radius, thickness,n,dz,dec):
    
    sag = radius - np.sqrt(radius**2 - y**2) #lens sag at y
    z = safe_arange(sag, thickness, dz, dec)
    
    sin_phi1 = y/radius
    sin_phi2 = sin_phi1/n
    phi1 = np.arcsin(sin_phi1)
    phi2 = np.arcsin(sin_phi2)
    theta = phi2-phi1 
    slope = np.tan(theta)
    ray = (slope*(z-sag)+y)
    return ray, slope, z

    
#Refraction at a planar surface
def plane_refract_ray(y, slope, thickness,n, z):
    
    theta1 = np.arctan(slope)
    theta2 = np.arcsin(n*np.sin(theta1))
    slope2 = np.tan(theta2)
    ray_air = ((z-thickness)* slope2 + y)
    
    return ray_air

