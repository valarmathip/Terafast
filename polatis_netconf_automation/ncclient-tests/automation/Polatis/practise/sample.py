def testGetConfigPortLabel(self):

        """ testing getconfig- port label operation """
        self.oxc.getconfig_port_label(file_name = 'get_port_label.xml', port_ids = portsDict['port_ids'], port_labels = portsDict['port_label'])



    def testGetConfigPortState(self):

        """ testing getconfig- port state operation """
        self.oxc.getconfig_port_state(file_name = 'get_port_state.xml', port_ids = portsDict['port_ids'], port_states = portsDict['port_state'])



    def testGetConfigPortStatus(self):

        """ testing getconfig- port status operation """
        self.oxc.getconfig_port_status(file_name = 'get_port_status.xml', port_ids = portsDict['port_ids'], port_status = portsDict['port_status'])



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



    def testGetConfigPowerAlarmStatus(self):

        """ testing getconfig- power alarm status operation """
        self.oxc.getconfig_power_alarm_status(file_name = 'get_power_alarm_status.xml', port_ids = portsDict['port_ids'], power_alarm_status = portsDict['power_alarm_status'])



    def testGetConfigPower(self):

        """ testing getconfig- power operation """
        self.oxc.getconfig_power(file_name = 'get_power.xml', port_ids = portsDict['port_ids'], power = portsDict['power'])




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

