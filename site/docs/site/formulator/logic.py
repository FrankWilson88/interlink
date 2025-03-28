import os
from flask import request
from interlink.toolkit import DB

def createQuery(db, user, password, table, *args):
  db_conn = DB(user, password).connect()
  cursor = db_conn.cursor(buffered=True)
  print(*args)
  sql = f'''SELECT * FROM {db}.{table};'''
  cursor.execute(sql)
  sql = cursor.fetchall()
  db_conn.close()
  if sql is not None:
    print(" *", table, "Report Read.")
  else:
    sql = " * No", table, "Report"
    print(" * No", table, "Report")
  return sql

def createNav(db, user, password):
  db_conn = DB(user, password).connect()
  cursor = db_conn.cursor(buffered=True)
  cursor.execute(f'''SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='{db}'; ''')
  sql = cursor.fetchall()
  db_conn.close()
  return sql

def createReport(db, user, password, table):
  error = f'''{db}.{table} Report Does Not Exist'''
  colName = ''
  colRow = ''
  db_conn = DB(user, password).connect()
  cursor = db_conn.cursor(buffered=True)
  cursor.execute(f'''SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = N'{db}' AND TABLE_NAME = N'{table}'; ''')
  check_table = cursor.fetchone()
  if check_table is not None:
    print(f''' * {db}.{table} Report Read.''')
    error = ''
    cursor.execute(f'''SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = N'{db}' AND TABLE_NAME = N'{table}';''')
    colName = cursor.fetchall()
    cursor.execute(f'''SELECT * FROM {db}.{table};''')
    colRow = cursor.fetchall()
    db_conn.close()
  else:
    print(error)
  return colName, colRow, error

def createForm(db, user, password, table):
  error = f'''{db}.{table} Form Does Not Exist.'''
  sql = ''
  db_conn = DB(user, password).connect()
  cursor = db_conn.cursor(buffered=True)
  cursor.execute(f'''SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = N'{db}' AND TABLE_NAME = N'{table}'; ''')
  check_table = cursor.fetchone()
  if check_table is not None:
    print(f''' * {db}.{table} Form Generated.''')
    error = f'''Please fill in all the boxes'''
    cursor.execute(f'''SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = N'{db}' AND TABLE_NAME = N'{table}' AND COLUMN_NAME NOT LIKE 'timestamp' AND COLUMN_KEY NOT LIKE 'PRI' AND COLUMN_KEY NOT LIKE 'UNI' AND COLUMN_KEY NOT LIKE 'MUL' AND COLUMN_NAME NOT LIKE 'updated';''')
    sql = cursor.fetchall()
    db_conn.close()
    if request.method == 'POST':
      try:
        colName = tuple(l[0] for l in sql)
        key = ", ".join(colName)
        value = tuple(request.values.get(l[0]) for l in sql)
        db_conn = DB(user, password).connect()
        cursor = db_conn.cursor(buffered=True)
        cursor.execute(f'''INSERT INTO {db}.{table} ({key}) VALUES {value};''')
        db_conn.commit()
        db_conn.close()
        error = f'''Success!'''
      except:
        error = f'''You must fill in all the boxes.'''
  return error, sql
