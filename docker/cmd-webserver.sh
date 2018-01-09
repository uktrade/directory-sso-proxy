#!/bin/bash -xe

gunicorn config.wsgi --bind 0.0.0.0:$PORT
