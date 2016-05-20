from lib.netconf.crossconnects import CrossConnects



#def testImport():
#    ob = cntStch.FooTestCase()
#    ob.test_connectSwitch()
    
    
class testOxc(): 

    @classmethod
    def setUpClass(cls):
        cls.oxc = CrossConnects()
        """Usage: <hostIP> <netconf-port> <username> <password> <timeout>\n"""
        cls.oxc.connect_switch('10.99.99.227', '830', 'admin', 'root', 60)
        cls.oxc.get_existing_port_list()
   
    #def testImport(self):
    #    self.ob = crossconnects()
    #    self.ob.test_connectSwitch('10.99.99.227')
    #
    #
    #def testCall(self):
    #    self.ob = crossconnects()
    #    self.ob.call()


    def testGetPairs(self):
        """Usage: <outputXml file>"""
        self.oxc.get_pairs(file_name = 'pairs.xml', ingress_ports = '1,2,3', egress_ports = '17,18,19' )
