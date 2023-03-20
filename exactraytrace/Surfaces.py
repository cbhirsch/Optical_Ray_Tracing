import numpy as np
import matplotlib.pyplot as plt
from exactraytrace.Functions import safe_arange

#Refraction at a spherical surface
def sphere_refract_ray(y, radius, thickness,n,dz,dec,prev = 0, dist= 0,slope = 0):

    #Intersection Check
    #Incoming Ray
    print("dz:",dz)
    print("dec:", dec)
    print("prev", prev)
    print("dist", dist)
    x_inc = safe_arange(prev,(prev + dist + thickness), dz, dec)
    print("x_inc shape:", x_inc.shape)
    print("x_inc start:",x_inc[0])
    print("x_inc finish:",x_inc[-1])
    Inc_Ray = slope* x_inc + y
    print("inc shape:", Inc_Ray.shape)

    #Lens Surface for plotting
    x_Lens = safe_arange(0, thickness,dz, dec)
    Lens_Surf = -np.sqrt(radius**2 - np.power((x_Lens - radius),2))
    
    #Plotting for reference
    fig, pltcheck = plt.subplots()
    pltcheck.plot(x_inc,Inc_Ray,'r')
    pltcheck.plot(x_Lens+dist,Lens_Surf, x_Lens+dist,-Lens_Surf,'b', linewidth = 2.0)

    try:
        idx = np.argwhere(np.diff(np.sign(Inc_Ray[int(dist/dz):]-Lens_Surf))).flatten()
        var = idx[0]
        pltcheck.plot(x_inc[var]+dist,Inc_Ray[var],'ro')
    except:
        idx = np.argwhere(np.diff(np.sign(Inc_Ray[int(dist/dz):]-(-Lens_Surf)))).flatten()
        var = idx[0]
        pltcheck.plot(x_inc[var]+dist,Inc_Ray[var],'ro')
    
    plt.show()

    
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
    phi1 = np.arcsin(sin_phi1)
    phi2 = np.arcsin(sin_phi2)
    theta = phi2-phi1 
    slope = np.tan(theta)
    ray = (slope*(z_lens-sag)+y)
    print("ray shape:", ray.shape)
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
    plt.show()
    return ray, slope, x_tot

    
#Refraction at a planar surface
def plane_refract_ray(y, slope, thickness,n, z):
    
    theta1 = np.arctan(slope)
    theta2 = np.arcsin(n*np.sin(theta1))
    slope2 = np.tan(theta2)
    ray_air = ((z-thickness)* slope2 + y)
    
    return ray_air

