#!/bin/bash

# Name of the application
NAME="aaa"
# Django project directory
DJANGODIR=/home/sk/aaa/aaa
# we will communicte using this unix socket
SOCKFILE=/home/sk/aaa/run/gunicorn.sock
# the user to run as
USER=sk
# the group to run as
# how many worker processes should Gunicorn spawn
NUM_WORKERS=3
# which settings file should Django use
DJANGO_SETTINGS_MODULE=aaa.settings
# WSGI module name
DJANGO_WSGI_MODULE=aaa.wsgi
echo "Starting $NAME as `whoami`"
# Activate the virtual environment
cd $DJANGODIR
source ../bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
# Create the run directory if it doesn't exist
$LOGFILE=/home/sk/aaa/logs/gunicorn.log


# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--user=$USER  \
--bind=unix:$SOCKFILE \
--log-level=debug \
--log-file= $LOGFILE