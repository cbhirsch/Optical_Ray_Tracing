import exactraytrace as raytrace

#Initialize Lens
Lens1 = raytrace.plano_convex(1.5168, 20, 2,dist = 20)
Lens2 = raytrace.plano_convex(2.635, 30, 2,dist = 20)

#Run the Ray Tracing
example1 = raytrace.Product_Matrix()
example1.start(5, 11, 0.01,2, dist = 2)
#example1.Add_Lens(Lens1)
#example1.Current()
example1.New_Add_Lens(Lens1)
example1.new_plot()
#example1.Matrix_state()
#example1.plot()
# example1.spherical_aberation()