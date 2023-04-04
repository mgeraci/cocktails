# Cocktails

Cocktails is a simple web app to manage cocktail recipes, written in Python,
using Django.

[cocktails.michaelgeraci.com](http://cocktails.michaelgeraci.com)

Features:

* Mobile-first responsive design
* Browse by ingredient, recipe, or source
* Search for recipes including an ingredient
* User authentication and private recipes
* Recipe multiplier for making larger batches
* Recipe entry with the Django Admin panel


## Installation

Assuming you have Python `3.9.0` or later:

* clone the repo
* `python -m venv cocktails-venv`
* `source cocktails-venv/bin/activate`
* `pip install -r requirements.txt`
* create a local database
* add the file `cocktails/localsettings.py` — see contents below
* `./manage.py migrate`
* `./manage.py createsuperuser` — you can use this to log in at localhost:8000/admin
* `./manage.py runserver`

Then you can visit localhost:8000 and you should see the site.

### localsetting.py

    DEBUG = True
    STATIC_ROOT = 'staticfiles'
    STATIC_URL = '/static/'

    # django's secret key
    SECRET_KEY = '[your secret key]'

    # create a user for login with a 4-digit password
    VIEWER_USERNAME = '[the username you create for the viewer]'

    # for sharing links, the production url (starting with `http`) must be
    # defined
    PRODUCTION_ROOT = 'https://cocktails.example.com'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '[your database name]',
            'USER': '[your database user]',
            'PASSWORD': '[your database user password]'
        }
    }


## CSS and JS

CSS is written using SASS, JS is in ES6, and both are managed with webpack.

The desired node Version is specified in `.nvmrc`. Assuming you have that
installed and activated (e.g. with `nvm use`), run `yarn install` to install
the JS packages required for this app.

Then to start webpack watching and compiling the files, run `yarn watch`. To
compile once and exit, run `yarn build`. Cachebusting is built into these
commands; filenames are created with a hash, and those hashes are stored in a
json file which python reads when creating the asset paths.


## Deployment Notes

Mostly for my own use, but to deploy:

* create a python application for the app and a static php application for the
  static files
* create domains for each
* create a database and database user, add those to localsettings.py
* add a virtualenv, and install the required packages:
	* `mkvirtualenv michael_cocktails`
	* `cd michael_cocktails`
	* `workon michael_cocktails`
	* `pip install -r requirements.txt`
	* `pip install --upgrade pip` if prompted
* in apache2/conf/httpd.conf:
	* delete `DirectoryIndex` and `DocumentRoot`, and the `<Directory>` block
	* Add `WYSGIPythonPath` — This is like a bash path, except it should point to the likely spots that python executables can be found:

			WSGIPythonPath [path-to-app]/michael_cocktails:[path-to-app]/michael_cocktails/cocktails:/home/katur/.virtualenvs/michael_cocktails/lib/python2.7/site-packages:/home/katur/.virtualenvs/michael_cocktails/lib/python2.7

	* Change WSGIDaemonProcess to use the python in our virtualenv:

			WSGIDaemonProcess michael_cocktails processes=2 threads=12 python-path=[path-to-app]/michael_cocktails:[path-to-app]/michael_cocktails/cocktails:[path-to-home]/.virtualenvs/michael_cocktails/lib/python2.7/site-packages:[path-to-home]/.virtualenvs/michael_cocktails/lib/python2.7

	* Add an alias to the wsgi executable

			WSGIScriptAlias / [path-to-app]/michael_cocktails/cocktails/cocktail/wsgi.py

* change any settings necessary in the static application (e.g., modify the `.htaccess` file to serve fonts with a longer expiration)

To deploy updates:

* `git pull`
* get static file updates, if necessary: `./cocktails/manage.py collectstatic`
* restart apache, if necessary: `./apache2/bin/restart`
