import sys
from typing import Tuple
from mazegen.maze_gen import MazeGenerator

RESET = "\033[0m"
WALL_COLORS = ["\033[97m", "\033[94m", "\033[96m", "\033[92m"]
ENTRY_COLOR = "\033[95m"
EXIT_COLOR = "\033[91m"
PATH_COLOR = "\033[93m"
PATTERN_COLOR = "\033[37m"


def print_maze(generator: MazeGenerator,
               show_path: bool, color_idx: int) -> None:
    """Renders the maze in the terminal using ASCII blocks and ANSI colors.

    Args:
        generator (MazeGenerator): The maze object containing the grid data.
        show_path (bool): Determines whether the solution path is displayed.
        color_idx (int): The current index for rotating wall colors.
    """
    h = generator.height * 2 + 1
    w = generator.width * 2 + 1

    display = [['██' for _ in range(w)] for _ in range(h)]
    colors = [['' for _ in range(w)] for _ in range(h)]

    wall_c = WALL_COLORS[color_idx % len(WALL_COLORS)]
    grid = generator.gen_maze

    for r in range(generator.height):
        for c in range(generator.width):
            dr = r * 2 + 1
            dc = c * 2 + 1
            cell = grid[r][c]

            if cell.is_ftwo:
                colors[dr][dc] = PATTERN_COLOR
                if r > 0 and grid[r-1][c].is_ftwo:
                    colors[dr-1][dc] = PATTERN_COLOR
                if c > 0 and grid[r][c-1].is_ftwo:
                    colors[dr][dc-1] = PATTERN_COLOR
                if (
                    r > 0 and c > 0
                    and grid[r-1][c].is_ftwo
                    and grid[r][c-1].is_ftwo
                    and grid[r-1][c-1].is_ftwo
                ):
                    colors[dr-1][dc-1] = PATTERN_COLOR
            else:
                display[dr][dc] = '  '
                if cell.north:
                    display[dr - 1][dc] = '  '
                if cell.south:
                    display[dr + 1][dc] = '  '
                if cell.west:
                    display[dr][dc - 1] = '  '
                if cell.east:
                    display[dr][dc + 1] = '  '

    for r in range(generator.height):
        for c in range(generator.width):
            dr = r * 2 + 1
            dc = c * 2 + 1
            cell = grid[r][c]

            if show_path and cell.is_path:
                if not cell.is_start and not cell.is_end:
                    display[dr][dc] = '██'
                    colors[dr][dc] = PATH_COLOR

                if cell.north and r > 0 and grid[r-1][c].is_path:
                    display[dr-1][dc] = '██'
                    colors[dr-1][dc] = PATH_COLOR

                if cell.west and c > 0 and grid[r][c-1].is_path:
                    display[dr][dc-1] = '██'
                    colors[dr][dc-1] = PATH_COLOR

            if cell.is_start:
                display[dr][dc] = '██'
                colors[dr][dc] = ENTRY_COLOR
            elif cell.is_end:
                display[dr][dc] = '██'
                colors[dr][dc] = EXIT_COLOR

    print("\n")
    for y in range(h):
        line = ""
        for x in range(w):
            if display[y][x] == '██':
                c = colors[y][x] if colors[y][x] else wall_c
                line += f"{c}██{RESET}"
            else:
                line += '  '
        print(line)


def interactive_loop(generator: MazeGenerator, entry: Tuple[int, int],
                     exit_coords: Tuple[int, int]) -> None:
    """Starts the interactive terminal loop for user inputs.

    Args:
        generator (MazeGenerator): The maze instance to be manipulated.
        entry (Tuple[int, int]): The starting coordinates.
        exit_coords (Tuple[int, int]): The finishing coordinates.
    """
    show_path = False
    color_idx = 0

    while True:
        print("\033[2J\033[H", end="")
        
        print_maze(generator, show_path, color_idx)
        print("\n==== A-Maze-ing ====")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

        try:
            choice = input("Choice? (1-4): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\033[2J\033[H", end="")
            print("Exiting A-Maze-ing...")
            sys.exit(0)

        if choice == '1':
            generator.generate_maze()
            generator.maze_solver()
        elif choice == '2':
            show_path = not show_path
        elif choice == '3':
            color_idx += 1
        elif choice == '4':
            print("\033[2J\033[H", end="")
            print("Exiting A-Maze-ing...")
            sys.exit(0)
