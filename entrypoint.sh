#!/bin/bash

if [ -z "$FLAG" ]; then
    echo "ERROR: FLAG environment variable is not set"
    exit 1
fi

exec gunicorn -w 2 -b 0.0.0.0:5000 "app:create_app()"
