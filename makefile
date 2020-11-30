ARGUMENTS = $(filter-out $@,$(MAKECMDGOALS)) $(filter-out --,$(MAKEFLAGS))

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

install_requirements:
	pip install -r requirements_test.txt

manage:
	ENV_FILES='secrets-do-not-commit,dev' ./manage.py $(ARGUMENTS)

# configuration for black and isort is in pyproject.toml
autoformat:
	isort $(PWD)
	black $(PWD)

checks:
	isort $(PWD) --check
	black $(PWD) --check --verbose
	flake8 .

pytest:
	ENV_FILES='test,dev' pytest $(ARGUMENTS)

requirements:
	pip-compile requirements.in
	pip-compile requirements_test.in

secrets:
	cp conf/env/secrets-template conf/env/secrets-do-not-commit; \
	sed -i -e 's/#DO NOT ADD SECRETS TO THIS FILE//g' conf/env/secrets-do-not-commit

webserver:
	ENV_FILES='secrets-do-not-commit,dev' python manage.py runserver 0.0.0.0:8004 $(ARGUMENTS)

.PHONY: autoformat clean install_requirements manage preflight pytest requirements webserver
