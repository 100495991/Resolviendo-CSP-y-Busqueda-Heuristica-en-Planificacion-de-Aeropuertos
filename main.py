#!usr/bin/env python3

class InputError(Exception):
    def __init__(self, message="Input Inválido"):
        self.message = message
        super().__init__(self.message)

def read_input(file):
    with open(file, "r") as f:
        lines = f.read().strip().split("\n")
        
    franjas = int(lines[0].split(': ')[1])

    dimensiones = (int(lines[1].split('x')[0]), int(lines[1].split('x')[1]))

    #El string de entrada se va divir en pares de numeros para introducirlos en una lista de tuplas de enteros
    # para poder trabajar facilmente con los datos
    talleres_std = []
    lista_posicones_std = lines[2].split(':')[1].split(" ")

    for item in lista_posicones_std:
        item = item[1:-1]  # Eliminar los paréntesis
        item = item.split(',')
        talleres_std.append((int(item[0]), int(item[1])))

    talleres_spc = []
    lista_posiciones_spc = lines[3].split(':')[1].split(" ")

    for item in lista_posiciones_spc:
        item = item[1:-1]  # Eliminar los paréntesis
        item = item.split(',')
        talleres_spc.append((int(item[0]), int(item[1])))

    parking = []
    lista_posiciones_parking = lines[4].split(':')[1].split(" ")

    for item in lista_posiciones_parking:
        item = item[1:-1]  # Eliminar los paréntesis
        item = item.split(',')
        parking.append((int(item[0]), int(item[1])))
    
    aviones = []
    
    for line in lines[5:]:
        element = line.split('-')
        aviones.append({
            "id": int(element[0]),
            "tipo": element[1],
            "mantenimiento": element[2] == "T",
            "tipo1": int(element[3]),
            "tipo2": int(element[4]),
        })

    print("Franjas: " + str(franjas))
    print("Dimensiones: " + str(dimensiones))
    print("Talleres STD: " + str(talleres_std))
    print("Talleres SPC: " + str(talleres_spc))
    print("Parking: " + str(parking))
    for i in aviones:
        print("Avion " + str(i["id"]) + ": " + str(i))

    

def main():
    # Llamada a la función read_input con un archivo de ejemplo
    try:
        input_file = "entrada.txt"  # Asegúrate de que este archivo exista
        read_input(input_file)
    except FileNotFoundError:
        print(f"Error: El archivo {input_file} no se encuentra.")
    except InputError as e:
        print(f"Error de entrada: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()