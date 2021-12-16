virtual-env:
	(. dev/bin/activate)
	pip install -r requirements_dev.txt


runserver:
	make virtual-env
	cd src/; \
		python manage.py collectstatic --noinput; \
		python manage.py runserver 8080;


check:
	make -s virtual-env
	mypy src/
	flake8 src/
	# Called from root to auto read config file "setup.cfg"
	make -s print-finished


tox:
	make -s virtual-env
	- rm -r .tox
	tox src/
	make print-finished


coverage:
	make -s virtual-env
	- rm .coverage
	- rm -r htmlcov
	coverage run --source=src/ --rcfile=.coveragerc -m pytest src/
	coverage html
	google-chrome htmlcov/index.html
	make print-finished


# Printing Definitions
bold := $(shell tput bold)
blue := $(shell tput setaf 4)
green := $(shell tput setaf 2)
sgr0 := $(shell tput sgr0)

print-finished:
	@printf '$(blue) Done -$(green)$(bold) :)$(sgr0)'
	 
