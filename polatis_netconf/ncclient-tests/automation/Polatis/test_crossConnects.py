"""Test Script"""
from lib.netconf.crossconnects import CrossConnects
 
    
class testOxc(): 

    @classmethod
    def setUpClass(cls):
        cls.oxc = CrossConnects()
        """Usage: <hostIP> <netconf-port> <username> <password> <timeout>\n"""
        cls.oxc.connect_switch('10.99.99.227', '830', 'admin', 'root', 60)
        cls.oxc.get_existing_port_list()
        cls.oxc.cleanup_existing_connections(file_name = 'cleanup.xml')


    def testGetCrossConnects(self):
        self.oxc.get_crossconnects(file_name = 'pairs.xml', ingress_ports = '1,2,3', egress_ports = '17,18,19')

    def testGetPairs(self):
        self.oxc.get_pairs(file_name = 'pairs.xml', ingress_ports = '1,2,3', egress_ports = '17,18,19')
    
    def testGetIngressPort(self):
        self.oxc.get_pairs(file_name = 'pairs.xml', ingress_ports = '1,2,3', egress_ports = '17,18,19')
    
    def testGetIngressPorts(self):
        self.oxc.get_pairs(file_name = 'pairs.xml', ingress_ports = '1,2,3', egress_ports = '17,18,19')
   
    def testGetEgressPort(self):
        self.oxc.get_pairs(file_name = 'pairs.xml', ingress_ports = '1,2,3', egress_ports = '17,18,19')
    
    def testGetEgressPorts(self):
        self.oxc.get_pairs(file_name = 'pairs.xml', ingress_ports = '1,2,3', egress_ports = '17,18,19')
    
    def testGetConfigCrossConnects(self):
        self.oxc.getconfig_crossconnects(file_name = 'pairs.xml', ingress_ports = '1,2,3', egress_ports = '17,18,19')

    def testEditConfigCreateOperation(self):
        self.oxc.editconfig_create_operation(file_name = 'pairs.xml', ingress_ports = '1,2,3', egress_ports = '17,18,19')
