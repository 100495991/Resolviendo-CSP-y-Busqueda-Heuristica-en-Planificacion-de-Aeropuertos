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

echo "Invalid1: Mapa con una colisión inevitables"
python ASTARRodaje.py ./ASTAR-tests/mapa04.csv 1
python ASTARRodaje.py ./ASTAR-tests/mapa04.csv 2
