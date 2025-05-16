import math  # Usamos funciones matemáticas como coseno y pi

#        RASTRIGIN
# Función multimodal (muchos mínimos locales)
# Mínimo global en x = [0, 0, ..., 0] con valor f(x) = 0
# Muy utilizada para evaluar la robustez de algoritmos metaheurísticos
def rastrigin(x):
    A = 10
    # A*len(x) define la forma global, el resto añade ondulaciones
    return A * len(x) + sum([(xi**2 - A * math.cos(2 * math.pi * xi)) for xi in x])


#        SPHERE 
# Función simple y convexa: mínimo global en el origen
# Ideal para probar convergencia en problemas sencillos
def sphere(x):
    return sum(xi ** 2 for xi in x)  # f(x) = x₁² + x₂² + ... + xₙ²


#         ROSENBROCK 
# Función no convexa, mínimo global en [1, 1, ..., 1]
# Tiene un "valle" estrecho donde los algoritmos tienen que maniobrar
# Es un clásico en benchmarks de optimización
def rosenbrock(x):
    return sum(100 * (x[i+1] - x[i]**2)**2 + (1 - x[i])**2 for i in range(len(x) - 1))
