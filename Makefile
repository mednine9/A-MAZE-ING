PYTHON = python3
PIP = pip3
ENTRY = a_maze_ing.py
CONFIG = config.txt

install:
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy build
	$(PIP) install -e ./mazegen

run:
	$(PYTHON) $(ENTRY) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(ENTRY) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf mazegen/build mazegen/dist mazegen/*.egg-info
	rm -f maze.txt

lint:
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

.PHONY: install run debug clean lint