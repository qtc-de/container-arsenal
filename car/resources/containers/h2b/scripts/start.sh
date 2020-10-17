#!/bin/bash

export FLASK_APP=h2b.py
flask run --host=127.0.0.1 --port=${FLASK_PORT}
