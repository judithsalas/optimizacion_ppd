import sys
import os

# Añadimos la ruta raíz del proyecto al path para poder importar 'clients' y 'shared'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Importamos Process de multiprocessing para ejecutar procesos en paralelo
from multiprocessing import Process

# Importamos la función principal del cliente genético
from clients.client_genetico import run_cliente

# Importamos la configuración (host y puerto del servidor)
from shared import config

# Número de clientes que queremos lanzar simultáneamente
NUM_CLIENTES = 5  # Puedes aumentar este número si quieres hacer más pruebas

# Punto de entrada del script
if __name__ == "__main__":
    procesos = []  # Lista para guardar las referencias a los procesos

    # Creamos y lanzamos múltiples procesos cliente
    for _ in range(NUM_CLIENTES):
        # Cada proceso ejecutará la función run_cliente con los parámetros del servidor
        p = Process(target=run_cliente, args=(config.host, config.port))
        p.start()             # Iniciamos el proceso
        procesos.append(p)    # Guardamos el proceso en la lista

    # Esperamos a que todos los procesos terminen antes de cerrar el script
    for p in procesos:
        p.join()
