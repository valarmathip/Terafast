import sys
from ncclient import manager


def writeToFile(fileName, data):

		f = open(fileName,'w')
		f.write(data)
		f.close()
	

def crossConnectOp(host, port, userName, password, timeout,operation, ingressPort, egressPort):
	
    print "Connecting to  switch <IP:Port = %s:%s>\n" % (host,port)
    swMgr = manager.connect_ssh(host=host, port=port, username=userName, password=password,timeout=timeout, hostkey_verify=False)

    opStr=''
    if operation == 'del':
        opStr = "ns:operation=\"delete\""

    crossConnectStr="""<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0"><cross-connects xmlns="http://www.polatis.com/yang/optical-switch"><pairs %s><ingress>%s</ingress><egress>%s</egress></pairs></cross-connects></config>""" %(opStr,ingressPort, egressPort)
    try:
        print "Issuing edit config to switch for cross-connect configuration\n"
        swMgr.edit_config(target='running', config=crossConnectStr )
    except:
        print "Error:"

if __name__ == '__main__':

    if len(sys.argv) !=  8:
        print "Usage: crossconnect.py <hostIP> <netconf-port> <username> <password> <operation - add/del> <ingressPort> <egressPort>\n"
        exit(0);
    crossConnectOp(sys.argv[1],sys.argv[2],sys.argv[3], sys.argv[4],60,sys.argv[5], sys.argv[6], sys.argv[7])
