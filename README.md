*This project has been created as part of the 42 curriculum by mboubaza, iel-fadi.*

## Description
A-Maze-ing is a Python-based procedural maze generator and visualizer. The application reads a configuration file to generate either perfect or imperfect mazes containing a mandatory "42" shape. It then solves the maze to find the shortest path, outputs the grid and path in a specific hexadecimal format, and provides an interactive visual representation of the maze in the terminal.

## Instructions
### Prerequisites
- Python 3.10 or later
- `pip`

### Installation & Execution
Use the provided `Makefile` to install dependencies and run the program:
```bash
make install
make run CONFIG=config.txt
```
Other available commands:
- `make lint`: Runs `flake8` and `mypy` for static type checking.
- `make lint-strict`: Runs strict mypy checks.
- `make debug`: Runs the program with `pdb`.
- `make clean`: Removes cache files and build artifacts.

## Configuration File Format
The program uses a `.txt` configuration file containing `KEY=VALUE` pairs. Comments can be added using `#`.
- **WIDTH**: Maze width in cells.
- **HEIGHT**: Maze height in cells.
- **ENTRY**: `x, y` coordinates for the entrance.
- **EXIT**: `x, y` coordinates for the exit.
- **OUTPUT_FILE**: Name of the file to save the generated maze and path.
- **PERFECT**: `True` for a perfect maze (one unique path), `False` for an imperfect maze (multiple paths/loops).
- **SEED**: An optional string or integer to seed the random number generator for reproducible mazes.

*Example config.txt:*
```ini
WIDTH = 5
HEIGHT = 5
ENTRY = 0, 0
EXIT =  0, 1
OUTPUT_FILE = maze.txt
PERFECT = False
SEED = 42
```

## Maze Generation Algorithm
**Algorithm Used:** Iterative Depth-First Search (DFS) with a Recursive Backtracker.

**Why this algorithm:** We chose this approach because it efficiently generates perfect mazes with deep, winding paths. By using an iterative stack-based approach rather than strict recursion, we avoided hitting Python's maximum recursion depth, ensuring the program can successfully generate massive grids without crashing.

## Code Reusability
The core generation logic is isolated into a standalone package named `mazegen`, which can be installed and reused in other projects.
    
**Installation:**
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```
    
**Usage Example:**
```python
from mazegen.maze_gen import MazeGenerator

# Instantiate the generator with custom parameters
gen = MazeGenerator(
    height=21, 
    width=21, 
    entrance=(0, 0), 
    departure=(20, 20), 
    seed="my_seed", 
    perfect=True
)

# Access the generated structure (returns a 2D list of Cell objects)
maze_grid = gen.generate_maze()

# Access the shortest solution path
solution_path = gen.maze_solver()
```

## Team and Project Management
- **Roles:** mboubaza handled the core back-end logic, including the `maze_gen` generation algorithm, pathfinding, and the configuration parser. iel-fadi managed the project's packaging (creating the `.whl` and `.tar.gz` files) and built the terminal visualizer.
- **Planning & Evolution:** We started by separating the core logic and visualizer to work independently. The plan remained largely intact, though we had to synchronize towards the end to ensure the visualizer properly interpreted the `Cell` objects and grid structure produced by the back-end.
- **What Worked Well & What Could Be Improved:** The division of labor worked exceptionally well, allowing us to focus on our strengths without stepping on each other's toes. One area for improvement was standardizing the coordinate system earlier; making sure `x,y` vs `row,col` was strictly consistent between the parser and generator would have saved us some debugging time.
- **Tools Used:** Git for version control, Makefile for automation, `flake8` for formatting, and `mypy` for strict type enforcement.

## Resources
- **AI Usage:** Artificial Intelligence was used exclusively for debugging complex type-hinting errors during the `make lint-strict` phase and for explaining certain graph theory concepts when implementing the pathfinding solver. It was not used to write the core generation or display logic.