#!/bin/bash

function makemigrations(){
python manage.py makemigrations
}
function migrate(){
python manage.py migrate
}
function runserver(){
python manage.py runserver
}
function a (){
python manage.py $1 $2
}
function push() {
cd ..
git add aaa
git commit -m 'x'
git push origin main

}
