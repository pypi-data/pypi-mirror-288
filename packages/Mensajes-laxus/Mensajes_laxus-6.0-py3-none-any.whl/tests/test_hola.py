import unittest
import numpy as np
from mensajes.bienvenida.saludos import generate_array

class PruebasHola(unittest.TestCase):
    def test_generar_array(self):
        np.testing.assert_equal([0, 1, 2, 3, 4, 5], generate_array(6))

