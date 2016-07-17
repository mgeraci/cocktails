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
