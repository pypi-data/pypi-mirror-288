import numpy as np

def saludar():
    print("te saludo desde saludos.saludar()")

def prueba():
    print("test for new version")

def generate_array(numeros):
    return np.arange(numeros)

class Saludo:
    def __init__(self):
        print("Im the Saludo's constructor")

if __name__ == "__main__":
    print(generate_array(10))

