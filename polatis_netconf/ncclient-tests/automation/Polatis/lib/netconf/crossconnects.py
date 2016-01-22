""" Python file that covers tabs under the "cross-connects".
"""
import re
import os
import nose
import time
import sys
import logging
import logging.config
import ConfigParser
import xml.dom.minidom

from createCsv import csvOutput

from xml.dom import minidom
from ncclient import manager
from xml.etree.ElementTree import *
from xml.dom.minidom import parse, parseString

logging.config.fileConfig('logging.ini')
LOG = logging.getLogger('polatis')

""" global declaration for already existing ingress and egress ports
"""

ex_ingress_ports = []
ex_egress_ports = []

""" global declaration for connecting required ingress and egress ports
"""

req_ingress_ports = []
req_egress_ports = []

""" global declaration for ingeress and egress ports list from get and
get-config rpc request
"""

parsed_ingress_ports = []
parsed_egress_ports = []

""" global declaration for xmlstr from output xml from get and get-config rpc request,
then create xml for edit-config rpc request
"""
xmlstr = ''

""" global variable - using ncclient for connecting the polatis box
"""
sw_mgr = ''


class CrossConnects:

    def connect_switch(self, host, port, userName, password, timeout):
        
        """ Connect switch.
            Arguments: 
            host        : IP address.
            port        : Valid Port No.
            username    : Valid User Name. 
            password    : Valid password.
            timeout     : valid switch timeout with sec
        """

        global sw_mgr

        LOG.info("Connecting to  switch <IP:Port = %s:%s>\n" % (host,port))
        sw_mgr = manager.connect_ssh(host=host, port=port, username=userName, password=password,timeout=timeout, hostkey_verify=False)



    def write_to_file(self, file_name, data):

        """ write the output xml from 'get' and 'get-config' rpc request
        Arguments: 
            file_name    : Give any name
            data        : XML output 
        """
        f = open(file_name,'w')
        f.write(data)
        f.close()


    def prettify(self, xmlstr):

        """Used for prettify the XML output from switch.
        Arguments: 
           xmlstr       : any xml string
        """
           
        reparsed = minidom.parseString(xmlstr)
        return reparsed.toprettyxml(indent=" ")

    def create_box(self, testcase_name):
        
        """create box for test case name.
        Arguments:
        testcase_name	:	valid testcase name
        """
        
    	l = len(testcase_name)+7
   	start_end_session = '       +' + (l * '-') + '+       '
    	middle = '| ' +'   '+ str(testcase_name) +'  '+ ' |'

        print '%s\n       %s\n%s\n\n' % (start_end_session, middle, start_end_session)


    def get_existing_port_list(self):

        """get the existing ingress and egress port list from config.txt file
        """
        config = ConfigParser.ConfigParser()
        
        
        config.read('config.txt')
        
        ingressPrtRange = (config.get("crossconnect", "ingressPortRange")).split('-')
        egressPrtRange = (config.get("crossconnect", "egressPortRange")).split('-')
        
        for i in range(int(ingressPrtRange[0]), int(ingressPrtRange[1])+1):
            ex_ingress_ports.append(i)
        
        
        for j in range(int(egressPrtRange[0]), int(egressPrtRange[1])+1):
            ex_egress_ports.append(j)
        
        LOG.info('ex_ingress_ports : %s\n\n' % ex_ingress_ports)
        LOG.info('ex_egress_ports : %s\n\n' % ex_egress_ports)

    def cleanup_existing_connections(self, **kwargs):
   
        global sw_mgr

        self.create_box('cleanup_existing_connections')
        LOG.info('-----[ create xml for cleanup the all oxc connections ]-----\n')
        config = Element('config', {'xmlns:xc':"urn:ietf:params:xml:ns:netconf:base:1.0"})
        crossconnect = SubElement(config, 'cross-connects', {'xmlns':"http://www.polatis.com/yang/optical-switch",
                                                             'nc:operation':"delete",
                                                             'xmlns:nc':"urn:ietf:params:xml:ns:netconf:base:1.0"})
        xmlstr = tostring(config)
        xmldata = sw_mgr.edit_config(target='running', config=xmlstr)

        print '\n\n'
        LOG.info('-----[ create xml for get operation ]-----\n')
        crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

        xmlstr = tostring(crossconnects)
        xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)

    def compare_list(self, xmlData):

        """compare the ingress and egress port list.
        Arguments:
           xmlData              : get the xml output from 'get - config'
        """
        
        global xmlstr
        parsed_ingress_ports = []
        parsed_egress_ports = []
    
        global req_ingress_ports
        global req_egress_ports
   
        p = 'PASS'
        f = 'FAIL'
    
        DOMTree = xml.dom.minidom.parseString(xmlData)
        collection = DOMTree.documentElement
    
        pairs = collection.getElementsByTagName("pairs")
    
        for port in pairs:
            try:
               ingress = port.getElementsByTagName('ingress')[0]
               ingPrt =  str(ingress.childNodes[0].data)
    
               parsed_ingress_ports.append(ingPrt)
            except:
               pass
           
            try:
               egress = port.getElementsByTagName('egress')[0]
               egrPrt =  str(egress.childNodes[0].data)
    
               parsed_egress_ports.append(egrPrt)
            except:
               pass
    
        LOG.info('-----[ validate the oxc connection ]-----\n\n')

        LOG.info('required_ingress_ports : %s' % req_ingress_ports)
        LOG.info('required egress ports : %s\n\n' % req_egress_ports )
        LOG.info('parsed_ingress_ports : %s' % parsed_ingress_ports)
        LOG.info('parsed egress ports : %s\n\n' % parsed_egress_ports )
    
        if str(req_ingress_ports) == str(parsed_ingress_ports) and str(req_egress_ports) == str(parsed_egress_ports):
            LOG.info('compare the both ingress and egress ports : PASS\n')
        elif str(req_ingress_ports) == str(parsed_ingress_ports):
            LOG.info('compare the ingress ports : PASS\n')
        elif str(req_egress_ports) == str(parsed_egress_ports):
            LOG.info('compare the egress ports : PASS\n')
        else:
            LOG.error('comparision failed : FAIL\n')


    def get_crossconnects(self, **kwargs):

        """create the oxc b/w given ingress and egress ports and create the xml for
        crossconects tag for get operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Fially save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """
      
        self.create_box('get_crossconnects')
        s = time.time()
        LOG.info('-----[ create oxc conection ]-----\n')
        self.edit_config_create_oxc_without_opr(kwargs['ingress_ports'], kwargs['egress_ports'])

        LOG.info('-----[ create xml for get operation ]-----\n')
        crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

        xmlstr = tostring(crossconnects)
        xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('cross-connects', 'get_crossconnects', d, result)


    def get_pairs(self, **kwargs):

        """create the oxc b/w given ingress and egress ports and create the xml for
        pairs tag for get operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Fially save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """
      
        self.create_box('get_pairs')
        s = time.time()
        LOG.info('-----[ create oxc conection ]-----\n')
        self.edit_config_create_oxc_without_opr(kwargs['ingress_ports'], kwargs['egress_ports'])
        
        LOG.info('-----[ create xml for get operation ]-----\n')
        crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
        pairs = SubElement(crossconnects, 'opsw:pairs')

        xmlstr = tostring(crossconnects)
        xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('cross-connects', 'get_pairs', d, result)


    def get_ingress_port(self, **kwargs):

        """create the oxc b/w given ingress and egress ports and create the xml for
        ingress tag for get operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Fially save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """

        self.create_box('get_ingress_port')
        s = time.time()
        LOG.info('-----[ create oxc conection ]-----\n')
        self.edit_config_create_oxc_without_opr(kwargs['ingress_ports'], kwargs['egress_ports'])
        
        LOG.info('-----[ create xml for get operation ]-----\n')
     	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
   	pairs = SubElement(crossconnects, 'opsw:pairs')
    	ingress = SubElement(pairs, 'opsw:ingress')

    	xmlstr = tostring(crossconnects)
    	xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('cross-connects', 'get_ingress_port', d, result)


    def get_ingress_ports(self, **kwargs):
        
        """create the oxc b/w given ingress and egress ports and create the xml for
        many ingress ports for get operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Fially save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """
    
	global ex_ingress_ports
    	global req_ingress_ports
    
        self.create_box('get_ingress_ports')
        s = time.time()
        LOG.info('-----[ create oxc conection ]-----\n')
        self.edit_config_create_oxc_without_opr(kwargs['ingress_ports'], kwargs['egress_ports'])
        
        LOG.info('-----[ create xml for get operation ]-----\n')

    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    	ingSymbol = re.split(r'[\d]', portList)

    	if str(ingSymbol[1]) == ',' or str(ingSymbol[1]) == '':
           req_ingress_ports = portList.split(',')
    
    	if str(ingSymbol[2]) == '-' or str(ingSymbol[1]) == '-':
           req_ingress_ports = []
           req_ingress_ports1 = portList.split('-')
           for i in range(int(req_ingress_ports1[0]), int(ingPLst1[1])+1):
               req_ingress_ports.append(i)
               LOG.info('ingress port list: %s' % req_ingress_ports)
        else:
           LOG.error('Give for example comma or hypen seperated values ...\n\n')
        
   	l = len(req_ingress_ports)
    	for i in range(0, l):
            a = req_ingress_ports[i]
            if a in ex_ingress_ports:
               pairs = SubElement(crossconnects, 'opsw:pairs')
               ingress = SubElement(pairs, 'opsw:ingress')
               ingress.text = str(a)
            else:
               pairs = SubElement(crossconnects, 'opsw:pairs')
               ingress = SubElement(pairs, 'opsw:ingress')
               ingress.text = str(a)
           
        xmlstr = tostring(crossconnects)
        xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('cross-connects', 'get_ingress_ports', d, result)

    
    def get_egress_port(self, **kwargs):   
        
        """create the oxc b/w given ingress and egress ports and create the xml for
        egress tag for get operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Fially save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """
    
        self.create_box('get_egress_port')
        s = time.time()
        LOG.info('-----[ create oxc conection ]-----\n')
        self.edit_config_create_oxc_without_opr(kwargs['ingress_ports'], kwargs['egress_ports'])
        
        LOG.info('-----[ create xml for get operation ]-----\n')
    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
        pairs = SubElement(crossconnects, 'opsw:pairs')
        egress = SubElement(pairs, 'opsw:egress')
    
        xmlstr = tostring(crossconnects)
        xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('cross-connects', 'get_egress_port', d, result)

    def get_egress_ports(self, **kwargs):
        
        """create the oxc b/w given ingress and egress ports and create the xml for
        many egress ports for get operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Fially save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """
    	
        global ex_egress_ports 
    	global req_egress_ports
    	
        self.create_box('get_egress_ports')
        s = time.time()
        LOG.info('-----[ create oxc conection ]-----\n')
        self.edit_config_create_oxc_without_opr(kwargs['ingress_ports'], kwargs['egress_ports'])
        
        LOG.info('-----[ create xml for get operation ]-----\n')
    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
    	                                                    'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

    	egrSymbol = re.split(r'[\d]', portList)
    	
    	if str(egrSymbol[1]) == ',' or str(egrSymbol[1]) == '':
    	    req_egress_ports = portList.split(',')
    	
    	if str(ingSymbol[2]) == '-' or str(ingSymbol[1]) == '-':
    	    req_egress_ports = []
    	    req_egress_ports1 = portList.split('-')
    	    for i in range(int(req_egress_ports1[0]), int(egrPLst1[1])+1):
    	        req_egress_ports.append(i)
    	    LOG.info('egress port list: %s' % req_egress_ports)
    	else:
    	    LOG.error('Give for example comma or hypen seperated values ...\n\n')
    	    
    	l = len(req_egress_ports)
    	for i in range(0, l):
    	    a = req_egress_ports[i]
    	    if a in ex_egress_ports:
    	       pairs = SubElement(crossconnects, 'opsw:pairs')
    	       egress = SubElement(pairs, 'opsw:egress')
    	       egress.text = str(a)
    	    else:
    	       pairs = SubElement(crossconnects, 'opsw:pairs')
    	       egress = SubElement(pairs, 'opsw:egress')
    	       egress.text = str(a)

    	xmlstr = tostring(crossconnects)
        xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('cross-connects', 'get_egress_ports', d, result)


    def get_edit_config(self, **kwargs):
        
        """create the oxc b/w given ingress and egress ports and create the xml for
        get the edit-config oxc connection tag for get operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Fially save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """
    	
        global ex_ingress_ports
    	global req_ingress_ports
    	global ex_egress_ports 
    	global req_egress_ports
    	
        self.create_box('get_editconfig')
        s = time.time()
        LOG.info('-----[ create oxc conection ]-----\n')
        self.edit_config_create_oxc_without_opr(kwargs['ingress_ports'], kwargs['egress_ports'])
        
        LOG.info('-----[ create xml for get operation ]-----\n')
    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    	try:
    	    l = len(req_egress_ports)
    	    for i in range(0, l):
    	        a = req_ingress_ports[i]
    	        b = req_egress_ports[i]
    	        if a in ex_ingress_ports and b in ex_egress_ports:
    	           pairs = SubElement(crossconnects, 'opsw:pairs')
    	           ingress = SubElement(pairs, 'opsw:ingress')
    	           ingress.text = str(a)
    	           egress = SubElement(pairs, 'opsw:egress')
    	           egress.text = str(b)
    	        else:
    	           pairs = SubElement(crossconnects, 'opsw:pairs')
    	           ingress = SubElement(pairs, 'opsw:ingress')
    	           ingress.text = str(a)
    	           egress = SubElement(pairs, 'opsw:egress')
    	           egress.text = str(b)
    	except Exception as err:
    	    LOG.error('\t\t-----[ Error from the Switch ]-----\n\n%s\n\n', err)


    	xmlstr = tostring(crossconnects)
        xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('cross-connects', 'get_editconfig', d, result)


    def get_rpc_request(self, xmlstr, file_name):
        
        """perform get operation for created xmlstr
        Arguments:
           xmlstr	         : required tag xmlstr
           file_name             : any file name
        """

        try:
            #LOG.info('Quering for running configuration data from switch using get\n\n')
            #LOG.info('Get  - Response from the switch...\n\n')
        

            #s = time.time()
            xmlData = sw_mgr.get(filter=('subtree',xmlstr)).data_xml
            print '\n\n'
            prettyXml = self.prettify(xmlData)
            LOG.info('-----[ get - response from the switch ]-----\n\n%s\n' % prettyXml)

            return xmlData
            #e = time.time()
            #t = int(round((e - s)* 1000))
            self.write_to_file(file_name,prettyXml)
            #csvOutput('OXC', testcase_name, t, 'PASS')
		
        except Exception as err:
            print '\n\n'
            LOG.error('\t\t-----[ Error from the Switch ]-----\n\n%s\n\n', err)
            #csvOutput('OXC', testcase_name, 0, 'FAIL')

    
    def getconfig_crossconnects(self, **kwargs):
        
        """create the oxc b/w given ingress and egress ports and create the xml for
        cross-connects tag for get-config operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Fially save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """
        
        self.create_box('getconfig_crossconnects')
        s = time.time()
        LOG.info('-----[ create oxc conection ]-----\n')
        self.edit_config_create_oxc_without_opr(kwargs['ingress_ports'], kwargs['egress_ports'])
        
        LOG.info('-----[ create xml for get-config operation ]-----\n')
	
    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",

    	                                                    'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

    	xmlstr = tostring(crossconnects)
        xmlout = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('cross-connects', 'getconfig_crossconnects', d, result)
   

    ### get-config - pairs ###

    def getconfig_pairs(file_name):
        
        """create the oxc b/w given ingress and egress ports and create the xml for
        get the edit-config oxc connection tag for get operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Fially save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """

    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
    	                                            'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    	pairs = SubElement(crossconnects, 'opsw:pairs')

    	xmlstr = tostring(crossconnects)
    	self.getconfig_rpc_request('getConfig - Query pairs', xmlstr, file_name)

    ### get-config - ingress ports ###

    def getconfig_ingress_port(file_name):
        
        """create the oxc b/w given ingress and egress ports and create the xml for
        get the edit-config oxc connection tag for get operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Fially save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """

    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
    	                                                'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    	pairs = SubElement(crossconnects, 'opsw:pairs')
    	ingress = SubElement(pairs, 'opsw:ingress')

    	xmlstr = tostring(crossconnects)
    	self.getconfig_rpc_request('getConfig - Query ingress', xmlstr, file_name)



    ### get-config - required ingress port list ###

    def getconfig_ingress_ports(file_name, portList):
	
        """create the oxc b/w given ingress and egress ports and create the xml for
	get the edit-config oxc connection tag for get operation, get the xml output from this, then parsed this xml
	, from parsed xml get the ingress and egress port list, then compare this ports
	with given ports.Fially save the output in final.csv file
	Arguments:
	file_name             : any file name
	ingressPort list      : valid ingress port list
	egressPort list       : valid egress port list
	"""
    
 	global ex_ingress_ports
    	global req_ingress_ports
    	
    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
    	                                                'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    	ingSymbol = re.split(r'[\d]', portList)

    	if str(ingSymbol[1]) == ',' or str(ingSymbol[1]) == '':
    	    req_ingress_ports = portList.split(',')
    	
    	if str(ingSymbol[2]) == '-' or str(ingSymbol[1]) == '-':
    	    req_ingress_ports = []
    	    req_ingress_ports1 = portList.split('-')
    	    for i in range(int(req_ingress_ports1[0]), int(ingPLst1[1])+1):
    	        req_ingress_ports.append(i)
    	    LOG.info('ingress port list: %s' % req_ingress_ports)
    	else:
    	    LOG.error('Give for example comma or hypen seperated values ...\n\n')
    	    
    	l = len(req_ingress_ports)
    	for i in range(0, l):
    	    a = req_ingress_ports[i]
    	    if a in ex_ingress_ports:
    	       pairs = SubElement(crossconnects, 'opsw:pairs')
    	       ingress = SubElement(pairs, 'opsw:ingress')
    	       ingress.text = str(a)
    	    else:
    	       pairs = SubElement(crossconnects, 'opsw:pairs')
    	       ingress = SubElement(pairs, 'opsw:ingress')
    	       ingress.text = str(a)
    	       
    	xmlstr = tostring(crossconnects)
    	self.getconfig_rpc_request('getConfig - Query given ingress ports', xmlstr, file_name)


    
    ### get-config - egress ports ###

    def getconfig_egress_port(self, **kwargs):   
        
        """create the oxc b/w given ingress and egress ports and create the xml for
        get the edit-config oxc connection tag for get operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Fially save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """
    
    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
    	                                                'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    	pairs = SubElement(crossconnects, 'opsw:pairs')
    	egress = SubElement(pairs, 'opsw:egress')
    	xmlstr = tostring(crossconnects)
    	self.getconfig_rpc_request('getConfig - Query egress ports', xmlstr, file_name)

    ### get-config - required egress port list ###

    def getconfig_egress_ports(self, **kwargs):
        
        """create the oxc b/w given ingress and egress ports and create the xml for
        get the edit-config oxc connection tag for get operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Fially save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """
    	global ex_egress_ports 
    	global req_egress_ports
    	
    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
    	                                                'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

    	egrSymbol = re.split(r'[\d]', portList)
    	
    	if str(egrSymbol[1]) == ',' or str(egrSymbol[1]) == '':
    	    req_egress_ports = portList.split(',')
    	
    	if str(ingSymbol[2]) == '-' or str(ingSymbol[1]) == '-':
    	    req_egress_ports = []
    	    req_egress_ports1 = portList.split('-')
    	    for i in range(int(req_egress_ports1[0]), int(egrPLst1[1])+1):
    	        req_egress_ports.append(i)
    	    LOG.info('egress port list: %s' % req_egress_ports)
    	else:
    	    LOG.error('Give for example comma or hypen seperated values ...\n\n')
    	    
    	l = len(req_egress_ports)
    	for i in range(0, l):
    	    a = req_egress_ports[i]
    	    if a in ex_egress_ports:
    	       pairs = SubElement(crossconnects, 'opsw:pairs')
    	       egress = SubElement(pairs, 'opsw:egress')
    	       egress.text = str(a)
    	    else:
    	       pairs = SubElement(crossconnects, 'opsw:pairs')
    	       egress = SubElement(pairs, 'opsw:egress')
    	       egress.text = str(a)

    	xmlstr = tostring(crossconnects)
    	self.getconfig_rpc_request('getConfig - Query given egress ports', xmlstr, file_name)

    ### get-config - from edit-config configuration ###
    
    def getconfig_edit_config(file_name):
        
        """create the oxc b/w given ingress and egress ports and create the xml for
        get the edit-config oxc connection tag for get operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Fially save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """
    	
        global ex_ingress_ports
    	global req_ingress_ports
    	global ex_egress_ports 
    	global req_egress_ports
    	   
    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
    	                                                'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    	try:
    	    l = len(req_egress_ports)
    	    for i in range(0, l):
    	        a = req_ingress_ports[i]
    	        b = req_egress_ports[i]
    	        if a in ex_ingress_ports and b in ex_egress_ports:
    	           pairs = SubElement(crossconnects, 'opsw:pairs')
    	           ingress = SubElement(pairs, 'opsw:ingress')
    	           ingress.text = str(a)
    	           egress = SubElement(pairs, 'opsw:egress')
    	           egress.text = str(b)
    	        else:
    	           pairs = SubElement(crossconnects, 'opsw:pairs')
    	           ingress = SubElement(pairs, 'opsw:ingress')
    	           ingress.text = str(a)
    	           egress = SubElement(pairs, 'opsw:egress')
    	           egress.text = str(b)
    	except Exception as err:
    	    LOG.error('\t\t-----[ Error from the Switch ]-----\n\n%s\n\n', err)

    	xmlstr = tostring(crossconnects)
    	self.getconfig_rpc_request('getConfig - Query ports list connected by using edit-config', xmlstr, file_name)


    ### get-config - for required switch operation ###

    def getconfig_rpc_request(self, xmlstr, file_name):
        
        """perform get-config operation for created xmlstr
        Arguments:
           xmlstr	         : required tag xmlstr
           file_name             : any file name
        """
      
        global sw_mgr
    	global cnt


    	try:
    	    xmlData = sw_mgr.get_config(source='running',  filter=('subtree',xmlstr)).data_xml
    	    print '\n\n'


    	    prettyXml = self.prettify(xmlData)
            LOG.info('-----[ getconfig - response from the switch ]-----\n\n%s\n' % prettyXml)
            return xmlData

    	    self.write_to_file(file_name, prettyXml);

    	    	
    	except Exception as err:
    	    print '\n\n'
    	    LOG.error('\t\t-----[ Error from the Switch ]-----\n\n%s\n\n', err)




    def create_xml(self, operation):

        """create xml file for required oxc connection
        Arguments:
           operation             : valid oxc opeation 
           
        """             
        global ex_ingress_ports
        global ex_egress_ports
        global req_ingress_ports
        global req_egress_ports
        global xmlstr
        
        l = len(req_ingress_ports)
        config = Element('config', {'xmlns:xc':"urn:ietf:params:xml:ns:netconf:base:1.0"})
        crossconnect = SubElement(config, 'cross-connects', {'xmlns':"http://www.polatis.com/yang/optical-switch"})


        for i in range(0, l):
            a = req_ingress_ports[i]
            b = req_egress_ports[i]
            if a in ex_ingress_ports and b in ex_egress_ports:
               pairs = SubElement(crossconnect, 'pairs', {'ns:operation':operation})
               ingress = SubElement(pairs, 'ingress')
               ingress.text = str(a)
               egress = SubElement(pairs, 'egress')
               egress.text = str(b)
            else:
               pairs = SubElement(crossconnect, 'pairs', {'ns:operation':operation})
               ingress = SubElement(pairs, 'ingress')
               ingress.text = str(a)
               egress = SubElement(pairs, 'egress')
               egress.text = str(b)
        
        xmlstr = tostring(config)
        return xmlstr


    def split_port_list(self, ingress_ports, egress_ports):

        """used to split ports list in the form of ',' and '-' seperated values
        Arguments:
           ingress_ports             : valid ingress ports
           egress_ports              : valid egress ports
        """
        
        global req_ingress_ports
        global req_egress_ports
        global ex_ingress_ports
        global ex_egress_ports

            
        ingSymbol = re.split(r'[\d]', ingress_ports)

        ### if-else loop is used to check the connecting operation(random/direct) ###
        if str(ingSymbol[0]) == ',' or str(ingSymbol[0]) == '':
            req_ingress_ports = ingress_ports.split(',')
            req_egress_ports = egress_ports.split(',')
    
        if str(ingSymbol[2]) == '-' or str(ingSymbol[1]) == '-':
            req_ingress_ports = []
            req_egress_ports = []
    
    
            list1 = ingress_ports.split('-')
            list2 = egress_ports.split('-')
            
    
            if int(list1[0]) > int(list1[1]) and int(list2[0]) > int(list2[1]):
                list1.reverse()
                list2.reverse()
                for i,j in zip(range(int(list1[0]), int(list1[1])+1), range(int(list2[0]), int(list2[1])+1)):
                    req_ingress_ports.append(i)
                    req_egress_ports.append(j)
                req_ingress_ports.reverse()
                req_egress_ports.reverse()
            elif int(list1[0]) > int(list1[1]) and int(list2[0]) < int(list2[1]):
                list1.reverse()
                for i,j in zip(range(int(list1[0]), int(list1[1])+1), range(int(list2[0]), int(list2[1])+1)):
                    req_ingress_ports.append(i)
                    req_egress_ports.append(j)
                req_ingress_ports.reverse()
            elif int(list2[0]) > int(list2[1]) and int(list1[0]) < int(list1[1]):
                list2.reverse()
                for i,j in zip(range(int(list1[0]), int(list1[1])+1), range(int(list2[0]), int(list2[1])+1)):
                    req_ingress_ports.append(i)
                    req_egress_ports.append(j)
                req_egress_ports.reverse()
            else:
                for i,j in zip(range(int(list1[0]), int(list1[1])+1), range(int(list2[0]), int(list2[1])+1)):
                    req_ingress_ports.append(i)
                    req_egress_ports.append(j)
    
        #else:
        #    LOG.error('SplitPortList---------------------------------')
        #    LOG.error('Give for example comma or hypen seperated values ...\n\n')


    
    def editconfig_create_operation(self, **kwargs):
    	global xmlstr
    	
        self.create_box('get_editconfig_create_operation')
    	self.split_port_list(kwargs['ingress_ports'], kwargs['egress_ports'])
        s = time.time()
        LOG.info('create xml using CREATE operation')
    	xmlstr = self.create_xml('create')
    	self.edit_config_opr()
        LOG.info('-----[ create xml using get-config operation ]-----')
    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",

    	                                                    'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

    	xmlstr = tostring(crossconnects)
        xmlout = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('cross-connects', 'getconfig_crossconnects', d, result)

    def deleteOXC_editConfig(ingress_ports, egress_ports):
    	global xmlstr
    	
    	self.split_port_list(ingress_ports, egress_ports)
    	self.create_xml('delete')
    	self.edit_config_opr('editConfig - delete OXC')

    def replaceOXC_editConfig(ingress_ports, egress_ports):
    	global xmlstr
    	
    	self.split_port_list(ingress_ports, egress_ports)
    	self.create_xml('replace')
    	self.edit_config_opr('editConfig - replace OXC')

    ### remove OXC for given ports ###
    def removeOXC_editConfig(ingress_ports, egress_ports):
    	global xmlstr
    	
    	self.split_port_list(ingress_ports, egress_ports)
    	self.create_xml('remove')
    	self.edit_config_opr('editConfig - remove OXC')


    ### merge OXC for given ports ###
    def mergeOXC_editConfig(ingress_ports, egress_ports):
    	global xmlstr
    	
    	self.split_port_list(ingress_ports, egress_ports)
    	self.create_xml('merge')
    	self.edit_config_opr('editConfig - merge OXC')



    def edit_config_create_oxc_without_opr(self, ingress_ports, egress_ports):

        """create oxc for given ingress and egress ports without any operation
        Arguments:
           ingress_ports             : valid ingress ports
           egress_ports              : valid egress ports
        """
        global req_ingress_ports
        global req_egress_ports
        global ex_ingress_ports
        global ex_egress_ports
        global xmlstr
        
        self.split_port_list(ingress_ports, egress_ports)
        
        l = len(req_ingress_ports)
        config = Element('config', {'xmlns:xc':"urn:ietf:params:xml:ns:netconf:base:1.0"})
        crossconnect = SubElement(config, 'cross-connects', {'xmlns':"http://www.polatis.com/yang/optical-switch"})
    
        for i in range(0, l):
            a = req_ingress_ports[i]
            b = req_egress_ports[i]
            if a in ex_ingress_ports and b in ex_egress_ports:
                pairs = SubElement(crossconnect, 'pairs')
                ingress = SubElement(pairs, 'ingress')
                ingress.text = str(a)
                egress = SubElement(pairs, 'egress')
                egress.text = str(b)
            else:
                pairs = SubElement(crossconnect, 'pairs')
                ingress = SubElement(pairs, 'ingress')
                ingress.text = str(a)
                egress = SubElement(pairs, 'egress')
                egress.text = str(b)
        
        xmlstr = tostring(config)
        self.edit_config_opr()
    
    
    def edit_config_opr(self):

        """ create the required oxc operationusing edit-config rpc request.
        Arguments:
        testcase_name              : test case name
        """
        
        global sw_mgr
        global xmlstr
        global cnt
        global ex_ingress_ports
        global req_ingress_ports
        global ex_egress_ports 
        global req_egress_ports
        s = time.time()
           
        try:
           LOG.info('ingress port list: %s' % req_ingress_ports)
           LOG.info('egress port list : %s\n\n' % req_egress_ports)
           
           LOG.info("pass xml for edit-config operation\n")
    
    
           xmldata = sw_mgr.edit_config(target='running', config=xmlstr)
           print "\n\n"
    
        
           LOG.info('edit-config - response from the switch\n\n%s\n\n' % xmldata)
    
           #crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
           #                                                'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
           #try:
           #   l = len(req_egress_ports)
           #   for i in range(0, l):
           #       a = req_ingress_ports[i]
           #       b = req_egress_ports[i]
           #       if a in ex_ingress_ports and b in ex_egress_ports:
           #          pairs = SubElement(crossconnects, 'opsw:pairs')
           #          ingress = SubElement(pairs, 'opsw:ingress')
           #          ingress.text = str(a)
           #          egress = SubElement(pairs, 'opsw:egress')
           #          egress.text = str(b)
           #       else:
           #          pairs = SubElement(crossconnects, 'opsw:pairs')
           #          ingress = SubElement(pairs, 'opsw:ingress')
           #          ingress.text = str(a)
           #          egress = SubElement(pairs, 'opsw:egress')
           #          egress.text = str(b)
           #except Exception as err:
           #   LOG.error('\t\t-----[ Error from the Switch ]-----\n\n%s\n\n' % err)
    
    
           #LOG.info('-----[ Compare the Edit Config and Get Config Ports ]-----\n\n')
           #xmlstr = tostring(crossconnects)
           #xmlData = sw_mgr.get_config(source='running',  filter=('subtree',xmlstr)).data_xml
           #print "\n\n"
         
           #prettyXml = self.prettify(xmlData)
           #LOG.info('Get  config -  Response from the switch\n\n%s \n\n' % prettyXml)
           #

           #result = self.cmpIngEgrPortLst(xmlData)
    
           #e = time.time()
           #t = int(round((e - s)* 1000))
           #csvOutput('OXC', testcase_name, t,'pass')
           ##LOG.info('result is %s' % result)
    
        except Exception as err:
           print "\n\n"
           LOG.error('\t\t-----[ Error from the Switch ]-----\n\n%s\n\n' %  err)
           #e = time.time()
           #t = int(round((e - s)* 1000))
    
           #csvOutput('OXC', testcase_name, t, 'fail')
    



        
