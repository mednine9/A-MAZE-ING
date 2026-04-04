import sys
from typing import Optional, Tuple
from collections import deque
from random import choice, random, seed as set_seed


class Cell:
    """Represents a single cell within the maze grid.

    Attributes:
        north (bool): True if the north wall is open, False if closed.
        east (bool): True if the east wall is open, False if closed.
        south (bool): True if the south wall is open, False if closed.
        west (bool): True if the west wall is open, False if closed.
        is_start (bool): Flag indicating if this is the entrance cell.
        is_end (bool): Flag indicating if this is the exit cell.
        is_path (bool): Flag indicating if this cell is part of the
        solution path.
        is_ftwo (bool): Flag indicating if this cell
        is part of the '42' pattern.
        next_block (str): Stores the direction of the next cell in the path.
    """

    def __init__(self,
                 value: int = 15,
                 is_start: bool = False,
                 is_end: bool = False,
                 is_path: bool = False,
                 is_ftwo: bool = False):
        """Initializes a cell with its specific wall configuration and states.

        Args:
            value (int, optional): The bitmask value representing closed walls.
            Defaults to 15 (all closed).
            is_start (bool, optional): Sets the cell as the maze entrance.
            Defaults to False.
            is_end (bool, optional): Sets the cell as the maze exit.
            Defaults to False.
            is_path (bool, optional): Marks the cell as part of the solution.
            Defaults to False.
            is_ftwo (bool, optional): Marks the cell as part of
            the '42' pattern. Defaults to False.
        """
        self.north: bool = bool(value & 1)
        self.east: bool = bool(value & 2)
        self.south: bool = bool(value & 4)
        self.west: bool = bool(value & 8)

        self.is_start = is_start
        self.is_end = is_end
        self.is_path = is_path
        self.is_ftwo = is_ftwo
        if is_path:
            self.next_block = ""

    def open_wall(self, direction: str) -> None:
        """Opens a specific wall of the cell.

        Args:
            direction (str): The cardinal direction of the wall to open
            ('north', 'south', 'east', 'west').
        """
        setattr(self, direction, True)

    def to_hex(self) -> str:
        """Serializes the cell's wall configuration
        into a hexadecimal character.

        Returns:
            str: A single uppercase hex character
            representing the closed walls.
        """
        value = (self.north * 1
                 + self.east * 2
                 + self.south * 4
                 + self.west * 8)
        return format(abs(15 - value), 'X')


