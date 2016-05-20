""" Python file that covers tabs under "cross-connects" container in optical switch.
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
from config import get_config_arg

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


""" global declaration for xmlstr from output xml from get and get-config rpc request,
then create xml for edit-config rpc request
"""
xmlstr = ''

""" global variable - using ncclient for connecting the polatis box
"""
sw_mgr = ''


class CrossConnects:

    def connect_switch(self):
        
        """ Connect switch.
            Arguments: 
            host        : IP address.
            port        : Valid Port No.
            username    : Valid User Name. 
            password    : Valid password.
            timeout     : valid switch timeout with sec
        """

        global sw_mgr
     
        host = get_config_arg("login_credentials", "host")
        port = get_config_arg("login_credentials", "port")
        username = get_config_arg("login_credentials", "user_name")
        password = get_config_arg("login_credentials", "password")
        timeout = get_config_arg("login_credentials", "timeout") 

        LOG.info("Connecting switch <IP:Port = %s:%s>\n" % (host,port))
        sw_mgr = manager.connect_ssh(host=host, port=port, username=username, password=password,timeout=int(timeout), hostkey_verify=False)



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
       
        print "\n" 
    	l = len(testcase_name)+7
   	start_end_session = '       +' + (l * '-') + '+       '
    	middle = '| ' +'   '+ str(testcase_name) +'  '+ ' |'

        print '%s\n       %s\n%s\n\n' % (start_end_session, middle, start_end_session)


    def get_existing_port_list(self):

        """get the existing ingress and egress port list from config.txt file
        """
        
        ingressPrtRange = (get_config_arg("cross_connects", "ingress_ports_range")).split('-')
        egressPrtRange = (get_config_arg("cross_connects", "egress_ports_range")).split('-')
        
        for i in range(int(ingressPrtRange[0]), int(ingressPrtRange[1])+1):
            ex_ingress_ports.append(i)
        
        
        for j in range(int(egressPrtRange[0]), int(egressPrtRange[1])+1):
            ex_egress_ports.append(j)
        
        LOG.info('ex_ingress_ports : %s\n\n' % ex_ingress_ports)
        LOG.info('ex_egress_ports : %s\n\n' % ex_egress_ports)

    def cleanup_existing_connections(self, **kwargs):
   
        global sw_mgr
        global req_ingress_ports
        global req_egress_ports 

        #self.create_box('test_cleanup_existing_connections')
        LOG.info('\n\n\t\t\t-----[ cleanup_existing_connections ]-----\n\n')
        LOG.info('-----[ create xml for cleanup the all oxc connections ]-----\n')
        config = Element('config', {'xmlns:ns':"urn:ietf:params:xml:ns:netconf:base:1.0"})
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
        req_ingress_ports = []
        req_egress_ports = []
        result = self.compare_list(xmlout)


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
       
        #self.create_box('test_edit_config_create_oxc_without_opr')
        LOG.info('\n\n\t\t\t-----[ edit_config_create_oxc_without_opr ]-----\n\n')
        LOG.info('-----[ create oxc conection ]-----\n') 
        self.split_port_list(ingress_ports, egress_ports)
        s = time.time()
        l = len(req_ingress_ports)
        config = Element('config', {'xmlns:ns':"urn:ietf:params:xml:ns:netconf:base:1.0"})
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
    
        LOG.info('-----[ validate oxc connection ]-----\n\n')

        LOG.info('required_ingress_ports : %s' % req_ingress_ports)
        LOG.info('required_egress_ports : %s\n\n' % req_egress_ports )
        LOG.info('parsed_ingress_ports : %s' % parsed_ingress_ports)
        LOG.info('parsed_egress_ports : %s\n\n' % parsed_egress_ports )
 
        

        if str(req_ingress_ports) == str(parsed_ingress_ports) and str(req_egress_ports) == str(parsed_egress_ports):
            LOG.info('compare both ingress and egress ports : PASS\n')
            return p
        elif str(req_ingress_ports) == str(parsed_ingress_ports):
            LOG.info('compare ingress ports : PASS\n')
            return p
        elif str(req_egress_ports) == str(parsed_egress_ports):
            LOG.info('compare egress ports : PASS\n')
            return p
        else:
            LOG.error('comparision failed : FAIL\n')
            return f
        


    def get_crossconnects(self, **kwargs):

        """create the oxc b/w given ingress and egress ports and create xml for
        crossconects tag for get operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """
      
        self.create_box('test_get_crossconnects')
        s = time.time()

        LOG.info('-----[ create xml for get operation ]-----\n')
        crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

        xmlstr = tostring(crossconnects)
        xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('cross-connects', 'get_crossconnects', d, result)
        nose.tools.assert_equals('PASS', result)


    def get_pairs(self, **kwargs):

        """create the oxc b/w given ingress and egress ports and create the xml for
        pairs tag for get operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """
      
        self.create_box('test_get_pairs')
        s = time.time()
        
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
        nose.tools.assert_equals('PASS', result)


    def get_ingress(self, **kwargs):

        """create the oxc b/w given ingress and egress ports and create the xml for
        ingress tag for get operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """

        self.create_box('test_get_ingress')
        s = time.time()
        
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
        nose.tools.assert_equals('PASS', result)


    def get_ingress_ports(self, **kwargs):
        
        """create the oxc b/w given ingress and egress ports and create the xml for
        many ingress ports for get operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """
    
	global ex_ingress_ports
    	global req_ingress_ports
    
        self.create_box('test_get_ingress_ports')
        s = time.time()
        
        LOG.info('-----[ create xml for get operation ]-----\n')

    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
        
        req_ingress_ports = kwargs['ingress_ports']
        
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
        nose.tools.assert_equals('PASS', result)

    
    def get_egress(self, **kwargs):   
        
        """create the oxc b/w given ingress and egress ports and create the xml for
        egress tag for get operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """
    
        self.create_box('test_get_egress')
        s = time.time()
        
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
        nose.tools.assert_equals('PASS', result)

    def get_egress_ports(self, **kwargs):
        
        """create the oxc b/w given ingress and egress ports and create the xml for
        many egress ports for get operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """
    	
        global ex_egress_ports 
    	global req_egress_ports
    	
        self.create_box('test_get_egress_ports')
        s = time.time()
        
        LOG.info('-----[ create xml for get operation ]-----\n')
    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
    	                                                    'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

    	req_egress_ports = kwargs['egress_ports']
    	    
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
        nose.tools.assert_equals('PASS', result)


    def get_rpc_request(self, xmlstr, file_name):
        
        """perform get operation for created xmlstr
        Arguments:
           xmlstr	         : required tag xmlstr
           file_name             : any file name
        """

        try:
            xmlData = sw_mgr.get(filter=('subtree',xmlstr)).data_xml
            print '\n\n'
            prettyXml = self.prettify(xmlData)
            LOG.info('-----[ get - response from the switch ]-----\n\n%s\n' % prettyXml)

            self.write_to_file(file_name,prettyXml)
            return xmlData
		
        except Exception as err:
            print '\n\n'
            LOG.error('-----[ Error from the Switch ]-----\n\n%s\n\n', err)

    
    def getconfig_crossconnects(self, **kwargs):
        
        """create the oxc b/w given ingress and egress ports and create the xml for
        cross-connects tag for get-config operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """
        
        self.create_box('test_getconfig_crossconnects')
        s = time.time()
        
        LOG.info('-----[ create xml for get-config operation ]-----\n')
	
    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",

    	                                                    'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

    	xmlstr = tostring(crossconnects)
        xmlout = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('cross-connects', 'getconfig_pairs', d, result)
        nose.tools.assert_equals('PASS', result)
   


    def getconfig_pairs(self, **kwargs):
        
        """create the oxc b/w given ingress and egress ports and create the xml for
        pairs tag for get-config  operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """

        self.create_box('test_getconfig_pairs')
        s = time.time()
        
        LOG.info('-----[ create xml for get-config operation ]-----\n')
    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
    	                                            'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    	pairs = SubElement(crossconnects, 'opsw:pairs')

    	xmlstr = tostring(crossconnects)
        xmlout = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('cross-connects', 'getconfig_crossconnects', d, result)
        nose.tools.assert_equals('PASS', result)


    def getconfig_ingress(self, **kwargs):
        
        """create the oxc b/w given ingress and egress ports and create the xml for
        single ingress port for get-config operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """

        self.create_box('test_getconfig_ingress')
        s = time.time()
        
        LOG.info('-----[ create xml for get-config operation ]-----\n')
    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
    	                                                'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    	pairs = SubElement(crossconnects, 'opsw:pairs')
    	ingress = SubElement(pairs, 'opsw:ingress')

    	xmlstr = tostring(crossconnects)
        xmlout = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('cross-connects', 'getconfig_ingress_port', d, result)
        nose.tools.assert_equals('PASS', result)




    def getconfig_ingress_ports(self, **kwargs):
	
        """create the oxc b/w given ingress and egress ports and create the xml for
	multiple ingress ports for get-config  operation, get the xml output from this, then parsed this xml
	, from parsed xml get the ingress and egress port list, then compare this ports
	with given ports.Finally save the output in final.csv file
	Arguments:
	file_name             : any file name
	ingressPort list      : valid ingress port list
	egressPort list       : valid egress port list
	"""
    
 	global ex_ingress_ports
    	global req_ingress_ports
        self.create_box('test_getconfig_ingress_ports')
        s = time.time()
        
        LOG.info('-----[ create xml for get-config operation ]-----\n')
    	
    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
    	                                                'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    	req_ingress_ports = kwargs['ingress_ports']
    	    
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
        xmlout = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('cross-connects', 'getconfig_ingress_ports', d, result)
        nose.tools.assert_equals('PASS', result)


    

    def getconfig_egress(self, **kwargs):   
        
        """create the oxc b/w given ingress and egress ports and create the xml for
        egress port tag for get-config operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """
    
        self.create_box('test_getconfig_egress')
        s = time.time()
        
        LOG.info('-----[ create xml for get-config operation ]-----\n')
    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
    	                                                'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    	pairs = SubElement(crossconnects, 'opsw:pairs')
    	egress = SubElement(pairs, 'opsw:egress')
    	xmlstr = tostring(crossconnects)
        xmlout = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('cross-connects', 'getconfig_egress_port', d, result)
        nose.tools.assert_equals('PASS', result)


    def getconfig_egress_ports(self, **kwargs):
        
        """create the oxc b/w given ingress and egress ports and create the xml for
        multiple egress ports for get-config operation, get the xml output from this, then parsed this xml
        , from parsed xml get the ingress and egress port list, then compare this ports
        with given ports.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        ingressPort list      : valid ingress port list
        egressPort list       : valid egress port list
        """
    	global ex_egress_ports 
    	global req_egress_ports
    	
        self.create_box('test_getconfig_egress_ports')
        s = time.time()
        
        LOG.info('-----[ create xml for get-config operation ]-----\n')
    	crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
    	                                                'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

        req_egress_ports = kwargs['egress_ports']
    	
    	    
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
        xmlout = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('cross-connects', 'getconfig_egress_ports', d, result)
        nose.tools.assert_equals('PASS', result)

    

    def getconfig_rpc_request(self, xmlstr, file_name):
        
        """perform get-config operation for created xmlstr
        Arguments:
           xmlstr	         : required tag xmlstr
           file_name             : any file name
        """
      
        global sw_mgr


    	try:
    	    xmlData = sw_mgr.get_config(source='running',  filter=('subtree',xmlstr)).data_xml
    	    print '\n\n'


    	    prettyXml = self.prettify(xmlData)
            LOG.info('-----[ getconfig - response from the switch ]-----\n\n%s\n' % prettyXml)

    	    self.write_to_file(file_name, prettyXml);
            return xmlData

    	    	
    	except Exception as err:
    	    print '\n\n'
    	    LOG.error('-----[ Error from the Switch ]-----\n\n%s\n\n', err)




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
       
        LOG.info('req_egress_ports : %s\n' % req_egress_ports)
        #LOG.info('type Ing port : %s\n' % type(req_ingress_ports))
        #LOG.info('type Eg port : %s \n' %  type(req_egress_ports))

        l = len(req_ingress_ports)
        config = Element('config', {'xmlns:ns':"urn:ietf:params:xml:ns:netconf:base:1.0"})
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

            
        #req_ingress_ports = ingress_ports.split(',')
        #req_egress_ports = egress_ports.split(',')
        req_ingress_ports = ingress_ports
        req_egress_ports = egress_ports
        #LOG.info(type(req_ingress_ports))
        #LOG.info(type(req_egress_ports))

    
    def editconfig_create_operation(self, **kwargs):
        
        """create the xml using CREATE operation, then get the configuration using
        get-config operation, parsed the output and then compare the both ports list
        Arguments:
        ingress_ports		: valid ingress ports
        egress ports		: valid egress ports
        """

    	global xmlstr
    	
        self.create_box('test_editconfig_create_operation')
    	self.split_port_list(kwargs['ingress_ports'], kwargs['egress_ports'])
        s = time.time()
        
        LOG.info('-----[ create xml for edit-config CREATE operation ]-----\n')
    	xmlstr = self.create_xml('create')
    	result = self.edit_config_opr()
        if result == 'PASS':
            LOG.info('-----[ create xml for get-config operation ]-----\n')
            crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",                                                                          'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

       	    xmlstr = tostring(crossconnects)
            xmlout = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
            result = self.compare_list(xmlout)
            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('cross-connects', 'editconfig_create_operation', d, result)
        else:
            LOG.info('getting error from switch : FAIL')
        nose.tools.assert_equals('PASS', result)

    def editconfig_replace_operation(self, **kwargs):
        
        """create the xml using replace operation, then get the configuration using
        get-config operation, parsed the output and then compare the both ports list
        Arguments:
        ingress_ports		: valid ingress ports
        egress ports		: valid egress ports
        """
    	global xmlstr
    	
        self.create_box('test_editconfig_replace_operation')
    	self.split_port_list(kwargs['ingress_ports'], kwargs['egress_ports'])
        s = time.time()
    	xmlstr = self.create_xml('replace')
    	result = self.edit_config_opr()
        if result == 'PASS':
            LOG.info('-----[ create xml for get-config operation ]-----\n')
    	    crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                            'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

    	    xmlstr = tostring(crossconnects)
            xmlout = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
            result = self.compare_list(xmlout)
            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('cross-connects', 'editconfig_replace_operation', d, result)
        else:
            LOG.info('getting error from switch : FAIL')

        nose.tools.assert_equals('PASS', result)


    def editconfig_delete_operation(self, **kwargs):
        
        """create the xml using DELETE operation, then get the configuration using
        get-config operation, parsed the output and then compare the both ports list
        Arguments:
        ingress_ports		: valid ingress ports
        egress ports		: valid egress ports
        """
    	global xmlstr
        global req_ingress_ports
        global req_egress_ports 
    	
        self.create_box('test_editconfig_delete_operation')
    	self.split_port_list(kwargs['ingress_ports'], kwargs['egress_ports'])
        s = time.time()
    	xmlstr = self.create_xml('delete')
    	result = self.edit_config_opr()
        
        if result == 'PASS':
            LOG.info('-----[ create xml for get-config operation ]-----\n')
    	    crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                            'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

    	    xmlstr = tostring(crossconnects)
            xmlout = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
            req_ingress_ports = []
            req_egress_ports = []
            result = self.compare_list(xmlout)
            LOG.info('req_ingress_ports : %s\n' % req_ingress_ports)
            LOG.info('req_egress_ports : %s\n' % req_egress_ports)
            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('cross-connects', 'editconfig_delete_operation', d, result)
        else:
            LOG.info('getting error from switch : FAIL')
        nose.tools.assert_equals('PASS', result)

    def editconfig_negative_case_with_invalid_ingress_port(self, **kwargs):
        
        """create the xml with invalid ingress port, then get the configuration using
        get-config operation, parsed the output and then compare the both ports list
        Arguments:
        ingress_ports		: valid ingress ports
        egress ports		: valid egress ports
        """
    	global xmlstr
        global req_ingress_ports
        global req_egress_ports 
   
	
        self.create_box('test_editconfig_negative_case_with_invalid_ingress_port')
    	#self.split_port_list(kwargs['ingress_ports'], kwargs['egress_ports'])
        req_ingress_ports = kwargs['ingress_ports'].split()
        req_egress_ports = kwargs['egress_ports']

        s = time.time()
    	xmlstr = self.create_xml('create')
    	result = self.edit_config_opr()
        if result == 'PASS':
            LOG.info('-----[ create xml for get-config operation ]-----\n')
            crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                            'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    
            xmlstr = tostring(crossconnects)
            xmlout = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
            result = self.compare_list(xmlout)
            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('cross-connects', 'editconfig_negative_case_with_ingress_port', d, result)
        else:
            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('cross-connects', 'editconfig_negative_case_with_ingress_port', d, 'PASS')
            LOG.info('getting error from switch using invalid ingress port : PASS\n\n')
        
        #e = time.time()
        #d = int(round((e - s)* 1000))
        #csvOutput('cross-connects', 'editconfig_negative_case_invalid_oxc_connection', d, result)
        nose.tools.assert_equals('FAIL', result)


    def editconfig_negative_case_with_invalid_egress_port(self, **kwargs):
        
        """create the xml with invalid egress port, then get the configuration using
        get-config operation, parsed the output and then compare the both ports list
        Arguments:
        ingress_ports		: valid ingress ports
        egress ports		: valid egress ports
        """
    	global xmlstr
        global req_ingress_ports
        global req_egress_ports 
   
	
        self.create_box('test_editconfig_negative_case_with_invalid_egress_port')
    	#self.split_port_list(kwargs['ingress_ports'], kwargs['egress_ports'])
        req_ingress_ports = kwargs['ingress_ports']
        req_egress_ports = kwargs['egress_ports']
        s = time.time()
    	xmlstr = self.create_xml('create')
    	result = self.edit_config_opr()
        if result == 'PASS':
            LOG.info('-----[ create xml for get-config operation ]-----\n')
    	    crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                            'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

    	    xmlstr = tostring(crossconnects)
            xmlout = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
            result = self.compare_list(xmlout)
            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('cross-connects', 'editconfig_negative_case_with_egress_port', d, result)
        else:
            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('cross-connects', 'editconfig_negative_case_with_ingress_port', d, 'PASS')
            LOG.info('getting error from switch using invalid egress port : PASS\n\n')

        #e = time.time()
        #d = int(round((e - s)* 1000))
        #csvOutput('cross-connects', 'editconfig_negative_case_invalid_oxc_connection', d, result)
        nose.tools.assert_equals('FAIL', result)

    def editconfig_negative_case_with_invalid_oxc_connection(self, **kwargs):
        
        """create the xml for invalid oxc operation, then get the configuration using
        get-config operation, parsed the output and then compare the both ports list
        Arguments:
        ingress_ports		: valid ingress ports
        egress ports		: valid egress ports
        """
    	global xmlstr
        global req_ingress_ports
        global req_egress_ports 
   
	
        self.create_box('test_editconfig_negative_case_for_invalid_oxc_connection')
    	#self.split_port_list(kwargs['ingress_ports'], kwargs['egress_ports'])
        req_ingress_ports = kwargs['ingress_ports'].split()
        req_egress_ports = kwargs['egress_ports'].split()
        s = time.time()
    	xmlstr = self.create_xml('create')
    	result = self.edit_config_opr()
        if result == 'PASS':
            LOG.info('-----[ create xml for get-config operation ]-----\n')
    	    crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                            'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

    	    xmlstr = tostring(crossconnects)
            xmlout = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
            result = self.compare_list(xmlout)
            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('cross-connects', 'editconfig_negative_case_invalid_oxc_connection', d, result)
        else:
            e = time.time()
            d = int(round((e - s)* 1000))
            #result = 'PASS'
            csvOutput('cross-connects', 'editconfig_negative_case_with_ingress_port', d, 'PASS')
            LOG.info('getting error from switch using invalid ingress and egress port : PASS\n\n')
        
        #e = time.time()
        #d = int(round((e - s)* 1000))
        #csvOutput('cross-connects', 'editconfig_negative_case_invalid_oxc_connection', d, result)
        nose.tools.assert_equals('FAIL', result)
        
    

    def edit_config_opr(self):

        """ create the required oxc operation using edit-config rpc request.
        Arguments:
        testcase_name              : test case name
        """
        
        global sw_mgr
        global xmlstr
        global ex_ingress_ports
        global req_ingress_ports
        global ex_egress_ports 
        global req_egress_ports
        
        p = 'PASS'
        f = 'FAIL'
           
        try:
           LOG.info('ingress port list: %s' % req_ingress_ports)
           LOG.info('egress port list : %s\n\n' % req_egress_ports)
           
           LOG.info("pass xml for edit-config operation\n")
    
    
           xmldata = sw_mgr.edit_config(target='running', config=xmlstr)
           print "\n\n"
    
        
           LOG.info('edit-config - response from the switch\n\n%s\n\n' % xmldata)
           return p
    
    
        except Exception as err:
           print "\n\n"
           LOG.error('-----[ Error from the Switch ]-----\n\n%s\n\n' %  err)
           return f
    





        
