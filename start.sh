#!/bin/sh

# Run the python script to initialize the database
python migrate.py

# Then start gunicorn (using the command you previously had in your Dockerfile)
# Using `exec` ensures Gunicorn replaces the shell script process and handles signals correctly
exec gunicorn --bind 0.0.0.0:5001 --workers 2 --timeout 120 --access-logfile - --error-logfile - app:app