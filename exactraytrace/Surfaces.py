import numpy as np
import matplotlib.pyplot as plt
from exactraytrace.Functions import safe_arange

#Refraction at a spherical surface
def sphere_refract_ray(y, radius, thickness,n,dz,dec, prev, dist= 0,slope = 0):
    print("------Sphere refract ray functions started------\n")
    print("Values Being Read in:")
    print("y = ", y)
    print("radius = ", radius)
    print("thickness = ", thickness)
    print("n = ", n)
    print("dz = ", dz)
    print("dec = ", dec)
    print("dist = ", dist)
    print("slope = ", slope)
    print("prev shape:", prev.shape)
    print("prev start:", prev[0])
    print("prev finsish:", prev[-1],"\n")

    #Intersection Check
    #Incoming Ray
    x_start = prev[-1] #where the refraction axis starts
    x_end = prev[-1]+thickness #Where the refraction axis ends
    x_sphere = safe_arange(x_start,x_end, dz, dec) 

    #Intersecting Ray
    int_ray = (slope* x_sphere) + y
    print("--checking for x & y intercept-- \n")
    print("properties of previous ray:")
    print("previous x & y shape:", x_sphere.shape, int_ray.shape)
    print("previous x & y start:", x_sphere[0], int_ray[0])
    print("previous x & y finish:", x_sphere[-1], int_ray[-1], "\n")


    #Lens Surface for plotting
    x_Lens = safe_arange(prev[-1], prev[-1] + thickness,dz, dec)
    Lens_Surf = -np.sqrt(radius**2 - np.power(((x_Lens-prev[-1]) - radius),2))
    print("Properties of Lens surface:")
    print("Lens x & y shape:", x_Lens.shape, Lens_Surf.shape)
    print("Lens x & y start:", x_Lens[0], Lens_Surf[0])
    print("Lens x & y finish:", x_Lens[-1], Lens_Surf[-1], "\n")

    #Intercept Function Inputs
    try:
        idx = np.argwhere(np.diff(np.sign(int_ray-Lens_Surf))).flatten()
        var = idx[0]
    except:
        idx = np.argwhere(np.diff(np.sign(int_ray-(-Lens_Surf)))).flatten()
        var = idx[0]
    
    x_val = (var*dz)+prev[-1] #x value of the y - intercept

    print("Lens intercept:")
    print("Lens X & Y", x_val, Lens_Surf[var])
    print("Ray X & Y", x_val, int_ray[var], "\n")
    
    fig1, testplot = plt.subplots()
    testplot.set_xlim(prev[0],(prev[-1]+thickness + dist))
    testplot.set_ylim(-8,8)
    testplot.plot(x_sphere, int_ray, 'r')
    testplot.plot(x_Lens, Lens_Surf, x_Lens, -Lens_Surf,'b', linewidth = 3.0 )
    testplot.plot( x_val, int_ray[var], 'o')

    plt.show()
    plt.close()
    
    #Refraction at spherical surface
    print("--Starting Refraction Calculations--\n")
    sag = radius - np.sqrt(radius**2 - int_ray[var]**2) #lens sag at y
    x_refract = safe_arange(sag, thickness, dz, dec)
    sin_phi1 = y/radius
    sin_phi2 = sin_phi1/n
    phi1 = np.arcsin(sin_phi1+slope)
    phi2 = np.arcsin(sin_phi2)
    theta = phi2-phi1 
    slope = np.tan(theta)
    ray = (slope*(x_refract-sag)+y)

    print("refraction calculations outputs:")
    print("sag = ", sag)
    print("refraction axis length:",x_refract.shape)
    print("refraction axis start", x_refract[0])
    print("refraction axis end", x_refract[-1])
    print("sin_phi1 = ", sin_phi1)
    print("sin_phi2 = ", sin_phi2)
    print("theta = ", theta)
    print("slope = ", slope)
    print("ray shape:", ray.shape)
    print("ray start:", ray[0])
    print("ray end:", ray[-1], "\n")


    #Fill in the gaps in the axis refraction axis
    x_fill = safe_arange(x_start,x_end-(len(x_refract)*dz), dz, dec)
    print("x axis fill properties:")
    print("x axis fill shape:", x_fill.shape)
    if len(x_fill)!= 0:
        print("x axis fill start", x_fill[0])
        print("x axis fill end", x_fill[-1], "\n")

        y_fill = int_ray[0:len(x_fill)]
        print("y axis fill properties:")
        print("y axis fill shape:", y_fill.shape)
        print("y axis fill start", y_fill[0])
        print("y axis fill end", y_fill[-1],"\n")

        #combining Fill values with refraction calculations
        ray_tot = np.concatenate((y_fill,ray))

    else:
        print("length of x fill = ", len(x_fill),"\n")

        #ray equals ray tot at origin
        ray_tot = ray

    #Test Figure
    fig2, testplot2 = plt.subplots()
    testplot2.set_xlim(prev[0],(prev[-1]+thickness + dist))
    testplot2.set_ylim(-8,8)
    testplot2.plot(x_sphere, ray_tot, 'r')
    testplot2.plot(x_Lens, Lens_Surf, x_Lens, -Lens_Surf,'b', linewidth = 3.0 )
    testplot2.plot( x_val, int_ray[var], 'o')

    plt.show()
    plt.close()

        
    return ray_tot, slope, x_sphere

    
#Refraction at a planar surface
def plane_refract_ray(y, slope, thickness,n, dist, prev,dz, dec):

    #Input Values print statements
    print("------Plane refract ray functions started------\n")
    print("Values Being Read in:")
    print("y = ", y)
    print("thickness = ", thickness)
    print("n = ", n)
    print("dist = ", dist)
    print("slope = ", slope)
    print("shape previous x axis", prev.shape)
    print("start previous x axis", prev[0])
    print("end of previous x axis", prev[-1], "\n")

    #Setting up plane refraction x-axis
    plane_start = prev[-1]
    plane_finish = prev[-1] + dist
    x_plane = safe_arange(plane_start+dz,plane_finish,dz, dec)

    #Output of x axis of planar surface
    print("output of x axis of planar surface:")
    print("x axis shape:", x_plane.shape)
    print("x axis start:", x_plane[0])
    print("x axis finish:", x_plane[-1], "\n")
    
    # Planar surface calculations
    theta1 = np.arctan(slope)
    theta2 = np.arcsin(n*np.sin(theta1))
    slope2 = np.tan(theta2)
    ray_air = ((x_plane-plane_start)* slope2 + y)

    #Ouput values print statements
    print("planar surface outputs:")
    print("theta1 = ", theta1)
    print("theta2 = ", theta2)
    print("slope2 = ", slope)
    print("ray air shape:", ray_air.shape)
    print("ray air start", ray_air[0])
    print("ray air end:", ray_air[-1],"\n")

    #Lens Surface
    x_back = plane_start*np.ones(11)
    y_back = safe_arange(-5,5,1, dec)

    fig3, testplot3 = plt.subplots()
    testplot3.set_xlim(prev[0],(prev[-1]+thickness + dist))
    testplot3.set_ylim(-8,8)
    testplot3.plot(x_back, y_back, 'b', linewidth = 3.0 )
    testplot3.plot( x_plane, ray_air, 'r')

    plt.show()
    plt.close()

    
    return ray_air,slope

