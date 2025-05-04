import socket
import pickle

HOST = 'localhost'
PORT = 5000

funcion_objetivo = 'rastrigin'
dimension = 5
limites = (-5.12, 5.12)
iteraciones = 1000

parametros = {
    'funcion': funcion_objetivo,
    'dimension': dimension,
    'limites': limites,
    'iteraciones': iteraciones
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("[SERVER] Esperando conexiones de clientes...")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"[SERVER] Conectado a {addr}")
            conn.sendall(pickle.dumps(parametros))
            resultado = pickle.loads(conn.recv(4096))
            print(f"[RESULTADO] Cliente {addr}: {resultado}")
