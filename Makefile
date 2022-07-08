all: .venv3
	.venv3/bin/python3 -m basecmd -h
	.venv3/bin/python3 -m basecmd -v debug

clean:
	rm -rf build dist *.egg-info  __pycache__

tidy: clean
	rm -rf .venv3

dist: setup.cfg .venv3
	.venv3/bin/python3 -m build -n
	
pypi: clean dist
	.venv3/bin/twine upload dist/*

.venv3:
	[ -d $@ ] || python3 -m venv $@
	.venv3/bin/pip3 install -U pip wheel build twine
	.venv3/bin/pip3 install --editable .
	touch $@
