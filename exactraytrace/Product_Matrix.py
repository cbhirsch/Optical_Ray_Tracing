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
        self.raymatrix = []
        self.x_axis = []

    def start(self, aperture, number_rays,y_start=0, dist=0, inf = True, dec = 1):
        
        #Setting up rays
        self.dy = (2*aperture+1)/number_rays
        self.y = np.linspace(aperture, -aperture, number_rays)
                
        #assigning data for slope of rays
        self.slope = np.zeros(number_rays, dtype= 'float', order= 'C')

        #Designating space for raymatrices
        self.raymatrix = np.zeros((len(self.y),2))
        self.x_axis = np.zeros((len(self.y),2))

        if inf == True: # If inf = True set up parallel rays
            for i in range(0, len(self.y)):
                #This term will determine rays current slope
                self.slope[i] = 0
                self.raymatrix[i] = self.y[i]*np.ones(2)
                self.x_axis[i] = [0, dist]

        elif inf == False: #If inf = False rays will become from a specific object distance
            for i in range(0, len(self.y)):
                #This term will determin rays current slope
                self.slope[i] = self.y[i]/dist
                self.raymatrix[i] = [0, self.y[i]]
                self.x_axis[i] = [0, dist]

        else:
            raise ValueError('Value must be either True or False')
            
        
    def Add_Lens(self, Lens):

        #Reading in lens data
        surfaces = Lens.surfaces
        distances = Lens.distances
        n_vals = Lens.n_vals
        diameter = Lens.diameter

        #initialize add raymatrices
        add_xmatrix = np.empty((len(self.y),0))
        add_ymatrix = np.empty((len(self.y),0))

        #Initialize matrices and designate data for add matrices
        for j in range(0, len(surfaces)):
            if surfaces[j] == float('inf'):
                add_xmatrix = np.hstack((add_xmatrix,np.zeros((len(self.y),2))))
                add_ymatrix = np.hstack((add_ymatrix,np.zeros((len(self.y),2))))
            else:
                add_xmatrix = np.hstack((add_xmatrix,np.zeros((len(self.y),2))))
                add_ymatrix = np.hstack((add_ymatrix,np.zeros((len(self.y),2))))


        #Ray Tracing Through Surfaces
        for i in range(0, len(self.y)):
            [x_vals, y_vals, slope] = refraction_Lens(surfaces, distances, n_vals, diameter, self.y[i],self.slope[i])
            add_xmatrix[i] = x_vals + self.x_axis[i,-1]
            add_ymatrix[i] = y_vals
            self.slope[i] = slope

        self.raymatrix = np.concatenate((self.raymatrix, add_ymatrix), axis = 1)
        self.x_axis = np.concatenate((self.x_axis, add_xmatrix), axis = 1)

        fig, ax = plt.subplots()
        for ray in range(0, len(self.y)):
            ax.plot(self.x_axis[ray], self.raymatrix[ray], 'r')

        ax.axis('equal')
        plt.show()

        #update y values
        for ray in range(0, len(self.y)):
            self.y[ray] = self.raymatrix[ray, -1]

        

        



        
        

        
