# viasofie
I'm using a virtualenv in python, your probably don't have to use it. (workon viasofie)

if you change anything in the model, don't forget to "python manage.py makemigrations" -> "python manage.py migrate"
***
To update the localization files, edit the .po files with a text editor.

django-admin makemessages -l en

OR

run django-admin makemessages -l fr

OR

run django-admin makemessages -l nl blkartbkatktrkba

AND

django-admin compilemessages
***
when having errors with classytags:
pip install django-classy-tags

when having errors with easy_thumbnails:
pip install easy_thumbnails
***

account for user control panel = test : test12345
account fro admin = admin : password123

