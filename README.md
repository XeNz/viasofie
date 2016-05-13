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

If you get an error saying you need to get gettext download the following files:
http://ftp.gnome.org/pub/gnome/binaries/win32/dependencies/gettext-tools-0.17.zip
http://ftp.gnome.org/pub/gnome/binaries/win32/dependencies/gettext-runtime-0.17-1.zip
extract them in your programfiles folder and add it to your path. 
If you still get errors: set gettext.exe and xgettext.exe to compatibility mode for windows xp and run as admin.

***
when having errors with classytags:
pip install django-classy-tags

when having errors with easy_thumbnails:
pip install easy_thumbnails
***

account for user control panel = test : test12345
account fro admin = admin : password123

***
screen

screen -ls

screen screen -r PID
