import numpy as np

def refraction_Lens(surfaces, distances, n_vals, diameter, y_start, slope_start):

    #Initializing starting values
    n_start = 1.0
    y_prev = y_start
    slope_prev = slope_start
    x_vals = []
    y_vals = []

    #Running through each plane
    for i in range(0, len(surfaces)):
        try:
            n_surf = n_vals[i]
        except:
            n_surf = 1.0

        if surfaces[i] == float('inf'):
            [n_start,slope_prev, x1, x2, y1, y2] = refract_plane(y_prev, slope_prev, n_start, n_surf, distances[i])
            y_prev = y2

            #Create Output Arrays to add to the x_vals & y_vals
            x_out = np.array([x1, x2])
            y_out = np.array([y1, y2])

            #Add the output arrays to x_val & y_vall arrays
            if len(x_vals) > 0:
                #shifting x_out array to the end of x_vals axis
                x_out = x_vals[-1]+x_out

                #combining the arrays
                x_vals = np.concatenate([x_vals ,x_out])
                y_vals = np.concatenate([y_vals, y_out])
            else:
                x_vals = x_out
                y_vals = y_out

        elif surfaces[i] > 0:
            [n_start, slope_prev, x1, x2, x3, y1, y2, y3] = refract_Pos(surfaces[i], y_prev, slope_prev, n_start, n_surf, distances[i], diameter)
        elif surfaces[i] < 0:
            [n_start, slope_prev, x1, x2, x3, y1, y2, y3] = refract_Neg(surfaces[i], y_prev, slope_prev, n_start, n_surf, distances[i], diameter)
        else:
            raise ValueError('Entry must be a non zero float or integer value') 
    
    return x_vals, y_vals, slope_prev
        
def refract_Pos(radius, y_start, slope_start, n_start, n_surf, distance, diameter):
    pass

def refract_Neg(radius, y_start, slope_start, n_start, n_surf, distance, diameter):
    pass

def refract_plane(y_start, slope_start, n_start, n_surf, distance):

    #Defining the Input Ray
    rad_i = np.arctan(slope_start)
    I_hat = np.array([np.cos(rad_i),np.sin(rad_i)])

    #Normal Vector for a plane always will be (-1, 0)
    N_hat = np.array([-1,0])

    #calling refraction function
    T_hat = Vec_Refraction(I_hat, N_hat, n_start, n_surf)

    #converting T_hat to slope
    slope_new = T_hat[1]/T_hat[0]

    #Solving for x & y values
    [x1, x2] = np.array([0,distance])
    y1 = y_start
    y2 = slope_new*x2 + y1

    return n_surf, slope_new, x1, x2, y1, y2 
    


def Vec_Refraction(I_hat, N_hat, n_start, n_surf):

    #Vector form of snell's law
    r = n_start/n_surf
    c1 = abs(np.dot(N_hat,I_hat))
    c2 = np.sqrt(1-r**2*(1-c1**2))
    T_hat = r*I_hat + (r*c1 - c2)*N_hat

    return T_hat