from constraint import Problem

class InputError(Exception):
    def __init__(self, message="Input Inválido"):
        self.message = message
        super().__init__(self.message)

def read_input(file):
    with open(file, "r") as f:
        lines = f.read().strip().split("\n")
        
    franjas = int(lines[0].split(': ')[1])
    dimensiones = tuple(map(int, lines[1].split('x')))

    talleres_std = [tuple(map(int, item[1:-1].split(','))) for item in lines[2].split(':')[1].split(" ")]
    talleres_spc = [tuple(map(int, item[1:-1].split(','))) for item in lines[3].split(':')[1].split(" ")]
    parking = [tuple(map(int, item[1:-1].split(','))) for item in lines[4].split(':')[1].split(" ")]

    aviones = []
    for line in lines[5:]:
        element = line.split('-')
        aviones.append({
            "id": int(element[0]),
            "tipo": element[1],
            "restr": element[2] == "T",
            "tipo1": int(element[3]),
            "tipo2": int(element[4]),
        })

    return franjas, dimensiones, talleres_std, talleres_spc, parking, aviones

def main():
    input_file = "entrada.txt"
    franjas, dimensiones, talleres_std, talleres_spc, parking, aviones = read_input(input_file)

    problem = Problem()

    # Modelado de las variables
    talleres_todos = talleres_std + talleres_spc + parking
    variables_creadas = []
    for avion in aviones:
        for franja in range(franjas):
            variable_name = f"avion{avion['id']}_franja{franja}"
            variables_creadas.append(variable_name)
            problem.addVariable(variable_name, talleres_todos)

    # Restricción 1: Cada taller puede atender hasta 2 aviones en una franja horaria
    for franja in range(franjas):
        for taller in talleres_todos:
            variables = [f"avion{avion['id']}_franja{franja}" for avion in aviones]
            problem.addConstraint(lambda *args: len(set(args)) <= 2, variables)

    # Restricción 2: No más de un avión JUMBO en el mismo taller en la misma franja horaria
    for franja in range(franjas):
        for taller in talleres_todos:
            jumbo_variables = [f"avion{avion['id']}_franja{franja}" for avion in aviones if avion["tipo"] == "JMB"]
            if jumbo_variables:
                problem.addConstraint(lambda *args: len(set(args)) <= 1, jumbo_variables)

    # Restricción 3: Tareas de mantenimiento estándar y especialista
    for avion in aviones:
        if avion["restr"]:
            for franja in range(1, franjas):
                problem.addConstraint(lambda pos1, pos2: pos1 in talleres_spc and pos2 in talleres_std,
                                      [f"avion{avion['id']}_franja{franja - 1}", f"avion{avion['id']}_franja{franja}"])

    # Restricción 4: Orden de tareas de mantenimiento
    for avion in aviones:
        if avion["restr"]:
            for franja in range(1, franjas):
                variables = [f"avion{avion['id']}_franja{f}" for f in range(franjas)]
                problem.addConstraint(lambda *args: all(arg in talleres_spc for arg in args[:avion["tipo2"]]) and
                                      all(arg in talleres_todos for arg in args[avion["tipo2"]:]), variables)

    # Restricción 5: Al menos uno de los talleres o parkings adyacentes debe estar vacío
    def adyacente_vacio(*args):
        posiciones = [pos for pos in args if pos is not None]
        return len(set(posiciones)) == len(posiciones)

    for franja in range(franjas):
        for y in range(dimensiones[0]):
            for x in range(dimensiones[1]):
                variables = []
                if (x, y) in talleres_todos:
                    variables.append(f"avion{y * dimensiones[1] + x}_franja{franja}")
                if (x + 1, y) in talleres_todos and (x + 1) < dimensiones[1]:
                    variables.append(f"avion{y * dimensiones[1] + (x + 1)}_franja{franja}")
                if (x - 1, y) in talleres_todos and (x - 1) >= 0:
                    variables.append(f"avion{y * dimensiones[1] + (x - 1)}_franja{franja}")
                if (x, y + 1) in talleres_todos and (y + 1) < dimensiones[0]:
                    variables.append(f"avion{(y + 1) * dimensiones[1] + x}_franja{franja}")
                if (x, y - 1) in talleres_todos and (y - 1) >= 0:
                    variables.append(f"avion{(y - 1) * dimensiones[1] + x}_franja{franja}")
                variables = [var for var in variables if var in variables_creadas]  # Verificar que las variables existen
                if variables:
                    problem.addConstraint(adyacente_vacio, variables)

    # Restricción 6: No dos aviones JUMBO adyacentes
    def no_jumbo_adyacente(*args):
        jumbos = [pos for pos in args if pos is not None and pos in talleres_todos]
        return len(jumbos) <= 1

    for franja in range(franjas):
        for y in range(dimensiones[0]):
            for x in range(dimensiones[1]):
                if (x, y) in talleres_todos:
                    variables = [
                        f"avion{y * dimensiones[1] + x}_franja{franja}",
                        f"avion{y * dimensiones[1] + (x + 1)}_franja{franja}" if (x + 1) < dimensiones[1] else None,
                        f"avion{y * dimensiones[1] + (x - 1)}_franja{franja}" if (x - 1) >= 0 else None,
                        f"avion{(y + 1) * dimensiones[1] + x}_franja{franja}" if (y + 1) < dimensiones[0] else None,
                        f"avion{(y - 1) * dimensiones[1] + x}_franja{franja}" if (y - 1) >= 0 else None
                    ]
                    variables = [var for var in variables if var in variables_creadas]  # Verificar que las variables existen
                    if variables:
                        problem.addConstraint(no_jumbo_adyacente, variables)

    # Resolver el problema
    soluciones = problem.getSolutions()
    print(len(soluciones))
    for solucion in soluciones:
        print(solucion)

main()
