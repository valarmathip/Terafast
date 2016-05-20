""" Test Set and Get Current and Boot Datetime """

from lib.netconf.current_and_boot_datetime import Set_Current_DateTime


class test_set_current_datetime():


    @classmethod
    def setUpClass(cls):

        """conecting switch"""
        cls.set_cur_dt = Set_Current_DateTime()
        cls.set_cur_dt.connect_switch()

    def testSetAndGetCurrentDateTime(self):

        """ testing set current datetime """
        self.set_cur_dt.set_and_get_current_datetime(file_name = 'get_current_datetime.xml')

    def testSetAndGetBootDateTime(self):

        """ testing set current datetime """
        self.set_cur_dt.set_and_get_boot_datetime(file_name = 'get_boot_datetime.xml')



 
