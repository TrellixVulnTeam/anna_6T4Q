export PYTHONPATH=$(PWD)

venv: .venv/bin/activate

.venv/bin/activate:
	@test -d .venv || python3 -m venv --clear .venv
	.venv/bin/python -m pip install -Ur requirements.txt
	@touch .venv/bin/activate

datasets: venv
	@.venv/bin/python anna/data/main.py data

test: venv
	@.venv/bin/python setup.py test

run: venv
	@.venv/bin/python anna/main.py data

notebook: venv
	@. .venv/bin/activate && jupyter notebook --notebook-dir=notebook

clean:
	rm -rf .venv

.PHONY: venv datasets test run clean notebook
