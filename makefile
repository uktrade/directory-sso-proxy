build: docker_test

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

test_requirements:
	pip install -r requirements_test.txt

FLAKE8 := flake8 . --exclude=migrations
PYTEST := pytest . --cov=. $(pytest_args) --capture=no

test:
	$(FLAKE8) && $(PYTEST)

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
	export SSO_PROXY_SECRET_KEY=debug; \
	export SSO_PROXY_SSO_SECRET=debug; \
	export SSO_PROXY_SSO_UPSTREAM=http://sso.trade.great.docker:8004

DOCKER_REMOVE_ALL := \
	docker ps -a | \
	grep -e sso_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

docker_remove_all:
	$(DOCKER_REMOVE_ALL)

docker_debug: docker_remove_all
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	docker-compose pull && \
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
	export SSO_SECRET=debug; \
	export PORT=8003; \
	export DEBUG=true; \
	export SSO_UPSTREAM=http://sso.trade.great.dev:8004

debug_webserver:
	$(DEBUG_SET_ENV_VARS); $(DJANGO_WEBSERVER);

debug_shell:
	$(DEBUG_SET_ENV_VARS); ./manage.py shell

debug_test:
	$(DEBUG_SET_ENV_VARS) && $(FLAKE8) && $(PYTEST)

debug: test_requirements debug_test

heroku_deploy_dev:
	docker build -t registry.heroku.com/directory-sso-proxy-dev/web .
	docker push registry.heroku.com/directory-sso-proxy-dev/web

heroku_deploy_demo:
	docker build -t registry.heroku.com/directory-sso-proxy-demo/web .
	docker push registry.heroku.com/directory-sso-proxy-demo/web

.PHONY: build clean test_requirements docker_test docker_run docker_debug docker_webserver_bash docker_test debug_webserver debug_test debug heroku_deploy_dev heroku_deploy_demo
