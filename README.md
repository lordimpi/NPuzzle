
# N-Puzzle Solver (BFS, DFS, A*)

Proyecto de referencia para el mini‑proyecto de IA: resolución del **N‑Puzzle** usando **BFS**, **DFS** y **A\*** con heurística de **distancia Manhattan**.

## Crear entorno virtual
```bash
python -m venv venv
```

## Activar entorno virtual
```bash
venv\Scripts\activate
```

## Instalar dependencias
```bash
pip install -r requirements.txt
```

## Uso rápido
```bash
python main.py --algoritmo a_estrella --tamano 6 --mezclas 20 --visualizar
```
<img width="800" height="683" alt="image" src="https://github.com/user-attachments/assets/2948bc66-8709-4430-960e-176e2f0427a8" />

## Uso con benchmarks
```bash
python benchmarks.py --algo all --size 3 --cases 3 --shuffle 20 --csv resultados.csv
```
