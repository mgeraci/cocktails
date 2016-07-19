Cocktails
=========

Cocktails is a simple web app to manage cocktail recipes. It's written in
Django.

Installation
------------

* clone the repo
* `mkvirtualenv cocktails`
* `pip install -r requirements.txt`
* add the file `cocktails/cocktails/localsettings.py`, with the following contents:

    DEBUG = True
    STATIC_ROOT = 'staticfiles'
    STATIC_URL = '/static/'
    SECRET_KEY = '[your secret key]'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '[your database name]',
            'USER': '[your database user]',
            'PASSWORD': '[your database user password]'
        }
    }

* `./cocktails/manage.py migrate`
* `./cocktails/manage.py runserver`

CSS and JS
----------

CSS is written using SASS, JS is in coffeescript, and both are managed with
gulp. The coffee is compiled with webpack. Assuming you already have node and
npm installed, to install all of the packages required to compile these files,
run:

	npm install

Then to start gulp watching and compiling the files, run:

	gulp

Deployment Notes
----------------

Mostly for my own use, to deploy:

* create a python application for the app and a static php application for the
  static files
* create domains for each
* create a database and database user, add those to localsettings.py
* tell apache what python file to run on start, by editing apache2/conf/httpd.conf
* delete DirectoryIndex and DocumentRoot, and the <Directory> block
* Add WYSGIPythonPath
* Change WSGIDaemonProcess to use the python in our virtualenv

		WSGIPythonPath [path-to-app]/michael_cocktails:[path-to-app]/michael_cocktails/cocktails:/home/katur/.virtualenvs/michael_cocktails/lib/python2.7/site-packages:/home/katur/.virtualenvs/michael_cocktails/lib/python2.7
		WSGIDaemonProcess michael_cocktails processes=2 threads=12 python-path=[path-to-app]/michael_cocktails:[path-to-app]/michael_cocktails/cocktails:/home/katur/.virtualenvs/michael_cocktails/lib/python2.7/site-packages:/home/    katur/.virtualenvs/michael_cocktails/lib/python2.7 27 WSGIPythonPath [path-to-app]/michael_cocktails:[path-to-app]/michael_cocktails/cocktails:/home/katur/.virtualenvs/michael_cocktails/lib/python2.7/site-packages:/home/katur/.virtualenvs/michael_cocktails/lib/python2.7
		WSGIScriptAlias / [path-to-app]/michael_cocktails/cocktails/cocktail/wsgi.py

To deploy updates:

* `git pull`
* `./cocktails/manage.py collectstatic`
