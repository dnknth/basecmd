all: .venv3
	.venv3/bin/python3 -m basecmd -h
	.venv3/bin/python3 -m basecmd -v debug

clean:
	rm -rf build dist *.egg-info

tidy: clean
	rm -rf .venv3

pypi: clean .venv3
	.venv3/bin/python3 -m build -n
	.venv3/bin/twine upload dist/*
	$(MAKE) clean

.venv3: setup.cfg
	[ -d $@ ] || python3 -m venv $@
	.venv3/bin/pip3 install -U pip wheel build twine
	.venv3/bin/pip3 install --editable .
	touch $@
