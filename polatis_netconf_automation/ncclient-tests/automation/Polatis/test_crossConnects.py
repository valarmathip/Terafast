"""Test oxc Script"""
from lib.netconf.crossconnects import CrossConnects
from lib.netconf.config import get_config_arg
from lib.netconf.get_switch_ports_info_from_ports_range import get_valid_ingress_port
from lib.netconf.get_switch_ports_info_from_ports_range import get_valid_egress_port

   
oxcDict = {

    #'valid_ingress_ports'        : get_config_arg('cross_connects', 'valid_ingress_ports'),
    #'valid_egress_ports'         : get_config_arg('cross_connects', 'valid_egress_ports'), 
    #'invalid_ingress_ports'      : get_config_arg('cross_connects', 'invalid_ingress_ports'),
    #'invalid_egress_ports'       : get_config_arg('cross_connects', 'invalid_egress_ports') 
    'valid_ingress_ports'        : get_valid_ingress_port(),
    'valid_egress_ports'         : get_valid_egress_port(),
    'invalid_ingress_ports'      : '100,101,102',
    'invalid_egress_ports'       : '200,201,202'

    }


class test_oxc_opr: 

    @classmethod
    def setUpClass(cls):
        cls.oxc = CrossConnects()
        """Usage: <hostIP> <netconf-port> <username> <password> <timeout>\n"""
        cls.oxc.connect_switch()
        cls.oxc.get_existing_port_list()
        cls.oxc.cleanup_existing_connections(file_name = 'cleanup.xml')
        cls.oxc.edit_config_create_oxc_without_opr(ingress_ports = oxcDict['valid_ingress_ports'], egress_ports = oxcDict['valid_egress_ports'])

    def testGetCrossConnects(self):

        """ testing get cross connects """

        self.oxc.get_crossconnects(file_name = 'get_crossconnects.xml')

    def testGetPairs(self):
       
        """ testing get pairs """
        self.oxc.get_pairs(file_name = 'get_pairs.xml')
    
    def testGetIngressPort(self):
         
        """ testing get ingress port """
        self.oxc.get_ingress(file_name = 'get_ingress_port.xml')
    
    def testGetIngressPorts(self):
        
        """ testing get pairs """
        self.oxc.get_ingress_ports(file_name = 'get_ingress_ports.xml', ingress_ports = oxcDict['valid_ingress_ports'])
   
    def testGetEgressPort(self):
        
        """ testing get egress port """
        self.oxc.get_egress(file_name = 'get_egress_port.xml')
    
    def testGetEgressPorts(self):
        
        """ testing get egress ports """
        self.oxc.get_egress_ports(file_name = 'get_egress_ports.xml', egress_ports = oxcDict['valid_egress_ports'])


    def testGetConfigCrossConnects(self):
        
        """ testing get-config crossconnects """
        self.oxc.getconfig_crossconnects(file_name = 'getconfig_crossconnects.xml')

    def testGetConfigPairs(self):
        
        """ testing get-config pairs """
        self.oxc.getconfig_pairs(file_name = 'getconfig_pairs.xml')

    def testGetConfigIngressPort(self):
        
        """ testing get-config ingress port """
        self.oxc.getconfig_ingress(file_name = 'getconfig_ingress_port.xml')

    def testGetConfigIngressPorts(self):
        
        """ testing get-config ingress ports """
        self.oxc.getconfig_ingress_ports(file_name = 'getconfig_ingress_ports.xml', ingress_ports = oxcDict['valid_ingress_ports'])

    def testGetConfigEgress_port(self):
        
        """ testing get-config egress port """
        self.oxc.getconfig_egress(file_name = 'getconfig_egress_port.xml')

    def testGetConfigEgressPorts(self):
        
        """ testing get-config egress ports """
        self.oxc.getconfig_egress_ports(file_name = 'getconfig_egress_ports.xml', egress_ports = oxcDict['valid_egress_ports'])
    
    def test_EditConfigCreateOperation(self):
        """ testing editconfig_create_operation """
        self.oxc.cleanup_existing_connections(file_name = 'cleanup.xml')
        self.oxc.editconfig_create_operation(file_name = 'editconfig_create_operation.xml', ingress_ports = oxcDict['valid_ingress_ports'], egress_ports = oxcDict['valid_egress_ports'])

 
    def test_EditConfigDeleteOperation(self):
        """ testing editconfig_delete_operation """
        self.oxc.edit_config_create_oxc_without_opr(ingress_ports = oxcDict['valid_ingress_ports'], egress_ports = oxcDict['valid_egress_ports'])
        self.oxc.editconfig_delete_operation(file_name = 'editconfig_create_operation.xml', ingress_ports = oxcDict['valid_ingress_ports'], egress_ports = oxcDict['valid_egress_ports'])

    def test_EditConfigReplaceOperation(self):
        """ testing editconfig_replace_operation """
        self.oxc.cleanup_existing_connections(file_name = 'cleanup.xml')
        self.oxc.edit_config_create_oxc_without_opr(ingress_ports = oxcDict['valid_ingress_ports'], egress_ports = oxcDict['valid_egress_ports'])

        egr_prts = oxcDict['valid_egress_ports']
        egress_prts = ''
            
        l = len(egr_prts)

        if len(egr_prts) == 8:
            for i in range(l-1, -1, -3):
                prt = ''.join(egr_prts[i-1]+egr_prts[i])
                if i == 1:
                    egress_prts = egress_prts+prt
                else:
                    egress_prts = egress_prts+prt+','
        elif len(egr_prts) == 11:
            for i in range(l-1, -1, -4):
                prt = ''.join(egr_prts[i-2]+egr_prts[i-1]+egr_prts[i])
                if i == 2:
                    egress_prts = egress_prts+prt
                else:
                    egress_prts = egress_prts+prt+','
        elif len(egr_prts) == 5:
            for i in range(l-1, -1, -2):
                prt = ''.join(egr_prts[i])
                if i == 0:
                    egress_prts = egress_prts+prt
                else:
                    egress_prts = egress_prts+prt+','
        elif len(egr_prts) == 1 or len(egr_prts) == 2 or len(egr_prts) == 3:
             egress_prts = oxcDict['valid_egress_ports']
        else:
            print "no of digits in each port should be same"

        self.oxc.editconfig_replace_operation(file_name = 'editconfig_create_operation.xml', ingress_ports = oxcDict['valid_ingress_ports'], egress_ports = egress_prts)



    def test_EditConfig_NegativeCase_With_Invalid_IngressPort(self):
        """ test_EditConfig_NegativeCase_With_IngressPort """
        
        self.oxc.cleanup_existing_connections(file_name = 'cleanup.xml')
        self.oxc.editconfig_negative_case_with_invalid_ingress_port(file_name = 'editconfig_create_operation.xml', ingress_ports = oxcDict['invalid_ingress_ports'], egress_ports = oxcDict['valid_egress_ports'])


    def test_EditConfig_NegativeCase_With_Invalid_EgressPort(self):
        """ test_EditConfig_NegativeCase_With_IngressPort """
        
        self.oxc.cleanup_existing_connections(file_name = 'cleanup.xml')
        self.oxc.editconfig_negative_case_with_invalid_egress_port(file_name = 'editconfig_create_operation.xml', ingress_ports = oxcDict['valid_ingress_ports'], egress_ports = oxcDict['invalid_egress_ports'])

   
    def test_EditConfig_NegativeCase_For_Invalid_Oxc_Connection(self):
        """ test_editconfig_negative_case_invalid_oxc_connection """
        
        self.oxc.cleanup_existing_connections(file_name = 'cleanup.xml')
        self.oxc.editconfig_negative_case_with_invalid_oxc_connection(file_name = 'editconfig_create_operation.xml', ingress_ports = oxcDict['invalid_ingress_ports'], egress_ports = oxcDict['invalid_egress_ports'])



