help:
	@echo "  env         install all production dependencies"
	@echo "  dev         install all production and development dependencies"
	@echo "  docs        build documentation"
	@echo "  clean       clean working directory"
	@echo "  lint        check style with pycodestyle"
	@echo "  test        run tests"
	@echo "  build       build the distribution"
	@echo "  coverage    run tests with code coverage"

env:
	pip install -r requirements.txt

dev: env
	pip install -r requirements.dev.txt
	pip install -r requirements.docs.txt

docs:
	$(MAKE) -C doc html

clean:
	rm -fr htmlcov
	rm -fr dist
	rm -fr .eggs
	rm -fr *.egg-info
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;

lint:
	pycodestyle --config=setup.cfg hyperwallet

test: dev lint
	python setup.py test

build: clean
	python setup.py check
	python setup.py sdist

coverage: clean
	coverage run setup.py test
	coverage html
	coverage report
