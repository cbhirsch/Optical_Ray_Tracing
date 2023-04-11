import numpy as np
import matplotlib.pyplot as plt
from exactraytrace.refraction import *

class Product_Matrix:
    """ 
    Designates the objec that will be used to build the matrix for plotting
    the rays as they travel through the lens system.
    """
    def __init__(self):
        self.raymatrix = np.array([])
        self.x_axis = np.array([])
        self.phantom_rays = np.array([])
        self.phantom_raypoint = np.array([])

    def start(self, aperture, number_rays,y_start=0, dist=0, inf = True):

        #Reading in number of rays

        self.number_rays = number_rays
        
        #Setting up rays
        start_rayheight = np.linspace(aperture, -aperture, number_rays)
                
        #assigning data for phantom ray & Ray point
        self.phantom_rays = np.zeros((number_rays,2), dtype= 'float', order= 'C')
        self.phantom_raypoint = np.zeros((number_rays,2), dtype= 'float', order= 'C')

        #Designating space for raymatrices
        self.raymatrix = np.zeros((number_rays,1))
        self.x_axis = np.zeros((number_rays,1))

        if inf == True: # If inf = True set up parallel rays
            for i in range(0, number_rays):
                #This term will determine rays starting point
                self.raymatrix[i] = start_rayheight[i]*np.ones(1)
                self.x_axis[i] = [0]

                #This is the phantom ray in the form ray = x*i_hat + y*j_hat & Phantom Ray point
                self.phantom_rays[i] = [1,0]
                self.phantom_raypoint[i] = np.array([0,self.raymatrix[i]]) + dist * self.phantom_rays[i]

        elif inf == False: #If inf = False rays will become from a specific object distance
            for i in range(0, number_rays):
                #This term will determin rays current slope
                self.raymatrix[i] = np.array([0])
                self.x_axis[i] = np.array([0])

                 #This is the phantom ray in the form ray = x*i_hat + y*j_hat normalized arount x & Phantom Ray point
                self.phantom_rays[i] = np.array([(dist/dist),(start_rayheight[i]/dist)])
                self.phantom_raypoint[i] = np.array([0,0]) + dist * self.phantom_rays[i]
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
        add_xmatrix = np.empty((self.number_rays,0))
        add_ymatrix = np.empty((self.number_rays,0))

        #Initialize matrices and designate data for add matrices
        add_xmatrix = np.hstack((add_xmatrix,np.zeros((self.number_rays,len(surfaces)))))
        add_ymatrix = np.hstack((add_ymatrix,np.zeros((self.number_rays,len(surfaces)))))


        #Ray Tracing Through Surfaces
        for i in range(0, self.number_rays):
            [x_vals, y_vals, self.phantom_rays[i]] = refraction_Lens(surfaces, distances, n_vals, diameter, start_pt,self.phantom_rays[i])
            add_xmatrix[i] = x_vals + self.x_axis[i,-1]
            add_ymatrix[i] = y_vals
            self.phantom_raypoint[i] = np.array([x_vals[-1],y_vals[-1]]) + distances[-1] * self.phantom_rays[i]

        self.raymatrix = np.concatenate((self.raymatrix, add_ymatrix), axis = 1)
        self.x_axis = np.concatenate((self.x_axis, add_xmatrix), axis = 1)


    def print_solution(self):

        #Add Phantom Ray points to solution
        phantom_y = self.phantom_raypoint[:, 1].reshape((11,1))
        phantom_x = self.phantom_raypoint[:,0].reshape((11,1))
        self.raymatrix = np.concatenate((self.raymatrix, phantom_y), axis = 1)
        self.x_axis = np.concatenate((self.x_axis, phantom_x), axis = 1)

        fig, ax = plt.subplots()
        for ray in range(0, self.number_rays):
            ax.plot(self.x_axis[ray], self.raymatrix[ray], 'r')

        ax.axis('equal')
        plt.show()  


        

        



        
        

        
