'''
Templeton is like the butler used to fetch the templates, fill in the proper parameters, and serve it to you on a silver platter. Templeton builds the skeleton website for you. All you have to do is type in the proper URL, or generate the navigation bar.

The easiest way to use templeton is to register its Blueprint's in your app. There are three; `404`, `500`, and `templetonBP`.  

```python
  __init__.py
      from interlink.templeton.views import templetonBP
      app.register_blueprint(templetonBP)
      app.register_error_handler(404, url_not_found)
      app.register_error_handler(500, internal_error)
```

The `templetonBP` has a default set of templates you can use to have a full website deployed. The URL's which Templeton uses are as follows:

```python
      127.0.0.1:8000/admin/<db>
      127.0.0.1:8000/forms/<db>/<table>
      127.0.0.1:8000/reports/<db>/<table>
      127.0.0.1:8000/<db>/<table> # for the blog you want everyone to see
      127.0.0.1:8000/admin/<db>
      127.0.0.1:8000/copyright/
      127.0.0.1:8000/404/
      127.0.0.1:8000/500/
      127.0.0.1:8000/docs/<page>/ # the docs page for this library.
      127.0.0.1:8000/loginRequired/
      127.0.0.1:8000/login/
      127.0.0.1:8000/register/
      127.0.0.1:8000/index/
```

Whatever the name of the database, type the name into the *db* parameter. Whatever the name of the table, type the name into the *table* parameter. It will generate a generic template for you.

The Tempulations are used to build a new url rule, based on the developers needs.  

> [!NOTE]  
> Remember that with templeton's tempulator, the generic templates are only coming from `interlink.templeton.views`. If you want to change where it's coming from you can use templeton's Tempulation, and create a new url loader function.

Templeton also comes equiped with a tempulator, which runs off of Tempulations. The tempulator is basically just [Flask Lazy Loading](https://flask.palletsprojects.com/en/3.0.x/patterns/lazyloading/#loading-late, "Flask Lazy Loading") URL's in a wrapper. This feature is used to route Templetons templates to a URL, but does not have an endpoint(e.g. does not load by default). It is used to add extra templates to the app, if needed, without added overhead to the base project. For example, if you make a blog, you should be able to build a blog without also loading the catalog from an ecommerce site into memory, and vice versa. By using the tempulator, you can load a blog without a journal, or an ecommerce site without a repository, or a snosberry without an everlasting gobbstopper. You can also use the tempulator to load one endpoint before the other. If you like templetons catalog view, and you're an ecommerce site you may want to load that as your index page. This would achieve those results. If you like the admin page, but need it rerouted to another URL, you would use templulator.

'''
from werkzeug.utils import import_string, cached_property

class Tempulation(object):
  '''
Generate a new url_rule from any view within your project. This is used if you would like to map out url rules for each of your own endpoints.  

Examples:

    # Use the Tempulation's to create a new URL:
    app.add_url_rule('/dash', view_func=Tempulation('interlink.templeton.views.dashboard'))

    # make a new tempulator
    def myNewTempulator(import_name, url_rules=[], **options):
        view = Tempulation(f"@{app_name@}.@{import_name@}")
        for url_rule in url_rules:
          app.add_url_rule(url_rule, view_func=view, **options)

  '''
  
  def __init__(self, import_name):
    '''
Initialize the Tempulation object. This will hold the variable for the new url_rule.  
  
Args:  
    object (str): Endpoint for new view
    '''
    self.__module__, self.__name__ = import_name.rsplit('.', 1)
    self.import_name = import_name
  @cached_property
  def view(self):
    return import_string(self.import_name)
  def __call__(self, *args, **kwargs):
    return self.view(*args, **kwargs)

def tempulator(import_name, url_rules=[], app = '', **options):
  '''
The tempulator is used to add extra templates to the app, if needed, without added overhead to the base project. For example, if you make a blog, you should be able to build a blog without also loading the catalog from an ecommerce site into memory, and vice versa. By using the tempulator, you can load a blog without a journal, or a ecommerce site without a repository, or a snosberry without an everlasting gobbstopper. You can also use the tempulator to load one endpoint before the other. If you like templetons catalog view, and you're an ecommerce site you may want to load that as your index page. This would achieve those results.

    --> views.py  
    # load templetons catalog view as the index view
    @templetonBP.route('/')
    @login
    def catalog():
      return tempulator("views.catalog", ['/catalog'], app = app)

    # add a single route to the catalog view
    tempulator('views.catalog', ['/catalog'], app = app)

    # add two routes to a single function endpoint
    url_rules = ['/catalog/','/catalog/<item>']
    tempulator('views.catalog', url_rules, app = app)
  
  '''
  
  view = Tempulation(f"{__name__}.{import_name}")
  for url_rule in url_rules:
    app.add_url_rule(url_rule, view_func=view, **options)
