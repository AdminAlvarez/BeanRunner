PYTHON ?= python3

.PHONY: all check run test clean re

all: check

check:
	$(PYTHON) -c "from pathlib import Path; files = [*Path('src').rglob('*.py'), *Path('tests').rglob('*.py'), *Path('verif/scripts').rglob('*.py')]; [compile(path.read_text(encoding='utf-8'), str(path), 'exec') for path in files]"

run:
	$(PYTHON) -m src.main

test:
	$(PYTHON) -m unittest discover -s tests -v
	$(PYTHON) verif/scripts/verify_hito1.py

clean:
	$(PYTHON) -c "import pathlib, shutil; roots = ('src', 'tests', 'verif/scripts'); [shutil.rmtree(path) for root in roots for path in pathlib.Path(root).rglob('__pycache__') if path.is_dir()]"

re: clean all