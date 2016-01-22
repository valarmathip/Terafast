import os
import sys

from lib.ports import *


### product information operations 

def portsInfo(opr):

    if opr == "connectSwitch":
        """Usage: <hostIP> <netconf-port> <username> <password> <timeout>\n"""
        connectSwitch('10.99.99.227', '830', 'admin', 'root', 60)

    if opr == "get_ports":
        """Usage: <output XML file>"""
        get_ports('get_ports.xml')

    if opr == "get_port_label":
        """Usage: <output XML file>"""
        get_port_label('get_port_label.xml')

    if opr == "get_port_state":
        """Usage: <output XML file>"""
        get_port_state('get_port_state.xml')

    if opr == "get_port_status":
        """Usage: <output XML file>"""
        get_port_status('get_port_status.xml')
    
    if opr == "get_opm":
        """Usage: <output XML file>"""
        get_opm('get_opm.xml')
   
    if opr == "get_selectedPortsInfo":
        """Usage: <port - sub tags variable name> <port - sub tags name> <'port-id's range':'subtags of opm'> <output XML file>"""
        #<port - sub tags variable name>                : port_id, port_label, port_state, port_status, opm
        #<port - sub tags name>                         : port-id, port-label, port-state, port-status, opm
        #<port-id's range/subtags of opm>               : see below three format
        #<port-id's range>                              : 1-5, 1,2,3
        #subtags of opm                                 : lamda, power-high-alarm, power-low-alarm, power-high-warning-offset, power
        #                                               : -low-warning-offset, power-alarm-control, power-alarm-status, power,offset        #                                               : , averaging-time-select, power-alarm-hyteresis, power-alarm-clear-holdoff
        # 1.                                            : 1-24/lamda, power-high-alarm
        # 2.                                            : 1,2,3...24/none
        # 3.                                            : 'allInfo'  (If you need all ports info)

        get_selectedPortsInfo('port_label,opm,port_id,port_status', 'port-label,opm,port-id,port-status', '1,4,10/power', 'get_selectedPortsInfo')

    if opr == "getConfig_ports":
        """Usage: <output XML file>"""
        getConfig_ports('getConfig_ports.xml')

    if opr == "getConfig_port_label":
        """Usage: <output XML file>"""
        getConfig_port_label('getConfig_port_label.xml')

    if opr == "getConfig_port_state":
        """Usage: <output XML file>"""
        getConfig_port_state('getConfig_port_state.xml')

    
    if opr == "getConfig_opm":
        """Usage: <output XML file>"""
        getConfig_opm('getConfig_opm.xml')
   
    if opr == "getConfig_selectedPortsInfo":
        """Usage: <port - sub tags variable name> <port - sub tags name> <'port-id's range':'subtags of opm'> <output XML file>"""
        #<port - sub tags variable name>                : port_id, port_label, port_state, port_status, opm
        #<port - sub tags name>                         : port-id, port-label, port-state, port-status, opm
        #<port-id's range/subtags of opm>               : see below three format
        #<port-id's range>                              : 1-5, 1,2,3
        #subtags of opm                                 : lamda, power-high-alarm, power-low-alarm, power-high-warning-offset, power
        #                                               : -low-warning-offset, power-alarm-control, power-alarm-status, power,offset        #                                               : , averaging-time-select, power-alarm-hyteresis, power-alarm-clear-holdoff
        # 1.                                            : 1-24/lamda, power-high-alarm
        # 2.                                            : 1,2,3...24/none
        # 3.                                            : 'allInfo'  (If you need all ports info)

        getConfig_selectedPortsInfo('port_id,port_status,opm', 'port-id,port-status,opm', '1,2,18,24/power-alarm-status', 'get_selectedPortsInfo')

    
    #if opr == "":
    #    """Usage: <output XML file>"""
    #    ('.xml')



### main

if __name__ == '__main__':
    portsInfo('connectSwitch')
    portsInfo('getConfig_selectedPortsInfo')
    portsInfo('get_selectedPortsInfo')
#    portsInfo('get_ports')
#    portsInfo('get_port_label')
#    portsInfo('get_port_state')
#    portsInfo('get_port_status')
#    portsInfo('get_opm')
#    portsInfo('get_selectedPortsInfo')
#    portsInfo('getConfig_ports')
#    portsInfo('getConfig_port_label')
#    portsInfo('getConfig_port_state')
#    portsInfo('getConfig_opm')
#    portsInfo('getConfig_selectedPortsInfo')

