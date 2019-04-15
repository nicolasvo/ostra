#!bin/bash

#python api/index.py
gunicorn --bind 0.0.0.0:$PORT wsgi:app
