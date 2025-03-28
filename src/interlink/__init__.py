# This file is used as a hub to import the functions of each of PADS API Libraries.
# Copyright Joe Corso armyglass@hotmail.com

'''
This is a collection of libraries written to work in Python’s flask framework. It will generate a form and report for any table in a database. It will also create the urls, and the navigation bar. You can customize your website by generating your own instance of the API; or you can register the Blueprint(e.g. app.register_blueprint(templetonBP)), which has its own set of templates etc. So essentially, if you create a database for a library like in all tutorials and you need a form template and a report template, it will generate the form or report from the table in the database, and fill in the details in the template. To render the page in the browser just type in the url which corresponds to the table name, or make a navigation bar to generate the links for you.

Examples:
    Setting up interlink is very easy. It depends on mysql-connector, and flask. Which will be downloaded automatically. First create your database, and tables. Then install:  

        python -m venv pads/env/my_env
        pads/env/my_env/bin/activate
        python -m pip install git+https://github.com/padsRepo/interlink.git 
        from interlink import *
        app.register_blueprint(templetonBP)
        app.register_error_handler(404, url_not_found)
        app.register_error_handler(500, internal_error)
    
    Enter URL in browser:
    
        127.0.0.1:8000/blog/manifest

Let's say you want to generate a blog. Use the formulator.Generator to
make a query of your blog table from your SQL database. Create a
variable from it, and then using Jinja's Templating Engine with Flask,
we can manipulate the variable in an html template anyway we want.

      from interlink import Generator

      @viewsBP.route('/blog/')
      def blog():
        gen = Generator('blog', 'DB_USER', 'DB_PASS')
        content = gen.generateReport('blog')
        return render_template('blog.html', content=content)

Then your blog template could look something like this:  

      {% raw %}
      {% extends 'base.html' %}
      {% block description %}Raw Thoughts{% endblock %}
      {% block keywords %}emo, roses are black violets are black my life is black everything is black{% endblock %}
      {% block title %}Blog{% endblock %}

      {% block content %}
        <article class="col-12 col-s-12 col-m-12">
          <h1>My personal shit show</h1>
          {{ error }}
          <table class="blog">
            <tr>
              {% for c in content %}
                <th>{{ c[3] }}</th>
              {% endfor %}
            </tr>
            {% for row in content %}
                {% for c in row %}
                <tr>{{ c }}</tr><br>
                {% endfor %}
            {% endfor %}
          </table>
        </article>
      {% endblock %}
      {% endraw %}

Then, you can style the page any way that you want without having to
keep going back and rewriting the logic for the form and report and also
start cluttering your templates folder with a bunch of different types
of forms, reports, navbars, blogs, logins, etc. It's just one, and it's
already made.

Conversely, you can build your project a bit more flexible. In your
views.py file you only need two specific views that will generate every
form, and report respectively. In the `index()` function you will see
the nav var set to `generateNav()`, this generates the navigation bar
for you. So put that where ever you want that to generate. If you're
familiar with flask's app factory, and Blueprints, then this should look
pretty simple. If not, check out the flask docs, it's pretty cool. They
look something like this:

---> views.py

      from flask import Blueprint, render_template
      import interlink as i

      viewsBP = Blueprint('/', __name__, url-prefix='/')

      @viewsBP.route(/)
      def index():
        gen = i.Generator('DB', 'DB_USER', 'DB_PASS')
        nav = gen.generateNav()
        return render_template('index.html', nav=nav)

      @viewsBP.route('/reports/<db>/<page>')
      def generateReport(db, page):
        gen = i.Generator(db, 'DB_USER', 'DB_PASS')
        colName, colRow, error, title = gen.generateReport(page)
        return render_template('reports.html', colName=colName, colRow=colRow, error=error, title=title)

      @viewsBP.route('/forms/<db>/<path>', methods=['GET', 'POST'])
      def generateForm(db, page):
        gen = i.Generator(db, 'DB_USER', 'DB_PASS')
        error, form, title = gen.generateForm(page)
        return render_template('forms.html', form=form, error=error, title=title)

      @viewsBP.route('/admin/<db>')
      def admin(db):
        nav = Generator(db, 'DB_USER', 'DB_PASS').generateNav()
        return render_template('admin.html', nav=nav, db=db, title=db)

Basically, make a route for a reports url and a route for a forms url so
that the computer doesn't confuse the two. For your route you need to
define a parameter for your database, and table. This is just to pass
into the `generateReport()` or `generateForm()` functions which is used
to find the table, and create the form or report. The report needs 4
parameters(One for the column names of the table, one for the data in
the table, a title, and a generic error) and the form needs 3(One to
generate the forms, a title, and a generic error). The `generateNav()`
doesn't need a parameter, but it searches for the database you set to
your `Generator.__init__()`. Make sure to register the views in your app
factory:

---> __init__.py

      from views import viewsBP
      app.regist_blueprint(viewsBP)

Make a template for your Forms:  
---> forms.html

      {% raw %}
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
      {% endraw %}

Make a template for your reports:  
---> reports.html

      {% raw %}
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
      {% endraw %}

Finally, make a navigation menu for it all. This just plops every link
onto the screen, so it's up to you to decide how to style it, maybe make
a dropdown menu with it or something. The formulator filters
"timestamp", "pri", "uni", "mul", "updated", and anything that starts
with "q". Be sure to decide which tables you actually want to use, and
which not; so you don't accidentally insert data to a table you're not
supposed to.

---> base.html

      {% raw %}
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
      {% endraw %}

That's it! So if you have a DB with tables named books, authors,
planets, solarSystems....etc. Just type in the url for the table name.
For example:

`https://www.website.com/reports/<dbname>/authors`  
OR  
`https://www.website.com/forms/<dbname>/solarSystems`  


Modules:  
  formulator: Form and Report Generator
  templeton: Template Generator
  safeHaven: Security Guard
  toolkit: Misc Tools

Classes:  
  Generator: Forms
  DB: Connect to DB

Functions:  
  tempulator: templates
  tempulation: Custom Views
  honeypot: distraction
  backdoor: entry way
  login: check user
  site_map: site map for SEO
  url_not_found: 404 Error
  internal_error: 500 Error
  templetonBP: Templeton Templates
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
