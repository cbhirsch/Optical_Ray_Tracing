import exactraytrace as raytrace

#Initialize Lens1
surfaces1 = [3.5,3.5]
distances1 = [1.5,5]
n_val1 = [1.5]
Lens1 = raytrace.spherical_Lens(surfaces1, distances1, n_val1,diameter = 3)

#Initialize Lens2
surfaces2 = [float('inf'),float('inf')]
distances2 = [4,3]
n_val2 = [1.5]
Lens2 = raytrace.spherical_Lens(surfaces2, distances2, n_val2,diameter = 3)

#Run the Ray Tracing
example1 = raytrace.Product_Matrix()
example1.start(5, 11, dist = 2, inf= False )
example1.Add_Lens(Lens2)
example1.print_solution()