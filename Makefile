virtual-env:
	(. dev/bin/activate)
	pip install -r requirements_dev.txt


runserver:
	make virtual-env
	cd src/; \
		python manage.py collectstatic --noinput; \
		python manage.py runserver 8080;


check-lint:
	make -s virtual-env
	flake8 src/
	# Called from root to auto read config file "setup.cfg"


check-type:
	make -s virtual-env
	mypy src/


check:
	make -s check-lint
	make -s check-type


tox:
	make -s virtual-env
	- rm -r .tox
	tox src/
