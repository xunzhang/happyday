from pg import DB
from config import DBNAME, HOST, PORT, USER, LOGIN_KEY

class PGDB(object):
    def __init__(self):
        pass

    def connect(self, dbname, host, port, user):
        self.db = DB(dbname=dbname, host=host, port=port, user=user)

    def connect_default(self):
        self.db = DB(dbname=DBNAME, host=HOST, port=PORT, user=USER)

    def close(self):
        self.db.close()
    
    def execute(self, sql):
        return self.db.query(sql)
    
    def drop_table(self, tbl):
        self.execute('DROP TABLE if exists %s' % tbl)

    def create_init_table(self, tbl):
        self.execute('CREATE TABLE %s (uid INT, iid INT, rating REAL)' % tbl)

    def copy(self, tbl, path, delimiter):
        self.execute("COPY %s FROM '%s' delimiter '%s'" % (tbl, path, delimiter))


