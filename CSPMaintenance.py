#!usr/bin/env python3
from constraint import Problem
import sys



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
    if lines[2].split(':')[1] != '':
        lista_posicones_std = lines[2].split(':')[1].split(" ")

        for item in lista_posicones_std:
            item = item[1:-1]  # Eliminar los paréntesis
            item = item.split(',')
            talleres_std.append((int(item[0]), int(item[1])))

    talleres_spc = []
    if lines[3].split(':')[1] != '':
        lista_posiciones_spc = lines[3].split(':')[1].split(" ")

        for item in lista_posiciones_spc:
            item = item[1:-1]  # Eliminar los paréntesis
            item = item.split(',')
            talleres_spc.append((int(item[0]), int(item[1])))

    parking = []
    if lines[4].split(':')[1] != '':
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
    """
    print("Franjas: " + str(franjas))
    print("Dimensiones: " + str(dimensiones))
    print("Talleres STD: " + str(talleres_std))
    print("Talleres SPC: " + str(talleres_spc))
    print("Parking: " + str(parking))
    for i in aviones:
        print("Avion " + str(i["id"]) + ": " + str(i))
    """
    
    return franjas, dimensiones, talleres_std, talleres_spc, parking, aviones


def main():

    if len(sys.argv) != 2:
        print("Uso: python CSPMaintenance.py <ruta del archivo entrada>")
        return -1

    # Llamada a la función read_input con el archivo introducido
    try:
        input_file = sys.argv[1]  # Asegurar que el archivo exista
        franjas, dimensiones, talleres_std, talleres_spc, parking, aviones = read_input(input_file)
    except FileNotFoundError:
        print(f"Error: El archivo {input_file} no se encuentra.")
    except InputError as e:
        print(f"Error de entrada: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


    problem = Problem()

    #Modelado de las variables, cada variable sera 1 avión en cada franja av1_0, av1_1, ...
    for i in range(len(aviones)):
        for j in range(franjas):
            problem.addVariable(f"av{i}_{j}", talleres_std + talleres_spc + parking)


    # Restriccion para que no haya más de dos aviones por taller y no haya mas de un avion tipo jumbo por taller
    for franja in range(franjas):
        standard_variables = [f"av{i}_{franja}" for i in range(len(aviones)) if aviones[i]["tipo"] == "STD"]
        jumbo_variables = [f"av{i}_{franja}" for i in range(len(aviones)) if aviones[i]["tipo"] == "JMB"]
        n_jmb = len(jumbo_variables)

        def max_2_aviones(*args):
            contador = {}
            args_jmb = args[:n_jmb]
            for elemento in args:
                if elemento in contador:
                    if elemento in args_jmb:
                        return False
                    contador[elemento] += 1
                else:
                    contador[elemento] = 1
                # Si un valor supera las dos repeticiones, se devuelve Flase
                if contador[elemento] > 2:
                    return False
            return True

        problem.addConstraint(max_2_aviones, jumbo_variables + standard_variables)

    
    # Restriccion si tiene asignada tarea especialista necesita pisar taller especialista
    # Si tiene asignada otra tarea, cualquier de los dos talleres
    for avion in aviones:

        def n_especialista(*args):
            n_spc = avion['tipo2']
            n_total = avion['tipo2'] + avion['tipo1']
            for posicion in args:
                if posicion in talleres_spc:
                    n_spc -= 1
                    n_total -= 1
                if posicion in talleres_std:
                    n_total -= 1
            if n_spc > 0: 
                return False
            if n_total > 0: 
                return False
            return True
    
        problem.addConstraint(n_especialista, [f"av{avion['id']-1}_{i}" for i in range(franjas)])
    
    # Restriccion hacer antes tareas especialistas que estandar
    for avion in aviones:
        
        if avion["mantenimiento"]:
            n_tareas2 = avion['tipo2']
            def orden_especialista(*args):
                for i in range(n_tareas2):
                    if args[i] not in talleres_spc:
                        return False
                return True
            problem.addConstraint(orden_especialista, [f"av{(avion['id'])-1}_{i}" for i in range(franjas)])

    
    # Verificar la  maniobrabilidad de los aviones
    for franja in range(franjas):

        def maniobrabilidad(*args):
            for avion in args:
                if not avion[0] == 0:
                    if not (avion[0]-1, avion[1]) in args:
                        continue
                if not avion[0] == dimensiones[0]-1:
                    if not (avion[0]+1, avion[1]) in args:
                        continue
                if not avion[1] == 0:
                    if not (avion[0], avion[1]-1) in args:
                        continue
                if not avion[1] == dimensiones[1]-1:
                    if not (avion[0], avion[1]+1) in args:
                        continue
                return False
            return True

        problem.addConstraint(maniobrabilidad, [f"av{i}_{franja}" for i in range(len(aviones))])
    
    
    # Dos aviones jumbo no pueden estar en talleres adyacentes
    for franja in range(franjas):
        
        def jumbos_juntos(*args):
            for avion in args:
                if not avion[0] == 0:
                    if (avion[0]-1, avion[1]) in args:
                        return False
                if not avion[0] == dimensiones[0]-1:
                    if (avion[0]+1, avion[1]) in args:
                        return False
                if not avion[1] == 0:
                    if (avion[0], avion[1]-1) in args:
                        return False
                if not avion[1] == dimensiones[1]-1:
                    if (avion[0], avion[1]+1) in args:
                        return False
            return True
    
        problem.addConstraint(jumbos_juntos, [f"av{avion['id']-1}_{franja}" for avion in aviones if avion['tipo']=="JMB"])
        

    

    soluciones = problem.getSolutions()
    
    # Escribir la solucion en el archivo .csv
    nombre_archivo = input_file[:-4] + ".csv"

    archivo = open(nombre_archivo, "w")

    archivo.write(f"N. Sol:  {len(soluciones)}\n")

    for i, solucion in enumerate(soluciones[:10]):
        archivo.write(f"Solución {i+1}: \n")
        for avion in aviones:
            archivo.write(f"\t{avion['id']}-{avion['tipo']}-{"T" if avion['mantenimiento'] else "F"}-{avion['tipo1']}-{avion['tipo2']}: ")
            
            for j in range(franjas):

                posicion = solucion[f'av{avion['id']-1}_{j}']
                if posicion in talleres_spc:
                    archivo.write(f"SPC{posicion}")
                if posicion in talleres_std:
                    archivo.write(f"STD{posicion}")
                if posicion in parking:
                    archivo.write(f"PRK{posicion}")
                if j < franjas-1:
                    archivo.write(", ")
                else:
                    archivo.write("\n")
                    
    archivo.close()
                        

main()
