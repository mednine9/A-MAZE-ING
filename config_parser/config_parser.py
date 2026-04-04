import sys
from typing import Dict, Tuple, Optional


class ConfigParser:
    """Parses and validates the A-Maze-ing configuration file."""

    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.width: int = 0
        self.height: int = 0
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (0, 0)
        self.output_file: str = ""
        self.perfect: bool = False
        self.seed: Optional[int] = None

    def parse(self) -> None:
        """Reads the file and extracts all configuration values."""
        raw_data: Dict[str, str] = {}

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, start=1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    if '=' not in line:
                        raise ValueError(
                            f"Line {line_num}: Invalid "
                            "syntax. Expected 'KEY=VALUE'.")

                    key, value = line.split('=', 1)
                    raw_data[key.strip()] = value.strip()

        except FileNotFoundError:
            self._fatal(
                f"Error: Configuration file '{self.filename}' not found.")
        except Exception as e:
            self._fatal(str(e))

        self._validate_and_assign(raw_data)

    def _validate_and_assign(self, data: Dict[str, str]) -> None:
        required_keys = ["WIDTH", "HEIGHT", "ENTRY",
                         "EXIT", "OUTPUT_FILE", "PERFECT"]

        for key in required_keys:
            if key not in data:
                self._fatal(
                    f"Error: Missing mandatory key '{key}' in config file.")

        try:
            self.width = int(data["WIDTH"])
            self.height = int(data["HEIGHT"])
            if self.width < 1 or self.height < 1:
                raise ValueError(
                    "WIDTH and HEIGHT must be strictly positive integers.")

            self.entry = self._parse_coords(data["ENTRY"], "ENTRY")
            self.exit = self._parse_coords(data["EXIT"], "EXIT")

            if not (0 <= self.entry[0] < self.width and
                    0 <= self.entry[1] < self.height):
                raise ValueError(
                    f"ENTRY coordinates {self.entry} "
                    "are outside the maze bounds.")
            if not (0 <= self.exit[0] < self.width and
                    0 <= self.exit[1] < self.height):
                raise ValueError(
                    f"EXIT coordinates {self.exit} "
                    "are outside the maze bounds.")
            if self.entry == self.exit:
                raise ValueError(
                    "ENTRY and EXIT coordinates cannot be exactly the same.")

            self.output_file = data["OUTPUT_FILE"]
            if not self.output_file:
                raise ValueError("OUTPUT_FILE cannot be empty.")

            perfect_str = data["PERFECT"].lower()
            if perfect_str == 'true':
                self.perfect = True
            elif perfect_str == 'false':
                self.perfect = False
            else:
                raise ValueError("PERFECT must be strictly 'True' or 'False'.")
            if "SEED" in data:
                self.seed = int(data["SEED"])

        except ValueError as ve:
            self._fatal(f"Configuration Error: {ve}")

    def _parse_coords(self, coord_str: str, key_name: str) -> Tuple[int, int]:
        """Safely splits an 'x,y' string into integer tuples.

        Args:
            coord_str (str): The raw coordinate string from the configuration.
            key_name (str): The name of the
            configuration key, used for error formatting.

        Returns:
            Tuple[int, int]: The parsed (column, row) coordinates.

        Raises:
            ValueError: If the string is incorrectly
            formatted or contains non-integers.
        """
        parts = coord_str.split(',')
        if len(parts) != 2:
            raise ValueError(f"{key_name} must be in the format 'x,y'.")
        try:
            return (int(parts[0].strip()), int(parts[1].strip()))
        except ValueError:
            raise ValueError(f"Coordinates for {key_name} must be integers.")

    def _fatal(self, message: str) -> None:
        """Prints a clean error to standard error and safely exits."""
        print(message, file=sys.stderr)
        sys.exit(1)
