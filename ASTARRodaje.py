#!usr/bin/env python3
import sys
from itertools import product
import time

class InputError(Exception):
    def __init__(self, message="Input Inválido"):
        self.message = message
        super().__init__(self.message)


#Clase que contendra los elementos de 1 nodo de A*
class Nodo:
    def __init__(self, estado, g, h, padre=None):
        #Coste acumulado
        self.g = g
        #Valor heuristico
        self.h = h
        #Estado es las posiciones de cada avion en el mapa
        self.estado = estado
        #Padre del nodo para poder reconstruir el camino
        self.padre = padre

    #Funcion que calcula la f directamente dentro
    def f(self):
        return self.g + self.h

#Clase que controla el flujo del algoritmo A* inputs y outputs
class AStarRodaje:
    def __init__(self, archivo, heuristica):
        #Valor de la heuristica que introducen por terminal
        self.heuristica = heuristica
        #Diccionario de todos los aviones y el mapa en formato { (posicion): color}
        self.aviones, self.mapa = self.read_input(archivo)
        #Lista de la solucion para poder imprimirla
        self.solucion = []
        self.nodos_expandidos = 0

    #Funcion para leer el archivo de entrada
    def read_input(self, file):
        try:
            with open(file, "r") as f:
                lineas = f.read().strip().split("\n")
        except FileNotFoundError:
            print(f"Error: El archivo {file} no se encuentra.")
            sys.exit(1)
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            sys.exit(1)
    
        n_aviones = int(lineas[0])
        aviones = []

        for linea in range(n_aviones):
            posiciones = lineas[linea+1].split(" ")
            inicio = tuple(map(int, posiciones[0][1:-1].split(',')))
            fin = tuple(map(int, posiciones[1][1:-1].split(',')))
            aviones.append({
                "id": linea,
                "inicio": inicio,
                "fin": fin
            })
        
        mapa = {}
        for i in range(n_aviones+1, len(lineas)):
            j = 0
            for tipo in lineas[i].split(';'):
                mapa[i-n_aviones-1, j] = tipo
                j += 1

        filas = len(lineas) - n_aviones - 1
        columnas = len(lineas[n_aviones+1].split(';'))
        self.dimensiones = (filas, columnas)
        return aviones, mapa

    #Funcion para comprobar que al expandir los movimientos posibles no se generen invalidos
    # invalidos: fuera del mapa, casilla gris
    def posicion_valida(self, posicion):
        x, y = posicion
        filas, columnas = self.dimensiones
        return 0 <= x < filas and 0 <= y < columnas and self.mapa.get(posicion) != "G"

    def aStar(self):
        lista_inicio = [avion["inicio"] for avion in self.aviones]
        lista_fin = [avion["fin"] for avion in self.aviones]

        lista_abierta = []
        lista_cerrada = set()

        nodo_inicial = Nodo(estado=lista_inicio, g=0, h=self.heuristica_global(lista_inicio, lista_fin))
        self.insertar_nodo(lista_abierta, nodo_inicial)

        # Almacenamos el tiempo de inicio
        start_time = time.time()

        while lista_abierta:
            actual = lista_abierta.pop(0)

            if actual.estado == lista_fin:
                # Calculamos el tiempo total de ejecución
                tiempo_ejecucion = time.time() - start_time
                makespan = actual.g  # El makespan es el tiempo máximo de los aviones en llegar(los pasos hasta la solucion)
                # Llamamos a guardar_solucion pasándole los pasos reconstruidos
                solucion = self.reconstruir_camino(actual)
                self.guardar_solucion(solucion)
                self.guardar_stats(tiempo_ejecucion, makespan, self.nodos_expandidos, nodo_inicial.h)
                return solucion

            lista_cerrada.add(tuple(actual.estado))

            for vecino in self.expandir_vecinos(actual, lista_fin):
                if tuple(vecino.estado) in lista_cerrada:
                    continue
                self.insertar_nodo(lista_abierta, vecino)

            # Incrementamos el contador de nodos expandidos
            self.nodos_expandidos = len(lista_cerrada)

        return None


    def reconstruir_camino(self, nodo):
        camino = []
        while nodo:
            camino.append(nodo.estado)
            nodo = nodo.padre
        return camino[::-1]

    def insertar_nodo(self, lista_abierta, nodo):
        for i, n in enumerate(lista_abierta):
            if nodo.f() < n.f():
                lista_abierta.insert(i, nodo)
                return
        lista_abierta.append(nodo)

    def calcular_heuristica(self, posicion1, posicion2):
        x1, y1 = posicion1
        x2, y2 = posicion2
        return abs(x1 - x2) + abs(y1 - y2)
       
    def heuristica_global(self, estado, meta):
        if self.heuristica==1:
            return sum(self.calcular_heuristica(pos, objetivo) for pos, objetivo in zip(estado, meta))
        else:
            return max(self.calcular_heuristica(pos, objetivo) for pos, objetivo in zip(estado, meta))


    def expandir_vecinos(self, nodo_actual, meta):
        vecinos = []
        movimientos = [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)]
        combinaciones = self.generar_combinaciones(len(self.aviones), movimientos)

        """
        Se itera sobre cada combinación de movimientos en la lista combinaciones, 
        que es una lista que contiene los movimientos para cada avión.
        """
        for movimiento in combinaciones:
            nuevo_estado = []
            valido = True
            posiciones_ocupadas = set()

            """
            zip(nodo_actual.estado, movimiento): Combina las posiciones actuales (nodo_actual.estado) y los movimientos 
            (movimiento) en tuplas. 
            Para cada tupla, posicion es una posición actual de un avión y mov es el movimiento que se va a aplicar a esa posición
            enumerate: Añade el índice i a cada tupla de la combinación para identificar a qué avión pertenece cada posición y movimiento.
            """

            for i, (posicion, mov) in enumerate(zip(nodo_actual.estado, movimiento)):
                nueva_posicion = (posicion[0] + mov[0], posicion[1] + mov[1])

                # Validar si la posición es válida en el mapa
                if not self.posicion_valida(nueva_posicion):
                    valido = False
                    break
                
                # Evitar que un avión espere en una casilla amarilla (Y)
                if self.mapa.get(nueva_posicion) == 'Y' and mov == (0, 0):
                    valido = False
                    break

                # Evitar que los aviones se crucen (no deben ocupar la misma casilla)
                if nueva_posicion in posiciones_ocupadas:
                    valido = False
                    break

                # Añadir la nueva posición a las posiciones ocupadas
                posiciones_ocupadas.add(nueva_posicion)

                nuevo_estado.append(nueva_posicion)

            # Verificar si hay intercambios de posiciones (dos aviones no deben intercambiarse)
            if valido:
                for i, pos_actual in enumerate(nuevo_estado):
                    if pos_actual in nodo_actual.estado and pos_actual != nodo_actual.estado[i]:
                        valido = False
                        break

            # Si el estado es válido, crear el vecino
            if valido:
                g = nodo_actual.g + 1
                h = self.heuristica_global(nuevo_estado, meta)
                vecino = Nodo(estado=nuevo_estado, g=g, h=h, padre=nodo_actual)
                vecinos.append(vecino)

        return vecinos

    def generar_combinaciones(self, n_aviones, movimientos):
        return list(product(movimientos, repeat=n_aviones))

    def guardar_solucion(self, solucion):
        # Nombre del archivo para la solución
        nombre_archivo = f"{sys.argv[1][:-4]}-{sys.argv[2]}.output"
        
        with open(nombre_archivo, 'w') as f:
            if not solucion:  # Si la solución está vacía o no existe
                f.write("No se encontró una solución.\n")
                return
            # Trasponer la solución, porque la solución está en formato de columnas por avión
            solucion_traspuesta = list(zip(*solucion))

            for pasos in solucion_traspuesta:
                movimientos = []
                for j in range(len(pasos) - 1):
                    # Determinar el tipo de movimiento entre dos posiciones
                    if pasos[j+1] == (pasos[j][0], pasos[j][1] + 1):
                        movimientos.append("→")
                    elif pasos[j+1] == (pasos[j][0], pasos[j][1] - 1):
                        movimientos.append("←")
                    elif pasos[j+1] == (pasos[j][0] + 1, pasos[j][1]):
                        movimientos.append("↓")
                    elif pasos[j+1] == (pasos[j][0] - 1, pasos[j][1]):
                        movimientos.append("↑")
                    else:
                        movimientos.append("w")  # Si no se mueve, es un 'w'
                
                # Para el último paso, si no hay movimiento, agregamos 'w'
                if len(pasos) > 1:
                    movimientos.append("")

                solucion_linea = " ".join([f"({p[0]},{p[1]}) {mov}" for p, mov in zip(pasos, movimientos)])
                f.write(solucion_linea + "\n")

    def guardar_stats(self, tiempo_ejecucion, makespan, nodos_expandidos, heuristica_inicial):
        nombre_archivo = f"{sys.argv[1][:-4]}-{sys.argv[2]}.stat"
        with open(nombre_archivo, 'w') as f:
            f.write("Estadísticas:\n")
            f.write(f"Tiempo total: {tiempo_ejecucion:.2f}s\n")
            f.write(f"Makespan: {makespan}\n")
            f.write(f"h inicial: {heuristica_inicial}\n")
            f.write(f"Nodos expandidos: {nodos_expandidos}\n")

def main():
    if len(sys.argv) != 3:
        print("Uso: python ASTARRodaje.py <path mapa.csv> <num-h>")
        return -1
    
    if sys.argv[2] != "1" and sys.argv[2] != "2":
        print("El número de heurística debe ser 1 o 2")
        return -1

    astar = AStarRodaje(sys.argv[1], int(sys.argv[2]))
    solucion = astar.aStar()
    if solucion == None:
        astar.guardar_solucion(solucion)  
    if solucion:
        print("Solución encontrada")
    else:
        print("No se encontró solución.")

main()
