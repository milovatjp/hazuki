init:
	pip install -r requirements.txt

venv:
	python3.10 -m venv .venv

venv-activate:
	source venv/bin/activate