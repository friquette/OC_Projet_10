# OC_Projet_10
Créez une API sécurisée RESTful en utilisant Django REST

## Set up the project
This project runs in python 3

Make a copy of this project on your hard drive <br>
`git clone https://github.com/friquette/OC_Projet_10.git`

Go in the root project and create a virtual environment <br>
`cd OC_Projet_10` <br>
`python -m venv env`

Activate your virtual environment <br>
- On Windows `env\Scripts\activate.bat`
- On Mac OS/Linux `source env/bin/activate`

Go in the project folder
`cd softdesk`

Install the packages <br>
`pip install -r requirements.txt`

## How to use it
For the first time you are using the application, migrate the tables in the database<br/>
`python manage.py migrate`

Run your server</br>
`python manage.py runserver` </br>

The database will be created in the root application folder and 
is named db.sqlite3 </br>

Before sending the application online, open the settings.py file in softdesk folder, 
and change the `DEBUG = True` to `DEBUG = False`

To interrupt your server, simply hit `CTRL+C` in your command prompt.

## Admin part

To create an admin user, go to the root application folder and enter:
`python manage.py createsuperuser`
and follow the instructions.

To access the admin site page, go to
`localhost:8000/admin` in your web browser.

## Documentation

To see the full document of the API, go to
`https://documenter.getpostman.com/view/14738930/UVC6k7JR`
