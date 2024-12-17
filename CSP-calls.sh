#!/bin/sh

echo "Para la restriccion 1 no hay tests proque no hay
ningun constraint para esa restriccion ya que se cumple 
sola al definir las variables y dominios
"

echo "Tests de la restricción 2"
python CSPMaintenance.py ./CSP-tests/test-restriccion-2-0.txt
echo "  Test 2.0: Comprobar que caben 2 aviones en un taller std"

python CSPMaintenance.py ./CSP-tests/test-restriccion-2-1.txt
echo "  Test 2.1: Comprobar que no cabe 1 avion JMB y 1 STD en un taller"

python CSPMaintenance.py ./CSP-tests/test-restriccion-2-2.txt
echo "  Test 2.2: Comprobar que quepan 2 aviones en un parking 
        (la restriccion es igual para todo tipo de posiciones: 
        talleres_std, talleres_jmb, parkings)"

python CSPMaintenance.py ./CSP-tests/test-restriccion-2-3.txt
echo "  Test 2.3: Comprobar que no quepan mas de dos aviones STD en un taller"

python CSPMaintenance.py ./CSP-tests/test-restriccion-2-4.txt
echo "  Test 2.4: Comprobar que no quepan mas de dos aviones JMB en un taller"

python CSPMaintenance.py ./CSP-tests/test-restriccion-2-5.txt
echo "  Test 2.5: Test general para ver las posiciones que cogen 4 aviones en 
        espacio de 2x2 en una franja de tiempo.
        Todas soluciones satisfacen la restriccion.
        (tambien actua la restriccion 5)
        "

echo "Tests de la restricción 3"
python CSPMaintenance.py ./CSP-tests/test-restriccion-3-0.txt
echo "  Test 3.0: Comprobar que un avion que tenga una tarea de tipo 2 tenga que
        pasar por el taller SPC"

python CSPMaintenance.py ./CSP-tests/test-restriccion-3-1.txt
echo "  Test 3.1: Comprobar que si no hay talleres SPC y un avion tiene tareas
        de tipo 2 no hay soluciones validas"

python CSPMaintenance.py ./CSP-tests/test-restriccion-3-2.txt
echo "  Test 3.2: Comprobar que si tiene una tarea de tipo uno tiene que pasar
        por un taller STD minimo una vez"

python CSPMaintenance.py ./CSP-tests/test-restriccion-3-3.txt
echo "  Test 3.3: Misma comprobacion que la anterior pero si no hay talleres STD
        tiene que pasar por talleres SPC
        "

echo "Tests de la restricción 4"

python CSPMaintenance.py ./CSP-tests/test-restriccion-4-0.txt
echo "  Test 4.0: Comprobar que un avion con una tarea de tipo 2 y otra de tipo 1
        con RESTR = "T" la tenga que estar antes en el taller SPC que en el STD"

python CSPMaintenance.py ./CSP-tests/test-restriccion-4-1.txt
echo "  Test 4.1: Compobar que si RESTR = "T", un avion puede estar en un PRK pero no puede
        estar en taller STD antes de estar en taller SPC
        "

echo "Tests de la restricción 5"

python CSPMaintenance.py ./CSP-tests/test-restriccion-5-0.txt
echo "  Test 5.0: Comprobar que no hayan aviones adyacentes. Al ser 4 aviones y dimensones 1x3,
        ningun avion puede estar en la posicion (0,1) en ninguna solucion"

python CSPMaintenance.py ./CSP-tests/test-restriccion-5-1.txt
echo "  Test 5.1: Como las posiciones (0,0) y (1,1) estan ocupadas por aviones JMB haciendo 
        tareas de tipo 2, el avion 3 no puede ponerse ni en (0,1) ni en (1,0) por 
        que sus posiciones adyacentes estan ocupadas
        "

echo "Tests de la restricción 6"

python CSPMaintenance.py ./CSP-tests/test-restriccion-6-0.txt
echo "  Test 6.0: Al haber dos aviones JMB en una cuadricula 2x2 solo pueden estar en 
        posiciones opuestas"

python CSPMaintenance.py ./CSP-tests/test-restriccion-6-1.txt
echo "  Test 6.1: Si solo hay dos posiciones disponibles y dos aviones JMB no puede haber
        soluciones disponibles
"