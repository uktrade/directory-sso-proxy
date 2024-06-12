ARGUMENTS = $(filter-out $@,$(MAKECMDGOALS)) $(filter-out --,$(MAKEFLAGS))

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

install_requirements:
	pip install --upgrade pip
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


# Usage: make pytest_single <path_to_file>::<method_name>
pytest_single:
	ENV_FILES='secrets-do-not-commit,test,dev' \
	pytest \
	    $(ARGUMENTS)
            --junit-xml=./results/pytest_unit_report.xml \
	    --cov-config=.coveragerc \
	    --cov-report=html \
	    --cov=. \

pytest_codecov:
	ENV_FILES='secrets-do-not-commit,test,dev' \
	pytest \
		--junitxml=test-reports/junit.xml \
		--cov-config=.coveragerc \
		--cov-report=term \
		--cov=. \
		--codecov \
		$(ARGUMENTS)

requirements:
	pip-compile requirements.in
	pip-compile requirements_test.in

secrets:
	@if [ ! -f ./conf/env/secrets-do-not-commit ]; \
		then sed -e 's/#DO NOT ADD SECRETS TO THIS FILE//g' conf/env/secrets-template > conf/env/secrets-do-not-commit \
			&& echo "Created conf/env/secrets-do-not-commit"; \
		else echo "conf/env/secrets-do-not-commit already exists. Delete first to recreate it."; \
	fi

webserver:
	ENV_FILES='secrets-do-not-commit,dev' python manage.py runserver 0.0.0.0:8004 $(ARGUMENTS)

.PHONY: autoformat clean install_requirements manage preflight pytest requirements webserver
