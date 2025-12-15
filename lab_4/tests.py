# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 15:40:07 2018

@author: Christian Bender
@license: MIT-license

This file contains the test-suite for the linear algebra library.
"""


import unittest
from lib import *


class Test(unittest.TestCase):
    def test_component_vector(self):
        x = Vector([1, 2, 3])
        self.assertEqual(x.component(0), 1)
        self.assertEqual(x.component(2), 3)

    def test__str__vector(self):
        x = Vector([0, 0, 0, 0, 0, 1])
        self.assertEqual(str(x), "(0, 0, 0, 0, 0, 1)")

    def test__len__vector(self):
        x = Vector([1, 2, 3, 4])
        self.assertEqual(len(x), 4)

    def test_euclidean_length(self):
        x = Vector([1, 2])
        self.assertAlmostEqual(x.euclidean_length(), 2.236, 3)

    def test__add__vector(self):
        x = Vector([1, 2, 3])
        y = Vector([1, 1, 1])
        self.assertEqual((x + y).component(0), 2)
        self.assertEqual((x + y).component(1), 3)
        self.assertEqual((x + y).component(2), 4)

    def test__sub__vector(self):
        x = Vector([1, 2, 3])
        y = Vector([1, 1, 1])
        self.assertEqual((x - y).component(0), 0)
        self.assertEqual((x - y).component(1), 1)
        self.assertEqual((x - y).component(2), 2)

    def test__mul__vector(self):
        x = Vector([1, 2, 3])
        a = Vector([2, -1, 4])
        b = Vector([1, -2, -1])
        self.assertEqual(str(x * 3.0), "(3.0, 6.0, 9.0)")
        self.assertEqual((a * b), 0)

    def test_zero_vector(self):
        self.assertTrue(str(zero_vector(10)).count("0") == 10)

    def test_unit_basis_vector(self):
        self.assertEqual(str(unit_basis_vector(3, 1)), "(0, 1, 0)")

    def test_axpy(self):
        x = Vector([1, 2, 3])
        y = Vector([1, 0, 1])
        self.assertEqual(str(axpy(2, x, y)), "(3, 4, 7)")

    def test_copy(self):
        x = Vector([1, 0, 0, 0, 0, 0])
        y = x.copy()
        self.assertEqual(str(x), str(y))

    def test_change_component_vector(self):
        x = Vector([1, 0, 0])
        x.change_component(0, 0)
        x.change_component(1, 1)
        self.assertEqual(str(x), "(0, 1, 0)")

    def test__str__matrix(self):
        a = Matrix([[1, 2, 3], [2, 4, 5], [6, 7, 8]], 3, 3)
        self.assertEqual(
            "|1, 2, 3|\n"
            "|2, 4, 5|\n"
            "|6, 7, 8|",
            str(a)
        )

    def test__mul__matrix(self):
        a = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 3)
        x = Vector([1, 2, 3])
        self.assertEqual("(14, 32, 50)", str(a * x))
        self.assertEqual(
            "|2, 4, 6|\n"
            "|8, 10, 12|\n"
            "|14, 16, 18|",
            str(a * 2)
        )

    def test_change_component_matrix(self):
        a = Matrix([[1, 2, 3], [2, 4, 5], [6, 7, 8]], 3, 3)
        a.change_component(0, 2, 5)
        self.assertEqual(
            "|1, 2, 5|\n"
            "|2, 4, 5|\n"
            "|6, 7, 8|",
            str(a)
        )

    def test_component_matrix(self):
        a = Matrix([[1, 2, 3], [2, 4, 5], [6, 7, 8]], 3, 3)
        self.assertEqual(7, a.component(2, 1), 0.01)

    def test__add__matrix(self):
        a = Matrix([[1, 2, 3], [2, 4, 5], [6, 7, 8]], 3, 3)
        b = Matrix([[1, 2, 7], [2, 4, 5], [6, 7, 10]], 3, 3)
        self.assertEqual(
            "|2, 4, 10|\n"
            "|4, 8, 10|\n"
            "|12, 14, 18|",
            str(a + b)
        )

    def test__sub__matrix(self):
        a = Matrix([[1, 2, 3], [2, 4, 5], [6, 7, 8]], 3, 3)
        b = Matrix([[1, 2, 7], [2, 4, 5], [6, 7, 10]], 3, 3)
        self.assertEqual(
            "|0, 0, -4|\n"
            "|0, 0, 0|\n"
            "|0, 0, -2|",
            str(a - b)
        )

    def test_square_zero_matrix(self):
        self.assertEqual(
            "|0, 0, 0, 0, 0|\n"
            "|0, 0, 0, 0, 0|\n"
            "|0, 0, 0, 0, 0|\n"
            "|0, 0, 0, 0, 0|\n"
            "|0, 0, 0, 0, 0|",
            str(square_zero_matrix(5))
        )


if __name__ == "__main__":
    unittest.main()
