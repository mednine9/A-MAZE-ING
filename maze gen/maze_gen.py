from typing import Optional, Tuple
from collections import deque
from time import time
from random import choice, random, seed as set_seed


class Cell:
    def __init__(self,
                 value: int = 15,
                 is_start: bool = False,
                 is_end: bool = False,
                 is_path: bool = False,
                 is_ftwo: bool = False):

        # True means wall is open
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
        """Opens a wall by setting its attribute to True."""
        setattr(self, direction, True)

    def to_hex(self) -> str:
        """Serialize back to a single hex character for the output file."""
        value = (self.north * 1
                 + self.east * 2
                 + self.south * 4
                 + self.west * 8)
        return format(abs(15 - value), 'X')


class MazeGenerator:
    def __init__(self,
                 height: int,
                 width: int,
                 entrance: Tuple[int, int],
                 departure: Tuple[int, int],
                 seed: Optional[int],
                 perfect: bool):
        self.height = height
        self.width = width
        self.entrance = entrance
        self.departure = departure
        self.seed = seed
        self.perfect = perfect
        self.benchmark = {
            "generation": 0.0,
            "solution": 0.0
        }
        self.gen_maze: list[list[Cell]] = [[]]

    def generate_maze(self) -> list[list[Cell]]:
        start_time = time()

        if self.seed is not None:
            set_seed(self.seed)

        # 1. Initialize grid with all walls closed (0 means closed in bitmask)
        self.gen_maze = [[Cell(0) for _ in range(self.width)]
                         for _ in range(self.height)]

        ent_r, ent_c = self.entrance
        ext_r, ext_c = self.departure
        self.gen_maze[ent_r][ent_c].is_start = True
        self.gen_maze[ext_r][ext_c].is_end = True

        # 2. Embed the "42" pattern if the maze is large enough
        if not (self.width < 10 or self.height < 7):
            self._embed_42_pattern()

        # 3. Create a visited grid for fast lookups.
        # We pre-mark the "42" cells as True so the algorithm avoids them.
        visited = [[self.gen_maze[r][c].is_ftwo for c in range(
            self.width)] for r in range(self.height)]

        # 4. The Iterative Depth-First Search
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
            for r in range(self.height):
                for c in range(self.width):
                    if self.gen_maze[r][c].is_ftwo:
                        continue

                    if r + 1 < self.height and not self.gen_maze[r + 1][c].is_ftwo:
                        if random() < 0.1:
                            self.gen_maze[r][c].open_wall('south')
                            self.gen_maze[r + 1][c].open_wall('north')

                    if c + 1 < self.width and not self.gen_maze[r][c + 1].is_ftwo:
                        if random() < 0.1:
                            self.gen_maze[r][c].open_wall('east')
                            self.gen_maze[r][c + 1].open_wall('west')

        self.benchmark["generation"] = time() - start_time
        return self.gen_maze

    def _embed_42_pattern(self) -> None:
        """Embeds the required 42 block in the center of the grid."""
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
        start_time = time()
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
            (-1, 0): "⮝",
            (1, 0): "⮟",
            (0, 1): "⮞",
            (0, -1): "⮜"
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

        self.benchmark["solution"] = time() - start_time

        return path


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

    print(f"\nMaze generated in {gen.benchmark['generation']:.4f} seconds")
    path = gen.maze_solver()
    print(f"Maze solved in {gen.benchmark['solution']:.4f} seconds")
    print(f"Path length: {len(path)}")
    print("Test completed.")
