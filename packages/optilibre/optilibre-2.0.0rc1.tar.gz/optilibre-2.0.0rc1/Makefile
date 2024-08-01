pypi: build
	twine upload --repository optilibre dist/* --config ./.pypirc

testpypi: build
	twine upload --repository optilibre dist/* --config ./.pypirc-test

build: clean_pypi
		python3 -m build

clean_pypi:
		rm -rf build dist

install:
	pip install dist/optilibre-*.whl --force-reinstall
