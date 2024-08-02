# LEMA TOOLS

Python packages required in productions environments


Handle development
```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install setuptools twine
pip install .
python3 setup.py sdist
python3 -m twine upload dist/*
```