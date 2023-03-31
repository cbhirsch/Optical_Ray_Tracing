import numpy as np
import matplotlib.pyplot as plt
#from exactraytrace.Functions import safe_arange

def safe_arange(start, stop, step, dec):
    round_start = round(start, dec)
    round_stop = round(stop, dec)
    int_start = round(round_start/step)
    int_stop = round(round_stop/step)

    return step * np.arange(int_start, int_stop+1)

def line_intercept(y_int, Lens_Surf, dz):

    try:
        idx = np.argwhere(np.diff(np.sign(y_int - Lens_Surf))).flatten()
        var = idx[0]
    except:
        idx = np.argwhere(np.diff(np.sign(y_int - (-Lens_Surf)))).flatten()
        if len(idx) != 0:
            var = idx[0]
        else:
            raise ValueError("Intercept doesn't intersect Lens")


    SAG = (var*dz)
    y_prime = y_int[var]

    return SAG, y_prime 

#Refraction at a spherical surface
def pos_spherical_surface( y, radius, aperture,n,dz=.01,dec=2, prev_n = 1,slope = float(0)):

    #Gives the distance to the next plane
    total_SAG = radius - np.sqrt(radius**2 - (aperture/2)**2)

    #Sets up a ray to intersect lens surface
    x_int = safe_arange(0, total_SAG, dz, dec)
    y_int = slope*x_int + y

    #Sets up the lens for intersection check
    Lens_x = safe_arange(0, total_SAG, dz, dec)
    Lens_Surf = np.sqrt(radius**2 - (Lens_x - radius)**2)

    #Find the Intercept
    [SAG, y_prime] = line_intercept(y_int, Lens_Surf, dz)

    #X length from the y intercept to the center
    YTC_Length = radius - SAG

    #Solve for Alpha
    alpha = np.arctan(slope)
    gamma = np.arctan(y_prime/YTC_Length)

    #Angle of Incidence
    rad_i = alpha + gamma

    #Snell's Law
    rad_r = np.arcsin((prev_n*np.sin(rad_i))/n)

    #Calculate new Slope
    beta = (rad_r-gamma)
    slope2 = np.tan(beta)

    #Ray 1 Matrix
    x_Ray1 = x_int[:int(SAG/dz)]
    y_Ray1 = y_int[:int(SAG/dz)]

    #Ray 2 Matrix
    x_Ray2 = Lens_x[int((SAG/dz)+dz):]
    y_Ray2 = slope2*(x_Ray2 -x_Ray2[0]) + y_Ray1[-1]

    #Output Matrix
    x_out = np.concatenate((x_Ray1,x_Ray2))
    y_out = np.concatenate((y_Ray1,y_Ray2))


    return slope2, x_out, y_out , Lens_x, Lens_Surf

[slope, x, y, Lens_x, Lens_y] = pos_spherical_surface(1, 10, 8,1.5,slope = 0 )
fig, pos_sphere = plt.subplots()
pos_sphere.plot(x, y, 'b')
pos_sphere.plot(Lens_x, Lens_y,Lens_x, -Lens_y, color = 'r', linewidth = 3.0)
pos_sphere.set_xlim(0,20)
print(slope)
plt.show()