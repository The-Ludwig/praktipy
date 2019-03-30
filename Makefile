.phony= test install dev

args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`

install:
	python3 setup.py install

test:
	python3 -m unittest discover

# Setup dev environment & install package
dev:
	pip install -e .[dev]

release:
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	twine check dist/*

	# upload to test.pypi.org for manual verification
	twine upload --repository testpypi dist/*
