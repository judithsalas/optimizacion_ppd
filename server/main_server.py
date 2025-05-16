# Importamos asyncio para programar de forma asíncrona
import asyncio
import sys
import os

# AÑADIMOS la ruta raíz del proyecto manualmente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importamos funciones auxiliares del servidor desde server_utils
from server.server_utils import (
    preparar_parametros,   # Prepara el diccionario con los parámetros para los clientes
    serializar,            # Convierte un objeto a bytes usando pickle
    deserializar,          # Convierte bytes de vuelta a un objeto Python
    imprimir_resultado,    # Muestra por pantalla el resultado recibido
    guardar_en_csv         # Guarda el resultado en un archivo CSV
)

# Importamos la configuración común (parámetros del problema y del socket)
from shared import config


# Función asíncrona que se ejecuta por cada cliente que se conecta
async def manejar_cliente(reader, writer):
    # Obtenemos la dirección del cliente conectado
    addr = writer.get_extra_info('peername')
    print(f"[SERVER] Conectado a {addr}")

    # Enviamos los parámetros del problema al cliente
    parametros = preparar_parametros()        # Crea el diccionario de parámetros
    writer.write(serializar(parametros))      # Serializamos y enviamos por el socket
    await writer.drain()                      # Esperamos a que el buffer se vacíe

    # Recibimos el resultado del cliente
    datos = await reader.read(4096)           # Leemos hasta 4096 bytes
    resultado = deserializar(datos)           # Convertimos de bytes a objeto Python

    # Mostramos y guardamos el resultado
    imprimir_resultado(addr, resultado)       # Muestra el resultado por consola
    guardar_en_csv(addr, resultado)           # Lo guarda en un CSV

    # Cerramos la conexión con el cliente
    writer.close()
    await writer.wait_closed()


# Función principal asíncrona que inicia el servidor
async def main():
    # Creamos el servidor que escuchará en la IP y puerto configurados
    server = await asyncio.start_server(
        manejar_cliente,         # Función que se ejecuta con cada cliente
        config.host,             # Dirección IP (localhost)
        config.port              # Puerto de conexión (ej. 5000)
    )

    # Mostramos por pantalla la dirección del servidor
    addr = server.sockets[0].getsockname()
    print(f"[SERVER] Servidor corriendo en {addr} (modo async)")

    # El servidor queda activo indefinidamente, aceptando nuevos clientes
    async with server:
        await server.serve_forever()


# Punto de entrada del programa: se lanza el bucle de eventos
if __name__ == "__main__":
    asyncio.run(main())  # Inicia el servidor usando asyncio
