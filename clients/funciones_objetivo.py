import math

def rastrigin(x):
    A = 10
    return A * len(x) + sum([(xi**2 - A * math.cos(2 * math.pi * xi)) for xi in x])
