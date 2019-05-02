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
    $ pip install -r requirements_text.txt

### Requirements

[Python 3.6](https://www.python.org/downloads/release/python-360/)

### Configuration

Secrets such as API keys and environment specific configurations are placed in `conf/.env` - a file that is not added to version control. You will need to create that file locally in order for the project to run.

Here are the env vars to get you going:

```
TEST_IP_RESTRICTOR_SKIP_SENDER_ID=debug
TEST_IP_RESTRICTOR_SKIP_SENDER_SECRET=debug
TEST_SSO_HEALTHCHECK_TOKEN=debug
SSO_SIGNATURE_SECRET=debug
SSO_UPSTREAM=debug
```

### Run the webserver

    $ make debug_webserver

### Run debug tests

    $ make debug_test

## Helpful links
* [Developers Onboarding Checklist](https://uktrade.atlassian.net/wiki/spaces/ED/pages/32243946/Developers+onboarding+checklist)
* [Gitflow branching](https://uktrade.atlassian.net/wiki/spaces/ED/pages/737182153/Gitflow+and+releases)
* [GDS service standards](https://www.gov.uk/service-manual/service-standard)
* [GDS design principles](https://www.gov.uk/design-principles)

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
