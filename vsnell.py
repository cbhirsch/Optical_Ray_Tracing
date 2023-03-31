import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

""" 
This is an example of the vector form of snell's law.
The equation will be utilized in a larger program.
"""


def Vec_Refraction(theta_i, n1, n2):
    #Convert to radians
    rad_i = np.radians(theta_i)

    #Converting to vector form
    I_hat = np.array([np.cos(rad_i),np.sin(rad_i)])

    #Normal Vector
    N_hat = np.array([-1,0])

    #Calcs
    r = n1/n2
    c1 = abs(np.dot(N_hat,I_hat))
    c2 = np.sqrt(1 - r**2*(1-c1**2))
    T_hat = r*I_hat + (r*c1 - c2)*N_hat

    #Output Theta
    theta_new = np.degrees(np.arctan(T_hat[1]/T_hat[0]))

    return theta_new

print(Vec_Refraction(15,1, 1.5))
