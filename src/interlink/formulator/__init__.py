'''
This is the formulator
'''
class Generator:
  '''
  The generator is the module used to generate your forms, reports, queries, and anything DB related.

Let's say you want to generate a blog. Use the formulator.Generator to make a query of your blog table from your SQL database. Create a variable from it, and then using Jinja's Templating Engine with Flask, we can manipulate the variable in an html template anyway we want.

Examples:

    from interlink import Generator
    @templetonBP.route('/forms/<db>/<page>', methods=['GET', 'POST'])
    def generateForm(db, page):
        gen = Generator(db, 'DB_USER', 'DB_PASS')
        error, form, title = gen.generateForm(page)
        return render_template('forms.html', error=error, form=form, title=title)

    from interlink import Generator
    @templetonBP.route('/reports/<db>/<page>')
    def generateReport(db, page):
      gen = Generator(db, 'DB_USER', 'DB_PASS')
      colName, colRow, error, title = gen.generateReport(page)
      return wrapper('reports.html', colName=colName, colRow=colRow, error=error, title=title)

    @viewsBP.route(/)
    def index():
      gen = i.Generator('DB', 'DB_USER', 'DB_PASS')
      nav = gen.generateNav()
      return render_template('index.html', nav=nav)
  '''
 
  def __init__(self, db, user, password):
    '''Initialize the Generator object.'''
    self.db = db
    self.user = user
    self.password = password
    
  def generateForm(self, table):
    '''
    Generate a form to enter data into the `table`
    
    Returns: 
      error (str): Success! Error!
      form (str): Success! 404 
      title (str): DB table name
    '''
    from .logic import createForm
    error, form = createForm(self.db, self.user, self.password, table)
    title = table
    return error, form, title
    
  def generateReport(self, table):
    '''
    Generate a report to enter data into the `table`
    
    Returns: 
      colName (str): DB Column Name 
      colRow (str): DB Column Row 
      error (str): Success! 404
      title (str): DB table name
    '''
    from .logic import createReport
    colName, colRow, error = createReport(self.db, self.user, self.password, table)
    title = table
    return colName, colRow, error, title
    
  def generateQuery(self, table):
    '''
    Run a custom SELECT statement to see the results.
    
    TODO: Start making it.
    '''
    from .logic import createQuery
    return createQuery(self.db, self.user, self.password, table)
    
  def generateNav(self):
    '''Generate a navigation bar for each table in the initialized object'''
    from .logic import createNav
    return createNav(self.db, self.user, self.password)
