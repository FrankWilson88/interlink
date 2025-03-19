print(" * Loading Formulator...")
from .logic import createQuery, createNav, createReport, createForm

class Generator:
  '''
 Used to generate your forms, reports, queries, and anything DB related
 Example Use:
    @templetonBP.route('/forms/<db>/<page>', methods=['GET', 'POST'])
    def generateForm(db, page):
      gen = Generator(db, 'DB_USER', 'DB_PASS')
      error, form, title = gen.generateForm(page)
      return render_template('forms.html', error=error, form=form, title=title)
  '''
 
  def __init__(self, db, user, password):
    '''Initialize the Generator object.'''
    self.db = db
    self.user = user
    self.password = password
    
  def generateForm(self, table):
    '''
    Generate a form to enter data into the `table`
    RETURN: error, form, title
    '''
    error, form = createForm(self.db, self.user, self.password, table)
    title = table
    return error, form, title
    
  def generateReport(self, table):
    '''
    Generate a report to enter data into the `table`
    RETURN: colName, colRow, error, title
    '''
    colName, colRow, error = createReport(self.db, self.user, self.password, table)
    title = table
    return colName, colRow, error, title
    
  def generateQuery(self, table):
    '''
    Run a custom SELECT statement to see the results.
    TODO: Start making it.
    '''
    return createQuery(self.db, self.user, self.password, table)
    
  def generateNav(self):
    '''Generate a navigation bar for each table in the initialized object'''
    return createNav(self.db, self.user, self.password)