import sys
from parcer import ConfigParser
from mazegen.maze_gen import MazeGenerator
import visualizer

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    # 1. Parsing
    parser = ConfigParser(sys.argv[1])
    parser.parse()

    # 2. Inversion des coordonnées (x,y) -> (y,x) (ligne, colonne) pour l'algorithme
    entry_row_col = (parser.entry[1], parser.entry[0])
    exit_row_col = (parser.exit[1], parser.exit[0])

    # 3. Génération
    generator = MazeGenerator(
        height=parser.height,
        width=parser.width,
        entrance=entry_row_col,
        departure=exit_row_col,
        seed=parser.seed, 
        perfect=parser.perfect
    )
    generator.generate_maze()
    path = generator.maze_solver()

    generator.save_to_file(parser.output_file, path)
    # 4. Affichage interactif
    # (On peut passer l'entry/exit original au visualizer s'il en a besoin)
    visualizer.interactive_loop(generator, parser.entry, parser.exit)

if __name__ == "__main__":
    main()