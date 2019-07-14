# Doppeldenk

Spacetrading is a boardgame under development from the designers of EuroCrisis (Doppeldenk Spiele). This repository contains a web application that enables us to test the game online and generate printing material for a prototype to test it offline.

## Deployed

[On heroku](https://whispering-hollows-23926.herokuapp.com/).

## Getting started

Follow the MDN Django Tutorial on [setting up Django](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment) and [preparing it for Heroku](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment#Update_the_app_for_Heroku):

~~~bash
# Tested in clean Ubuntu 18.04.2 LTS VM
sudo apt install git
mkdir workspace
cd workspace
git clone git@github.com:claudiobierig/doppeldenk.git
cd doppeldenk

# Setup database
sudo apt-get install libpq-dev postgresql postgresql-contrib
sudo -u postgres psql
#################### in psql commandline
CREATE USER admin WITH PASSWORD 'admin';
CREATE DATABASE doppeldenk;
\q
####################

sudo apt-get install python3-pip python3-dev
sudo pip3 install virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS=' -p /usr/bin/python3 '
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh
source ~/.bashrc
#now in virtualenv
mkvirtualenv doppeldenk
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser #user: admin, pw: admin, bypass security for local setup
python manage.py runserver
~~~

For deploying to heroku follow the tutorial a bit longer.

## Run Tests

~~~bash
# Testcases only include the correct implementation of the rules
# Testcases also generate printing material
python3 manage.py test
~~~

## Open Points

Listed in TODO.md

## Generate Prototype

~~~bash
sudo apt-get install pdfposter
cd printing_material
bash generate_printing_material.sh
~~~

The printing material should be located in the same folder. Html pages need to be printed with 200% Zoom.

## License

Used artwork and software is listed with the according license in ACKNOWLEDGEMENT.md. The rest of the project is under the [MIT](https://opensource.org/licenses/MIT) license.
