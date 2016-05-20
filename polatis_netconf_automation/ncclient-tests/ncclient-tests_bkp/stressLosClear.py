import sys
from ncclient import manager


def writeToFile(fileName, data):

		f = open(fileName,'w')
		f.write(data)
		f.close()
	

def losClearOp(host, port, userName, password, timeout):
	
    print "Connecting to  switch <IP:Port = %s:%s>\n" % (host,port)
    swMgr = manager.connect_ssh(host=host, port=port, username=userName, password=password,timeout=timeout, hostkey_verify=False)

    ports = [1,2,3,4,5,6,7,8,9,10]
    for x in ports:
        losClear="""<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0"><ports xmlns="http://www.polatis.com/yang/optical-switch"><port><port-id>%d</port-id><port-label/><port-state>PC_ENABLED</port-state><opm><lambda>1550.0</lambda><power-high-alarm>25.0</power-high-alarm><power-low-alarm>-60.0</power-low-alarm><power-high-warning-offset>25.0</power-high-warning-offset><power-low-warning-offset>0.0</power-low-warning-offset><power-alarm-control>POWER_ALARM_DISABLED</power-alarm-control><offset xmlns="http://www.polatis.com/yang/polatis-switch">10.0</offset><averaging-time-select xmlns="http://www.polatis.com/yang/polatis-switch">4</averaging-time-select><power-alarm-hysteresis xmlns="http://www.polatis.com/yang/polatis-switch">1.0</power-alarm-hysteresis><power-alarm-clear-holdoff xmlns="http://www.polatis.com/yang/polatis-switch">60</power-alarm-clear-holdoff></opm></port></ports>""" %x
        try:
            print "Issuing edit config to switch for los alarm configuration\n"
            swMgr.edit_config(target='running', config=losClear )
        except:
            print "Error:"

if __name__ == '__main__':

    if len(sys.argv) !=  5:
        print "Usage: losclear.py <hostIP> <netconf-port> <username> <password>\n"
        exit(0);
    losClearOp(sys.argv[1],sys.argv[2],sys.argv[3], sys.argv[4],60)
