init:
	pip install -r requirements.txt

venv:
	python3.9 -m venv .venv3.9

venv-activate:
	source venv/bin/activate