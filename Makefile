.phony= test

install:
	python3 setup.py install

test:
	python -m unittest discover
