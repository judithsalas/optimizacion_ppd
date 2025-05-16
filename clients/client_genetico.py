# Importamos módulos necesarios
import socket       # Para conectarse al servidor mediante sockets TCP
import pickle       # Para serializar/deserializar los datos enviados y recibidos
import random       # Para operaciones aleatorias (mutación, cruce, etc.)
import time         # Para medir el tiempo de ejecución
from clients import funciones_objetivo  # Importamos las funciones objetivo definidas

# Parámetros del algoritmo genético
POP_SIZE = 50         # Tamaño de la población
CROSS_RATE = 0.7      # Probabilidad de cruce
MUTATION_RATE = 0.01  # Probabilidad de mutación por gen

# Inicializa la población aleatoria dentro de los límites indicados
def init_population(dimension, limites):
    return [[random.uniform(*limites) for _ in range(dimension)] for _ in range(POP_SIZE)]

# Calcula la aptitud (fitness) de un individuo, negando la función objetivo para minimizar
def fitness(individuo, funcion):
    return -funcion(individuo)

# Realiza cruce entre dos padres (crossover de un punto aleatorio por gen)
def crossover(p1, p2):
    return [p1[i] if random.random() < 0.5 else p2[i] for i in range(len(p1))]

# Aplica mutación a cada gen con cierta probabilidad, añadiendo una pequeña perturbación
def mutate(individuo, limites):
    return [x + random.uniform(-0.1, 0.1) if random.random() < MUTATION_RATE else x for x in individuo]

# Evoluciona la población actual hacia una nueva generación
def evolucionar(poblacion, limites, funcion):
    # Ordenamos la población por su fitness (mejor primero)
    poblacion.sort(key=lambda ind: fitness(ind, funcion), reverse=True)
    
    # Selección elitista: mantenemos los 2 mejores individuos
    nueva_pob = poblacion[:2]
    
    # Llenamos el resto de la nueva población con hijos cruzados y mutados
    while len(nueva_pob) < POP_SIZE:
        p1, p2 = random.choices(poblacion[:25], k=2)  # Selección de padres entre los mejores 25
        hijo = mutate(crossover(p1, p2), limites)
        nueva_pob.append(hijo)
    
    return nueva_pob

# Función principal del cliente genético
def run_cliente(host, port):
    # Creamos un socket TCP y nos conectamos al servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))  # Conexión al servidor

        # Recibimos los parámetros del problema desde el servidor
        parametros = pickle.loads(s.recv(4096))
        dimension = parametros['dimension']
        limites = parametros['limites']
        iteraciones = parametros['iteraciones']
        nombre_funcion = parametros['funcion']

        # Obtenemos la función objetivo a partir del nombre recibido
        funcion = getattr(funciones_objetivo, nombre_funcion)

        # Inicializamos la población y buscamos el mejor individuo inicial
        poblacion = init_population(dimension, limites)
        mejor = min(poblacion, key=funcion)
        start = time.time()  # Tiempo de inicio de la optimización

        # Bucle de evolución
        for _ in range(iteraciones):
            poblacion = evolucionar(poblacion, limites, funcion)
            candidato = min(poblacion, key=funcion)
            if funcion(candidato) < funcion(mejor):
                mejor = candidato  # Actualizamos el mejor si encontramos uno nuevo

        duracion = time.time() - start  # Tiempo total de ejecución

        # Preparamos el resultado final con los datos del mejor individuo encontrado
        resultado = {
            'algoritmo': 'Genético',
            'mejor_valor': funcion(mejor),
            'solucion': mejor,
            'tiempo': duracion
        }

        # Enviamos el resultado de vuelta al servidor
        s.sendall(pickle.dumps(resultado))
        print(f"[CLIENTE GENÉTICO] Resultado enviado: {resultado}")
