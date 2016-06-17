Viasofie project Groep 4 - Developer manual:

Requirements: 


We used Python 3.5.1 for this project. We recommend using a virtualenv to use Python 3.5.1 if you have another Python version installed.
-	PIP
-	virtualenv, virtualenvwrapper
-	Python 3.5.1
-	mysqlclient-python (https://github.com/PyMySQL/mysqlclient-python)
-	Downloaded Master from github project


Using virtualenv:


virtualenv –p PYTHONPATH VIRTUALENVNAME
or
mkvirtualenv –p PYTHONPATH VIRTUALENVNAME
PYTHONPATH = path to Python 3.5.1 executable
VIRTUALENVNAME = name you choose for the virtual env
workon VIRTUALENVNAME


Installing the project dependent requirements:


cd to the project folder
pip install  -r requirements.txt
	Normally all the correct requirements should be installed with this command.
	When having problems with the installation of Pillow look at this link. 
python manage.py runserver
or
python managy.py runserver 0.0.0.0:80 (when running on a server)
	The server should now be running.
	Try 127.0.0.1:8000 / public_IP_of_the_server:80 to access the website.
Changing the settings
-Change the SMTP server settings:
Find the following variables and change accordingly: EMAIL_USE_TLS,EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT
-Change the database settings:
Find the DATABASES variable.
-Change the allowed hosts:
Find the ALLOWED_HOSTS variable.
-Change the SITE URL:
Change the ‘domain’ and ‘name’ column in the django_site table in the database.
-Create a superuser:
django-admin createsuperuser

Current testdata:


Admin:
	Username: admin
	Password: password123
Test users:
	Username: test
	Password: password12345
	Username: test3
	Password: password12345

