print(" * Loading Templeton...")

import interlink
from werkzeug.utils import import_string, cached_property
from __init__ import app

def __doc__():
  '''
Templeton is like the butler used to fetch the templates, and fill in
the proper parameters. Most of templeton works under the hood, so if
done well, you won't notice it's there.

The easiest way to use templeton is to register its Blueprint's in your
app. There are three, `404` `500` `templetonBP`

    --> __init__.py
    from interlink.views import templetonBP
    app.register_blueprint(templetonBP)
    app.register_error_handler(404, url_not_found)
    app.register_error_handler(500, internal_error)
  '''
  
def tempulation(object):
  '''
Generate a new url_rule from interlinks templates.

Examples:

      from flask import Flask
      from interlink import tempulation
      app = Flask(__name__)
      app.add_url_rule('/', view_func=tempulation('yourapplication.views.index'))
      app.add_url_rule('/user/<username>', view_func=tempulation('yourapplication.views.user'))

      # make a new tempulator
      def myNewTempulator(import_name, url_rules=[], **options):
          view = tempulation(f"@{app_name@}.@{import_name@}")
          for url_rule in url_rules:
            app.add_url_rule(url_rule, view_func=view, **options)
  '''
  def __init__(self, import_name):
      self.__module__, self.__name__ = import_name.rsplit('.', 1)
      self.import_name = import_name
  @cached_property
  def view(self):
      return import_string(self.import_name)
  def __call__(self, *args, **kwargs):
      return self.view(*args, **kwargs)

def tempulator(import_name, url_rules=[], **options):
  '''
Templeton comes equiped with a tempulator, which runs off of
tempulations. The tempulator is used for flasks Lazy Loading URL's.
Remember that with templeton's tempulator, the generic templates are
only coming from `interlink.templeton.views`. If you want to change
where it's coming from you can use templeton's tempulation, and create a
new url loader function

[Flask Lazy Loading](https://flask.palletsprojects.com/en/3.0.x/patterns/lazyloading/#loading-late, "Flask Lazy Loading")

    --> views.py
    @templetonBP.route('/')
    @login
    def catalog():
      return tempulator("views.catalog", ['/catalog'])

    # add a single route to the index view
    tempulator('views.catalog', ['/catalog'])

    # add two routes to a single function endpoint
    url_rules = ['/catalog/','/catalog/<item>']
    tempulator('views.catalog', url_rules)
  '''
  view = tempulation(f"{__name__}.{import_name}")
  for url_rule in url_rules:
    app.add_url_rule(url_rule, view_func=view, **options)
