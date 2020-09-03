# eMenu

###Requirements and installation
eMenu API requires at least Python 3.6.\
Before installing libraries for application set up your virtual environment. Execute following commands:
```
pip install virtualenv
virtualenv nameofyourvenv
source nameofyourvenv/bin/activate
``` 
After preparing your virtual env run `pip install -r requirements.txt` to install all required libraries.\
Application requires to run following commands in `eMenu` directory:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
The two first ones prepares database to usage and the last one creates your user.\
If you want to have working daily reporter you need to set parameters `EMAIL_HOST` and `EMAIL_PORT` in 
`eMenu/eMenu/settings.py` which provides to your email server (`EMAIL_HOST_USER` `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS` 
and `EMAIL_USE_SSL` only if are needed). Also is need creating cron. Run `crontab -e` and provide following entry: 
`0 10 * * * /pathToPythonVirtualenv/python eMenu/manage.py sendreport` but remember to set proper path to your virtual 
environment with python.

###Starting
Run command `python manage.py runserver` in `eMenu` directory to start application.\
Application is going to run on localhost with port 8000. Swagger documentation is available at 
http://localhost:8000/swagger.