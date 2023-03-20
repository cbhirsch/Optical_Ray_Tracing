import numpy as np
import matplotlib.pyplot as plt
from exactraytrace.Surfaces import sphere_refract_ray,plane_refract_ray
from exactraytrace.Functions import safe_arange

class Product_Matrix:
    """ 
    Designates the object that will be used to build the matrix for plotting
    the rays as they travel through the lens system.
    """
    def __init__(self):
        self.raymatrix = []

    """ 
    Function used for tracking the current state of the class
    """
    def Current(self):
        print("This is the information on current product matrix:")
        print("Aperture:",self.aperture)
        print("# of Rays:",  self.number_rays)
        print("decimal places:", self.dec)
        print("y rays:", self.y)
        # print("Lens Radius:", self.radius)
        print("raymatrix:", self.raymatrix)
        print("z_opticaxis:", self.z_optaxis)

    """
    This function defines the starting conditions of the ray tracing algorithm:

    The function can take in the below variables:
    aperture- this defines the starting aperture of the lens and is used to determine 
    the total height of the ray fan

    number_rays- this variable dictates the number of rays that will be used for ray tracing

    dz- This is the number of steps designated for building the matrix

    dec- This is the number of decimal places designated in dz 

    dist- This is the distance of starting point to the fist lens

    inf- This dictates whether the rays are projecting from a focus point or are parellel
    which is considered infinity focus in optics
    """

    def start(self,aperture, number_rays, dz, dec, dist = 0, inf = "True"):
        self.aperture = aperture
        self.number_rays = number_rays
        self.slope = np.zeros(number_rays, dtype= 'int', order = 'C')
        self.dist = dist
        self.dz = dz
        self.dec = dec

        #Generate ray starting heights
        self.dy = (2*aperture + 1)/number_rays
        self.y = safe_arange(-aperture, aperture, self.dy, dec)

        #Designating space for raymatrix

        self.raymatrix = np.zeros((len(self.y), int(dist/dz)+1))
        
        #This function will fill the starting values in the raymatrix
        if inf == "True":
            for i in range(0,len(self.y)):
                #This term will determine rays current slope
                self.slope[i] = 0
                self.raymatrix[i] = self.y[i]*np.ones(int(dist/dz)+1)
        else:
            pass

        self.z_optaxis = safe_arange(0,dist, dz, dec)
        self.Prev_Start = self.z_optaxis[0] #This variable tracks previous ray starting location
        print("1st ray x & Y: \n", self.z_optaxis.shape, self.raymatrix[i].shape)
        



    def Matrix_state(self):
        print("raymatrix: \n", self.raymatrix.shape)

    def New_Add_Lens(self, Lens):
        self.thickness = Lens.thickness

        #Setting up new Z-axis
        end_axis = self.z_optaxis[-1] #End of current axis
        print("end_axis:",end_axis)
        z_back = safe_arange(end_axis+self.thickness, Lens.dist,self.dz, self.dec)
        add_axis = safe_arange(end_axis, (self.thickness + Lens.dist),self.dz, self.dec)
        self.z_optaxis = np.concatenate((self.z_optaxis, add_axis[1:]))

        #Setting up new raymatrix
        add_raymatrix = np.zeros((len(self.y),(len(add_axis))))
        print("shape additional ray matrix: \n", add_raymatrix.shape)

        #ray tracing through surfaces
        for i in range(0, len(self.y)):
            print("iteration #:", i)
            #Refraction at spherical surface
            [ray_lens, slope, x_lens] =  sphere_refract_ray(self.y[i], Lens.radius, Lens.thickness, Lens.n, self.dz, self.dec, self.Prev_Start,self.dist ,self.slope[i])

            #Refractionat plane surface
            ray_air = plane_refract_ray(ray_lens[-1], slope, Lens.thickness, Lens.n, z_back)

            #Adding Rays 
            Total_Ray = np.concatenate((ray_lens,ray_air))
            print("total ray shape:", Total_Ray.shape)
            print("start:", Total_Ray[0])
            print("end:", Total_Ray[-1])



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
    
    def new_plot(self):
        fig, ray_tracing = plt.subplots()
        ray_tracing.set(xlim = (min(self.z_optaxis)-1, max(self.z_optaxis)),ylim = (min(self.y)-6,max(self.y)+6))
        for i in range(0,len(self.y)):
            ray_tracing.plot(self.z_optaxis, self.raymatrix[i], 'r') #Rays
        
        plt.show()
    
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

#Lens Setup

""" 
Currently trying to get this class to take the output 
of the start class.  

"""

class Lens:
    pass

class plano_convex(Lens):
    def __init__(self, n, radius, thickness,dist = 5.0):
        self.n = n
        self.radius = radius
        self.thickness = thickness
        self.dist = dist
    
    def Current(self):
        print("This is the information Lens:")
        print("n:",self.n)
        print("radius:",  self.radius)
        print("thickness:", self.thickness)
        print("distance to next:", self.dist)
