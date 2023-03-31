import exactraytrace as raytrace

#Initialize Lens
Lens1 = raytrace.plano_convex(1.5168, 20, 2,dist = 80)
Lens2 = raytrace.plano_convex(2.635, 30, 2,dist = 20)

#Run the Ray Tracing
example1 = raytrace.Product_Matrix()
example1.start(5, 11, 0.01,2, dist = 5)
example1.New_Add_Lens(Lens1)