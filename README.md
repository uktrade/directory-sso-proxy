# directory-sso-proxy

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gitflow-image]][gitflow]
[![calver-image]][calver]

---

## Development

### Installing

    $ git clone https://github.com/uktrade/directory-sso-proxy
    $ cd directory-sso-proxy
    $ virtualenv .venv -p python3.6
    $ source .venv/bin/activate
    $ make requirements

### Getting started

    $ make webserver

### Requirements

[Python 3.6.12](https://www.python.org/downloads/release/python-3612/)

[Postgres](https://www.postgresql.org/)

[Redis](https://redis.io/)

### Configuration

Secrets such as API keys and environment specific configurations are placed in `conf/env/secrets-do-not-commit` - a file that is not added to version control. To create a template secrets file with dummy values run `make secrets`.

### Commands

| Command                      | Description                              |
| ---------------------------- | ---------------------------------------- |
| make clean                   | Delete pyc files                         |
| make pytest                  | Run all tests                            |
| make pytest test_foo.py      | Run all tests in file called test_foo.py |
| make pytest -- --last-failed | Run the last tests to fail               |
| make pytest -- -k foo        | Run the test called foo                  |
| make pytest -- <foo>         | Run arbitrary pytest command             |
| make manage <foo>            | Run arbitrary management command         |
| make webserver               | Run the development web server           |
| make requirements            | Compile the requirements file            |
| make install_requirements    | Installed the compile requirements file  |
| make secrets                 | Create your secret env var file          |
| make flake8                  | Run flake8 linting                       |
| make checks                  | Run black, isort, flake8 in check mode   |
| make autoformat              | Run black and isort in file-writing mode |

## Helpful links

-   [Developers Onboarding Checklist](https://uktrade.atlassian.net/wiki/spaces/ED/pages/32243946/Developers+onboarding+checklist)
-   [Gitflow branching](https://uktrade.atlassian.net/wiki/spaces/ED/pages/737182153/Gitflow+and+releases)
-   [GDS service standards](https://www.gov.uk/service-manual/service-standard)
-   [GDS design principles](https://www.gov.uk/design-principles)

## Related projects:

https://github.com/uktrade?q=directory
https://github.com/uktrade?q=great

[code-climate-image]: https://codeclimate.com/github/uktrade/directory-sso-proxy/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/directory-sso-proxy
[circle-ci-image]: https://circleci.com/gh/uktrade/directory-sso-proxy/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-sso-proxy/tree/master
[codecov-image]: https://codecov.io/gh/uktrade/directory-sso-proxy/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-sso-proxy
[gitflow-image]: https://img.shields.io/badge/Branching%20strategy-gitflow-5FBB1C.svg
[gitflow]: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow
[calver-image]: https://img.shields.io/badge/Versioning%20strategy-CalVer-5FBB1C.svg
[calver]: https://calver.org
