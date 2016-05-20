"""Test Ports Script"""
from lib.netconf.ports import Ports
from lib.netconf.config import get_config_arg
from lib.netconf.get_switch_ports_info_from_ports_range import get_valid_ingress_port


portsDict = {

    #'port_ids'        		 : get_config_arg('ports', 'port_ids'),
    #'port_label'                 : get_config_arg('ports', 'port_label'),
    #'port_state'        	 : get_config_arg('ports', 'port_state'),
    #'lambda'        		 : get_config_arg('ports', 'lambda'),
    #'power_high_alarm'       	 : get_config_arg('ports', 'power_high_alarm'),
    #'power_low_alarm'            : get_config_arg('ports', 'power_low_alarm'),
    #'power_high_warning_offset'  : get_config_arg('ports', 'power_high_warning_offset'),
    #'power_low_warning_offset'   : get_config_arg('ports', 'power_low_warning_offset'),
    #'power_alarm_control'        : get_config_arg('ports', 'power_alarm_control'),
    #'offset'        		 : get_config_arg('ports', 'offset'),
    #'averaging_time_select'      : get_config_arg('ports', 'averaging_time_select'),
    #'power_alarm_hysteresis'     : get_config_arg('ports', 'power_alarm_hysteresis'),
    #'power_alarm_clear_holdoff'  : get_config_arg('ports', 'power_alarm_clear_holdoff')
    'port_ids'        		 : get_valid_ingress_port(),
    'port_label'                 : 'port1,port2,port3',
    'port_state'        	 : 'PC_ENABLED,PC_DISABLED,PC_ENABLED',
    'port_status'        	 : 'PO_ENABLED,PO_DISABLED,PO_ENABLED',
    'lambda'        		 : '1550.0,1260.0,1640.0',
    'power_high_alarm'       	 : '25.0,10.0,25.0',
    'power_low_alarm'            : '-60.0,-20.0,-60.0',
    'power_high_warning_offset'  : '25.0,25.0,15.0',
    'power_low_warning_offset'   : '0.0,-20.0,0.0',
    'power_alarm_control'        : 'POWER_ALARM_DISABLED,POWER_ALARM_CONTINUOUS,POWER_ALARM_SINGLE',
    'power_alarm_status'         : 'POWER_ALARM_STATUS_OFF,POWER_ALARM_STATUS_ARMED,POWER_ALARM_STATUS_ARMED',
    'offset'        		 : '0.0,0.0,0.0',
    'averaging_time_select'      : '1,4,7',
    'power_alarm_hysteresis'     : '1.0,3.0,5.0',
    'power_alarm_clear_holdoff'  : '60,360,3600'


    }




