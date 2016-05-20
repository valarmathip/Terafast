import sys
from ncclient import manager


def getCapabilities(host, port, userName, password, timeout):
	
    print "Connecting to  switch <IP:Port = %s:%s>\n" % (host,port)
    swMgr = manager.connect_ssh(host=host, port=port, username=userName, password=password,timeout=timeout, hostkey_verify=False)
    print "The capabilities advertised by Switch are:\n"
    for c in swMgr.server_capabilities:
        print c


if __name__ == '__main__':
    if len(sys.argv) !=  5:
        print "Usage: getcapabilities.py <hostIP> <netconf-port> <username> <password>\n";
        exit(0);
    getCapabilities(sys.argv[1],sys.argv[2],sys.argv[3], sys.argv[4],60)
