#!/bin/bash

gunicorn --timeout 100 --bind 0.0.0.0:${PORT} wsgi_app:app
