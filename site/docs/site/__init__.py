# This file is used as a hub to import the functions of each of PADS API Libraries.
# Copyright Joe Corso armyglass@hotmail.com
'''
This is a collection of libraries written to work in Python’s flask framework. It will generate a form and report for any table in a database. It will also create the urls, and the navigation bar. You can customize your website by generating your own instance of the API; or you can register the Blueprint(e.g. app.register_blueprint(templetonBP)), which has its own set of templates etc. So essentially, if you create a database for a library like in all tutorials and you need a form template and a report template, it will generate the form or report from the table in the database, and fill in the details in the template. To render the page in the browser just type in the url which corresponds to the table name, or make a navigation bar to generate the links for you.
'''
# metadata
__version__ = '0.0.4'
__author__ = 'Joe Corso'
__date__ = '01-21-2024'
__updated__ = '03-18-2025'
__copyright__ = 'Copyright 2024 Joe Corso'
__license__ = 'MIT License'
__email__ = 'pads.email.address@gmail.com'
__status__ = 'Development'
__description__ = "Interlink will generate a form and report for any table in a database. It will also create the urls, and the navigation bar."

# formulator functions
from interlink.formulator import Generator

# templeton functions
from interlink.templeton import tempulator
from interlink.templeton.views import url_not_found, internal_error, templetonBP

# safe haven functions
from interlink.safeHaven import honeypot, backdoor, login

# toolkit functions
from interlink.toolkit import DB, get_script_path, site_map

print(f' * Interlink {__version__} is online')
