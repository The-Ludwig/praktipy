#!/bin/bash
rm -rf dist/*
python setup.py sdist bdist_wheel
twine check dist/*

# upload to test.pypi.org for manual verification
twine upload --repository pypi dist/*
