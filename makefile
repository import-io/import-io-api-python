PACKAGE=importio2
VERSION=$(shell python -c "from $(PACKAGE).version import __version__ ; print(__version__)")
TAR_FILE=dist/$(PACKAGE)-$(VERSION).tar.gz

all: clean install 

install: build
	python setup.py install

build:
	python setup.py sdist

doc:
	pandoc -f markdown -t plain README.md > README.txt

rebuild: clean install

upload:
	python setup.py sdist upload
	
clean:
	/bin/rm -rf build dist site MANIFEST
	pip freeze | grep "$(PACKAGE)==$(VERSION)" && pip uninstall -y $(PACKAGE)
