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

    return franjas, dimensiones, talleres_std, talleres_spc, parking, aviones

def main():

    if len(sys.argv) != 2:
        print("Uso: python CSPMaintenance.py <ruta del archivo entrada>")
        return -1

    try:
        input_file = sys.argv[1]
        franjas, dimensiones, talleres_std, talleres_spc, parking, aviones = read_input(input_file)
    except FileNotFoundError:
        print(f"Error: El archivo {input_file} no se encuentra.")
    except InputError as e:
        print(f"Error de entrada: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

    problem = Problem()

    talleres_todos = talleres_std + talleres_spc + parking
    for i in range(len(aviones)):
        for j in range(franjas):
            problem.addVariable(f"av{i}_{j}", talleres_todos)

    # Restricción: no más de dos aviones por taller y no más de un avión JUMBO por taller
    for franja in range(franjas):
        variables = [f"av{i}_{franja}" for i in range(len(aviones))]
        def max_2_aviones(*args):
            contador = {}
            for index, elemento in enumerate(args):
                if elemento in contador:
                    if aviones[index]["tipo"] == "JMB":
                        return False
                    contador[elemento] += 1
                else:
                    contador[elemento] = 1
                if contador[elemento] > 2:
                    return False
            return True
        problem.addConstraint(max_2_aviones, variables)

    # Restricción: tareas especialistas necesitan taller especialista
    for avion in aviones:
        if avion["tipo2"] > 0:
            def n_especialista(*args):
                n = avion['tipo2']
                for elemento in args:
                    if elemento in talleres_spc:
                        n -= 1
                return n <= 0
            problem.addConstraint(n_especialista, [f"av{avion['id']-1}_{i}" for i in range(franjas)])

    # Restricción: hacer tareas especialistas antes de estándar
    for avion in aviones:
        if avion["mantenimiento"]:
            def orden_especialista(*args):
                for i in range(avion['tipo2']):
                    if args[i] not in talleres_spc:
                        return False
                return True
            problem.addConstraint(orden_especialista, [f"av{avion['id']-1}_{i}" for i in range(franjas)])

    # Restricción: maniobrabilidad de los aviones
    for franja in range(franjas):
        def maniobrabilidad(*args):
            posiciones = {avion: (avion[0], avion[1]) for avion in args}
            for pos in posiciones.values():
                x, y = pos
                vecinos = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                if any(v in posiciones.values() for v in vecinos):
                    return False
            return True
        problem.addConstraint(maniobrabilidad, [f"av{i}_{franja}" for i in range(len(aviones))])

    # Restricción: no dos aviones JUMBO adyacentes
    for franja in range(franjas):
        def jumbos_juntos(*args):
            posiciones = {avion: (avion[0], avion[1]) for avion in args}
            for pos in posiciones.values():
                x, y = pos
                vecinos = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                if any(v in posiciones.values() for v in vecinos):
                    return False
            return True
        problem.addConstraint(jumbos_juntos, [f"av{avion['id']-1}_{franja}" for avion in aviones if avion['tipo'] == "JMB"])

    soluciones = problem.getSolutions()

    print(f"N. Sol:  {len(soluciones)}")
    if soluciones:
        for idx, solucion in enumerate(soluciones[:3]):
            print(f"Solución {idx + 1}:")
            for avion in range(len(aviones)):
                for franja in range(franjas):
                    print(f"Avión {avion}, Franja {franja}: {solucion[f'av{avion}_{franja}']}")

main()
