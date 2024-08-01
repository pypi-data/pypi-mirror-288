# del old build
rm -rf build
rm -rf dist
rm -rf generator_cucumber.egg-info
# setuptools
pip3 install setuptools
# twine
pip3 install twine
# build
pip3 install build
# public
pyproject-build && twine upload --skip-existing dist/*