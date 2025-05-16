import pickle    # Para serializar y deserializar objetos
import csv       # Para escribir en archivos CSV
import os        # Para verificar si un archivo ya existe

# Importamos los parámetros de configuración definidos en config.py
from shared import config


def preparar_parametros():
    """
    Devuelve un diccionario con los parámetros de configuración
    que serán enviados al cliente para iniciar la ejecución del algoritmo.
    """
    return {
        'funcion': config.funcion_objetivo,
        'dimension': config.dimension,
        'limites': config.limites,
        'iteraciones': config.iteraciones
    }


def serializar(objeto):
    """
    Convierte un objeto de Python a una secuencia de bytes usando pickle,
    para poder enviarlo por un socket.
    """
    return pickle.dumps(objeto)


def deserializar(datos):
    """
    Convierte una secuencia de bytes (recibida por socket)
    de nuevo a un objeto Python usando pickle.
    """
    return pickle.loads(datos)


def imprimir_resultado(addr, resultado):
    """
    Imprime en pantalla el resultado enviado por un cliente,
    incluyendo su dirección IP y los datos del algoritmo.
    """
    print(f"[RESULTADO] Cliente {addr}: {resultado}")


def guardar_en_csv(addr, resultado, archivo='resultados.csv'):
    """
    Guarda el resultado recibido de un cliente en un archivo CSV.

    Si el archivo no existe, escribe una cabecera con los nombres de los campos.
    Luego añade una fila con los datos del cliente y el resultado obtenido.
    """
    campos = ['cliente', 'algoritmo', 'mejor_valor', 'solucion', 'tiempo']
    existe = os.path.exists(archivo)

    # Abrimos el archivo en modo 'a' (añadir), sin sobrescribir
    with open(archivo, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=campos)

        # Escribimos la cabecera solo si el archivo es nuevo
        if not existe:
            writer.writeheader()

        # Creamos la fila con los datos del cliente y resultado
        fila = {
            'cliente': str(addr),
            'algoritmo': resultado.get('algoritmo'),
            'mejor_valor': resultado.get('mejor_valor'),
            'solucion': resultado.get('solucion'),
            'tiempo': resultado.get('tiempo')
        }

        # Escribimos la fila en el CSV
        writer.writerow(fila)
