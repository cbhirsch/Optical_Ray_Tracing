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


def ray_sphere_intersection(ray_origin, theta_i, sphere_center, sphere_radius):
    """ 
    Determine the intersection of a ray with a sphere  
    """
    #starting Conditions
    dist = 5
    [p1x, p1y] = ray_origin
    rad_i = np.radians(theta_i)
    slope_i = np.tan(rad_i)
    
    #Calculating pt2
    p2x = dist
    p2y = slope_i*p2x+ p1y

    #Circle Center
    [cx, cy] = sphere_center

    #Locating x and y variables
    [x1, y1] = [(p1x - cx),(p1y - cy)]
    [x2, y2] = [(p2x - cx),(p2y-cy)]

    #Change in x & y variables
    [dx, dy] = [(x2-x1),(y2-y1)]
    dr = (dx ** 2 + dy ** 2)** .5
    D = (x1 * y2) - (x2 * y1)
    discriminant = (sphere_radius**2) * (dr**2) - D**2

    if discriminant < 0: #No intersection between circle and line
        raise ValueError('Ray Doesnt intersect Lens')
    
    elif discriminant == 0: #Line is tangent
        raise ValueError('Ray is tangent to the sphere')

    else: # There may be 0, 1, or 2 intersections with the segment
        x1 = ((D*dy + sgn(dy)*dx * (discriminant**.5))/dr**2) + cx
        x2 = ((D*dy - sgn(dy)*dx * (discriminant**.5))/dr**2) + cx  
        y1 = ((-D*dx + abs(dy) * (discriminant**.5))/ dr**2) + cy
        y2 = ((-D*dx - abs(dy) * (discriminant**.5))/ dr**2) + cy
        return x1, y1, x2, y2 


def sgn(x):
    if x < 0:
        return -1
    else:
        return 1
    

intersection_points = ray_sphere_intersection([0, 0], 15, [10, 0], 5)

print("intersection_points:", intersection_points)

fig, ax = plt.subplots()
t = np.arange(-np.pi, np.pi, 0.1)
r = 5
pos = [10, 0]
x = r * np.cos(t) + pos[0]
y = r * np.sin(t) + pos[1]
ax.plot(x, y, 'b')

if intersection_points is not None:
    if len(intersection_points) == 2:
        ax.plot(intersection_points[0], intersection_points[1], 'ro')
    elif len(intersection_points) == 4:
        ax.plot(intersection_points[0], intersection_points[1], 'ro')
        ax.plot(intersection_points[2], intersection_points[3], 'ro')

plt.show()
