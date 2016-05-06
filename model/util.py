from pg import DB

def db_connect():
  db = DB(dbname='postgres',
        host='ec2-52-39-229-191.us-west-2.compute.amazonaws.com',
        port=5432,user='gpadmin')
  return db


def db_query(db, sql):
  v = db.query(sql)
  return v


def createtable(db):
  db_query(db, "DROP TABLE if exists netflix_sample")
  db_query(db, "CREATE TABLE netflix_sample (uid INT, mid INT, rating REAL)")
  return

