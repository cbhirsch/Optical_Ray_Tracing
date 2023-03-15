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

    def Matrix_state(self):
        print("raymatrix: \n", self.raymatrix.shape)

    def Add_Lens(self, Lens):
        self.thickness = Lens.thickness

        self.radius = Lens.radius
        power = ( Lens.n - 1)/Lens.radius #lens power
        f = 1/power #paraxial focal length

        #setting up the Z-Axis
        zmax = np.floor(f + .1*f)
        self.z_front = safe_arange(0,Lens.thickness, self.dz, self.dec)
        z_back = safe_arange(Lens.thickness, zmax+2*self.dz, self.dz, self.dec)
        self.z_optaxis = np.concatenate((self.z_front, z_back))

        #Setting up the empty raymatrix likely to change this step in future iterations
        self.raymatrix = np.zeros((len(self.y),len(self.z_optaxis)))

        #Ray Tracing
        for i in range(0, len(self.y)):
            #Refraction at spherical surface
            [ray_lens, slope, x_lens] =  sphere_refract_ray(self.y[i], Lens.radius, Lens.thickness, Lens.n, self.dz, self.dec)

            #Refractionat plane surface
            ray_air = plane_refract_ray(ray_lens[-1], slope, Lens.thickness, Lens.n, z_back)

            #Incomeing Ray
            x_front_air = safe_arange(0, x_lens[0], self.dz, self.dec)
            ray_front_air = self.y[i]*np.ones((len(x_front_air)))

            #Create matrix of rays (adjust length if necessary)
            ray_length = len(ray_lens) + len(ray_air) + len(x_front_air)
            optic_axis_length = len(self.z_optaxis)

            if ray_length <= optic_axis_length:
                self.raymatrix[i] = self.raymatrix[i] + np.concatenate((ray_front_air, ray_lens, ray_air))
            else:
                concatenated_string = np.concatenate((ray_front_air, ray_lens[0: len(ray_lens)-1], ray_air))
                self.raymatrix[i] = self.raymatrix[i] + concatenated_string

        return self.raymatrix, self.z_front, self.z_optaxis, zmax, self.thickness
    
    def plot(self):
        thickness = self.thickness
        x_front = self.z_front
        self.x_optaxis = self.z_optaxis

        #Figure
        front_lens = np.sqrt(self.radius**2 - np.power((x_front-self.radius),2))
        fig, ray_tracing = plt.subplots()
        ray_tracing.set(xlim = (min(self.z_optaxis)-1, max(self.z_optaxis)),ylim = (min(self.y)-6,max(self.y)+6))
        for i in range(0,len(self.y)):
            ray_tracing.plot(self.z_optaxis, self.raymatrix[i], 'r') #Rays
        
        #Lens front surface
        ray_tracing.plot(x_front, front_lens,'b', x_front, -front_lens, 'b', linewidth = 3.0)

        # Len Back Surface
        x_back = [thickness, thickness]
        y_back = [max(front_lens),-max(front_lens)]
        ray_tracing.plot(x_back,y_back, 'b', linewidth = 3.0 )

        #Optical axis
        ray_tracing.plot(self.x_optaxis, np.zeros(len(self.x_optaxis)), 'k--')
        
        plt.show()
    
    def spherical_aberation(self):

        #Find where each ray crosses optical axis
        ray_focus = np.zeros((1,len(self.y)), dtype = int, order = 'c')
        for i in range(len(self.y)):
            ray_focus[0,i]=np.argmin(abs(self.raymatrix[i]))

        #Find where paraxial ray crosses optical axis
        paraxial_focus = int(ray_focus[0,int(np.ceil(len(self.y)/2))])

        #Ray fan plot
        fig, ray_fan_plot = plt.subplots()
        ray_fan_plot.plot(self.y, self.raymatrix[:,paraxial_focus])
        plt.show()

        #Spherical Aberation
        pos_y = np.transpose(np.argwhere(self.y>0))
        spher_ab = self.x_optaxis[ray_focus[0,pos_y[0]]]
        fig, spher_ab_plot = plt.subplots()
        spher_ab_plot.plot(spher_ab - spher_ab[1],self.y[np.argwhere(self.y>0)])
        plt.show()


    






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
    def __init__(self, n, radius, thickness):
        self.n = n
        self.radius = radius
        self.thickness = thickness
    
    def Current(self):
        print("This is the information Lens:")
        print("n:",self.n)
        print("radius:",  self.radius)
        print("thickness:", self.thickness)


""" #Example Code
if __name__ == "__main__":

    #Initialize Lens
    Lens1 = plano_convex(1.5168, 20, 2)
    Lens2 = plano_convex(2.635, 30, 2)

    #Run the Ray Tracing
    example1 = Product_Matrix()
    example1.start(5, 11, 0.01,2,)
    example1.Add_Lens(Lens1)
    example1.Current()
    example1.Matrix_state()
    example1.plot()
    example1.spherical_aberation() """