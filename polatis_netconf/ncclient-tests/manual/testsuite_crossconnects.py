import os
import sys

from lib.crossconnects import *


### cross connects operations 

def oxC(opr):
    
    if opr == "connectSwitch":
        """Usage: <hostIP> <netconf-port> <username> <password> <timeout>\n"""
        connectSwitch('10.99.99.227', '830', 'admin', 'root', 60)

    if opr == "getExistingPortList":
        getExistingPortList()

    if opr == "crossconnects_get":
        """Usage: <outputXml file>"""
        crossconnects_get('crossConnects.xml')

    if opr == "pairs_get":
        """Usage: <outputXml file>"""
        pairs_get('pairs.xml')

    if opr == "ingress_get":
        """Usage: <outputXml file>"""
        ingress_get('ingress.xml')

    if opr == "ingressports_get":
        """Usage: <outputXml file> <port list : only ',' & '-' seperated values>"""
        ingressports_get('get_ingressPrt.xml', '10-14')

    if opr == "egress_get":
        """Usage: <outputXml file>"""
        egress_get('egress.xml')

    if opr == "egressports_get":
        """Usage: <outputXml file> <port list : only ',' & '-' seperated values>"""
        egressports_get('get_egressPrt.xml', '17-21')

    if opr == "editconfig_get":
        """Usage: <outputXml file>"""
        editconfig_get('get_edit_config.xml')

        
    if opr == "crossconnects_getConfig":
        """Usage: <outputXml file>"""
        crossconnects_getConfig('getConfig_crossConnects.xml')

    if opr == "pairs_getConfig":
        """Usage: <outputXml file>"""
        pairs_getConfig('getConfig_pairs.xml')

    if opr == "ingress_getConfig":
        """Usage: <outputXml file>"""
        ingress_getConfig('getConfig_ingress.xml')

    if opr == "ingressports_getConfig":
        """Usage: <outputXml file> <port list : only ',' & '-' seperated values>"""
        ingressports_getConfig('getConfig_ingressPrt.xml', '10-14')

    if opr == "egress_getConfig":
        """Usage: <outputXml file>"""
        egress_getConfig('getConfig_egress.xml')

    if opr == "egressports_getConfig":
        """Usage: <outputXml file> <port list : only ',' & '-' seperated values>"""
        egressports_getConfig('getConfig_egressPrt.xml', '17-21')

    if opr == "editconfig_getConfig":
        """Usage: <outputXml file>"""
        editconfig_getConfig('getConfig_edit_config.xml')

    if opr == "createOxcWO_Opr_editConfig":
        """<ingress port list : only ',' & '-' seperated values> <egress port list : only ',' & '-' seperated values>"""
        createOxcWO_Opr_editConfig('10-6', '20-24')

    if opr == "createOXC_editConfig":
        """<ingress port list : only ',' & '-' seperated values> <egress port list : only ',' & '-' seperated values>"""
        createOXC_editConfig('1,2,3', '17,18,19')

    if opr == "deleteOXC_editConfig":
        """<ingress port list : only ',' & '-' seperated values> <egress port list : only ',' & '-' seperated values>"""
        deleteOXC_editConfig('6-10', '20-24')

    if opr == "replaceOXC_editConfig":
        """<ingress port list : only ',' & '-' seperated values> <egress port list : only ',' & '-' seperated values>"""
        replaceOXC_editConfig('11', '23')


### main 


if __name__ == '__main__':
    oxC('connectSwitch')
    oxC('getExistingPortList')
    oxC('createOxcWO_Opr_editConfig')
"""
    oxC('connectSwitch')
    oxC('getExistingPortList')
    oxC('deleteOXC_editConfig')
    oxC('ingressports_get')
    oxC('ingressports_getConfig')
    oxC('createOxcWO_Opr_editConfig')
    oxC('replaceOXC_editConfig')
    oxC('editconfig_getConfig')
"""

