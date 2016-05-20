import sys
from ncclient import manager


def writeToFile(fileName, data):

		f = open(fileName,'w')
		f.write(data)
		f.close()
	

def getConfigPort(host, port, userName, password, timeout,outFileName, expr):
	
    print "Connecting to  switch <IP:Port = %s:%s>\n" % (host,port)
    swMgr = manager.connect_ssh(host=host, port=port, username=userName, password=password,timeout=timeout, hostkey_verify=False)

    try:
        print "Quering for running configuration data from switch using get_config\n"
        if expr is not None:
            xmlData = swMgr.get_config(source='running', filter=('xpath',expr)).data_xml
        else:
            xmlData = swMgr.get_config(source='running').data_xml

        writeToFile(outFileName,xmlData);
		
    except:
        print "Error:"

if __name__ == '__main__':

    if len(sys.argv) !=  7:
        print "Usage: getconfigport.py <hostIP> <netconf-port> <username> <password> <output-xml-file> <xpath filter or * for no filter>\n";
        exit(0);
    expr = sys.argv[6]
    if sys.argv[6] == '*':
        expr = None
    getConfigPort(sys.argv[1],sys.argv[2],sys.argv[3], sys.argv[4],60,sys.argv[5], expr)
