# viasofie
I'm using a virtualenv in python, your probably don't have to use it. (workon viasofie)

if you change anything in the model, don't forget to "python manage.py makemigrations" -> "python manage.py migrate"
***
To update the localization files, edit the .po files with a text editor. 

django-admin makemessages -l en 

OR

run django-admin makemessages -l fr 

OR

run django-admin makemessages -l nl

AND

django-admin compilemessages
***
when having errors with classytags

pip install django-classy-tags
