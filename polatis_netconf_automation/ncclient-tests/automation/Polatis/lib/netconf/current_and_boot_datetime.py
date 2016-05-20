import sys
import datetime
import logging
import logging.config
import xml.dom.minidom
import ConfigParser
import time
import nose
import paramiko
import re

from ncclient import manager
from lxml import etree as etree
from ncclient.xml_ import *
from xml.etree.ElementTree import *
from xml.dom import minidom
from xml.dom.minidom import parse, parseString
from config import get_config_arg
from createCsv import csvOutput

logging.config.fileConfig('logging.ini')
LOG = logging.getLogger('polatis')

class Set_Current_DateTime:

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
        global host

        host = get_config_arg("login_credentials", "host")
        port = get_config_arg("login_credentials", "port")
        username = get_config_arg("login_credentials", "user_name")
        password = get_config_arg("login_credentials", "password")
        timeout = get_config_arg("login_credentials", "timeout")

        LOG.info("Connecting switch <IP:Port = %s:%s>\n" % (host,port))
        sw_mgr = manager.connect_ssh(host=host, port=port, username=username, password=password,timeout=int(timeout), device_params = {'name':'junos'},hostkey_verify=False)



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

        global curr_time
        #LOG.info("curr_time : %s" % curr_time)
        #LOG.info("type curr_time : %s" % type(curr_time))

        parsed_curr_time = ''

        p = 'PASS'
        f = 'FAIL'

        DOMTree = xml.dom.minidom.parseString(xmlData)
        collection = DOMTree.documentElement

        ct = collection.getElementsByTagName("system-config")
        
        tag_list = ['current-datetime', 'boot-datetime']
        l = len(tag_list)

        for t in ct:
            for i in range(0, l):
                try:
                    set_curr_time_tag = t.getElementsByTagName(tag_list[i])[0]
                    set_curr_time_tag_value =  str(set_curr_time_tag.childNodes[0].data)

                except:
                    pass

        LOG.info('-----[ validate datetime ]-----\n\n')
        match = re.search(r'(\d+-\d+-\d+T\d+:\d+)', set_curr_time_tag_value)
        set_curr_time_tag_value = match.group(1)

        LOG.info("parsed datetime : %s \n" % set_curr_time_tag_value)
        LOG.info('existing datetime : %s\n\n' % curr_time)


        if str(curr_time) == str(set_curr_time_tag_value):
            LOG.info('compare both existing datetime and parsed datetime : PASS\n')
            return p
        else:
            LOG.error('comparision failed : FAIL\n')
            return f
    



    def get_rpc_request(self, xmlstr):

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

            #self.write_to_file(file_name,prettyXml)
            return xmlData

        except Exception as err:
            print '\n\n'
            LOG.error('-----[ Error from the Switch ]-----\n\n%s\n\n', err)


    def set_and_get_current_datetime(self, **kwargs):

        """create xml to get current datetime info then parse get switch output xml 
        , compare it with existing values.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        """

     
        global sw_mgr
        global host
        global curr_time
 
        self.create_box('test_set_and_get_current_datetime')
        username = get_config_arg("login_credentials", "cli_username")
        password = get_config_arg("login_credentials", "cli_password")
        s = time.time()
   
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh.connect(host, username=username, password=password)
        
        stdin, stdout, stderr = ssh.exec_command("date -u +'%Y-%m-%dT%H:%M:%S.%s%z'")
           
        t = stdout.readlines()      


        now = datetime.datetime.now()
        curr_time = now.isoformat()
        

        LOG.info('-----[ create xml for set operation ]-----\n')

        xmlstr = """<set-current-datetime xmlns="http://www.polatis.com/yang/optical-switch"><current-datetime>%s</current-datetime></set-current-datetime>""" % curr_time


        LOG.info('%s\n\n' % xmlstr)
        try:
            xmlout = sw_mgr.rpc(xmlstr)
            print '\n\n'
            LOG.info('-----[ output from switch ]-----\n\n%s\n\n' % xmlout)
            result = 'PASS'
            LOG.info('-----[ create xml for get operation ]-----\n')
            sys_config = Element('opsw:system-config', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
            cur_time = SubElement(sys_config, 'opsw:current-datetime')

            
            xmlstr = tostring(sys_config)
            xmlout = self.get_rpc_request(xmlstr)
            prettyXml = self.prettify(xmlout)
            self.write_to_file(kwargs['file_name'], prettyXml);

            curr_time = str(t).split('\'') 
            match = re.search(r'(\d+-\d+-\d+T\d+:\d+)', curr_time[1])
            curr_time = match.group(1)

            result = self.compare_list(xmlout)
            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('set-current-datetime', 'set_and_get_current_datetime', d, result)
        except:
            result = 'FAIL'
            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('set-current-datetime', 'set_and_get_current_datetime', d, result)
        nose.tools.assert_equals('PASS', result)

 



    def set_and_get_boot_datetime(self, **kwargs):

        """create xml to get restart datetime info then parse get switch output xml 
        , compare it with existing values.Finally save the output in final.csv file
        Arguments:
        file_name             : any file name
        """

     
        global sw_mgr
        global host
        global curr_time
 
        self.create_box('test_set_and_get_boot_datetime')
        username = get_config_arg("login_credentials", "cli_username")
        password = get_config_arg("login_credentials", "cli_password")
        s = time.time()
   
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh.connect(host, username=username, password=password)
        
        stdin, stdout, stderr = ssh.exec_command("date -u +'%Y-%m-%dT%H:%M:%S.%s%z'")
        sys_restart = ssh.exec_command("reboot")
           
        t = stdout.readlines()      


        now = datetime.datetime.now()
        curr_time = now.isoformat()
        

        LOG.info('-----[ create xml for set operation ]-----\n')

        xmlstr = """<system-restart xmlns="http://www.polatis.com/yang/optical-switch">"""


        LOG.info('%s\n\n' % xmlstr)
        try:
            xmlout = sw_mgr.rpc(xmlstr)
        except:
            time.sleep(180)
            print '\n\n'
            self.connect_switch()
            #LOG.info('-----[ output from switch ]-----\n\n%s\n\n' % xmlout)
            LOG.info('-----[ create xml for get operation ]-----\n')
            sys_config = Element('opsw:system-config', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
            boot_time = SubElement(sys_config, 'opsw:boot-datetime')

            xmlstr = tostring(sys_config)

            xmlout = self.get_rpc_request(xmlstr)
            prettyXml = self.prettify(xmlout)
            self.write_to_file(kwargs['file_name'], prettyXml);

            curr_time = str(t).split('\'') 
            match = re.search(r'(\d+-\d+-\d+T\d+:\d+)', curr_time[1])
            curr_time = match.group(1)

            result = self.compare_list(xmlout)
            e = time.time()
            d = int(round((e - s)* 1000))
            csvOutput('set-current-datetime', 'set_and_get_boot_datetime', d, result)
        nose.tools.assert_equals('PASS', result)

 
