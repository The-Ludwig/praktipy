.phony= test install dev release

install:
	python3 setup.py install

test:
	python -m unittest discover

# Setup dev environment & install package
dev:
	pip install -e .[dev]

# Build & upload to test.pypi.org for manual verification
release:
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	twine check dist/*

	twine upload --repository testpypi dist/*
