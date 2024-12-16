#!usr/bin/env python3
import sys

class InputError(Exception):
    def __init__(self, message="Input Inválido"):
        self.message = message
        super().__init__(self.message)

        

# Se crea una clase para controlar el rodaje de los aviones con A*, de modo que se isntancia
# la heuristica con la que se quiere resolver, los n aviones y el mapa que tendran que tomar estos

class AStarRodaje:
    def __init__(self, archivo, heuristica):
        self.heuristica = heuristica
        self.aviones, self.mapa = self.read_input(archivo)
        self.solucion = []
        
    def read_input(self, file):
        try:
            with open(file, "r") as f:
                lineas = f.read().strip().split("\n")
        except FileNotFoundError:
            print(f"Error: El archivo {file} no se encuentra.")
        except InputError as e:
            print(f"Error de entrada: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            
            
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
                mapa[i-n_aviones-1,j] = tipo
                j += 1

        return aviones, mapa    

    #Funcion para comprobar si la posicion a la que se extiende un nodo es valida
    #Se supone q todas las posiciones de salida de los aviones y las posiciones de meta son validas

    def posicion_valida(self, posicion):
        return self.mapa[posicion] != "G" and posicion in self.mapa

    def aStart(self, inicio, meta):
        # Definir la lista abierta de los nodos, 
        lista_abierta = []
        # Se añade
        self.push_node(lista_abierta, (0, inicio)) # (f_score, position)

    def push_node(self, lista_abierta, node):
        lista_abierta.append(node)
        lista_abierta.ordenar_lista(lista_abierta)


def main():
    if len(sys.argv) != 3:
        print("Uso: python ASTARRodaje.py <path mapa.csv> <num-h>")
        return -1
    
    if sys.argv[2] != "1" and sys.argv[2] != "2":
        print("El número de heurística debe ser 1 o 2")
        return -1

    AStarRodaje(sys.argv[1], int(sys.argv[2]))

main()