class MazeGenerator:
    """Handles the procedural generation, solving, and saving of a maze.

    Attributes:
        height (int): The number of rows in the maze.
        width (int): The number of columns in the maze.
        entrance (Tuple[int, int]): The (row, col)
        coordinates of the start point.
        departure (Tuple[int, int]): The (row, col)
        coordinates of the end point.
        seed (Optional[int]): The seed for the random number generator.
        perfect (bool): Determines if the maze should have
        only one unique path.
        gen_maze (list[list[Cell]]): The 2D grid containing the Cell objects.
    """

    def __init__(self,
                 height: int,
                 width: int,
                 entrance: Tuple[int, int],
                 departure: Tuple[int, int],
                 seed: Optional[int],
                 perfect: bool):
        """Initializes the MazeGenerator with specified configurations.

        Args:
            height (int): The height of the maze grid.
            width (int): The width of the maze grid.
            entrance (Tuple[int, int]): Coordinates for the maze entry.
            departure (Tuple[int, int]): Coordinates for the maze exit.
            seed (Optional[int]): PRNG seed for reproducible generation.
            perfect (bool): True for a perfect maze, False
            for an imperfect maze.
        """
        self.height = height
        self.width = width
        self.entrance = entrance
        self.departure = departure
        self.seed = seed
        self.perfect = perfect
        self.gen_maze: list[list[Cell]] = []

    def generate_maze(self) -> list[list[Cell]]:
        """Generates the maze structure using an Iterative Depth-First Search.

        Returns:
            list[list[Cell]]: The fully generated 2D grid of Cell objects.
        """
        if self.seed is not None:
            set_seed(self.seed)

        self.gen_maze = [[Cell(0) for _ in range(self.width)]
                         for _ in range(self.height)]

        ent_r, ent_c = self.entrance
        ext_r, ext_c = self.departure
        self.gen_maze[ent_r][ent_c].is_start = True
        self.gen_maze[ext_r][ext_c].is_end = True

        if not (self.width < 10 or self.height < 7):
            self._embed_42_pattern()
        else:
            print(
                "Error: Maze size is too small to "
                "embed the '42' pattern.", file=sys.stderr)

        visited = [[self.gen_maze[r][c].is_ftwo for c in range(self.width)]
                   for r in range(self.height)]

        stack = [(ent_r, ent_c)]
        visited[ent_r][ent_c] = True

        directions = [
            (-1, 0, 'north', 'south'),
            (1, 0, 'south', 'north'),
            (0, 1, 'east', 'west'),
            (0, -1, 'west', 'east')
        ]

        while stack:
            curr_r, curr_c = stack[-1]
            unvisited_neighbors = []

            for dr, dc, wall, opp_wall in directions:
                nr, nc = curr_r + dr, curr_c + dc

                if 0 <= nr < self.height and 0 <= nc < self.width:
                    if not visited[nr][nc]:
                        unvisited_neighbors.append((nr, nc, wall, opp_wall))

            if unvisited_neighbors:
                nr, nc, wall, opp_wall = choice(unvisited_neighbors)

                self.gen_maze[curr_r][curr_c].open_wall(wall)
                self.gen_maze[nr][nc].open_wall(opp_wall)

                visited[nr][nc] = True
                stack.append((nr, nc))
            else:
                stack.pop()

        if not self.perfect:
            for r in range(1, self.height - 1):
                for c in range(1, self.width - 1):
                    if self.gen_maze[r][c].is_ftwo:
                        continue

                    cell = self.gen_maze[r][c]
                    closed_walls = []
                    directions_map = {
                        'north': (r - 1, c, 'south'),
                        'south': (r + 1, c, 'north'),
                        'east':  (r, c + 1, 'west'),
                        'west':  (r, c - 1, 'east')
                    }

                    for wall, (nr, nc, opp_wall) in directions_map.items():
                        if not getattr(cell, wall):
                            if not self.gen_maze[nr][nc].is_ftwo:
                                closed_walls.append((wall, nr, nc, opp_wall))

                    if len(closed_walls) >= 3 and random() < 0.4:
                        wall, nr, nc, opp_wall = choice(closed_walls)
                        cell.open_wall(wall)
                        self.gen_maze[nr][nc].open_wall(opp_wall)

        return self.gen_maze

    def _embed_42_pattern(self) -> None:
        """Embeds the required '42' structural
        block in the center of the grid."""
        four_two = [
            [0, 1, 0, 1, 0, 0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 1, 1, 0],
        ]

        rw_off = self.height // 2 - 2
        cl_off = self.width // 2 - 5

        for r, row in enumerate(four_two):
            for c, val in enumerate(row):
                if val:
                    if r == 0 and rw_off - 1 >= 0:
                        self.gen_maze[rw_off - 1][cl_off + c].south = False
                    self.gen_maze[rw_off + r][cl_off + c - 1].east = False
                    self.gen_maze[rw_off + r][cl_off + c] = Cell(0)
                    self.gen_maze[rw_off + r][cl_off + c].is_ftwo = True

    def maze_solver(self) -> list[Tuple[int, int]]:
        """Finds the shortest valid path from the
        entrance to the departure using BFS.

        Returns:
            list[Tuple[int, int]]: An ordered list of
            coordinates representing the path.
        """
        directions = {
            "east":  (0,  1),
            "west":  (0, -1),
            "south": (1,  0),
            "north": (-1, 0),
        }
        start = self.entrance
        departure = self.departure
        maze = self.gen_maze

        visited: dict[Tuple[int, int],
                      Optional[Tuple[int, int]]] = {start: None}
        queue = deque([start])

        while queue:
            r, c = queue.popleft()

            if (r, c) == departure:
                break

            for wall, (dr, dc) in directions.items():
                if not getattr(maze[r][c], wall):
                    continue
                nr, nc = r + dr, c + dc
                if (nr, nc) in visited:
                    continue
                if not (0 <= nr < len(maze) and 0 <= nc < len(maze[0])):
                    continue
                visited[(nr, nc)] = (r, c)
                queue.append((nr, nc))

        path = []
        current: Optional[Tuple[int, int]] = departure
        while current is not None:
            path.append(current)
            current = visited.get(current)
        path.reverse()

        dir_map = {
            (-1, 0): "N",
            (1, 0): "S",
            (0, 1): "E",
            (0, -1): "W"
        }

        for i in range(len(path)):
            r, c = path[i]
            maze[r][c].is_path = True

            if i < len(path) - 1:
                nr, nc = path[i + 1]
                dr, dc = nr - r, nc - c
                maze[r][c].next_block = dir_map[(dr, dc)]
            else:
                maze[r][c].next_block = ""

        return path

    def save_to_file(self, filename: str,
                     path_coords: list[Tuple[int, int]]) -> None:
        """Writes the generated maze and its solution to a text file.

        Args:
            filename (str): The target file path for the output.
            path_coords (list[Tuple[int, int]]): The solution path coordinates.

        Raises:
            IOError: If the file cannot be opened or written to.
        """
        try:
            with open(filename, 'w') as f:
                for row in self.gen_maze:
                    line = "".join([cell.to_hex() for cell in row])
                    f.write(line + "\n")

                f.write("\n")

                ent_r, ent_c = self.entrance
                ext_r, ext_c = self.departure
                f.write(f"{ent_c},{ent_r}\n")
                f.write(f"{ext_c},{ext_r}\n")

                dir_map = {(-1, 0): "N", (1, 0): "S",
                           (0, 1): "E", (0, -1): "W"}
                path_str = ""
                for i in range(len(path_coords) - 1):
                    r, c = path_coords[i]
                    nr, nc = path_coords[i+1]
                    path_str += dir_map[(nr - r, nc - c)]
                f.write(path_str + "\n")
        except IOError as e:
            print(f"File error: {e}")


if __name__ == "__main__":
    print("=== MazeGenerator Test ===")
    gen = MazeGenerator(height=21, width=21,
                        entrance=(0, 0), departure=(20, 20),
                        seed=42, perfect=True)
    maze = gen.generate_maze()
    for row in maze:
        for cell in row:
            print(cell.to_hex(), end="")
        print()

    path = gen.maze_solver()
    print(f"\nPath length: {len(path)}")
    print("Test completed.")
