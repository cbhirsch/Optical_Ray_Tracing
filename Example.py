import lib.All_in_one as raytrace

#Initialize Lens
Lens1 = raytrace.plano_convex(1.5168, 20, 2)
Lens2 = raytrace.plano_convex(2.635, 30, 2)

#Run the Ray Tracing
raytrace.example1 = raytrace.Product_Matrix()
raytrace.example1.start(5, 11, 0.01,2,)
raytrace.example1.Add_Lens(Lens1)
raytrace.example1.Current()
raytrace.example1.Matrix_state()
raytrace.example1.plot()
raytrace.example1.spherical_aberation()