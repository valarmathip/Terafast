# FlowHandler Library Call.
import time
import threading
from policyuser import PolicyUser

add_flow_dict = {}

class BaseFlowHandler(object):

    def __init__(self):
        #self.add_flow_dict = {}
	pass
    def add_flow(self): pass
 
    def get_flow(self): pass

    def delete_flow(self): pass


class RyuFlowHandler(BaseFlowHandler):

    def __init__(self):
        super(RyuFlowHandler, self).__init__()
	from flow_stats import FlowStats
	self.flowStats = FlowStats()
	self.firstTimeFlg = 1
	self.flowStateChange = 1
	self.flow_timeout = 30 #2mins
	self.flow_priority = 32765
	self.polling_interval = 10
	self.file_path = '/home/ryu/csvfiles'
	self.port_info = {}
	self.policy= PolicyUser('/home/ryu/tf_users.csv')


    def get_port_info(self):
	self.port_info = self.flowStats.get_port_info().values()[0];
	print "port info is:", self.port_info

    def get_port_no(self, intf_name='eth1'):
	port_no = 0
	for port in self.port_info:
		if port['name'] == intf_name:
			return port['port_no']

	return port_no

    def timerHandler(self):
	#self.add_flow_dict = {}
	#print 'Inside Timer Handler....'
        # Carry out Flow Stats.
        self.flowStats.stats_collector()
	# getting statistics for every 10 seconds.
        threading.Timer(self.polling_interval, self.timerHandler).start()
    
    def pre_flow_handler(self):

	print 'clear all the flows in the switch'
	self.flowStats.clear_all_flows()
	print 'add a static arp flow in the switch'
	self.flowStats.add_arp_flow()

    def fwd_entry(self, datapath, match, action, inport):
        ofproto = datapath.ofproto
        inst = [datapath.ofproto_parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS, action)]
        self.install_flows(datapath, match, inst, action, inport)

    def rev_entry(self, datapath, match, action, inport):
        ofproto = datapath.ofproto
        inst = [datapath.ofproto_parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS, action)]
        if match['ip_proto'] == 17:
	    match = datapath.ofproto_parser.OFPMatch(eth_src=match['eth_dst'], 
                                                     eth_dst=match['eth_src'],
                                                     ipv4_src=match['ipv4_dst'],
                                                     ipv4_dst=match['ipv4_src'],
                                                     udp_src=match['udp_dst'],
                                                     udp_dst=match['udp_src'],
                                                     ip_proto=match['ip_proto'],
                                                     eth_type=0x800, in_port=inport
                                                     )
        self.install_flows(datapath, match, inst, action, inport)

    def get_flow_stats_obj(self):
	return self.flowStats

    def get_flow_direction(self,flow):
 	#find sub ip and direction
    	sub_ip = flow['srcIp']
    	dir = 'FWD'

    	if not self.policy.isIpValidSub(sub_ip):
            sub_ip = flow['dstIp']
            dir = 'REV'
            if not self.policy.isIpValidSub(sub_ip):
                #print "both ipis belongs to valid range. how did we get here!!!!", flow
                return -1
	return dir
	
    def add_flow(self, msg, datapath, **kwargs):

	#if self.flowStateChange == 1:
	#    self.pre_flow_handler()
	#    self.flowStateChange =0
 
	#self.add_flow_dict = {}
        ofproto = datapath.ofproto
        #self.buffer_id = ofproto.OFP_NO_BUFFER
        msg = msg

        if (kwargs['proto'] == 6):
	    if (kwargs['offset']==0):
                match = datapath.ofproto_parser.OFPMatch(in_port=kwargs['in_port'], eth_dst=kwargs['dstMac'], eth_src=kwargs['srcMac'], eth_type=0x800, ipv4_src=kwargs['srcIp'], ipv4_dst=kwargs['dstIp'], ip_proto=kwargs['proto'], tcp_src=kwargs['srcPort'], tcp_dst=kwargs['dstPort'])
	    else:
		match = datapath.ofproto_parser.OFPMatch(in_port=kwargs['in_port'], eth_dst=kwargs['dstMac'], eth_src=kwargs['srcMac'], eth_type=0x800, ipv4_src=kwargs['srcIp'], ipv4_dst=kwargs['dstIp'], ip_proto=kwargs['proto']) 
	    
        elif (kwargs['proto'] == 17):
	    if (kwargs['offset']==0):
                match = datapath.ofproto_parser.OFPMatch(in_port=kwargs['in_port'], eth_dst=kwargs['dstMac'], eth_src=kwargs['srcMac'], eth_type=0x800, ipv4_src=kwargs['srcIp'], ipv4_dst=kwargs['dstIp'], ip_proto=kwargs['proto'], udp_src=kwargs['srcPort'], udp_dst=kwargs['dstPort'] )
	    else:
		match = datapath.ofproto_parser.OFPMatch(in_port=kwargs['in_port'], eth_dst=kwargs['dstMac'], eth_src=kwargs['srcMac'], eth_type=0x800, ipv4_src=kwargs['srcIp'], ipv4_dst=kwargs['dstIp'], ip_proto=kwargs['proto'])

        else:
            match = datapath.ofproto_parser.OFPMatch(in_port=kwargs['in_port'], eth_dst=kwargs['dstMac'], eth_src=kwargs['srcMac'], eth_type=0x800, ipv4_src=kwargs['srcIp'], ipv4_dst=kwargs['dstIp'], ip_proto=kwargs['proto'])
	    #kwargs['srcPort']=kwargs['dstPort']=0

	
	if 'offset' in kwargs.keys():
	    if (kwargs['offset']==0):	
                self.fwd_key = kwargs['srcIp'] + '_' + str(kwargs['srcPort']) + '_' + kwargs['dstIp'] + '_' + str(kwargs['dstPort'])
	    else:
                self.fwd_key = kwargs['srcIp'] + '_' + kwargs['dstIp'] + '_' + str(kwargs['proto'])
	else:
            self.fwd_key = kwargs['srcIp'] + '_' + kwargs['dstIp'] + '_' + str(kwargs['proto'])


	kwargs['byte_count'] = kwargs['packet_count'] = kwargs['delta_bytes'] = kwargs['delta_packets'] =kwargs['app_id']=  0
	kwargs['create_time'] = kwargs['last_seen_time'] = time.time()

	self.install_flows(msg, datapath, match, kwargs['actions'], kwargs['in_port'])

        #self.fwd_entry(datapath, match, kwargs['fwd_actions'], kwargs['in_port'])
        #self.rev_entry(datapath, match, kwargs['rev_actions'], kwargs['out_port'])

	
	add_flow_dict[self.fwd_key] = kwargs
	#print 'Initial Flow Dict :', add_flow_dict

	#print '\n call timer handler....'
	if self.firstTimeFlg == 1:
        	threading.Timer(self.polling_interval, self.timerHandler).start()
		self.firstTimeFlg =0

	

    def delete_flow(self, flow):

	flow_key = self.get_flow_key(flow)
	del add_flow_dict[flow_key] 
	#print '\n\n AFTER DELETe : ', add_flow_dict

    def get_flow_key(self,flow):
	if 'srcPort' in flow.keys():
	    flow_key = flow['srcIp'] + '_' + str(flow['srcPort']) + '_' + flow['dstIp'] + '_' + str(flow['dstPort']) 
	else:
	    flow_key = flow['srcIp'] + '_' + flow['dstIp'] + '_' + str(flow['proto']) 
	
	return flow_key

    def get_flow_timeout(self):

	return self.flow_timeout

    def dump_flows_to_file(self):
	#print '\n\n Inside Dump flows..!!!'
	total_tx_bytes = total_tx_pkts = total_rx_bytes = total_rx_pkts = 0
	
	# write the flow entries in the csv
	fileTime = str(time.time())
	fo = open('%s/flow_%s.csv.Pending' % (self.file_path,fileTime), 'w+')
	fo1 = open('%s/total_traffic_%s.csv.Pending' % (self.file_path,fileTime), 'w+')
        fo.write('#InPort,OutPort,SrcMac,DstMac,SrcIp,DstIp,SrcPort,DstPort,Protocol,Packets,Bytes,DelPackets,DelBytes,CreateTime,LastSeen,AppID,Tos \n')
	for flow in add_flow_dict.values():
	    #print '\n\n Flow !!! :', flow

 	    if flow['delta_bytes'] == 0 :  

		if (time.time() - flow['last_seen_time']) > self.get_flow_timeout() :
		#delete the flow from ofctl table and software flow table
		   self.delete_flow(flow)
	   
	    else:
		if self.get_flow_direction(flow) == 'FWD':
		   total_tx_bytes += flow['delta_bytes']
		   total_tx_pkts += flow['delta_packets']
		elif self.get_flow_direction(flow) == 'REV':
		   total_rx_bytes += flow['delta_bytes']
		   total_rx_pkts += flow['delta_packets']
		else:
		    pass
			
	        fo.write("%u,%u,%s,%s,%s,%s,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u\n" % ( (flow['in_port']), (flow['out_port']),flow['srcMac'], flow['dstMac'],flow['srcIp'], flow['dstIp'], (flow['srcPort']), (flow['dstPort']), (flow['proto']),(flow['packet_count']), (flow['byte_count']), (flow['delta_packets']), (flow['delta_bytes']),  (flow['create_time']), (flow['last_seen_time']), (flow['app_id']),(flow['tos']))) 

	fo.close()
	fo1.write("%s,%u,%u,%u,%u\n" % (fileTime,total_tx_bytes,total_rx_bytes,total_tx_pkts, total_rx_pkts))
	fo1.close()

	
    def update_flow_stats(self, flow):
	#print '\n\n\ Inside Update stats - add_flow_dict ....!!!!:', add_flow_dict
	try:
		if not flow['ethType'] == 2054:
			# if the flow is neither udp or tcp, for flow key, we need src/dstport which is 0
			flow_key = self.get_flow_key(flow)
			new_flow = prev_entry = add_flow_dict[(flow_key)]
			
	                new_flow['delta_bytes']= flow['byte_count'] - prev_entry['byte_count']	
	        	new_flow['delta_packets'] = flow['packet_count'] - prev_entry['packet_count']

			if new_flow['delta_bytes'] != 0:
				new_flow['byte_count'] = flow['byte_count']
				new_flow['packet_count'] = flow['packet_count']
	    			new_flow['last_seen_time'] = time.time()		
			add_flow_dict[flow_key] = new_flow
	except Exception as err:
		pass
	    	#print ' Error: !!!!  ', err

	#self.flowStats.dump_flows(add_flow_dict)


    def install_flows(self, msg, datapath, match, action, in_port):    
        ofproto = datapath.ofproto
	inst = [datapath.ofproto_parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS, action)]

        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, cookie=0, cookie_mask=0, table_id=0,
            command=ofproto.OFPFC_ADD, idle_timeout=self.flow_timeout, hard_timeout=0,
            priority=self.flow_priority, buffer_id=ofproto.OFP_NO_BUFFER,
            out_port=ofproto.OFPP_ANY,
            out_group=ofproto.OFPG_ANY,
            flags=0, match=match, instructions=inst)
        datapath.send_msg(mod)

	data = None
	if msg.buffer_id == ofproto.OFP_NO_BUFFER:
	    data = msg.data
	out = datapath.ofproto_parser.OFPPacketOut(
	    datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port,
	    actions=action, data=data)
        datapath.send_msg(out)

