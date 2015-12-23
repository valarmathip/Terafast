#!/usr/bin/python

import MySQLdb

class MySqlAccess:

    def __init__(self, host, user_name, passwd, db_name):
			
# Open database connection
        self.db = MySQLdb.connect(host,user_name,passwd,db_name)

# prepare a cursor object using cursor() method
        self.cursor = self.db.cursor()

    def close(self):
        self.db.close()

    def get_records(self, sql,args=None):

        self.results = None
        #try:
            # Execute the SQL command
        if not args== None:
            self.cursor.execute(sql,args)
        else:
            self.cursor.execute(sql)
   		    # Fetch all the rows in a list of lists.
        self.results = self.cursor.fetchall()
        #except:
        #print "Error: unable to fecth data"
        return self.results

    def load_file(self,file_name, table_name, ignoreHeader=True):
        if ignoreHeader == True:
            statement = "load data infile \'%s\' into table %s fields terminated by \',\' lines terminated by \'\\n\' ignore 1 lines" % (file_name, table_name)
        else:
            statement = "load data infile \'%s\' into table %s fields terminated by \',\' lines terminated by \'\\n\'" % (file_name, table_name)
        self.cursor.execute(statement)
        self.cursor.execute('commit')
            

