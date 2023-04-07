import numpy as np
import matplotlib.pyplot as plt

# define lens parameters
surface_radii = [3.5, -3.5]
distances = [1.5, 5]
n_vals = [1.5, 1]

# define focus point
focus_point = np.array([0, -10])

# define rays
num_rays = 5
ray_angles = np.linspace(-np.pi/6, np.pi/6, num_rays)
ray_directions = np.stack((np.sin(ray_angles), np.cos(ray_angles)), axis=-1)

# calculate ray intersections
ray_origins = np.tile(focus_point, (num_rays, 1))
ray_intersections = []
for r in range(num_rays):
    for s in range(len(surface_radii)):

        if s+1 < len(n_vals):
            n1, n2 = n_vals[s], n_vals[s+1]
        else:
            n1, n2 = n_vals[s], 1
        
        R = surface_radii[s]
        d = distances[s]
        origin, direction = ray_origins[r], ray_directions[r]
        center = np.array([origin[0], origin[1]+R])
        if R == 0:  # flat surface
            intersection = np.array([origin[0], origin[1]+n1*d])
        else:
            C = center - np.array([0, R])
            P = origin - C
            a = np.dot(direction, direction)
            b = 2*np.dot(direction, P)
            c = np.dot(P, P) - R**2
            disc = b**2 - 4*a*c
            if disc < 0:
                raise ValueError("No intersection")
            else:
                t1 = (-b + np.sqrt(disc))/(2*a)
                t2 = (-b - np.sqrt(disc))/(2*a)
                t = np.minimum(t1, t2)
                intersection = origin + t*direction
        ray_intersections.append(intersection)
ray_intersections = np.reshape(ray_intersections, (num_rays, len(surface_radii), 2))

# plot rays and intersections
fig, ax = plt.subplots()
for r in range(num_rays):
    ax.plot(ray_origins[r, 0], ray_origins[r, 1], 'ko')
    ax.plot(ray_intersections[r, :, 0], ray_intersections[r, :, 1], 'bo-')
plt.show()