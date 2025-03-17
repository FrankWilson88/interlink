print(" * Loading Templeton...")

from werkzeug.utils import import_string, cached_property
from __init__ import app

class Tempulation(object):
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
  The tempulator is used for flasks Lazy Loading URL's.
  Remember that with templeton's tempulator, the generic templates are only comin from interlink.templeton.views
  If you want to change where it's coming you can use templeton's Tempulation, and create a new url loader function
  See the full docs here:
  https://flask.palletsprojects.com/en/3.0.x/patterns/lazyloading/#loading-late

  Examples:

  @templetonBP.route('/')
  @login
  def task():
    return tempulator("views.index", ['/'])

  # add a single route to the index view
  tempulator('views.index', ['/'])

  # add two routes to a single function endpoint
  url_rules = ['/user/','/user/<username>']
  tempulator('views.user', url_rules)
  '''
  view = Tempulation(f"{__name__}.{import_name}")
  for url_rule in url_rules:
    app.add_url_rule(url_rule, view_func=view, **options)
