import os
from flask import Blueprint, render_template, request
from . import interlink
from interlink.formulator import Generator
from interlink.safeHaven import backdoor, login, honeypot
from interlink.toolkit import site_map

templates = os.path.dirname(__file__) + '/templates/'
templetonBP = Blueprint('templeton', __name__, url_prefix='/', template_folder=templates)

def wrapper(page = 'template.html', **kwargs):
  '''Used to wrap all the web pages in default params. TODO: make a decorator.'''
  ip = request.remote_addr
  return render_template(page, version=interlink.__version__, updated=interlink.__updated__, author=interlink.__author__, siteMap=site_map(), ip=ip, **kwargs)

def index():
  '''
  Interlinks default index page.
  Example:
    tempulator('views.index', ['/index'])
  '''
  title = f"Index"
  article = f'''
  Article Content. This is content coming from views.py. This is some Metadata about interlink I've added for the example: <br>
  '''
  varA = f'''New:<br>'''
  #article = article.join('<br>')
  return wrapper('template.html', title=title, article=article, varA=varA)

def catalog():
  title = f'Catalog'
  return wrapper('template.html', title=title)

@templetonBP.route('/interlink/')
def interlinkData():
  title = "Interlink Metadata"
  return wrapper('data.html', title=title)
  
# Generic templeton templates
@templetonBP.errorhandler(404)
def url_not_found(e):
  return wrapper("404.html", title="** This Page Does Not Exist **", description="I can\'t find that URL...", error=f'''{e}'''), 404

@templetonBP.errorhandler(500)
def internal_error(e):
  return wrapper("500.html", title="** There is an error with my code **", description="There\'s something wrong with me...Some dumbass programmer made a K18 error....", error=f'''{e}'''), 500

@templetonBP.route('/docs/<page>', defaults={'page': 'index.html'})
@templetonBP.route('/docs/<page>')
def documentation(page):
  return render_template('guide/' + page)

@templetonBP.route('/reports/<db>/<page>')
@backdoor
@login
@honeypot
def generateReport(db, page):
  gen = Generator(db, 'DB_USER', 'DB_PASS')
  colName, colRow, error, title = gen.generateReport(page)
  return wrapper('reports.html', colName=colName, colRow=colRow, error=error, title=title)

@templetonBP.route('/forms/<db>/<page>', methods=['GET', 'POST'])
@backdoor
@login
@honeypot
def generateForm(db, page):
  gen = Generator(db, 'DB_USER', 'DB_PASS')
  error, form, title = gen.generateForm(page)
  return wrapper('forms.html', form=form, error=error, title=title)

@templetonBP.route('/admin/<db>')
@backdoor
@login
@honeypot
def admin(db):
  nav = Generator(db, 'DB_USER', 'DB_PASS').generateNav()
  return wrapper('admin.html', nav=nav, db=db, title=db)

@templetonBP.route('/loginRequired/', methods=['GET', 'POST'])
def loginRequired():
  message = 'Please Log in'
  if request.method == 'POST':
    fakeName = request.form['username']
    fakePass = request.form['password']
    message = "Your Username or Password is incorrect"
    print(' * The user is attempting to log in!\n   User:', fakeName, 'Password:', fakePass)
    print(' * The user is attempting to log in!\n   User:', fakeName, 'Password:', fakePass, file=open(os.environ.get('LOG_DIR') + '/pads.log', 'a'))
    session.clear()
  return render_template('login.html', message=message)
  
@templetonBP.route('/login/', methods=['GET', 'POST'])
def secure_login():
  message = 'This is a Secure Login'
  if request.method == 'POST':
    session['username'] = request.form['username']
    session['passwd'] = request.form['password']
    try:
      db_conn = DB(db, user, password).connect()
      cursor = db_conn.cursor()
      cursor.execute(f'''SELECT passwd FROM profile WHERE username = "{ session['username'] }";''')
      p = cursor.fetchone()
      if pwHash.check_password_hash(p[0], session['passwd']):
        sql = f'''SELECT username, passwd FROM profile WHERE username = "{ session['username'] }" AND passwd = "{ p[0] }";'''
        cursor.execute(sql)
        sql = cursor.fetchone()
        db_conn.close()
        if sql is not None:
          message = 'You are logged in.'
          return redirect(url_for('/.index'))
        else:
          print('User does not exist.')
          return wrapper('login.html')
    except:
      print(' * The user is attempting to log in!\n   User:', session['username'])
      print(' * The user is attempting to log in!\n   User:', session['username'], file=open(os.environ.get('LOG_DIR') + '/pads.log', 'a'))
      message = "Your Username or Password is incorrect"
  return wrapper('login.html', message=message)
  
@templetonBP.route('/register/', methods=['GET', 'POST'])
def secure_registration(db, user, pw):
  error = 'This is a Secure Registration'
  print('this')
  if request.method == 'POST':
    print('that')
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    db_conn = DB(db, user, pw).connect()
    cursor = db_conn.cursor()
    cursor.execute(f'''SELECT ROW_COUNT() FROM profile;''')
    row_count = cursor.fetchall()
    if row_count is None:
      error = '** Registration is closed. Contact the Administator. **'
    else:
      #try:
        pass_hash = pwHash.generate_password_hash(password).decode('UTF-8')
        print(pass_hash)
        #salt = os.urandom(32)
        sql = f'''INSERT INTO profile(name, username, passwd, email) VALUES("{ name }", "{ username }", "{ pass_hash }", "{ email }");'''
        cursor.execute(sql)
        db_conn.commit()
        db_conn.close()
        print("Someone has made a profile!")
        print("Someone has made a profile!", file=open(os.environ.get('LOG_DIR') + '/pads.log', 'a'))
        return redirect(url_for('/.login'))
      #except:
        print('No.')
  else:
    error = 'Something went wrong.'
  return wrapper('register.html', error=error)
