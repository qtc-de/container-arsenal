#!/bin/bash

chown 1000:1000 /dummy
export FLASK_APP=h2b.py
su-exec nobody flask run --host=127.0.0.1 --port=${FLASK_PORT}
