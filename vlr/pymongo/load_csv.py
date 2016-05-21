import pymongo
from pymongo import MongoClient
import csv


class ConnectMongo():

    """
    """
    def __init__(self, host, port, db_name, coll_name):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.coll_name = coll_name
        self.conn = self.mongodb_connection()
        self.db = self.getDatabase(self.conn, self.db_name)
        self.db_coll_conn = self.getCollection(self.db, self.coll_name)

    def mongodb_connection(self):
        """ connect to mongodb"""

        try:
            conn = MongoClient(self.host, self.port)
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to server: %s, Error is: %s" % (self.host, e)
        return conn

    def getDatabase(self, conn, db_name):
        """ Connect to the required database"""
        try:
            db = conn[db_name]
        except Exception as err:
            print "Error while connecting to database: %s is: %s" % (db_name, err)
        return db

    def getCollection(self, db, coll_name):
        """ create a handle for collection"""
        
        try:
            collection = db[coll_name]
        except Exception as err:
            print "Error when getting collection details is: %s" % err
        return collection
         

    def load_csv(self, filename, header):
        """ 
        Read the csv file and insert each line in mongodb
        filename : Name of the csv file
        header : header of the csv file as a list
        """
 
        csvfile = open(filename)
        reader = csv.DictReader(csvfile)
        doc = []
        for each in reader:
            row={}
            for field in header:
                row[field]=each[field]
            doc.append(row)

        print "document is", doc   
         
        self.db_coll_conn.insert_many(doc)

    def search_content(self, search_dict = {}, sort_option = [], limit_value = 10):
        """ Search the required content from csv based on the colloumn using find"""

        count = self.db_coll_conn.count()
        print "count is", count
        #search_out = self.db_coll_conn.find({'Server IP': '10.6.1.3'}).sort([('machine name', 1)]).limit(10)
        if not sort_option: 
            search_out = self.db_coll_conn.find(search_dict).limit(limit_value)
        else:
            search_out = self.db_coll_conn.find(search_dict).sort(sort_option).limit(limit_value)
        for doc in search_out:
            print "search output is", doc

obj = ConnectMongo("10.6.7.23", 27017, 'teraDB', 'teraCollection')
obj.load_csv("/home/mravi/valar.csv", ["Server IP", "machine name", "State"])
obj.search_content(search_dict = {'Server IP': '10.6.6.4'}, sort_option = [('machine name', 1)], limit_value = 20)
