SHELL=/bin/bash
PYTHON=python3.8
PIP=pip

create-env:
	$(PYTHON) -m venv venv
	echo "RUN: source/venv/activate to activate recently created environment."

install:
	$(PIP) install -r requirements.txt

make-migrations:
	$(PYTHON) manage.py makemigrations $(APP)

migrate:
	$(PYTHON) manage.py migrate

serve:
	$(PYTHON) manage.py runserver

createsuperuser:
	$(PYTHON) manage.py createsuperuser

clean-db:
	rm -rf db.sqlite3

clean-migrations:
	echo "Cleaning Migrations..."
	rm -rf **/migrations

clean-db-with-migration: clean-db clean-migrations

clean-env:
	rm -rf venv

clean: clean-db clean-env clean-migrations

build:
	$(PYTHON) manage.py migrate

shell:
	$(PYTHON) manage.py shell

collect-static:
	$(PYTHON) manage.py collectstatic

get-token:
	$(PYTHON) manage.py  drf_create_token $(USER)

isort:
	isort .

pylint:
	DJANGO_SETTINGS_MODULE=backend.settings pylint --load-plugins pylint_django accounts

black:
	black accounts backend cart homepage_content item item_group log reviews transaction utils manage.py passenger_wsgi.py
