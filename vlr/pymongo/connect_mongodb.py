import commands


class ManageMongoDB():
    """To connect to the mongod db and load the CSV file into mongodb"""

    def __init__(self, host, port, username, password, db_name, collection_name):
    
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_name = db_name
        self.collection_name = collection_name
        #self.file_path = file_path

    def load_document(self, file_type, file_name):
        """ Load the required file into mongodb using mongoimport"""

        status, output = commands.getstatusoutput("mongoimport -h %s -p %s -u %s -p %s -d %s -c %s --type %s --file %s --headerline" % (self.host, self.port, self.username, self.password, self.db_name, self.collection_name, file_type, file_name)) 
        print "status is", status
        print "output is", output

obj = ManageMongoDB('10.6.7.23', 27017, 'tera-user', 'abcd123', 'terafast', 'tera_vmList')
obj.load_document('csv', '/home/mravi/valar.csv')
