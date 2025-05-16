# Proyecto de Optimización Distribuida con Algoritmo Genético

Este proyecto implementa un sistema distribuido para resolver problemas de optimización utilizando un algoritmo genético. Su desarrollo está basado en los principales conceptos de la asignatura de Programación Paralela y Distribuida.

---

## Arquitectura y Tecnologías

El sistema sigue una arquitectura **cliente-servidor** de tipo **Maestro-Trabajadores**:

* **Servidor (maestro)**: implementado de forma **asíncrona** usando `asyncio`, se encarga de enviar la configuración del problema a cada cliente y de recibir los resultados de cada uno.
* **Clientes (trabajadores)**: implementados como **procesos independientes** usando `multiprocessing`. Cada cliente ejecuta un **algoritmo genético** sobre la función objetivo recibida.

La comunicación se realiza mediante **sockets TCP** utilizando `pickle` para serializar y deserializar los datos entre procesos.

---

## Funcionamiento del Sistema

1. El servidor define la función objetivo (por ejemplo `rastrigin`, `sphere` o `rosenbrock`) y sus parámetros (dimensiones, límites, iteraciones).
2. Cada cliente recibe estos datos y ejecuta el algoritmo genético de forma paralela y autónoma.
3. Al finalizar, cada cliente envía al servidor su mejor resultado encontrado (valor mínimo, vector de entrada y tiempo de ejecución).
4. El servidor registra todos los resultados en un archivo `resultados.csv` para su posterior análisis.

---

## Funciones Objetivo Implementadas

* **Rastrigin**: multimodal, con muchos mínimos locales.
* **Sphere**: convexa y sencilla.
* **Rosenbrock**: desafiante, con un valle estrecho.

Estas funciones permiten probar el comportamiento del algoritmo en diferentes escenarios.

---

## Estructura del Proyecto

```
optimizacion_ppd/
├── clients/
│   ├── client_genetico.py
│   ├── funciones_objetivo.py
│   └── __init__.py
├── server/
│   ├── main_server.py
│   ├── server_utils.py
│   └── __init__.py
├── shared/
│   ├── config.py
│   └── __init__.py
├── launcher/
│   └── launch_clients.py
├── resultados.csv
└── README.md
```

---

## Ejecución del Proyecto

1. Ejecutar el servidor desde la raíz del proyecto:

   ```bash
   python server/main_server.py
   ```

2. En otra terminal, lanzar los clientes:

   ```bash
   python launcher/launch_clients.py
   ```

3. Ver los resultados guardados en `resultados.csv`.

---

## Conceptos Aplicados de la Asignatura

* Arquitectura Maestro-Trabajadores
* Programación asíncrona con `asyncio`
* Paralelismo con `multiprocessing`
* Comunicación entre procesos con `socket` y `pickle`
* Modularización del código
* Persistencia de resultados en CSV
* Pruebas con funciones objetivo clásicas de optimización

---

## Autoría

Proyecto desarrollado por Javier González, Juan de León, Álvaro González y Judith M.ª Salas
