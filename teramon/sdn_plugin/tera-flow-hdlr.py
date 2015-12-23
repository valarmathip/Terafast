# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_2
from ryu.lib.packet import packet
from ryu.lib.packet import ipv4
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types

from flow_handler import RyuFlowHandler
from threading import Thread
from policyuser import PolicyUser
from flow_stats import FlowStats

class TeraFlowHandler(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_2.OFP_VERSION]

    def __init__(self, *args, **kwargs):

        super(TeraFlowHandler, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.ryu_fl_hdlr = RyuFlowHandler()

	self.policy= PolicyUser('/home/ryu/tf_users.csv')
	self.subscriber_port=0
	self.network_port=0
	self.eth_list = []	

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):

	# if this is the first pkt to the system, lets get the port info and save it
	if self.subscriber_port== 0:
		self.ryu_fl_hdlr.get_port_info()
		self.subscriber_port = self.ryu_fl_hdlr.get_port_no(intf_name='eth1')
		self.network_port = self.ryu_fl_hdlr.get_port_no(intf_name='eth2')
		print "sub_port and net_port is", self.subscriber_port, self.network_port
		

        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        in_port = msg.match['in_port']
		

	if in_port == self.subscriber_port:
	    out_port = self.network_port
	elif in_port == self.network_port:
	    out_port = self.subscriber_port
	else:
	    print "the inport is invalid. Cannot happen!!!!!\n"		
	    pass
 
	#packet is received here!!!
        pkt = packet.Packet(msg.data)
	# get ethernet data for flow
	srcMac = pkt.protocols[0].src
	dstMac = pkt.protocols[0].dst
	ethType = pkt.protocols[0].ethertype

	#if we see an arp pkt, probably the arp is not installed, lets first install and return
	if ethType  == 2054:
	    self.ryu_fl_hdlr.pre_flow_handler()
	    return
	
	if ethType  != 2048:
	    if not (ethType in self.eth_list):
		self.eth_list.append(ethType)
	        print '\n #####   Non IP Packet : ethType is -> ', ethType
		print '\n #####   Non IP Packet :  -> ', pkt
	        print '\n #####   List of Non IP EthType :  -> ', self.eth_list
	    return

	# get ip data for flow
	proto = pkt.protocols[1].proto
	srcIp = pkt.protocols[1].src
	dstIp = pkt.protocols[1].dst
	tos = pkt.protocols[1].tos
	offset = pkt.protocols[1].offset

	if not (self.policy.isIpValidSub(srcIp)):
	    if not (self.policy.isIpValidSub(dstIp)):
		pass
            	#print "Not an allowed flow, lets install deny flow for this guy", srcIp, dstIp
	        #matchDict = { 'eth_type':2048,'ipv4_src':srcIp }
	    	#self.ryu_fl_hdlr.get_flow_stats_obj().deny_flow_via_rest(matchDict=matchDict)
	
        #udp or tcp
	if (proto == 17 or proto == 6):
	    srcPort = pkt.protocols[2].src_port
            dstPort = pkt.protocols[2].dst_port		
	# icmp
	if (proto == 1): 
            icmpType = pkt.protocols[2].type
            icmpCode = pkt.protocols[2].code

	
        #fwd_actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
        #rev_actions = [datapath.ofproto_parser.OFPActionOutput(in_port)]

        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]	
        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            if ((proto == 17 or proto == 6) and (offset == 0)):
                self.ryu_fl_hdlr.add_flow(
			msg, datapath, in_port=in_port,
			out_port=out_port, srcMac=srcMac, dstMac=dstMac,
			srcIp=srcIp, dstIp=dstIp, proto=proto, tos=tos, 
			actions=actions, srcPort=srcPort, dstPort=dstPort,
			offset=offset
		)

	    elif (proto == 1):
                self.ryu_fl_hdlr.add_flow(
			msg, datapath, in_port=in_port, out_port=out_port,
			srcMac=srcMac, dstMac=dstMac, srcIp=srcIp, dstIp=dstIp, 
			proto=proto, tos=tos, actions=actions, 
			icmpType=icmpType, icmpCode=icmpCode
		)
	    
	    else:
                self.ryu_fl_hdlr.add_flow(
			msg, datapath, in_port=in_port, out_port=out_port, 
			srcMac=srcMac, dstMac=dstMac, srcIp=srcIp, dstIp=dstIp, 
			proto=proto, tos=tos,actions=actions, offset=offset
		)


	
        #data = None
        #if msg.buffer_id == ofproto.OFP_NO_BUFFER:
        #    data = msg.data

        #out = datapath.ofproto_parser.OFPPacketOut(
        #    datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port,
        #    actions=fwd_actions, data=data)
        #datapath.send_msg(out)

