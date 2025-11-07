*__version__*  

0.1.7  

*__author__*  

Joe Corso  

*__date__*  

01-21-2024  

*__updated__*  

10-18-2025  

*__copyright__*  

Copyright 2024 Joe Corso  

*__license__*  

MIT License  

*__email__*  

pads.email.address@gmail.com  

*__status__*  

Development  

*__description__*  

Flask Generator for Forms, Reports, URLs and templates.  

\pagebreak
## interlink

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

| Modules | Description |
|-|-|  
  [formulator](#formulator) |  Form and Report Generator  
  [templeton](#templeton) |  Template Generator  
  [safeHaven](#safehaven) |  Security Guard  
  [toolkit](#toolkit) |  Misc Tools  

| Classes | Description |
|-|-|  
  [Generator](#generator) |  Object method used to query database  
  [DB](#db) |  Object method used to connect and close connection to database  
  [Tempulation](#tempulation) |  Custom Views  

| Functions | Description |
|-|-|  
  | [tempulator](#tempulator) |  templates  
  | [honeypot](#honeypot) |  distraction  
  | [backdoor](#backdoor) |  entry way  
  | [login](#login) |  check user  
  | [site_map](#site_map) |  site map for SEO  
  | [url_not_found](#url_not_found) |  404 Error  
  | [internal_error](#internal_error) |  500 Error  
  | [templetonBP](#templetonbp) |  Templeton Templates  

\pagebreak
## formulator

The formulator is used as the SQL engine to gather the data from the database to populate the template.

The formulator module makes use of the `Generator()` object, to connect to the database, find the proper table, query the results, and return a value that can be passed into an html template. It is the main module behind the Interlink library. It acts as the SQL engine, to generate a return value, that can be manipulated to the developers needs. It's main dependancy is the `toolkit.DB()` object for connection to a database. Make sure you have the proper environment variables set to ensure proper connection. If the project does not fit into the `templetonBP` this module will assist in automating redundant SQL statements, form, and report development, and navigation menus which need to sort administration, from users, from bad actors. It can be used along side other modules in the library as well as imported directly into your own project.

Let's say you dont like templetons blog template and you want to use your own blog template. Use the `formulator.Generator` to make a query of your blog table from your SQL database. Create a variable from it, and then using Jinja's Templating Engine with Flask, we can manipulate the variable in an html template anyway we want.

In your views.py file you only need two specific views that will generate every form, and report respectively. In the `index()` function you will see the nav variable set to `generateNav()`. This generates the navigation bar for you. It can be used in the template to build the navigation menu. If you're familiar with flask's Blueprints, then this should look pretty simple. If not, check out the flask docs, it's pretty cool.

Basically, make a route for a reports url and a route for a forms url so that the computer doesn't confuse the two. For your route you need to define a parameter for your database, and table. This is just to pass into the `generateReport()` or `generateForm()` functions which is used to find the table, and create the form or report. The report needs 4 parameters(One for the column names of the table, one for the data in the table, a title, and a generic error) and the form needs 3(One to generate the forms, a title, and a generic error). The `generateNav()` doesn't need a parameter, but it searches for the database you set to your `Generator.__init__()`. Make sure to register the views:

```python
    __init__.py

      from views import viewsBP
      app.regist_blueprint(viewsBP)
```
```python
    views.py

      from flask import Blueprint, render_template
      import interlink as i

      viewsBP = Blueprint('/', __name__, url-prefix='/')

      @viewsBP.route(/)
      def index():
        gen = i.Generator('DB', 'DB_USER', 'DB_PASS')
        nav = gen.generateNav()
        return render_template('index.html', nav=nav)

      @viewsBP.route('/<db>/<table>')
      def blog(db, table):
        gen = Generator(db, 'DB_USER', 'DB_PASS')
        content = gen.generateQuery(table)
        return render_template('template.html', content=content)

      @viewsBP.route('/reports/<db>/<table>')
      def generateReport(db, table):
        gen = i.Generator(db, 'DB_USER', 'DB_PASS')
        colName, colRow, error, title = gen.generateReport(table)
        return render_template('reports.html', colName=colName, colRow=colRow, error=error, title=title)

      @viewsBP.route('/forms/<db>/<table>', methods=['GET', 'POST'])
      def generateForm(db, table):
        gen = i.Generator(db, 'DB_USER', 'DB_PASS')
        error, form, title = gen.generateForm(table)
        return render_template('forms.html', form=form, error=error, title=title)

      @viewsBP.route('/admin/<db>')
      def admin(db):
        nav = Generator(db, 'DB_USER', 'DB_PASS').generateNav()
        return render_template('admin.html', nav=nav, db=db, title=db)
```
Make a template for your Forms:  
```jinja
      forms.html

      {% extends 'base.html' %}
      {% block description %}{% endblock %}
      {% block keywords %}{% endblock %}
      {% block title %}{{ title }}{% endblock %}

      {% block content %}

      <article class="index">
        <section class="col-6 col-s-6 col-m-6">
          <fieldset class="form">
            <label>{{ error }}</label>
            <form method="POST">
              {% for f in form %}
                <label for="{{ f[0] }}">{{ f[0] }}</label>
                <input type="text" name="{{ f[0] }}">
              {% endfor %}
              <input type="submit" value="submit">
            </form>
          </fieldset>
        </section>
      </article>

      {% endblock %}
```
Make a template for your reports:  
```jinja
      reports.html

      {% extends 'base.html' %}
      {% block description %}{% endblock %}
      {% block keywords %}{% endblock %}
      {% block title %}{{ title }}{% endblock %}

      {% block content %}

        <article class="col-12 col-s-12 col-m-12">
          <h1>{{ title }} Report</h1>
          {{ error }}
          <table class="data">
            <tr>
              {% for c in colName %}
                <th>{{ c[0] }}</th>
              {% endfor %}
            </tr>
            {% for row in colRow %}
              <tr>
                {% for c in row %}
                <td>{{ c }}</td>
                {% endfor %}
              </tr>
            {% endfor %}
          </table>
        </article>

      {% endblock %}
```
Finally, make a navigation menu for it all. The formulator filters
"timestamp", "pri", "uni", "mul", "updated", and "q".
```jinja
      base.html

      <nav class="pc mobile">
        <a href="{{ url_for('/.index') }}">Index</a>
        <div class="dropdown">
          <span>Reports</span>
          <div class="dropdownContent">
            {% for p in nav %}
            <a href="{{ url_for('templeton.generateReport', db='{}'.format(db),  page='{}'.format(p[0])) }}">{{ p[0] }}</a>
            {% endfor %}
          </div>
        </div>
        <div class="dropdown">
          <span>Forms</span>
          <div class="dropdownContent">
            {% for p in nav %}
            <a href="{{ url_for('templeton.generateForm', db='{}'.format(db),  page='{}'.format(p[0])) }}">{{ p[0] }}</a>
            {% endfor %}
          </div>
        </div>
      </nav>
```
That's it! So if you have a DB with tables named books, authors,
planets, solarSystems....etc. Just type in the url for the table name.
For example:

`https://www.website.com/reports/<dbname>/authors`  
OR  
`https://www.website.com/forms/<dbname>/solarSystems`  

### Generator
The generator is the module used to generate your forms, reports, queries, and anything DB related. It wraps the core functionality of the modeule into a reusable Class Object which you can use to recall a connection or query to a specifc database and table. In practice, the developer would not have to write the boilpate code needed to connect, query, and close connection to the database. By leveraging the concept of OOP, the intent is to mitigate, and slow down DDOS attacks, by preventing the end user from creating multiple concurrent conections to any given website.

#### __init__
Initialize the Generator object. This would, in theory, create an new object in the session which the server could point back to.

| Args | Description |
|-|-|  
  db (str) |  Name of [db] to connect  
  user (str) |  Name of user to connect with. Take from 'DB_USER' env var.  
  password (str) |  Password used to connect with. Taken from 'DB_PASS' env var.  

#### generateForm
Generate a form using *table* name to populate the `form.html` template.

| Args | Description |
|-|-|
  table (str) |  Table name of table within database

| Returns | Description |
|-|-|  
  error (str) |  200 404 500  
  form (str) |  Data used to populate template   
  title (str) |  Name of *db* given from *__init__*  

#### generateReport
Generate a report using *table* name to populate the `report.html` template.

| Returns | Description |
|-|-|  
  colName (str) |  Name of each column in the *table*  
  colRow (str) |  Data within each row of the *table*  
  error (str) |  200 404 500  
  title (str) |  Name of *db* given from *__init__*  

#### generateQuery
Run a custom SELECT statement to see the results.  

| Args | Description |
|-|-|  
  table (str) |  Table name to query

| Returns | Description |
|-|-|  
  sql (str) |  Index of the data for each column in a record

TODO:  
  - Add *args to select different columns.

#### generateNav
Generate a navigation bar for each *table* which the *user* has access.

\pagebreak
## safeHaven

Safe Haven is like the security team for the president. Always lurking
in the shadows, ready to defend your best interest. Since these are
decorators they're easy to use.

[Python Decorators](https://peps.python.org/pep-0318/, "Python Decorators")

All you have to do is add the appropriate decorator to each page that
you want to add the functionality to. Here's a simple index page, that I
want really locked down.

    @viewsBP.route('/')
    @backdoor
    @honeypot
    @login
    def index():
      return render_template('index.html')

And there's nothing more to it then that. Safe Haven checks that the
person connecting passes, and if not redirects them to the appropriate
page. If you're using templeton's Blueprints it will redirect to its
login screen, and everything works seamlessly.

### honeypot
Python decorator you can use as a honeypot.  Any IP Adress that is black
listed will be redirected to a login page that logs the username and
password they attempt to use.

### backdoor
Python decorator you can use as a backdoor.  Any page which has this
decorator will give IP Address' on the whitelist full access to the
page.

### login
Python decorator you can use to check if a user is logged in.  If not,
they will be redirected to a login page from where they can log in.

\pagebreak
## templeton

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

### Tempulation
Generate a new url_rule from any view within your project. This is used if you would like to map out url rules for each of your own endpoints.  

Examples:

    # Use the Tempulation's to create a new URL:
    app.add_url_rule('/dash', view_func=Tempulation('interlink.templeton.views.dashboard'))

    # make a new tempulator
    def myNewTempulator(import_name, url_rules=[], **options):
        view = Tempulation(f"@{app_name@}.@{import_name@}")
        for url_rule in url_rules:
          app.add_url_rule(url_rule, view_func=view, **options)

  

#### __init__
Initialize the Tempulation object. This will hold the variable for the new url_rule.  
  
| Args | Description |
|-|-|  
    object (str) |  Endpoint for new view
    

#### view
None

#### __call__
None

### tempulator
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
  
  

\pagebreak
## toolkit

This is the Toolkit Module. It contains classes and functions that are reuseable across the entire library.

### DB
Connects to MariaDB

| Returns | Description |
|-|-| 
    mydb (str) |  Conn to db

Example:

    @viewsBP.route('/report/<db>/<page>')
    def myFuntion(db, user, password):
      db_conn = DB(db, user, password).connect()
      cursor = db_conn.cursor(buffered=True)
      cursor.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='{db}'; ")
      sql = cursor.fetchone()
      db_conn.close()
      return sql
  

#### __init__
Initialize the database object

#### connect
Used to make connection to MariaDB

#### close
Used to close connection to MariaDB

