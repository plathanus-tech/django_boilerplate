runserver:
	cd src/; \
		pdm run python manage.py collectstatic --noinput; \
		pdm run python manage.py runserver 8080;


checks:
	- rm -r .tox
	pdm run tox src/
	make print-finished


coverage:
	- rm .coverage
	- rm -r htmlcov
	pdm run coverage run --source=src/ --rcfile=.coveragerc -m pytest src/
	pdm run coverage html
	google-chrome htmlcov/index.html
	make print-finished


# Printing Definitions
bold := $(shell tput bold)
blue := $(shell tput setaf 4)
green := $(shell tput setaf 2)
sgr0 := $(shell tput sgr0)

print-finished:
	@printf '$(blue) Done -$(green)$(bold) :)$(sgr0)'
	 
