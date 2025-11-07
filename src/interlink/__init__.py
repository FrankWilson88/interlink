# This file is used as a hub to import the functions of each of PADS API Libraries.
# Copyright Joe Corso pads.email.address@hotmail.com

'''
Flask Generator for Forms, Reports, URLs and templates.

This is a collection of libraries written to work in Python’s flask framework. It will generate a form and report for any table in a database. It will also create the urls, and the navigation bar. You can customize your website by generating your own instance of the API; or you can register the Blueprint(e.g. app.register_blueprint(templetonBP)), which has its own set of templates.  
So essentially, if you create a database for a library like in all tutorials and you need a form template and a report template, it will generate the form or report from the table in the database, and fill in the details in the template. To render the page in the browser just type in the url which corresponds to the table name, or make a navigation bar to generate the links for you.

Examples:

Setting up interlink is very easy. It depends on mysql-connector, and flask. Which will be downloaded automatically when installed. Let's say we want to make a blog, and we have a database named "blog" with a table named "manifest". This documentation is not in the same scope of writing SQL, we will assume you've set up your blog any way you want. That's the beauty of interlink, it doesn't matter.

1. First create your database, and tables. Then build your flask project, activate your virtual env, and install interlink:  

```bash
        $ python -m venv path/to/venv/my_env
        $ . path/to/venv/my_env/bin/activate
        $ python -m pip install git+https://github.com/padsRepo/interlink.git
```

2. There are a few [enviroment variables](https://docs.python.org/3/library/os.html#os.environ) that need to be set to get full functionality from Interlink. These variables can be placed in an .env file for best practices. This documentation shows the full `__init__.py` file for easier reading.

```python
    __init__.py
        import os
        from flask import Flask, Blueprint, render_template, url_for
        from views import viewsBP

        KEY = os.urandom(16)
        os.environ['SECRET_KEY'] = str(KEY) # REQUIRED
        os.environ['DB_USER'] = '<username>' # REQUIRED
        os.environ['DB_PASS'] = '<password>' # REQUIRED
        os.environ['BASE_DIR'] = os.path.dirname(__file__)
        os.environ['LOG_DIR'] = os.environ.get('BASE_DIR') + '/log'
        os.environ['whitelist'] = '["127.0.0.1", "192.168.0.37"]' # REQUIRED
        os.environ['blacklist'] = '["71.71.71.71"]' # REQUIRED

        app = Flask(__name__)
        app.config.from_mapping(SECRET_KEY=os.environ.get('SECRET_KEY'))
        app.config['UPLOAD_FOLDER'] = 'repo/'

        from interlink import *
        app.register_blueprint(viewsBP) # Your views.py file
        app.register_blueprint(templetonBP) # Add to use interlinks templating engine
        app.register_error_handler(404, url_not_found) # From the templeton lib
        app.register_error_handler(500, internal_error) # From the templeton lib

        if debug == False:
         app.run(debug=True, host='0.0.0.0', port='8000')
         
```

3. The `templetonBP` has all the templates you need. There is a default admin, forms, reports, blog, login, index page, and its own documentation. It helps to load the `templetonBP` **after** your own library. If you have variables set outside the scope of the `__init__.py` file, interlink will not find them.  
Enter the URL into the browser, interlink also has it's own navigation bar:

```python
        127.0.0.1:8000/admin/blog
        127.0.0.1:8000/forms/blog/manifest
        127.0.0.1:8000/reports/blog/manifest
        127.0.0.1:8000/blog/manifest # for the blog you want everyone to see
        127.0.0.1:8000/admin/blog
        127.0.0.1:8000/copyright/
        127.0.0.1:8000/404/
        127.0.0.1:8000/500/
        127.0.0.1:8000/docs/<page>/ # the docs page for this library.
        127.0.0.1:8000/loginRequired/
        127.0.0.1:8000/login/
        127.0.0.1:8000/register/
        127.0.0.1:8000/index/
```

4. tying in navigation to interlink from your first index file.

Closing  

Modules:  
  formulator: Form and Report Generator  
  templeton: Template Generator  
  safeHaven: Security Guard  
  toolkit: Misc Tools  

Classes:  
  Generator: Object method used to query database  
  DB: Object method used to connect and close connection to database  
  Tempulation: Custom Views  

Functions:  
  tempulator: templates  
  honeypot: distraction  
  backdoor: entry way  
  login: check user  
  site_map: site map for SEO  
  url_not_found: 404 Error  
  internal_error: 500 Error  
  templetonBP: Templeton Templates  
'''

# metadata
__version__ = '0.1.7'
__author__ = 'Joe Corso'
__date__ = '01-21-2024'
__updated__ = '10-18-2025'
__copyright__ = 'Copyright 2024 Joe Corso'
__license__ = 'MIT License'
__email__ = 'pads.email.address@gmail.com'
__status__ = 'Development'
__description__ = "Flask Generator for Forms, Reports, URLs and templates."
#__all__ = ['formulator', 'templeton', 'safeHaven', 'toolkit']

from interlink.formulator import Generator
from interlink.templeton import Tempulation, tempulator
from interlink.templeton.views import templetonBP, url_not_found, internal_error
from interlink.safeHaven import honeypot, backdoor, login
from interlink.toolkit import DB, site_map
