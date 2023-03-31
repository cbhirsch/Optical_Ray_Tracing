import unittest
from vsnell import Vec_Refraction
import numpy as np

class TestCalc(unittest.TestCase):

    def test_Vec_Refraction(self):
        #Test 1
        theta1 = 15
        n1 = 1
        n2 = 1.5
        theta_comp1 = np.degrees(np.arcsin((n1*np.sin(np.radians(theta1))/n2)))
        theta_test1 = Vec_Refraction(theta1,n1,n2)
        self.assertEqual(theta_test1,theta_comp1)

        #Test 2
        theta2 = 15
        n1_2 = 1.5
        n2_2 = 1
        theta_comp2 = np.degrees(np.arcsin((n1_2*np.sin(np.radians(theta2))/n2_2)))
        theta_test2 = Vec_Refraction(theta2,n1_2,n2_2)
        self.assertEqual(theta_test2,theta_comp2)

        #Test 3
        theta3 = 0
        n1_3 = 1.5
        n2_3 = 1.2
        theta_comp3 = np.degrees(np.arcsin((n1_3*np.sin(np.radians(theta3))/n2_3)))
        theta_test3 = Vec_Refraction(theta3,n1_3,n2_3)
        self.assertEqual(theta_test3,theta_comp3)