class test_ports_opr():

    @classmethod
    def setUpClass(cls):
        
        """conecting switch"""
        cls.oxc = Ports()
        cls.oxc.connect_switch()

    def testEditConfigCreatePortLabel(self):

        """ testing create port label operation """
        self.oxc.editconfig_create_port_label(file_name = 'editconfig_create_port_label.xml', port_ids = portsDict['port_ids'], port_labels = portsDict['port_label'])


    def testEditConfigCreatePortState(self):

        """ testing create port label operation """
        self.oxc.editconfig_create_port_state(file_name = 'editconfig_create_port_label.xml', port_ids = portsDict['port_ids'], port_states = portsDict['port_state'])


    def testEditConfigCreateLambda(self):

        """ testing create lambda operation """
        self.oxc.editconfig_create_lambda(file_name = 'editconfig_create_port_label.xml', port_ids = portsDict['port_ids'], lambdas = portsDict['lambda'])


    def testEditConfigCreatePowerHighAlarm(self):

        """ testing create editconfig_create_power_high_alarm operation """
        self.oxc.editconfig_create_power_high_alarm(file_name = 'editconfig_create_port_label.xml', port_ids = portsDict['port_ids'], power_high_alarms = portsDict['power_high_alarm'])



    def testEditConfigCreatePowerLowAlarm(self):

        """ testing create power_low_alarm operation """
        self.oxc.editconfig_create_power_low_alarm(file_name = 'editconfig_create_port_label.xml', port_ids = portsDict['port_ids'], power_low_alarms = portsDict['power_low_alarm'])


    def testEditConfigCreatePowerHighWarningOffset(self):

        """ testing create power_high_warning_offset operation """
        self.oxc.editconfig_create_power_high_warning_offset(file_name = 'editconfig_create_port_label.xml', port_ids = portsDict['port_ids'], power_high_warning_offsets = portsDict['power_high_warning_offset'])



    def testEditConfigCreatePowerLowWarningOffset(self):

        """ testing create power_low_warning_offset  operation """
        self.oxc.editconfig_create_power_low_warning_offset(file_name = 'editconfig_create_port_label.xml', port_ids = portsDict['port_ids'], power_low_warning_offsets = portsDict['power_low_warning_offset'])




    def testEditConfigCreatePowerAlarmControl(self):

        """ testing create power_alarm_control operation """
        self.oxc.editconfig_create_power_alarm_control(file_name = 'editconfig_create_port_label.xml', port_ids = portsDict['port_ids'], power_alarm_controls = portsDict['power_alarm_control'])



    def testEditConfigCreateOffset(self):

        """ testing create offset operation """
        self.oxc.editconfig_create_offset(file_name = 'editconfig_create_port_label.xml', port_ids = portsDict['port_ids'], offsets = portsDict['offset'])



    def testEditConfigCreateAveragingTimeSelect(self):

        """ testing create averaging_time_select operation """
        self.oxc.editconfig_create_averaging_time_select(file_name = 'editconfig_create_port_label.xml', port_ids = portsDict['port_ids'], averaging_time_selects = portsDict['averaging_time_select'])



    def testEditConfigCreatePowerAlarmHysteresis(self):

        """ testing create power_alarm_hysteresis operation """
        self.oxc.editconfig_create_power_alarm_hysteresis(file_name = 'editconfig_create_port_label.xml', port_ids = portsDict['port_ids'], power_alarm_hysteresis = portsDict['power_alarm_hysteresis'])



    def testEditConfigCreatePowerAlarmClearHoldOff(self):

        """ testing create power_alarm_clear_holdoff operation """
        self.oxc.editconfig_create_power_alarm_clear_holdoff(file_name = 'editconfig_create_port_label.xml', port_ids = portsDict['port_ids'], power_alarm_clear_holdoff = portsDict['power_alarm_clear_holdoff'])




    def testGetPortLabel(self):

        """ testing get- port label operation """
        self.oxc.get_port_label(file_name = 'get_port_label.xml', port_ids = portsDict['port_ids'], port_labels = portsDict['port_label'])



    def testGetPortState(self):

        """ testing get- port state operation """
        self.oxc.get_port_state(file_name = 'get_port_state.xml', port_ids = portsDict['port_ids'], port_states = portsDict['port_state'])



    def testGetPortStatus(self):

        """ testing get- port status operation """
        self.oxc.get_port_status(file_name = 'get_port_status.xml', port_ids = portsDict['port_ids'], port_status = portsDict['port_status'])



    def testGetLambda(self):

        """ testing get- port lambda operation """
        self.oxc.get_lambda(file_name = 'get_lambda.xml', port_ids = portsDict['port_ids'], lambdas = portsDict['lambda'])



    def testGetPowerHighAlarm(self):

        """ testing get- power high alarm operation """
        self.oxc.get_power_high_alarm(file_name = 'get_power_high_alarm.xml', port_ids = portsDict['port_ids'], power_high_alarms = portsDict['power_high_alarm'])



    def testGetPowerLowAlarm(self):

        """ testing get- power low alarm operation """
        self.oxc.get_power_low_alarm(file_name = 'get_power_low_alarm.xml', port_ids = portsDict['port_ids'], power_low_alarms = portsDict['power_low_alarm'])



    def testGetPowerHighWarningOffsets(self):

        """ testing get- power high warning offest operation """
        self.oxc.get_power_high_warning_offset(file_name = 'get_power_high_warning_offset.xml', port_ids = portsDict['port_ids'], power_high_warning_offsets = portsDict['power_high_warning_offset'])



    def testGetPowerLowWarningOffset(self):

        """ testing get- power low warning offset operation """
        self.oxc.get_power_low_warning_offset(file_name = 'get_power_low_warning_offset.xml', port_ids = portsDict['port_ids'], power_low_warning_offsets = portsDict['power_low_warning_offset'])



    def testGetPowerAlarmControl(self):

        """ testing get- power alarm control operation """
        self.oxc.get_power_alarm_control(file_name = 'get_power_alarm_control.xml', port_ids = portsDict['port_ids'], power_alarm_controls = portsDict['power_alarm_control'])



    def testGetPowerAlarmStatus(self):

        """ testing get- power alarm status operation """
        self.oxc.get_power_alarm_status(file_name = 'get_power_alarm_status.xml', port_ids = portsDict['port_ids'], power_alarm_status = portsDict['power_alarm_status'])



    def testGetPower(self):

        """ testing get- power operation """
        self.oxc.get_power(file_name = 'get_power.xml', port_ids = portsDict['port_ids'], power = portsDict['power'])




    def testGetOffset(self):

        """ testing get- offset label operation """
        self.oxc.get_offset(file_name = 'get_offset.xml', port_ids = portsDict['port_ids'], offsets = portsDict['offset'])


    def testGetAveragingTimeSelect(self):

        """ testing get- averaging time select operation """
        self.oxc.get_averaging_time_select(file_name = 'get_averaging_time_select.xml', port_ids = portsDict['port_ids'], averaging_time_selects = portsDict['averaging_time_select'])



    def testGetPowerAlarmHyteresis(self):

        """ testing get- power alarm hysteresis operation """
        self.oxc.get_power_alarm_hysteresis(file_name = 'get_port_label.xml', port_ids = portsDict['port_ids'], power_alarm_hysteresis = portsDict['power_alarm_hysteresis'])

    def testGetPowerAlarmClearHoldOff(self):

        """ testing get- power alarm clear hold off operation """
        self.oxc.get_power_alarm_clear_holdoff(file_name = 'get_power_alarm_clear_holdoff.xml', port_ids = portsDict['port_ids'], power_alarm_clear_holdoff = portsDict['power_alarm_clear_holdoff'])




    def testGetConfigPortLabel(self):

        """ testing getconfig- port label operation """
        self.oxc.getconfig_port_label(file_name = 'get_port_label.xml', port_ids = portsDict['port_ids'], port_labels = portsDict['port_label'])



    def testGetConfigPortState(self):

        """ testing getconfig- port state operation """
        self.oxc.getconfig_port_state(file_name = 'get_port_state.xml', port_ids = portsDict['port_ids'], port_states = portsDict['port_state'])



    def testGetConfigLambda(self):

        """ testing getconfig- port lambda operation """
        self.oxc.getconfig_lambda(file_name = 'get_lambda.xml', port_ids = portsDict['port_ids'], lambdas = portsDict['lambda'])



    def testGetConfigPowerHighAlarm(self):

        """ testing getconfig- power high alarm operation """
        self.oxc.getconfig_power_high_alarm(file_name = 'get_power_high_alarm.xml', port_ids = portsDict['port_ids'], power_high_alarms = portsDict['power_high_alarm'])



    def testGetConfigPowerLowAlarm(self):

        """ testing getconfig- power low alarm operation """
        self.oxc.getconfig_power_low_alarm(file_name = 'get_power_low_alarm.xml', port_ids = portsDict['port_ids'], power_low_alarms = portsDict['power_low_alarm'])



    def testGetConfigPowerHighWarningOffsets(self):

        """ testing getconfig- power high warning offest operation """
        self.oxc.getconfig_power_high_warning_offset(file_name = 'get_power_high_warning_offset.xml', port_ids = portsDict['port_ids'], power_high_warning_offsets = portsDict['power_high_warning_offset'])



    def testGetConfigPowerLowWarningOffset(self):

        """ testing getconfig- power low warning offset operation """
        self.oxc.getconfig_power_low_warning_offset(file_name = 'get_power_low_warning_offset.xml', port_ids = portsDict['port_ids'], power_low_warning_offsets = portsDict['power_low_warning_offset'])



    def testGetConfigPowerAlarmControl(self):

        """ testing getconfig- power alarm control operation """
        self.oxc.getconfig_power_alarm_control(file_name = 'get_power_alarm_control.xml', port_ids = portsDict['port_ids'], power_alarm_controls = portsDict['power_alarm_control'])



    def testGetConfigOffset(self):

        """ testing getconfig- offset label operation """
        self.oxc.getconfig_offset(file_name = 'get_offset.xml', port_ids = portsDict['port_ids'], offsets = portsDict['offset'])


    def testGetConfigAveragingTimeSelect(self):

        """ testing getconfig- averaging time select operation """
        self.oxc.getconfig_averaging_time_select(file_name = 'get_averaging_time_select.xml', port_ids = portsDict['port_ids'], averaging_time_selects = portsDict['averaging_time_select'])



    def testGetConfigPowerAlarmHyteresis(self):

        """ testing getconfig- power alarm hysteresis operation """
        self.oxc.getconfig_power_alarm_hysteresis(file_name = 'get_port_label.xml', port_ids = portsDict['port_ids'], power_alarm_hysteresis = portsDict['power_alarm_hysteresis'])

    def testGetConfigPowerAlarmClearHoldOff(self):

        """ testing getconfig- power alarm clear hold off operation """
        self.oxc.getconfig_power_alarm_clear_holdoff(file_name = 'get_power_alarm_clear_holdoff.xml', port_ids = portsDict['port_ids'], power_alarm_clear_holdoff = portsDict['power_alarm_clear_holdoff'])

