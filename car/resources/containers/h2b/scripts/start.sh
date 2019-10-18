#!/bin/bash

chown 1000:1000 /dummy
export FLASK_APP=h2b.py
flask run --host=0.0.0.0
