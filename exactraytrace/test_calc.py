import unittest
import Surfaces
import numpy as np

class TestCalc(unittest.TestCase):

    def test_safe_arange(self):
        basic_ray = Surfaces.safe_arange(0, 22.2, .1, 1)
        self.assertEqual(len(basic_ray), 223)
        self.assertEqual(basic_ray[0], float(0))
        self.assertEqual(round(basic_ray[-1], 1),float(22.2))

    def test_line_intercept(self):

        """ Positive Lens Surface """
        #Lens properties
        radius = 20
        aperture = 5
        dz = .01
        dec = 2

        #SAG calculation
        SAG = radius - np.sqrt(radius**2 - (aperture/2)**2)

        #Lens Surface
        Lens_x = Surfaces.safe_arange(0, SAG, dz, dec)
        Lens_Surf = np.sqrt(radius**2 - (Lens_x - radius)**2)

        #Intesecting ray properties
        slope = 0
        height = 4

        #Intersecting rays
        x_int = Surfaces.safe_arange(0, SAG, dz, dec)
        y_int = slope*x_int - height

        [x , y] = Surfaces.line_intercept(y_int, Lens_Surf, dz)

        #self.assertEqual(x_int, 4)
        self.assertEqual(y_int, 4)




    #def test_sphere_refract_ray(self):
        