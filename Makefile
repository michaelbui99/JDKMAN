PY := python3

build:
	@echo "Building JDKMAN..."
	${PY} setup.py build

clean:
	${PY} setup.py clean

install: build
	${PY} -m pip install .

uninstall:
	${PY} -m pip uninstall jdkman