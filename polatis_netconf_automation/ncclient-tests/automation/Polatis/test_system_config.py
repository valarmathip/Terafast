"""Test Ports Script"""
from lib.netconf.system_config import System_Config
from lib.netconf.config import get_config_arg

sysDict = {

    'name'		 : 'optical,polatis,switch',
    'password'		 : 'optical,polatis,switch',
    'group'		 : 'admin,view,user',
    #'interface_status'   : 'eth0,10.99.99.227,10.99.99.154,255.0.0.0,10.255.255.255,00:50:c2:2b:48:a3',
    #'interface'          : 'eth0,10.99.99.227,10.99.99.154,255.0.0.0,10.255.255.255',
    'interface_status'   : get_config_arg('system_config', 'interface_status'),
    'interface'          : get_config_arg('system_config', 'interface'),
    'mode_preserve'      : 'MODE_PRESERVE',
    'mode_volatile'      : 'MODE_VOLATILE'
    #'interface_status'   : 'eth0,host,10.99.99.154,255.0.0.0,10.255.255.255,00:50:c2:2b:48:a3'

}



class test_system_config_opr:


    @classmethod
    def setUpClass(cls):

        """conecting switch"""
        cls.sys_cfg = System_Config()
        cls.sys_cfg.connect_switch()

    def testEditConfigCreateUserWithPasswordAndGroup(self):

        """ testing create user with password and group """
        self.sys_cfg.editconfig_create_user_with_password_and_group(file_name = 'editconfig_create_user_with_pw_grp.xml', names = sysDict['name'], passwords = sysDict['password'], groups = sysDict['group'])



    def testEditConfigCreateUserWithoutPasswordAndGroup(self):

        """ testing create user without password and group """
        self.sys_cfg.editconfig_create_user_without_password_and_group(file_name = 'editconfig_create_user_without_pw_grp.xml', names = sysDict['name'])


    def testGetInterfaceStatus(self):

        """ testing create user without password and group """
        self.sys_cfg.get_interface_status(file_name = 'get_interface_status.xml', interface_status = sysDict['interface_status'])

    
    def testGetInterface(self):

        """ testing create user without password and group """
        self.sys_cfg.get_interface(file_name = 'get_interface.xml', interface = sysDict['interface'])


    def testEditConfigCreateStartupModeWithModePreserve(self):

        """ testing create startup mode with mode preserve """
        self.sys_cfg.editconfig_create_startup_mode_with_mode_preserve(file_name = 'get_startup_mode_with_mode_preserve.xml', mode_preserve = sysDict['mode_preserve'])


    def testEditConfigCreateStartupModeWithModeVolatile(self):

        """ testing create startup mode with mode volatile """
        self.sys_cfg.editconfig_create_startup_mode_with_mode_volatile(file_name = 'get_startup_mode_with_mode_volatile.xml', mode_volatile = sysDict['mode_volatile'])



    def testEditConfigDeleteAllUsers(self):

        """ testing delete all users """
        self.sys_cfg.editconfig_delete_all_users(file_name = 'editconfig_delete_all_users.xml')



    def testGetStartupMode(self):

        """ testing get startup mode """
        self.sys_cfg.get_startup_mode(file_name = 'get_startup_mode.xml',  mode_volatile = sysDict['mode_volatile'])

    def testGetConfigStartupMode(self):

        """ testing get startup mode """
        self.sys_cfg.getconfig_startup_mode(file_name = 'get_startup_mode.xml',  mode_volatile = sysDict['mode_volatile'])


    def testGetUserWithGroup(self):

        """ testing get user """
        self.sys_cfg.get_user_with_group(file_name = 'get_user.xml',  names = sysDict['name'], groups = sysDict['group'], passwords = sysDict['password']) 


    def testGetConfigUserWithGroup(self):

        """ testing get user """
        self.sys_cfg.getconfig_user_with_group(file_name = 'get_user.xml',  names = sysDict['name'], groups = sysDict['group'], passwords = sysDict['password']) 


    def testGetCurrentDatetime(self):

        """ testing get currrent datetime """
        self.sys_cfg.get_current_datetime(file_name = 'get_user.xml') 


    #def testSetCurrentDatetime(self):

    #    """ testing set current datetime """
    #    self.sys_cfg.set_current_datetime() 

