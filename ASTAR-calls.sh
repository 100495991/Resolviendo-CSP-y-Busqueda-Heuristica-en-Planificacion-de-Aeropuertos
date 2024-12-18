#!/bin/sh

echo "Valid1: Mapa con 1 única casilla de espera"
python ASTARRodaje.py ./ASTAR-tests/mapa.csv 1
python ASTARRodaje.py ./ASTAR-tests/mapa.csv 2

echo "Valid2: Mapa con todas las casillas blancas"
python ASTARRodaje.py ./ASTAR-tests/mapa02.csv 1
python ASTARRodaje.py ./ASTAR-tests/mapa02.csv 2

echo "Valid3: Mapa con restricciones  de casillas amarillas"
python ASTARRodaje.py ./ASTAR-tests/mapa03.csv 1
python ASTARRodaje.py ./ASTAR-tests/mapa03.csv 2

echo "Valid4: Mapa con un avión"
python ASTARRodaje.py ./ASTAR-tests/mapa04.csv 1
python ASTARRodaje.py ./ASTAR-tests/mapa04.csv 2

echo "Valid5 Mapa con 3 aviones"
python ASTARRodaje.py ./ASTAR-tests/mapa05.csv 1
python ASTARRodaje.py ./ASTAR-tests/mapa05.csv 2

echo "Invalid1: Mapa con una colisión inevitable"
python ASTARRodaje.py ./ASTAR-tests/mapa06.csv 1
python ASTARRodaje.py ./ASTAR-tests/mapa06.csv 2

echo "Invalid2: Mapa con todo casillas grises"
python ASTARRodaje.py ./ASTAR-tests/mapa07.csv 1
python ASTARRodaje.py ./ASTAR-tests/mapa07.csv 2

echo "valid5: Matriz columna"
python ASTARRodaje.py ./ASTAR-tests/mapa08.csv 1
python ASTARRodaje.py ./ASTAR-tests/mapa08.csv 2

echo "valid6: Matriz fila"
python ASTARRodaje.py ./ASTAR-tests/mapa09.csv 1
python ASTARRodaje.py ./ASTAR-tests/mapa09.csv 2

echo "valid7: Una sola casilla en blanco"
python ASTARRodaje.py ./ASTAR-tests/mapa10.csv 1
python ASTARRodaje.py ./ASTAR-tests/mapa10.csv 2



