""" python file this covers under product information container in optical switch"""

import os
import nose
import time
import sys
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


""" global variable - using ncclient for connecting the polatis box
"""
sw_mgr = ''
existing_product_info = []

class Product_Information:


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

        LOG.info('connecting switch <IP:Port = %s:%s>\n' %(host, port))
        sw_mgr = manager.connect_ssh(host=host, port=port, username=username, password=password, timeout=int(timeout), hostkey_verify=False)



    def write_to_file(self,file_name, data):

        """ write the output xml from 'get' and 'get-config' rpc request
        Arguments: 
            file_name    : Give any name
            data        : XML output 
        """

        f = open(file_name, 'w')
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
        testcase_name   :       valid testcase name
        """

        print '\n'
        l = len(testcase_name) + 7
        start_end_session = '       +' + (l * '-') + '+       ' 
        middle = '| ' +'   '+ str(testcase_name) +'  '+ ' |'

        print '%s\n       %s\n%s\n\n' % (start_end_session, middle, start_end_session)



    def compare_list(self, xmlData):


        """compare existing and required product information.
        Arguments:
           xmlData              : get the xml output from 'get - config'
        """

        global existing_product_info

        product_info_values = []
        ports_info_values = []

        p = 'PASS'
        f = 'FAIL'

        DOMTree = xml.dom.minidom.parseString(xmlData)
        collection = DOMTree.documentElement

        product_info = collection.getElementsByTagName("product-information")
        ports_info = collection.getElementsByTagName("ports")

        product_information_list = ['manufacturer', 'serial-number', 'model-name', 'software-version']

        ports_information_list = ['port-id', 'port-type', 'has_opm', 'has_oxc']

        

        for info in product_info:
            for i in range(0, len(product_information_list)):
                try:
                    info_tag = info.getElementsByTagName(product_information_list[i])[0]
                    info_tag_value =  str(info_tag.childNodes[0].data)
               
                    product_info_values.append(info_tag_value)
                except:
                    pass

        for info in ports_info:
        
            for i in range(0, len(ports_information_list)):
                try:
                    if ports_information_list[i] == 'port-id':
                        info_tag = info.getElementsByTagName(ports_information_list[i])[0]
                        info_tag_value =  str(info_tag.childNodes[0].data)
               
                        product_info_values.append(info_tag_value)
                    else:
                        info_tag = info.getElementsByTagName(ports_information_list[i])[0]
                        info_tag_value =  str(info_tag.childNodes[0].data)
               
                        ports_info_values.append(info_tag_value)
                    
                except:
                    pass

        product_info_values = product_info_values + ports_info_values
        LOG.info('-----[ validate product information ]-----\n\n')

        LOG.info("existing_product_info : %s \n" % existing_product_info)
        LOG.info('required_product_info : %s\n\n' % product_info_values)
        #LOG.info('parsed_egress_ports : %s\n\n' % parsed_egress_ports )



        if str(existing_product_info) == str(product_info_values):
            LOG.info('compare both existing_product_info and required product_info : PASS\n')
            return p
        else:
            LOG.error('comparision failed : FAIL\n')
            return f                                           

    def get_rpc_request(self, xmlstr, file_name):

        """perform get operation for created xmlstr
        Arguments:
           xmlstr                : required tag xmlstr
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
       


    def get_manufacturer(self, **kwargs):

        """create xml to get manufacturer info then parse get manufacturer switch output xml 
        , compare it with existing values.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        manufacturer          : manufacturer value
        """

        self.create_box('test_get_manufacturer')
        s = time.time()

        global existing_product_info

        existing_product_info = kwargs['manufacturer'].split()

        LOG.info('-----[ create xml for get operation ]-----\n')
        product_info = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
        manufacturer = SubElement(product_info, 'opsw:manufacturer')

        xmlstr = tostring(product_info)
        xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('product-information', 'get_manufacturer', d, result)
        nose.tools.assert_equals('PASS', result)



 
    def get_serial_number(self, **kwargs):

        """create xml to get serial_number info then parse get manufacturer switch output xml 
        , compare it with existing values.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        manufacturer          : manufacturer value
        """

        self.create_box('test_get_serial_number')
        s = time.time()

        global existing_product_info

        existing_product_info = kwargs['serial_number'].split()

        LOG.info('-----[ create xml for get operation ]-----\n')
        product_info = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
        serial_name = SubElement(product_info, 'opsw:serial-number')

        xmlstr = tostring(product_info)
        xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('product-information', 'get_serial_number', d, result)
        nose.tools.assert_equals('PASS', result)

    def get_model_name(self, **kwargs):

        """create xml to get model name info then parse get manufacturer switch output xml 
        , compare it with existing values.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        manufacturer          : manufacturer value
        """

        self.create_box('test_get_model_name')
        s = time.time()

        global existing_product_info

        existing_product_info = kwargs['model_name'].split()

        LOG.info('-----[ create xml for get operation ]-----\n')
        product_info = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
        model_name = SubElement(product_info, 'opsw:model-name')

        xmlstr = tostring(product_info)
        xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('product-information', 'get_model_name', d, result)
        nose.tools.assert_equals('PASS', result)

    def get_software_version(self, **kwargs):

        """create xml to get software version info then parse get manufacturer switch output xml 
        , compare it with existing values.Finally save the output in final.csv file
        Arguments:
        file_name                 : any file name
        software_version          : software_version value
        """

        self.create_box('test_get_software_version')
        s = time.time()

        global existing_product_info

        existing_product_info = kwargs['software_version'].split()

        LOG.info('-----[ create xml for get operation ]-----\n')
        product_info = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
        software_version = SubElement(product_info, 'opsw:software-version')

        xmlstr = tostring(product_info)
        xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('product-information', 'get_software_version', d, result)
        nose.tools.assert_equals('PASS', result)

    def get_ingress_ports_type_info(self, **kwargs):

        """create xml to get ingress port type info then parse get manufacturer switch output xml 
        , compare it with existing values.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        manufacturer          : manufacturer value
        """

        self.create_box('test_get_ingress_ports_type_info')
        s = time.time()

        global existing_product_info

        ingress_port_ids = kwargs['ingress_port_ids']
        port_types = ['INGRESS_PORT', 'INGRESS_PORT', 'INGRESS_PORT']

        LOG.info('-----[ create xml for get operation ]-----\n')
        product_info = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                            'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
        #ports = SubElement(product_info, 'opsw:ports')
        for id in range(0, len(ingress_port_ids)):
            ports = SubElement(product_info, 'opsw:ports')
            port_id = SubElement(ports, 'opsw:port-id')
            port_id.text = str(ingress_port_ids[id])
            port_type = SubElement(ports, 'opsw:port-type')
            
        existing_product_info = ingress_port_ids + port_types 

        xmlstr = tostring(product_info)
        xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('product-information', 'get_ingress_ports_type_info', d, result)
        nose.tools.assert_equals('PASS', result)




    def get_ingress_ports_has_opm_info(self, **kwargs):

        """create xml to get ingress ports has opm info info then parse get manufacturer switch output xml 
        , compare it with existing values.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        manufacturer          : manufacturer value
        """

        self.create_box('test_get_ingress_ports_has_opm_info')
        s = time.time()

        global existing_product_info

        ingress_port_ids = kwargs['ingress_port_ids']
        has_opm_values = ['true', 'true', 'true']

        LOG.info('-----[ create xml for get operation ]-----\n')
        product_info = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                            'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
        #ports = SubElement(product_info, 'opsw:ports')
        for id in range(0, len(ingress_port_ids)):
            ports = SubElement(product_info, 'opsw:ports')
            port_id = SubElement(ports, 'opsw:port-id')
            port_id.text = str(ingress_port_ids[id])
            has_opm = SubElement(ports, 'opsw:has_opm')
            
        existing_product_info = ingress_port_ids + has_opm_values 

        xmlstr = tostring(product_info)
        xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('product-information', 'get_ingress_ports_has_opm', d, result)
        nose.tools.assert_equals('PASS', result)

    def get_ingress_ports_has_oxc_info(self, **kwargs):

        """create xml to get ingress port has oxc info then parse get manufacturer switch output xml 
        , compare it with existing values.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        manufacturer          : manufacturer value
        """

        self.create_box('test_get_ingress_ports_has_oxc_info')
        s = time.time()

        global existing_product_info

        ingress_port_ids = kwargs['ingress_port_ids']
        has_oxc_values = ['true', 'true', 'true']

        LOG.info('-----[ create xml for get operation ]-----\n')
        product_info = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                            'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
        #ports = SubElement(product_info, 'opsw:ports')
        for id in range(0, len(ingress_port_ids)):
            ports = SubElement(product_info, 'opsw:ports')
            port_id = SubElement(ports, 'opsw:port-id')
            port_id.text = str(ingress_port_ids[id])
            has_oxc = SubElement(ports, 'opsw:has_oxc')
            
        existing_product_info = ingress_port_ids + has_oxc_values

        xmlstr = tostring(product_info)
        xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('product-information', 'get_ingress_ports_has_oxc', d, result)
        nose.tools.assert_equals('PASS', result)




    def get_egress_ports_type_info(self, **kwargs):

        """create xml to get egress ports type info then parse get manufacturer switch output xml 
        , compare it with existing values.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        manufacturer          : manufacturer value
        """

        self.create_box('test_get_egress_ports_type_info')
        s = time.time()

        global existing_product_info

        egress_port_ids = kwargs['egress_port_ids']
        port_types = ['EGRESS_PORT', 'EGRESS_PORT', 'EGRESS_PORT']

        LOG.info('-----[ create xml for get operation ]-----\n')
        product_info = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                            'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
        #ports = SubElement(product_info, 'opsw:ports')
        for id in range(0, len(egress_port_ids)):
            ports = SubElement(product_info, 'opsw:ports')
            port_id = SubElement(ports, 'opsw:port-id')
            port_id.text = str(egress_port_ids[id])
            port_type = SubElement(ports, 'opsw:port-type')
            
        existing_product_info = egress_port_ids + port_types 

        xmlstr = tostring(product_info)
        xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('product-information', 'get_egress_ports_type_info', d, result)
        nose.tools.assert_equals('PASS', result)




    def get_egress_ports_has_opm_info(self, **kwargs):

        """create xml to get egress ports has opm info info then parse get manufacturer switch output xml 
        , compare it with existing values.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        manufacturer          : manufacturer value
        """

        self.create_box('test_get_egress_ports_has_opm_info')
        s = time.time()

        global existing_product_info

        egress_port_ids = kwargs['egress_port_ids']
        has_opm_values = ['true', 'true', 'true']

        LOG.info('-----[ create xml for get operation ]-----\n')
        product_info = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                            'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
        #ports = SubElement(product_info, 'opsw:ports')
        for id in range(0, len(egress_port_ids)):
            ports = SubElement(product_info, 'opsw:ports')
            port_id = SubElement(ports, 'opsw:port-id')
            port_id.text = str(egress_port_ids[id])
            has_opm = SubElement(ports, 'opsw:has_opm')
            
        existing_product_info = egress_port_ids + has_opm_values 

        xmlstr = tostring(product_info)
        xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('product-information', 'get_egress_ports_has_opm', d, result)
        nose.tools.assert_equals('PASS', result)

    def get_egress_ports_has_oxc_info(self, **kwargs):

        """create xml to get egress port has oxc info then parse get manufacturer switch output xml 
        , compare it with existing values.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        manufacturer          : manufacturer value
        """

        self.create_box('test_get_egress_ports_has_oxc_info')
        s = time.time()

        global existing_product_info

        egress_port_ids = kwargs['egress_port_ids']
        has_oxc_values = ['true', 'true', 'true']

        LOG.info('-----[ create xml for get operation ]-----\n')
        product_info = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                            'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
        #ports = SubElement(product_info, 'opsw:ports')
        for id in range(0, len(egress_port_ids)):
            ports = SubElement(product_info, 'opsw:ports')
            port_id = SubElement(ports, 'opsw:port-id')
            port_id.text = str(egress_port_ids[id])
            has_oxc = SubElement(ports, 'opsw:has_oxc')
            
        existing_product_info = egress_port_ids + has_oxc_values

        xmlstr = tostring(product_info)
        xmlout = self.get_rpc_request(xmlstr, kwargs['file_name'])
        result = self.compare_list(xmlout)
        e = time.time()
        d = int(round((e - s)* 1000))
        csvOutput('product-information', 'get_egress_ports_has_oxc', d, result)
        nose.tools.assert_equals('PASS', result)

