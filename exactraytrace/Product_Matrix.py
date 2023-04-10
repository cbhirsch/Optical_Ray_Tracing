import numpy as np
import matplotlib.pyplot as plt
from exactraytrace.refraction import *
from exactraytrace.Functions import safe_arange

class Product_Matrix:
    """ 
    Designates the objec that will be used to build the matrix for plotting
    the rays as they travel through the lens system.
    """
    def __init__(self):
        self.raymatrix = np.array([])
        self.x_axis = np.array([])
        self.phantom_rays = np.array([])

    def start(self, aperture, number_rays,y_start=0, dist=0, inf = True, dec = 1):
        
        #Setting up rays
        self.aperture = np.linspace(aperture, -aperture, number_rays)
                
        #assigning data for slope of rays
        self.phantom_rays = np.zeros((number_rays,2), dtype= 'float', order= 'C')

        #Designating space for raymatrices
        self.raymatrix = np.zeros((len(self.aperture),1))
        self.x_axis = np.zeros((len(self.aperture),1))

        if inf == True: # If inf = True set up parallel rays
            for i in range(0, len(self.aperture)):
                #This term will determine rays starting point
                self.raymatrix[i] = self.y[i]*np.ones(1)
                self.x_axis[i] = [0]

                #This is the phantom ray in the form ray = x*i_hat + y*j_hat
                self.phantom_rays = [1,0]

        elif inf == False: #If inf = False rays will become from a specific object distance
            for i in range(0, len(self.aperture)):
                #This term will determin rays current slope
                self.raymatrix[i] = np.array([0])
                self.x_axis[i] = np.array([0])

                #This is a phantom ray normalized around the x term
                self.phantom_rays[i] = np.array([(dist/dist),(self.aperture[i]/dist)])
        else:
            raise ValueError('Value must be either True or False')
            
        
    def Add_Lens(self, Lens):

        #Reading in lens data
        surfaces = Lens.surfaces
        distances = Lens.distances
        n_vals = Lens.n_vals
        diameter = Lens.diameter

        #Reading in start point
        start_pt = np.array([self.x_axis[-1], self.raymatrix[-1]])

        #initialize add raymatrices
        add_xmatrix = np.empty((len(self.aperture),0))
        add_ymatrix = np.empty((len(self.aperture),0))

        #Initialize matrices and designate data for add matrices
        add_xmatrix = np.hstack((add_xmatrix,np.zeros((len(self.aperture),len(surfaces)))))
        add_ymatrix = np.hstack((add_ymatrix,np.zeros((len(self.aperture),len(surfaces)))))


        #Ray Tracing Through Surfaces
        for i in range(0, len(self.aperture)):
            [x_vals, y_vals, self.phantom_rays[i]] = refraction_Lens(surfaces, distances, n_vals, diameter, start_pt,self.phantom_rays[i])
            add_xmatrix[i] = x_vals + self.x_axis[i,-1]
            add_ymatrix[i] = y_vals

        self.raymatrix = np.concatenate((self.raymatrix, add_ymatrix), axis = 1)
        self.x_axis = np.concatenate((self.x_axis, add_xmatrix), axis = 1)

        fig, ax = plt.subplots()
        for ray in range(0, len(self.aperture)):
            ax.plot(self.x_axis[ray], self.raymatrix[ray], 'r')

        ax.axis('equal')
        plt.show()

        #update y values
        for ray in range(0, len(self.aperture)):
            self.aperture[ray] = self.raymatrix[ray, -1]

        

        



        
        

        
