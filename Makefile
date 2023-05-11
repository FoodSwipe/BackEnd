SHELL=/bin/bash
PYTHON=python
PIP=pip

ADMIN_EMAIL := admin@test.com
ADMIN_USERNAME := admin
ADMIN_PASSWORD := admin


create-admin:
	DJANGO_SUPERUSER_PASSWORD=$(ADMIN_PASSWORD) $(PYTHON) manage.py createsuperuser --username $(ADMIN_USERNAME) --email $(ADMIN_EMAIL) --noinput

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

.PHONY: prod
prod:
	gunicorn backend.wsgi:application --config gunicorn.py

createsuperuser:
	$(PYTHON) manage.py createsuperuser

clean-db:
	rm -rf db.sqlite3

clean-migrations:
	rm -rf **/migrations

load-fresh-migrations:
	make clean-migrations
	make make-migrations APP=accounts
	make migrate
	make make-migrations APP=item
	make make-migrations APP=item_group
	make make-migrations APP=reviews
	make make-migrations APP=cart
	make make-migrations APP=transaction
	make make-migrations APP=homepage_content
	make make-migrations APP=log
	make migrate

clean-db-with-migration: clean-db clean-migrations

super-fresh: clean-db-with-migration load-fresh-migrations create-admin

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

isort:
	isort .

black:
	black .

lint:
	black .
	isort .
