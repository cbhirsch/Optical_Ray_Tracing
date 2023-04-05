import numpy as np

class Lens:
    pass

class spherical_Lens(Lens):
    def __init__(self,surfaces, distances, n_vals, diameter):

        self.diameter = diameter
        
        if len(surfaces) < 2:
            raise ValueError('must be more that one surface') 
        else:
            self.surfaces = surfaces

        if len(surfaces) != len(distances):
            raise ValueError('distances must match surfaces')
        else: 
            self.distances = distances
        
        if len(surfaces) != len(n_vals)+1:
            raise ValueError('Must be one less n value than surfaces')
        else:
            self.n_vals = n_vals
            
class aspherical_Lens(Lens):
    pass
        
