import numpy as np
import matplotlib.pyplot as plt
from exactraytrace.Functions import circle_eq
from scipy.spatial.distance import cdist

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
            [n_start, slope_prev, x1, x2, y1, y2] = refract_Pos(surfaces[i], y_prev, slope_prev, n_start, n_surf, distances[i], diameter)
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

        elif surfaces[i] < 0:
            [n_start, slope_prev, x1, x2, x3, y1, y2, y3] = refract_Neg(surfaces[i], y_prev, slope_prev, n_start, n_surf, distances[i], diameter)
        else:
            raise ValueError('Entry must be a non zero float or integer value') 
    
    return x_vals, y_vals, slope_prev
        
def refract_Pos(radius, y_start, slope_start, n_start, n_surf, distance, diameter):

    #Locating the center of the circle
    cy = 0
    cx = np.sqrt(radius**2 - (diameter/2)**2)
    sphere_center = [cx,cy]

    #Origin of Ray
    ray_origin = [0, y_start]

    #convert slope to vector
    array_start = np.array([1,slope_start])
    vector_start = array_start/np.linalg.norm(array_start)

    #Intersect previous ray with circle
    [ x1_int, y1_int, x2_int, y2_int] = ray_sphere_intersection(ray_origin, vector_start, sphere_center, radius, distance)

    #output pts
    pt1_int = [x1_int, y1_int]
    pt2_int = [x2_int, y2_int]

    #Check which point to use for refraction
    if pt1_int[0] < pt2_int[0]:
        pt_ref = pt1_int
    else:
        pt_ref = pt2_int

    #Calculating the normal vector
    y_norm = pt2_int[1]
    x_norm = np.sqrt(radius**2 - y_norm**2)
    vec_norm = [-x_norm,y_norm]
    N_hat = vec_norm/np.linalg.norm(vec_norm)

    #Defining the Input Ray
    rad_i = np.arctan(slope_start)
    I_hat = np.array([np.cos(rad_i),np.sin(rad_i)])


    #Calculating Refraction using snell's law
    T_hat = Vec_Refraction(I_hat, N_hat, n_start, n_surf)

    #converting T_hat to slope
    slope_new = T_hat[1]/T_hat[0]

    #Solving for x & y values
    [x1, x2] = np.array([pt_ref[0],pt_ref[0]+ distance])
    y1 = pt_ref[1]
    y2 = slope_new*(x2-x1) + y1

    return n_surf, slope_new, x1, x2, y1, y2

def refract_plane(y_start, slope_start, n_start, n_surf, distance):

    #Defining the Input Ray
    rad_i = np.arctan(slope_start)
    I_hat = np.array([np.cos(rad_i),np.sin(rad_i)])

    #Normal Vector for a plane always will be (-1, 0)
    N_hat = np.array([-1,0])

    #calling refraction function
    T_hat = vector_refraction(I_hat, N_hat, n_start, n_surf)

    #converting T_hat to slope
    slope_new = T_hat[1]/T_hat[0]

    #Solving for x & y values
    [x1, x2] = np.array([0,distance])
    y1 = y_start
    y2 = slope_new*x2 + y1

    return n_surf, slope_new, x1, x2, y1, y2 

def refract_Neg(radius, y_start, slope_start, n_start, n_surf, distance, diameter):
    pass

def ray_sphere_intersection(p, d, c, r):
    # Calculate intersection of ray with sphere surface
    A = np.dot(d, d)
    B = 2 * np.dot(d, p - c)
    C = np.dot(p - c, p - c) - r**2
    discr = B**2 - 4*A*C

    # Check if ray intersects the sphere
    if discr < 0:
        raise ValueError('Ray doesnt intersect the lens')

    # Calculate intersection point(s)
    t1 = (-B + np.sqrt(discr)) / (2*A)
    t2 = (-B - np.sqrt(discr)) / (2*A)
    p1 = p + t1*d
    p2 = p + t2*d

    # Return closest intersection point
    dists = cdist([p1, p2], [p])
    return p1 if dists[0] < dists[1] else p2


def vector_refraction(I_hat, N_hat, n_start, n_surf):

    #Vector form of snell's law
    r = n_start/n_surf
    c1 = abs(np.dot(N_hat,I_hat))
    c2 = np.sqrt(1-r**2*(1-c1**2))
    T_hat = r*I_hat + (r*c1 - c2)*N_hat

    return T_hat
