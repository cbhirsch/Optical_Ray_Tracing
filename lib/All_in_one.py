import numpy as np
import matplotlib.pyplot as plt

#Useful Functions

""" 

The functions below will be callable libraries that can be used throughout
The Program.  They are not designed to be included in the main program.

"""

#This arange function is designed to be more precise with floating point numbers
def safe_arange(start, stop, step, dec):
    round_start = round(start, dec)
    round_stop = round(stop, dec)
    int_start = round(round_start/step)
    int_stop = round(round_stop/step)

    return step * np.arange(int_start, int_stop+1)


# These are the Surface Functions

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

def plane_refract_ray(y, slope, thickness,n, z):
    
    theta1 = np.arctan(slope)
    theta2 = np.arcsin(n*np.sin(theta1))
    slope2 = np.tan(theta2)
    ray_air = ((z-thickness)* slope2 + y)
    
    return ray_air
    
""" 
Main Program 
This describes the ultimate goal of this program and how it's 
intended to be used when called by a user.
Current program may or may not operate this way currently.

The main program will work by calling functions as follows below:

#Starting Conditions
start can be equal too 'inf' or 'point'
start = exactraytrace.start(start = 'inf', dist, #_of_rays, aperture)

#Lens1
lens_1 = exactraytrace.lens(front_surf, back_surface, dia, n, dist)

Will neet to return the ending location of y and a slope value and
communicate this to the next call location.

#Lens2
lens_2 = exactraytrace.lens(front_surf, back_surface, dia, n, dist)

Will neet to return the ending location of y and a slope value and
communicate this to the next call location.

#Finish
Final = concatenate(start, lens_1, len_2)

This final function will combine a ray matrix for both X & Y terms

plot

plt.show()

This will plot all data for the Ray Matrix terms

"""
class Product_Matrix:
    def __init__(self):
        self.raymatrix = []

    def Current(self):
        print("This is the information on current product matrix:")
        print("Aperture:",self.aperture)
        print("# of Rays:",  self.number_rays)
        print("decimal places:", self.dec)
        print("y rays:", self.y)
        print("Lens Radius:", self.radius)

    def start(self,aperture, number_rays, dz, dec, dist = 0):
        self.aperture = aperture
        self.number_rays = number_rays
        # This is a placeholder for now
        self.slope = 0
        self.dz = dz
        self.dec = dec

        #Generate ray starting heights
        self.dy = (2*aperture + 1)/number_rays
        self.y = safe_arange(-aperture, aperture, self.dy, dec)

    def Add_Lens(self, Lens):
        self.radius = Lens.radius

    






#Starting Conditions
""" class start(raymatrix):
    def __init__(self,aperture, number_rays, dz, dec):
        self.aperture = aperture
        self.number_rays = number_rays
        self.dz = dz
        self.dec = dec
        self.dy = (2*aperture +1)/number_rays
        self.y = safe_arange(-aperture, aperture, self.dy, dec) """


#Lens Setup

""" 
Currently trying to get this class to take the output 
of the start class.  

"""

class Lens:
    pass

class plano_convex(Lens):
    def __init__(self,n,radius, thickness):
        self.n = n
        self.radius = radius
        self.thickness = thickness
    
    def Current(self):
        print("This is the information Lens:")
        print("n:",self.n)
        print("radius:",  self.radius)
        print("thickness:", self.thickness)
    
""" class Image_plane(raymatrix):
    pass
 """

#Initialize Lens
Lens1 = plano_convex(1.5168, 20, 2)
Lens2 = plano_convex(2.635, 30, 2)

#Run the Ray Tracing
example1 = Product_Matrix()
example1.start(5, 11, 0.001,3,)
example1.Add_Lens(Lens1)
example1.Current()
example1.Add_Lens(Lens2)
example1.Current()