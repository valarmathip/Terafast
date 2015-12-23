import pycurl
import json
import time
import requests
import threading
from StringIO import StringIO
from flow_handler import RyuFlowHandler

def get_flow_handler_obj(dpid):
	return dpidTable[dpid];

class FlowStats(object):

    def __init__(self):
	self.dpId = '27834080684'
        self.fetch_url = 'http://10.6.3.5:8080/stats/flow/%s' % self.dpId
        self.flow_add_url= 'http://10.6.3.5:8080/stats/flowentry/add'
	self.flow_delete_url = 'http://10.6.3.5:8080/stats/flowentry/delete_strict'
	self.flows_delete_url= 'http://10.6.3.5:8080/stats/flowentry/delete'
	self.port_info_url= 'http://10.6.3.5:8080/stats/portdesc/%s' % self.dpId
        self.get_switch_stats_url = 'http://10.6.3.5:8080/stats/switches'
	self.sess = requests.Session()
	self.aging_time = 60 # one min aging
	self.match_map = {"dl_src":"eth_src", "dl_dst":"eth_dst",
			 "dl_type":"eth_type", "nw_src":"ipv4_src", 
			"nw_dst":"ipv4_dst", "nw_proto":"ip_proto",
			"tp_src":["udp_src", "tcp_src"], 
			"tp_dst":["udp_dst", "tcp_dst"],
	}
	
	# check if the switch  datapath is up? sit on a loop till datapath is ready

    def get_rest_service_status(self):
	
	for i in range(10):
	    try:
	        res = self.sess.get(self.get_switch_stats_url)	
	        if res.status_code == 200: 
	            print '\n\n DpId !!!:', json.loads(res.text)
		    return True 
	    except:
		print '\n\n !! Except.....'
		time.sleep(1)
	else:
	    raise Exception(' \n ....REST has not started even after 10 secs...!!!!')

    def get_port_info(self):
	res = self.sess.get(self.port_info_url)
	return json.loads(res.text)

    def get_flow_stats(self):
        #buffer = StringIO()
        res = self.sess.get(self.fetch_url)
        #print "Result : ", json.loads(res.text)
        return json.loads(res.text)
  
    def clear_all_flows(self):
	payloadDict = {'dpid':self.dpId}
	self.sess.post(self.flows_delete_url, data=json.dumps(payloadDict))

    def add_arp_flow(self):

	matchDict = { 'eth_type':'2054' };
	actionList = []
	actionList.append({ 'type' : 'OUTPUT', 'port' : '4294967290'})
	payloadDict = {}
	payloadDict['dpid'] = self.dpId
	payloadDict['priority']=32765
	payloadDict['match'] = matchDict
	payloadDict['actions'] = actionList
	
	self.sess.post(self.flow_add_url, data=json.dumps(payloadDict))

    def deny_flow_via_rest(self, priority=32768, hard_timeout=0, matchDict=None):
	
	payloadDict = {}
	payloadDict['dpid'] = self.dpId
	payloadDict['priority']= priority
	payloadDict['hard_timeout'] = hard_timeout
	payloadDict['match'] = matchDict
	
	self.sess.post(self.flow_add_url, data=json.dumps(payloadDict))

	
    def convert_rest_flow_to_our_flow(self,rest_flow):

	our_flow = {}
	
	our_flow['priority'] = rest_flow['priority']
	our_flow['byte_count'] = rest_flow['byte_count']
	our_flow['packet_count']=rest_flow['packet_count']
	our_flow['srcMac']=rest_flow['match']['dl_src']
	our_flow['dstMac']=rest_flow['match']['dl_dst']
	our_flow['ethType']=rest_flow['match']['dl_type']
	our_flow['srcIp'] = rest_flow['match']['nw_src']
	our_flow['dstIp'] = rest_flow['match']['nw_dst']
	our_flow['proto'] = rest_flow['match']['nw_proto']
	our_flow['in_port'] = rest_flow['match']['in_port']
	our_flow['srcPort'] = our_flow['dstPort'] = 0
	if our_flow['proto'] == 6 or our_flow['proto'] == 17 :
		our_flow['srcPort']=rest_flow['match']['tp_src']
		our_flow['dstPort']=rest_flow['match']['tp_dst']

	return our_flow

	

    def get_match_dict(self, match):

	
	new_match = {}
	for key, value in self.match_map.iteritems():
	    print '\n\n Key....!!! ', key
	    if key == "tp_src" :
		if match['nw_proto'] == 17:
		    new_match[value[0]] = match[key]
		elif match['nw_proto'] == 6:
		    new_match[value[1]] = match[key]
		else:
		    pass
	    elif key == "tp_dst" :
		if match['nw_proto'] == 17:
		    new_match[value[0]] = match[key]
		elif match['nw_proto'] == 6:
		    new_matvalue[value[1]] = match[key]
		else:
		    pass
	    else:
	        new_match[value] = str(match[key])
	
	new_match["ip_proto"] = match['nw_proto']	
	new_match["in_port"] = "1"
	return new_match

 
    def delete_flow_from_ofctl(self, flow):

	print '\n\n Inside Delete Flow', flow

	flow_data = {}
	flow_data["priority"] = str(flow['priority'])
	flow_data["dpid"] = self.dpId
	flow_data["match"] = self.get_match_dict(flow['match'])
	flow_data["actions"] = [{"type":"OUTPUT","port":"2"}]
	#flow_data["actions"] = get_actions(flow[actions])

	dictStr = json.dumps(flow_data)
	req = self.sess.post(self.flow_delete_url,dictStr)
 	if not req.status_code == 200:
	    print 'Unable to delete the flow from ofctl table via curl...!!!'

	# delete the same flow from flow table as well....
	flow_key = flow['match']['nw_src'] + '_' + str(flow['match']['tp_src']) + '_' + flow['match']['nw_dst'] + '_' + str(flow['match']['tp_dst'])
#	RyuFlowHandler().delete_flow(flow_key)


    def stats_collector(self):
	flows = self.get_flow_stats() 	
        #print "\n\n STATS FLows:", flows

	for value in flows.itervalues():
	    for flow in value:
		#ignore arp flows
		if flow['actions'] == [] :
			continue
		if flow['match']['dl_type'] != 2054 :
			tera_flow = self.convert_rest_flow_to_our_flow(flow)
			RyuFlowHandler().update_flow_stats(tera_flow)
	RyuFlowHandler().dump_flows_to_file()


