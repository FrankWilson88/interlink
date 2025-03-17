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
    self.db = db
    self.user = user
    self.password = password
    
  def generateForm(self, table):
    error, form = createForm(self.db, self.user, self.password, table)
    title = table
    return error, form, title
    
  def generateReport(self, table):
    colName, colRow, error = createReport(self.db, self.user, self.password, table)
    title = table
    return colName, colRow, error, title
    
  def generateQuery(self, table):
    return createQuery(self.db, self.user, self.password, table)
    
  def generateNav(self):
    return createNav(self.db, self.user, self.password)