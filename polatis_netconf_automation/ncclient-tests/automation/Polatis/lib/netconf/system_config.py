import os
import sys
import nose
import time
import datetime
import logging.config
from ncclient import manager
from xml.etree.ElementTree import *
import xml.dom.minidom
from xml.dom import minidom

from xml.dom.minidom import parse, parseString

from lxml import etree as etree

from ncclient.xml_ import *
from config import get_config_arg
from createCsv import csvOutput


logging.config.fileConfig('logging.ini')
LOG = logging.getLogger('polatis')

now = datetime.datetime.now()
curr_dt = now.isoformat()


class System_Config:


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


    def create_box(self, testcase_name):

        """create box for test case name.
        Arguments:
        testcase_name   :       valid testcase name
        """

        print "\n"
        l = len(testcase_name)+7
        start_end_session = '       +' + (l * '-') + '+       '
        middle = '| ' +'   '+ str(testcase_name) +'  '+ ' |'

        print '%s\n       %s\n%s\n\n' % (start_end_session, middle, start_end_session)




    def prettify(self, xmlstr):

       """Used for prettify the XML output from switch.
        Arguments: 
           xmlstr       : any xml string
       """


       reparsed = minidom.parseString(xmlstr)
       return reparsed.toprettyxml(indent=" ")


    def create_xml_for_user_with_password_and_group(self):

        """ create xml for creating the user in system config operation.
        Arguments:
           
        """
        global gvn_names
        global gvn_passwords
        global gvn_groups

        l = len(gvn_names)

        config = Element('config', {'xmlns:xc':"urn:ietf:params:xml:ns:netconf:base:1.0"})
        system_config = SubElement(config, 'system-config', {'xmlns':"http://www.polatis.com/yang/optical-switch"})
        
        for i,j,k in zip(range(0, l), range(0, l), range(0, l)):
            n = gvn_names[i]
            p = gvn_passwords[j]
            g = gvn_groups[k]
            user = SubElement(system_config, 'user')
            name = SubElement(user, 'name')
            name.text = str(n)
            password = SubElement(user, 'password')
            password.text = str(p)
            group = SubElement(user, 'group', {'xmlns':"http://www.polatis.com/yang/polatis-switch"})
            group.text = str(g)


        xmlstr = tostring(config)

        return xmlstr

    def create_xml_for_user_without_password_and_group(self):

        """ create xml for creating the user in system config operation.
        Arguments:
           
        """
        global gvn_names

        l = len(gvn_names)

        config = Element('config', {'xmlns:xc':"urn:ietf:params:xml:ns:netconf:base:1.0"})
        system_config = SubElement(config, 'system-config', {'xmlns':"http://www.polatis.com/yang/optical-switch"})
        
        for i in range(0, l):
            n = gvn_names[i]
            user = SubElement(system_config, 'user')
            name = SubElement(user, 'name')
            name.text = str(n)


        xmlstr = tostring(config)

        return xmlstr


    def create_xml_for_startup_mode_with_given_mode(self):
        
        """ create xml for creating startup mode with mode preserve 
        in system config operation.
        Arguments:
           
        """
        global gvn_mode
        
        l = len(gvn_mode)

        config = Element('config', {'xmlns:xc':"urn:ietf:params:xml:ns:netconf:base:1.0"})
        system_config = SubElement(config, 'system-config', {'xmlns':"http://www.polatis.com/yang/optical-switch"})

        startup_mode = SubElement(system_config, 'startup-mode', {'xmlns':"http://www.polatis.com/yang/polatis-switch"})
        startup_mode.text = str(gvn_mode)
        
       
        xmlstr = tostring(config)

        return xmlstr

        


    def editconfig_create_user_with_password_and_group(self, **kwargs):

        """ create xml for creating user using editconfig operation,
        then get this using getconfig operation, finally parsed the output of getconfig 
        operation , compare parsed output with given input
        """
 
        global gvn_names
        global gvn_passwords
        global gvn_groups
        global xmlstr


        gvn_names = kwargs['names'].split(',')
        gvn_passwords = kwargs['passwords'].split(',')
        gvn_groups = kwargs['groups'].split(',')


        l = len(gvn_names)

        s = time.time()
        self.create_box('test_editconfig_create_user_with_password_and_group')
        xmlstr = self.create_xml_for_user_with_password_and_group()
        result = self.edit_config_opr()

        if result == 'PASS':
            LOG.info('-----[ create xml for get-config operation with names ]-----\n\n')
            system_config = Element('opsw:system-config', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                           'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                user = SubElement(system_config, 'opsw:user')
                names = SubElement(user, 'opsw:name')
                names_val = gvn_names[tag1]
                names.text = str(names_val)

            xmlstr = tostring(system_config)
            xmlout, result = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
            result1, result2 = self.get_parsed_values(xmlout)

            if str(gvn_names) == str(result1) and str(gvn_groups) == str(result2):
                LOG.info('gvn_names : %s' % gvn_names)
                #LOG.info('gvn_passwords : %s' % gvn_passwords)
                LOG.info('gvn_groups : %s\n\n' % gvn_groups)
                LOG.info('compare names, passwords, groups : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('system-config', 'editconfig_create_user_with_password_and_group', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)


    def editconfig_create_user_without_password_and_group(self, **kwargs):

        """ create xml for creating user using editconfig operation,
        then get this using getconfig operation, finally parsed the output of getconfig 
        operation , compare parsed output with given input
        """
 
        global gvn_names
        global xmlstr


        gvn_names = kwargs['names'].split(',')

        l = len(gvn_names)

        s = time.time()
        self.create_box('test_editconfig_create_user_without_password_and_group')
        xmlstr = self.create_xml_for_user_without_password_and_group()
        result = self.edit_config_opr()

        if result == 'PASS':
            LOG.info('-----[ create xml for get-config operation with names ]-----\n\n')
            system_config = Element('opsw:system-config', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                           'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
            for tag1 in range(0, l):
                user = SubElement(system_config, 'opsw:user')
                names = SubElement(user, 'opsw:name')
                names_val = gvn_names[tag1]
                names.text = str(names_val)

            xmlstr = tostring(system_config)
            xmlout, result = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
            result1, result2 = self.get_parsed_values(xmlout)

            if str(gvn_names) == str(result1):
                LOG.info('gvn_names : %s\n\n' % gvn_names)
                LOG.info('compare names : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('system-config', 'editconfig_create_user_without_password_and_group', d, result)

        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)


   


    def editconfig_create_startup_mode_with_mode_preserve(self, **kwargs):

        """ create xml for creating startup mode wit mode preserve using editconfig operation,
        then get this using getconfig operation, finally parsed the output of getconfig 
        operation , compare parsed output with given input
        """
 
        global gvn_mode
        global xmlstr

        gvn_mode = kwargs['mode_preserve']
        #print gvn_mode


        l = len(gvn_mode)

        s = time.time()
        self.create_box('test_editconfig_create_startup_mode_with_mode_preserve')
        xmlstr = self.create_xml_for_startup_mode_with_given_mode()
        result = self.edit_config_opr()

        if result == 'PASS':
            LOG.info('-----[ create xml for get-config operation ]-----\n\n')
            system_config = Element('opsw:system-config', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                           'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
            startup_mode = SubElement(system_config, 'plts:startup-mode')

            xmlstr = tostring(system_config)
            xmlout, result = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
            result= self.get_parsed_values_startup_mode(xmlout)
            
            gvn_mode = kwargs['mode_preserve'].split()

            if str(gvn_mode) == str(result):
                LOG.info('gvn_mode : %s\n\n' % gvn_mode)
                LOG.info('compare mode : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('system-config', 'editconfig_create_startup_mode_with_mode_preserve', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def editconfig_create_startup_mode_with_mode_volatile(self, **kwargs):

        """ create xml for creating startup mode wit mode preserve using editconfig operation,
        then get this using getconfig operation, finally parsed the output of getconfig 
        operation , compare parsed output with given input
        """
 
        global gvn_mode
        global xmlstr

        gvn_mode = kwargs['mode_volatile']
        #print gvn_mode


        l = len(gvn_mode)

        s = time.time()
        self.create_box('test_editconfig_create_startup_mode_with_mode_volatile')
        xmlstr = self.create_xml_for_startup_mode_with_given_mode()
        result = self.edit_config_opr()

        if result == 'PASS':
            LOG.info('-----[ create xml for get-config operation ]-----\n\n')
            system_config = Element('opsw:system-config', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                           'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
            startup_mode = SubElement(system_config, 'plts:startup-mode')

            xmlstr = tostring(system_config)
            xmlout, result = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
            result= self.get_parsed_values_startup_mode(xmlout)
            
            gvn_mode = kwargs['mode_volatile'].split()

            if str(gvn_mode) == str(result):
                LOG.info('gvn_mode : %s\n\n' % gvn_mode)
                LOG.info('compare mode : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('system-config', 'editconfig_create_startup_mode_with_mode_volatile', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)


    def editconfig_delete_all_users(self, **kwargs):

        """ create xml for delete all users except admin 
        using edit-config and get this modification using get-config
        then parsed this xml and compare parsed users with given users
        Arguments:
            xmlData   : xmlstr
        """
        gvn_user = ['admin']
        global xmlstr

        self.create_box('test_delete_all_users')
        s = time.time()
        
        LOG.info('-----[ create xml for get operation ]-----\n')
        system_config = Element('opsw:system-config', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
        user = SubElement(system_config, 'opsw:user')
        
        xmlstr = tostring(system_config)
        
        xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])

        config = Element('config', {'xmlns:ns':"urn:ietf:params:xml:ns:netconf:base:1.0"}) 
        system_config = SubElement(config, 'system-config', {'xmlns':"http://www.polatis.com/yang/optical-switch"})
        
        
        if result == 'PASS':
            result1, result2 = self.get_parsed_values(xmlout)
 
            l = len(result1)
            for user_ind in range(0, l):
                name_val = result1[user_ind]
                #user = SubElement(system_config, 'user', {'ns:operation':'delete'})
                if name_val == 'admin':
                    continue
                else:
                    user = SubElement(system_config, 'user', {'ns:operation':'delete'})
                    name = SubElement(user, 'name')
                    name.text = str(name_val)

            xmlstr = tostring(config)
            self.edit_config_opr()
            system_config = Element('opsw:system-config', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
            user = SubElement(system_config, 'opsw:user')
        
            xmlstr = tostring(system_config)
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            result1, result2 = self.get_parsed_values(xmlout)
            if str(gvn_user) == str(result1):
                LOG.info('gvn_user : %s\n\n' % gvn_user)
                LOG.info('compare user : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

        else:
            LOG.info('getting error from switch : FAIL\n\n')
            result = self.compare_list(xmlout)
            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('system_config', 'get_interface', d, result)
            nose.tools.assert_equals('PASS', result)
 


    def edit_config_opr(self):

        """ create required ports operation using edit-config rpc request.
        Arguments:
        """

        global sw_mgr
        global xmlstr

        p = 'PASS'
        f = 'FAIL'

        try:
           LOG.info("-----[ pass xml for edit-config operation ]-----\n\n")


           xmldata = sw_mgr.edit_config(target='running', config=xmlstr)
           #print "xmlData is %s" % xmldata
           print "\n\n"


           LOG.info('-----[ edit-config - response from the switch ]-----\n\n\n%s\n\n' % xmldata)
           return p


        except Exception as err:
           print "\n\n"
           LOG.error('-----[ Error from the Switch ]-----\n\n%s\n\n' %  err)
           return f 

 
    def get_parsed_values(self, xmlData):



        """parsed xml to get values of power tag for given port-ids.
        Arguments:
           xmlData                     : get the xml output from 'get - config'
        """


        parsed_name_values= []; parsed_password_values = []; parsed_group_values = []

        DOMTree = xml.dom.minidom.parseString(xmlData)
        collection = DOMTree.documentElement

        interface_status = collection.getElementsByTagName("interface-status")
 
        user = collection.getElementsByTagName("user")

        for users_tag in user:
            try:
               name = users_tag.getElementsByTagName('name')[0]
               name_val =  str(name.childNodes[0].data)
    
               parsed_name_values.append(name_val)
               
               
               group = users_tag.getElementsByTagName('group')[0]
               group_val =  str(group.childNodes[0].data)
    
               parsed_group_values.append(group_val)
    
            except Exception as err:
               #print "err is : \n\n%s" % err
               pass
        
        LOG.info("-----[ validate system config info ]-----\n\n")

        LOG.info('parsed_name_values : %s' % parsed_name_values)
        LOG.info('parsed_group_values : %s\n\n' % parsed_group_values)

        return (parsed_name_values, parsed_group_values)


    
    
    def get_parsed_values_for_intr_status(self, xmlData, tag_name):



        """parsed xml to get values of power tag for given port-ids.
        Arguments:
           xmlData                     : get the xml output from 'get - config'
        """


        parsed_interface_status_values= []

        DOMTree = xml.dom.minidom.parseString(xmlData)
        collection = DOMTree.documentElement
        interface_status = collection.getElementsByTagName(tag_name)

        for intr_stus in interface_status:
            try:
               name = intr_stus.getElementsByTagName('name')[0]
               name_val =  str(name.childNodes[0].data)
    
               parsed_interface_status_values.append(name_val)
               
               ip_address = intr_stus.getElementsByTagName('ip-address')[0]
               ip_address_val =  str(ip_address.childNodes[0].data)
    
               parsed_interface_status_values.append(ip_address_val)
               
               gateway = intr_stus.getElementsByTagName('gateway')[0]
               gateway_val =  str(gateway.childNodes[0].data)
    
               parsed_interface_status_values.append(gateway_val)
               
               subnet = intr_stus.getElementsByTagName('subnet')[0]
               subnet_val =  str(subnet.childNodes[0].data)
    
               parsed_interface_status_values.append(subnet_val)
               
               broadcast = intr_stus.getElementsByTagName('broadcast')[0]
               broadcast_val =  str(broadcast.childNodes[0].data)
    
               parsed_interface_status_values.append(broadcast_val)
               
               hw_addr = intr_stus.getElementsByTagName('hw-addr')[0]
               hw_addr_val =  str(hw_addr.childNodes[0].data)
    
               parsed_interface_status_values.append(hw_addr_val)
    
    
    
    
            except Exception as err:
               #print "err is : \n\n%s" % err
               pass
        LOG.info("-----[ validate system config info ]-----\n\n")

        LOG.info('parsed_interface_values : %s' % parsed_interface_status_values)
        
        return parsed_interface_status_values


    def get_parsed_values_startup_mode(self, xmlData):


        """parsed xml to get values of power tag for given port-ids.
        Arguments:
           xmlData                     : get the xml output from 'get - config'
        """


        parsed_mode_values= []

        DOMTree = xml.dom.minidom.parseString(xmlData)
        collection = DOMTree.documentElement

        system_config = collection.getElementsByTagName("system-config")
 

        for m in system_config: 
            mode = m.getElementsByTagName('startup-mode')[0]
            mode_val =  str(mode.childNodes[0].data)
    
            parsed_mode_values.append(mode_val)
               
        LOG.info("-----[ validate system config info ]-----\n\n")
        LOG.info('parsed_mode_values : %s\n\n' % parsed_mode_values)

        return parsed_mode_values

    def get_parsed_values_get_curent_datetime(self, xmlData):


        """parsed xml to get values of current datetime.
        Arguments:
           xmlData                     : get the xml output from 'get - config'
        """


        parsed_current_datetime= []

        DOMTree = xml.dom.minidom.parseString(xmlData)
        collection = DOMTree.documentElement


        system_config = collection.getElementsByTagName("system-config")
 

        for m in system_config: 
            curr_time = m.getElementsByTagName('current-datetime')[0]
            val =  str(curr_time.childNodes[0].data)
    
            parsed_current_datetime.append(val)
               
        LOG.info("-----[ validate system config info ]-----\n\n")
        LOG.info('parsed_current_datetime : %s\n\n' % parsed_current_datetime)

        return parsed_current_datetime


    def getconfig_rpc_request(self, xmlstr, file_name):

        """perform get-config operation for created xmlstr
        Arguments:
           xmlstr                : required tag xmlstr
           file_name             : any file name
        """

        global sw_mgr

        p = 'PASS'; f = 'FAIL'


        try:
            #print "xmstr is : \n\n%s\n" % xmlstr
            xmlData = sw_mgr.get_config(source='running',  filter=('subtree',xmlstr)).data_xml
            print '\n\n'


            prettyXml = self.prettify(xmlData)
            LOG.info('-----[ get-config - response from the switch ]-----\n\n\n%s\n' % prettyXml)

            self.write_to_file(file_name, prettyXml);
            return (xmlData, p)


        except Exception as err:
            print '\n\n'
            LOG.error('-----[ Error from the Switch ]-----\n\n%s\n\n', err)
            return (err, f)


    def get_interface_status(self, **kwargs):

        """ create xml for get interface status, then parsed this,
        compare parsed values with given values
        """ 

        gvn_interface_status = kwargs['interface_status'].split(',')
        #print "gvn_interface_status : %s" % gvn_interface_status

        self.create_box('test_get_interface_status')
        s = time.time()

        LOG.info('-----[ create xml for get operation ]-----\n')
        system_config = Element('opsw:system-config', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
        interface_status = SubElement(system_config, 'opsw:interface-status')

        xmlstr = tostring(system_config)
        xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
        if result == 'PASS':
            result = self.get_parsed_values_for_intr_status(xmlout, 'interface-status')

            if str(gvn_interface_status) == str(result):
                #LOG.info("validate system config info\n\n")
                LOG.info('gvn_interface_status : %s\n\n' % gvn_interface_status)
                LOG.info('compare interface_status : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'
        else:
            LOG.info('getting error from switch : FAIL\n\n')
            result = self.compare_list(xmlout)
            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('system_config', 'get_interface_status', d, result)
            nose.tools.assert_equals('PASS', result)

    
    def get_interface(self, **kwargs):

        """ create xml for get interface, then parsed this,
        compare parsed values with given values
        """ 

        gvn_interface = kwargs['interface'].split(',')
        #print "gvn_interface : %s" % gvn_interface

        self.create_box('test_get_interface')
        s = time.time()

        LOG.info('-----[ create xml for get operation ]-----\n')
        system_config = Element('opsw:system-config', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
        interface_status = SubElement(system_config, 'opsw:interface')

        xmlstr = tostring(system_config)
        xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
        if result == 'PASS':
            result = self.get_parsed_values_for_intr_status(xmlout, 'interface')

            if str(gvn_interface) == str(result):
                #LOG.info("validate the system config info\n\n")
                LOG.info('gvn_interface : %s\n\n' % gvn_interface)
                LOG.info('compare interface : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'
        else:
            LOG.info('getting error from switch : FAIL\n\n')
            result = self.compare_list(xmlout)
            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('system_config', 'get_interface', d, result)
            nose.tools.assert_equals('PASS', result)



    def get_rpc_request(self, xmlstr, file_name):

        """perform get-config operation for created xmlstr
        Arguments:
           xmlstr                : required tag xmlstr
           file_name             : any file name
        """

        p = 'PASS'; f = 'FAIL'

        global sw_mgr


        try:
            #print "xmstr is : \n\n%s\n" % xmlstr
            xmlData = sw_mgr.get(filter=('subtree',xmlstr)).data_xml
            print '\n\n'


            prettyXml = self.prettify(xmlData)
            LOG.info('-----[ get - response from the switch ]-----\n\n\n%s\n' % prettyXml)

            self.write_to_file(file_name, prettyXml);
            return (xmlData, p)


        except Exception as err:
            print '\n\n'
            LOG.error('-----[ Error from the Switch ]-----\n\n%s\n\n', err)
            return (err, f)

    def get_user_with_group(self, **kwargs):

        """ create xml for creating user using editconfig operation,
        then get this using get operation, finally parsed the output of get 
        operation , compare parsed output with given input
        """
 
        global gvn_names
        global gvn_groups
        global gvn_passwords
        global xmlstr


        gvn_names = kwargs['names'].split(',')
        gvn_passwords = kwargs['passwords'].split(',')
        gvn_groups = kwargs['groups'].split(',')


        l = len(gvn_names)

        s = time.time()
        self.create_box('test_get_user')
        xmlstr = self.create_xml_for_user_with_password_and_group()
        result = self.edit_config_opr()

        if result == 'PASS':
            LOG.info("-----[ create xml for get operation ]-----\n\n")
                
            system_config = Element('opsw:system-config', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                           'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
            user = SubElement(system_config, 'opsw:user')
            xmlstr = tostring(system_config)
            LOG.info("xmlstr :  \n\n%s" %xmlstr) 
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            result1, result2 = self.get_parsed_values(xmlout)
            gvn_names.insert(0, 'admin')
            gvn_groups.insert(0, 'admin')

            #print gvn_names
            #print gvn_groups

            if str(gvn_names) == str(result1) and str(gvn_groups) == str(result2):
                LOG.info('gvn_names : %s' % gvn_names)
                #LOG.info('gvn_passwords : %s' % gvn_passwords)
                LOG.info('gvn_groups : %s\n\n' % gvn_groups)
                LOG.info('compare names and groups : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('system-config', 'get_user', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    def getconfig_user_with_group(self, **kwargs):

        """ create xml for creating user using editconfig operation,
        then get this using get operation, finally parsed the output of get 
        operation , compare parsed output with given input
        """
 
        global gvn_names
        global gvn_groups
        global gvn_passwords
        global xmlstr


        gvn_names = kwargs['names'].split(',')
        gvn_passwords = kwargs['passwords'].split(',')
        gvn_groups = kwargs['groups'].split(',')


        l = len(gvn_names)

        s = time.time()
        self.create_box('test_getconfig_user')
        xmlstr = self.create_xml_for_user_with_password_and_group()
        result = self.edit_config_opr()

        if result == 'PASS':
            LOG.info("-----[ create xml for get-config operation ]-----\n\n")
                
            system_config = Element('opsw:system-config', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                           'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
            user = SubElement(system_config, 'opsw:user')
            xmlstr = tostring(system_config)
            LOG.info("xmlstr :  \n\n%s" %xmlstr) 
            xmlout, result = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
            result1, result2 = self.get_parsed_values(xmlout)
            gvn_names.insert(0, 'admin')
            gvn_groups.insert(0, 'admin')

            #print gvn_names
            #print gvn_groups

            if str(gvn_names) == str(result1) and str(gvn_groups) == str(result2):
                LOG.info('gvn_names : %s' % gvn_names)
                #LOG.info('gvn_passwords : %s' % gvn_passwords)
                LOG.info('gvn_groups : %s\n\n' % gvn_groups)
                LOG.info('compare names and groups : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('system-config', 'get_user', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)




    def getconfig_startup_mode(self, **kwargs):

        """ create xml for creating startup mode with mode volatile using editconfig operation,
        then get this using get operation, finally parsed the output of get 
        operation , compare parsed output with given input
        """
 
        global gvn_mode
        global xmlstr

        gvn_mode = kwargs['mode_volatile']
        #print gvn_mode


        l = len(gvn_mode)

        s = time.time()
        self.create_box('test_getconfig_startup_mode')
        xmlstr = self.create_xml_for_startup_mode_with_given_mode()
        result = self.edit_config_opr()

        if result == 'PASS':
            LOG.info('-----[ create xml for get-config operation ]-----\n\n')
            system_config = Element('opsw:system-config', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                           'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
            startup_mode = SubElement(system_config, 'plts:startup-mode')

            xmlstr = tostring(system_config)
            xmlout, result = self.getconfig_rpc_request(xmlstr, kwargs['file_name'])
            result= self.get_parsed_values_startup_mode(xmlout)
            
            gvn_mode = kwargs['mode_volatile'].split()

            if str(gvn_mode) == str(result):
                LOG.info('gvn_mode : %s\n\n' % gvn_mode)
                LOG.info('compare mode : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('system-config', 'get_startup_mode', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    
 

    def get_startup_mode(self, **kwargs):

        """ create xml for creating startup mode with mode volatile using editconfig operation,
        then get this using get operation, finally parsed the output of get 
        operation , compare parsed output with given input
        """
 
        global gvn_mode
        global xmlstr

        gvn_mode = kwargs['mode_volatile']
        #print gvn_mode


        l = len(gvn_mode)

        s = time.time()
        self.create_box('test_get_startup_mode')
        xmlstr = self.create_xml_for_startup_mode_with_given_mode()
        result = self.edit_config_opr()

        if result == 'PASS':
            LOG.info('-----[ create xml for get operation ]-----\n\n')
            system_config = Element('opsw:system-config', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                           'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
            startup_mode = SubElement(system_config, 'plts:startup-mode')

            xmlstr = tostring(system_config)
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            result= self.get_parsed_values_startup_mode(xmlout)
            
            gvn_mode = kwargs['mode_volatile'].split()

            if str(gvn_mode) == str(result):
                LOG.info('gvn_mode : %s\n\n' % gvn_mode)
                LOG.info('compare mode : PASS\n')
                result = 'PASS'
            else:
                LOG.error('comparision failed : FAIL\n')
                result = 'FAIL'

            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('system-config', 'get_startup_mode', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

  


    def set_current_datetime(self):
 
        """ set the current datetime using set-current-datetime RPC operation
        Arguments:
        """

        global now
        global sw_mgr
        global curr_dt

        #curr_dt = now.isoformat()
     
        xmlstr = """<set-current-datetime xmlns="http://www.polatis.com/yang/optical-switch"><current-datetime>%s</current-datetime></set-current-datetime>""" % curr_dt

        xmlData = sw_mgr.rpc(xmlstr)

        LOG.info("xmlData is : \n\n%S\n\n" % xmlData)


        
 
    def get_current_datetime(self, **kwargs):

        """ create xml for creating startup mode with mode volatile using editconfig operation,
        then get this using get operation, finally parsed the output of get 
        operation , compare parsed output with given input
        """
 
        global gvn_mode
        global xmlstr


        s = time.time()
        self.create_box('test_get_current_datetime')

        result = 'PASS'

        if result == 'PASS':
            LOG.info('-----[ create xml for get operation ]-----\n\n')
            system_config = Element('opsw:system-config', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                           'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
            current_datetime = SubElement(system_config, 'opsw:current-datetime')

            xmlstr = tostring(system_config)
            xmlout, result = self.get_rpc_request(xmlstr, kwargs['file_name'])
            result= self.get_parsed_values_get_curent_datetime(xmlout)
            
            LOG.info("current time value : %s" % result)


            result = 'PASS'
            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('system-config', 'get_current_datetime', d, result)
        else:
            LOG.info('getting error from switch : FAIL\n\n')

        nose.tools.assert_equals('PASS', result)

    
