import socket
import pickle
import random
import time
from clients.funciones_objetivo import rastrigin

HOST = 'localhost'
PORT = 5000

POP_SIZE = 50
CROSS_RATE = 0.7
MUTATION_RATE = 0.01

def init_population(dimension, limites):
    return [[random.uniform(*limites) for _ in range(dimension)] for _ in range(POP_SIZE)]

def fitness(individuo):
    return -rastrigin(individuo)

def crossover(p1, p2):
    return [p1[i] if random.random() < 0.5 else p2[i] for i in range(len(p1))]

def mutate(individuo, limites):
    return [x + random.uniform(-0.1, 0.1) if random.random() < MUTATION_RATE else x for x in individuo]

def evolucionar(poblacion, limites):
    poblacion.sort(key=fitness, reverse=True)
    nueva_pob = poblacion[:2]
    while len(nueva_pob) < POP_SIZE:
        p1, p2 = random.choices(poblacion[:25], k=2)
        hijo = mutate(crossover(p1, p2), limites)
        nueva_pob.append(hijo)
    return nueva_pob

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    parametros = pickle.loads(s.recv(4096))
    dimension = parametros['dimension']
    limites = parametros['limites']
    iteraciones = parametros['iteraciones']

    poblacion = init_population(dimension, limites)
    mejor = min(poblacion, key=rastrigin)
    start = time.time()

    for _ in range(iteraciones):
        poblacion = evolucionar(poblacion, limites)
        candidato = min(poblacion, key=rastrigin)
        if rastrigin(candidato) < rastrigin(mejor):
            mejor = candidato

    duracion = time.time() - start
    resultado = {
        'algoritmo': 'Genético',
        'mejor_valor': rastrigin(mejor),
        'solucion': mejor,
        'tiempo': duracion
    }
    s.sendall(pickle.dumps(resultado))
    print("[CLIENTE GENÉTICO] Resultado enviado.")
