import numpy as np
import matplotlib.pyplot as plt

#Useful Function
def safe_arange(start, stop, step, dec):
    round_start = round(start, dec)
    round_stop = round(stop, dec)
    int_start = round(round_start/step)
    int_stop = round(round_stop/step)


    return step * np.arange(int_start, int_stop+1)

#Starting Conditions
class start:
    def __init__(self,aperture, number_rays, dz, dec):
        self.aperture = aperture
        self.number_rays = number_rays
        self.dz = dz
        self.dec = dec
        self.dy = (2*aperture +1)/number_rays
        self.y = safe_arange(-aperture, aperture, self.dy, dec)

#Lens Setup
class Lens:
    def plano_convex(self,n, radius, thickness, d_next):
       self.n = n
       self.radius = radius
       self.thickness = thickness
       self.d_next = d_next 