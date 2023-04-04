import numpy as np
import matplotlib.pyplot as plt

class Product_Matrix:
    """ 
    Designates the objec that will be used to build the matrix for plotting
    the rays as they travel through the lens system.
    """
    def __init__(self):
        self.raymatrix = []
        self.x_axis = []

    def start(self, aperture, number_rays,y_start=0, dist=0, inf = True):
        
        #Setting up rays
        self.dy = (2*aperture + 1)/number_rays
        self.y = np.arange(aperture, -aperture-1, -self.dy)
        
        #Initializing initial x_axis
        self.x_axis = [0, dist]
                
        #assigning data for slope of rays
        self.slope = np.zeros(number_rays, dtype= 'float', order= 'C')

        #Designating space for raymatrix
        self.raymatrix = np.zeros((len(self.y),2))

        if inf == True: # If inf = True set up parallel rays
            for i in range(0, len(self.y)):
                #This term will determine rays current slope
                self.slope[i] = 0
                self.raymatrix[i] = self.y[i]*np.ones(2)

        elif inf == False: #If inf = False rays will become from a specific object distance
            for i in range(0, len(self.y)):
                #This term will determin rays current slope
                self.slope[i] = self.y[i]/dist
                self.raymatrix[i] = [0, self.y[i]]

        else:
            raise ValueError('Value must be either True or False')
        

        
