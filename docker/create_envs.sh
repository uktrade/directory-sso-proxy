#!/bin/bash -xe

python ./docker/env_writer.py \
    ./docker/env.json \
    ./docker/env.test.json \
    ./docker/directory-sso/env.test.json \
    ./docker/directory-sso/env-postgres.test.json
