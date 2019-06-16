# Doppeldenk

Spacetrading is a boardgame under development from the designers of EuroCrisis (Doppeldenk Spiele). This repository contains a webapplication that enables us to test the game online and generate printing material for a prototype to test it offline.

## Deployed

[On heroku](https://whispering-hollows-23926.herokuapp.com/).

## Getting started

Follow the [MDN Django Tutorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment#Update_the_app_for_Heroku):

~~~bash
# Tested only under Ubuntu 18.04.2 LTS
# There might be additional requirements needed
sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
~~~

For deploying to heroku follow the tutorial a bit longer.

## Run Tests

~~~bash
# Testcases only include the correct implementation of the rules
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
