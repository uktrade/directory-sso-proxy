# directory-sso-proxy

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gemnasium-image]][gemnasium]

---

## Requirements
[Docker >= 1.10](https://docs.docker.com/engine/installation/)

[Docker Compose >= 1.8](https://docs.docker.com/compose/install/)

## Local installation

    $ git clone https://github.com/uktrade/directory-sso-proxy
    $ cd directory-sso-proxy
    $ make

## Running with Docker
Requires all host environment variables to be set.

    $ make docker_run

### Run debug webserver in Docker
Provides defaults for all environment variables.

    $ make docker_debug

### Run tests in Docker

    $ make docker_test

### Host environment variables for docker-compose
``.env`` files will be automatically created with ``env_writer.py``, based on ``env.json``


## Debugging

### Setup debug environment

    $ make debug

### Run debug webserver

    $ make debug_webserver

### Run debug tests

    $ make debug_test


[code-climate-image]: https://codeclimate.com/github/uktrade/directory-sso-proxy/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/directory-sso-proxy

[circle-ci-image]: https://circleci.com/gh/uktrade/directory-sso-proxy/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-sso-proxy/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-sso-proxy/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-sso-proxy

[gemnasium-image]: https://gemnasium.com/badges/github.com/uktrade/directory-sso-proxy.svg
[gemnasium]: https://gemnasium.com/github.com/uktrade/directory-sso-proxy
