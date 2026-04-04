import sys
from config_parser.config_parser import ConfigParser
from mazegen.maze_gen import MazeGenerator
import visualizer


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    parser = ConfigParser(sys.argv[1])
    parser.parse()

    entry_row_col = (parser.entry[1], parser.entry[0])
    exit_row_col = (parser.exit[1], parser.exit[0])

    generator = MazeGenerator(
        height=parser.height,
        width=parser.width,
        entrance=entry_row_col,
        departure=exit_row_col,
        seed=parser.seed,
        perfect=parser.perfect
    )

    try:
        generator.generate_maze()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    path = generator.maze_solver()

    generator.save_to_file(parser.output_file, path)

    visualizer.interactive_loop(generator, parser.entry, parser.exit)


if __name__ == "__main__":
    main()
