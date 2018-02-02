build: docker_test

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

test_requirements:
	pip install -r requirements_test.txt

FLAKE8 := flake8 . --exclude=migrations,.venv
PYTEST := pytest . --cov=. $(pytest_args) --capture=no
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

DOCKER_COMPOSE_REMOVE_AND_PULL := docker-compose -f docker-compose.yml -f docker-compose-test.yml rm -f && docker-compose -f docker-compose.yml -f docker-compose-test.yml pull
DOCKER_COMPOSE_CREATE_ENVS := ./docker/create_envs.sh

docker_run:
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose up --build

DOCKER_SET_DEBUG_ENV_VARS := \
	export SSO_PROXY_PORT=8004; \
	export SSO_PROXY_DEBUG=true; \
	export SSO_PROXY_SIGNATURE_SECRET=proxy_signature_debug; \
	export SSO_PROXY_SSO_SIGNATURE_SECRET=signature_secret_debug; \
	export SSO_PROXY_SECRET_KEY=debug; \
	export SSO_PROXY_SSO_UPSTREAM=http://sso.trade.great.docker:8003; \
	export SSO_PROXY_PYTHONWARNINGS=all; \
	export SSO_PROXY_PYTHONDEBUG=true; \
	export SSO_PROXY_SECURE_HSTS_SECONDS=0; \
	export SSO_PORT=8003; \
	export SSO_DEBUG=true; \
	export SSO_SECRET_KEY=debug; \
	export SSO_POSTGRES_USER=debug; \
	export SSO_POSTGRES_PASSWORD=debug; \
	export SSO_POSTGRES_DB=sso_debug; \
	export SSO_DATABASE_URL=postgres://debug:debug@postgres:5432/sso_debug; \
	export SSO_SESSION_COOKIE_DOMAIN=.trade.great; \
	export SSO_SSO_SESSION_COOKIE=debug_sso_session_cookie; \
	export SSO_CSRF_COOKIE_SECURE=false; \
	export SSO_SESSION_COOKIE_SECURE=false; \
	export SSO_EMAIL_HOST=debug; \
	export SSO_EMAIL_PORT=debug; \
	export SSO_EMAIL_HOST_USER=debug; \
	export SSO_EMAIL_HOST_PASSWORD=debug; \
	export SSO_DEFAULT_FROM_EMAIL=debug; \
	export SSO_LOGOUT_REDIRECT_URL=http://buyer.trade.great:8001; \
	export SSO_REDIRECT_FIELD_NAME=next; \
	export SSO_ALLOWED_REDIRECT_DOMAINS=example.com,exportingisgreat.gov.uk,great; \
	export SSO_UTM_COOKIE_DOMAIN=.great; \
	export SSO_SIGNATURE_SECRET=signature_secret_debug; \
	export SSO_DEFAULT_REDIRECT_URL=http://buyer.trade.great:8001; \
	export SSO_SSO_PROFILE_URL=http://profile.trade.great:8006; \
	export SSO_DIRECTORY_API_EXTERNAL_CLIENT_BASE_URL=http://buyer.trade.great:8001/api/external/; \
	export SSO_DIRECTORY_API_EXTERNAL_SIGNATURE_SECRET=debug; \
	export SSO_EXOPS_APPLICATION_CLIENT_ID=debug; \
	export SSO_CACHE_BACKEND=locmem; \
	export SSO_SECURE_SSL_REDIRECT=false; \
	export SSO_HEALTH_CHECK_TOKEN=debug; \
	export SSO_GOOGLE_TAG_MANAGER_ID=debug; \
	export SSO_PROXY_PYTHONWARNINGS=all; \
	export SSO_PROXY_PYTHONDEBUG=true; \
	export SSO_PROXY_SECURE_SSL_REDIRECT=false; \
	export SSO_PROXY_HEALTH_CHECK_TOKEN=debug; \
	export SSO_PROXY_TEST_API_ENABLE=true; \
	export SSO_PROXY_TEST_API_AUTH_TOKEN=debug

docker_test_env_files:
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS)

DOCKER_REMOVE_ALL := \
	docker ps -a | \
	grep -e directory -e sso | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

docker_remove_all:
	$(DOCKER_REMOVE_ALL)

docker_debug: docker_remove_all
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose build && \
	docker-compose run --service-ports webserver make django_webserver

docker_webserver_bash:
	docker exec -it ssoproxy_webserver_1 sh

docker_test: docker_remove_all
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose -f docker-compose-test.yml build && \
	docker-compose -f docker-compose-test.yml run sut

DEBUG_SET_ENV_VARS := \
	export SECRET_KEY=debug; \
	export SIGNATURE_SECRET=proxy_signature_debug; \
	export SSO_SIGNATURE_SECRET=api_signature_debug; \
	export PORT=8004; \
	export DEBUG=true; \
	export SSO_UPSTREAM=http://sso.trade.great:8003; \
	export SECURE_HSTS_SECONDS=0; \
	export PYTHONWARNINGS=all; \
	export PYTHONDEBUG=true; \
	export SECURE_SSL_REDIRECT=false; \
	export HEALTH_CHECK_TOKEN=debug; \
	export SSO_HEALTH_CHECK_TOKEN=debug; \
	export TEST_API_ENABLE=true; \
	export TEST_API_AUTH_TOKEN=debug


debug_webserver:
	$(DEBUG_SET_ENV_VARS); $(DJANGO_WEBSERVER);

debug_shell:
	$(DEBUG_SET_ENV_VARS); ./manage.py shell

debug_test:
	$(DEBUG_SET_ENV_VARS) && $(FLAKE8) && $(PYTEST)

debug: test_requirements debug_test

integration_tests:
	cd $(mktemp -d) && \
	git clone https://github.com/uktrade/directory-tests && \
	cd directory-tests && \
	make docker_integration_tests

heroku_deploy_dev:
	docker build -t registry.heroku.com/directory-sso-proxy-dev/web .
	docker push registry.heroku.com/directory-sso-proxy-dev/web

compile_requirements:
	python3 -m piptools compile requirements.in

compile_test_requirements:
	python3 -m piptools compile requirements_test.in

compile_all_requirements: compile_requirements compile_test_requirements

.PHONY: build clean test_requirements docker_test docker_run docker_debug docker_webserver_bash docker_test debug_webserver debug_test debug heroku_deploy_dev smoke_tests
