clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

test_requirements:
	pip install -r requirements_test.txt

FLAKE8 := flake8 . --exclude=migrations,.venv
PYTEST := pytest . --ignore=node_modules --ignore=.venv --ignore=venv --cov=. --cov-config=.coveragerc --capture=no $(pytest_args)
CODECOV := \
	if [ "$$CODECOV_REPO_TOKEN" != "" ]; then \
	   codecov --token=$$CODECOV_REPO_TOKEN ;\
	fi

test:
	$(FLAKE8) && $(PYTEST) && $(CODECOV)

DJANGO_WEBSERVER := \
	python manage.py migrate; \
	python manage.py runserver 0.0.0.0:$$PORT

django_webserver:
	$(DJANGO_WEBSERVER)

DEBUG_SET_ENV_VARS := \
	export SECRET_KEY=debug; \
	export PORT=8004; \
	export DEBUG=true; \
	export SECURE_HSTS_SECONDS=0; \
	export PYTHONWARNINGS=all; \
	export PYTHONDEBUG=true; \
	export SECURE_SSL_REDIRECT=false; \
	export HEALTH_CHECK_TOKEN=debug; \
	export SSO_HEALTH_CHECK_TOKEN=debug; \
	export SSO_SIGNATURE_SECRET=api_signature_debug ;\
	export SSO_UPSTREAM=http://sso.trade.great:8003



debug_webserver:
	$(DEBUG_SET_ENV_VARS); $(DJANGO_WEBSERVER);

debug_shell:
	$(DEBUG_SET_ENV_VARS) && ./manage.py shell

debug_test:
	$(DEBUG_SET_ENV_VARS) && $(FLAKE8) && $(PYTEST)

debug_pytest:
	$(DEBUG_SET_ENV_VARS) && $(PYTEST)

debug: test_requirements debug_test

compile_requirements:
	python3 -m piptools compile requirements.in
	python3 -m piptools compile requirements_test.in

.PHONY: build clean test_requirements debug_webserver debug_test debug heroku_deploy_dev smoke_tests
