'''
This is the Toolkit Module. It contains classes and functions that are reuseable across the entire library.
'''

import os
import sys
import mysql.connector
from flask import url_for

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def has_no_empty_params(rule):
  defaults = rule.defaults if rule.defaults is not None else ()
  arguments = rule.arguments if rule.arguments is not None else ()
  return len(defaults) >= len(arguments)

def site_map():
  from __init__ import app
  links = []
  for rule in app.url_map.iter_rules():
  # Filter out rules we can't navigate to in a browser
  # and rules that require parameters
    if "GET" in rule.methods and has_no_empty_params(rule):
      url = url_for(rule.endpoint, **(rule.defaults or {}))
      links.append((url, rule.endpoint))
  # links is now a list of url, endpoint tuples
  return links

class DB:
  '''
Connects to MariaDB

Returns: 
    mydb (str): Conn to db

Example:

    @viewsBP.route('/report/<db>/<page>')
    def myFuntion(db, user, password):
      db_conn = DB(db, user, password).connect()
      cursor = db_conn.cursor(buffered=True)
      cursor.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='{db}'; ")
      sql = cursor.fetchone()
      db_conn.close()
      return sql
  '''
  def __init__(self, user, password, db = ''):
    '''Initialize the database object'''
    self.db = db
    self.user = user
    self.password = password
  def connect(self):
    '''Used to make connection to MariaDB'''
    mydb = mysql.connector.connect(
    host = 'localhost',
    database = os.environ.get(self.db),
    user = os.environ.get(self.user),
    password = os.environ.get(self.password)
    )
    return mydb
  def close(self):
    '''Used to close connection to MariaDB'''
    db = DB(self.db, self.user, self.password)
    if db is not None:
      db.close()
