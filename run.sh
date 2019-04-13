#!/bin/sh

# Simple script that helps in pushing the package on pypi

# Remove existing build
rm -rf dist build

# Go to repository
cd pali

# move library modules on the top
ln -s src/*.py .

# Remove tests / examples from installation
rm -rf tests
mv LICENSE README.md setup.py ../
cd -
python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
cd pali

git clean -fX
git checkout .

