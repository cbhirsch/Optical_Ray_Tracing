import numpy as np
import matplotlib.pyplot as plt
from exactraytrace.Functions import safe_arange

#Refraction at a spherical surface
def sphere_refract_ray(y, radius, thickness,n,dz,dec,prev = 0, dist= 0,slope = 0):

    #Intersection Check
    #Incoming Ray
    x_inc = safe_arange(prev,(prev + dist + thickness), dz, dec)
    Inc_Ray = slope* x_inc + y


    #Lens Surface for plotting
    x_Lens = safe_arange(0, thickness,dz, dec)
    Lens_Surf = -np.sqrt(radius**2 - np.power((x_Lens - radius),2))
    
    """ 
    #Plotting for reference
    fig, pltcheck = plt.subplots()
    pltcheck.plot(x_inc,Inc_Ray,'r')
    pltcheck.plot(x_Lens+dist,Lens_Surf, x_Lens+dist,-Lens_Surf,'b', linewidth = 2.0) 
    """

    try:
        idx = np.argwhere(np.diff(np.sign(Inc_Ray[int(dist/dz):]-Lens_Surf))).flatten()
        var = idx[0]
        #pltcheck.plot(x_inc[var]+dist,Inc_Ray[var],'ro')
    except:
        idx = np.argwhere(np.diff(np.sign(Inc_Ray[int(dist/dz):]-(-Lens_Surf)))).flatten()
        var = idx[0]
        #pltcheck.plot(x_inc[var]+dist,Inc_Ray[var],'ro')
    
    #plt.show()

    
    sag = radius - np.sqrt(radius**2 - Inc_Ray[var]**2) #lens sag at y
    z_lens = safe_arange(sag, thickness, dz, dec)
    z_front = x_inc[:int((z_lens[0]+dist)/dz)]
    x_tot = np.concatenate((z_front,z_lens+dist))
    """     
    print(int(z_lens[0]/dz))
    print("z shape:", z.shape)
    print("z start:",z[0])
    print("z finish:",z[-1]) """
    
    sin_phi1 = y/radius
    sin_phi2 = sin_phi1/n
    phi1 = np.arcsin(sin_phi1+slope)
    phi2 = np.arcsin(sin_phi2)
    theta = phi2-phi1 
    slope = np.tan(theta)
    ray = (slope*(z_lens-sag)+y)
    #print("ray shape:", ray.shape)
    y_inc = Inc_Ray[:(len(Inc_Ray)-len(ray))]
    if len(x_tot) == (len(y_inc)+len(ray)):
        ray_tot = np.concatenate((y_inc,ray))
    else:
        y_inc = Inc_Ray[:(len(Inc_Ray)-len(ray)-1)]
        ray_tot = np.concatenate((y_inc,ray))
    fig, raycheck = plt.subplots()
    raycheck.set(xlim = (0, 30))
    raycheck.plot(x_Lens+dist,Lens_Surf, x_Lens+dist,-Lens_Surf,'b', linewidth = 2.0)
    raycheck.plot( x_tot, ray_tot, 'b')
    #plt.show()
    return ray_tot, slope, x_tot

    
#Refraction at a planar surface
def plane_refract_ray(y, slope, thickness,n, z):
    
    print("z in plane-ref:",z.shape)
    theta1 = np.arctan(slope)
    print("theta1:",theta1)
    theta2 = np.arcsin(n*np.sin(theta1))
    print("theta2:", theta2)
    slope2 = np.tan(theta2)
    print("slope2:", slope2)
    ray_air = ((z-thickness)* slope2 + y)
    print("ray_air:", ray_air)
    print("ray_air shape",ray_air.shape)
    
    return ray_air,slope2

