import os, sys, time
import commands, re
import datetime
import pycurl
import json
from StringIO import StringIO

prev_flow_stats = {}
new_dict = {}
firstTime = True
appIdTable = {}
proto_table = {}

def protoTable(protoFile):

    #fd = open("protofile.txt", "r")
    fd = open(protoFile, "r")
    fileOutput = fd.read()
    global proto_table

    for line in fileOutput.splitlines():
        #print "line is", line
        out_list = line.split(',')
        app_name = out_list[-1].split('@')[1]
        #value = "%s" % app_name
        for i in out_list:
            if '@' in i:
                i = i.split('@')[0]
	    proto_table[i] = app_name

    #print proto_table

    fd.close()

def appTable(appFile):

    fd = open(appFile, "r")
    fileOutput = fd.read()
    global appIdTable
    for line in fileOutput.splitlines():
        out_list = line.split()
        appIdTable[out_list[0]] = out_list[1]
    #print "Application table is", appIdTable

def getAppId(proto, src_port, dst_port, line):
  
    global appIdTable
    global proto_table

    #print "line is", line
    #print "proto num is", proto
    #print "type of proto no is", type(proto)
    if proto == '17':
        proto_name = 'udp'
    elif proto == '6':
	proto_name = 'tcp'
    else:
	proto_name = ' '
 
 
    #if src_port and dst_port and proto_name:
    if (src_port != ' ') and (dst_port != ' ') and (proto_name != ' '):
	for key in proto_table.keys():
	    key_list = key.split(":")
            if key_list[0] == proto_name:
	        #print "proto name is matched with table"
	        port_list = key_list[1].split('-')
		if (int(src_port) >= int(port_list[0])) and (int(src_port) <= int(port_list[1])):
		     app_name =  proto_table[key]
	             #print "app name is ", app_name 
		     break
		elif (int(dst_port) >= int(port_list[0])) and (int(dst_port) <= int(port_list[1])):
		     app_name =  proto_table[key]
		     #print "app name is", app_name
		     break
		else:
		     #print "either src port nor the dst port is not matched with the proto_table"
		     pass
        else:
	    #print "proto name is not matched with the proto table"
	    app_name = "unknown"
    else:
    	app_name = "unknown"
	       
    # Get the application ID from the app_id table
    appId =  appIdTable.get(app_name, None)
    if appId is not None:
    	#print "app id is", appId
    	return appId
    else:
	#print "app id not found in the appTable"
	return 0
 

def flowTable():
    currTime = time.strftime("%H:%M:%S", time.localtime())
   
    table_column_header = "skb_priority, src_mac, dst_mac, eth_type, src_ip, dst_ip, proto, tos, ttl, frag, src_port, dst_port, packets, bytes, used_time, flags, bandwidht, appId\n"
    flow_stats_dict = {}
    global prev_flow_stats
    prev_bytes = 0
    global firstTime
    currTime = datetime.datetime.now()
    #currTime = time.strftime("%H:%M:%S", time.localtime())
    #fileName = "flowStats_%s.csv" % currTime
    fileName = "flowStats.csv"
    print "Get the flow stats at time: %s" % currTime
    status, output = commands.getstatusoutput("ovs-dpctl dump-flows")
    for line in output.splitlines():
        remat = re.search(r'.*skb_priority\((.*?)\)', line)
        if remat:
            priority = remat.group(1)
	else:
	    priority = ' '
        remat = re.search(r'.*eth\(src=(.*?)\,', line)
        if remat:
  	    src_mac_addr = remat.group(1)
	else:
	    src_mac_addr = ' '
	remat = re.search(r'.*?dst=(.*?)\)\,', line)
	if remat:
            dst_mac_addr = remat.group(1)
	else:
	    dst_mac_addr = ' '
	remat = re.search(r'.*?eth_type\((.*?)\)\,', line)
	if remat:
	    eth_type = remat.group(1)
	else:
	    eth_type = ' '
	remat = re.search(r'.*?ipv4\(src=(.*?)\/', line)
	if remat:
	    src_ip_addr = remat.group(1)
	else:
	    src_ip_addr = ' '
	remat = re.search(r'.*?ipv4\(src=\S+\,dst=(.*?)\/', line)
	if remat:
	    dst_ip_addr = remat.group(1)
	else:
	    dst_ip_addr = ' '
	remat = re.search(r'.*proto=(.*?)\/', line)
        if remat:
	    proto_no = remat.group(1)
	else:
	    proto_no = ' '
        remat = re.search(r'.*tos=(.*?)\/', line)
	if remat:
            type_of_service = remat.group(1)
	else:
	    type_of_service = ' '
        remat = re.search(r'.*ttl=(.*?)\/', line)
	if remat:
            time_to_live = remat.group(1)
	else:
   	    time_to_live = ' '
        remat = re.search(r'.*frag=(.*?)\/', line)
        if remat:
            frag_offset = remat.group(1)
	else:
	    frag_offset = ' '
        if 'udp' in line:
            remat = re.search(r'.*udp\(src=(.*?)\,', line)
            if remat:
                src_port = remat.group(1)	   
                #print "source port is", src_port
            else:
                src_port = ' ' 
	    remat = re.search(r'.*udp\(src=\S+\,dst=(.*?)\)', line)
	    if remat:
                dst_port = remat.group(1)
	    else:
                dst_port = ' '
        elif 'tcp' in line:
	    remat = re.search(r'.*tcp\(src=(.*?)\,', line)
	    if remat:
            	src_port = remat.group(1)
	    else:
                src_port = 'unknownIP'
            remat = re.search(r'.*tcp\(src=\S+\,dst=(.*?)\)', line)
	    if remat:
                dst_port = remat.group(1)
            else:
                dst_port = 'unknowIP '
        else:
            src_port = ' '
            dst_port = ' '

	remat = re.search(r'.*packets:(.*?)\,', line)
	if remat:
            packets = remat.group(1)
	else:
	    packets = ' '
        remat = re.search(r'.*bytes:(.*?)\,', line)
	if remat:
            bytes = remat.group(1)
	else:
	    bytes = ' '
        remat = re.search(r'.*used:(.*?)\,', line)
	if remat:
            used_time = remat.group(1)
	else:
	    used_time = ' '
        remat = re.search(r'.*actions:(.*)', line)
	if remat:
            actions = remat.group(1)
            actions = actions.replace(",", ";")
	    
	else:
	    actions = ' '
        remat = re.search(r'.*flags:(.*?)\,', line)
	if remat:
	    flags = remat.group(1)
	else:
            flags = ' '
	remat = re.search(r'.*in_port\((.*?)\)\,', line)
        if remat:	
	    in_port = remat.group(1)

        appId = getAppId(proto_no, src_port, dst_port, line)
        bandwidth = 0
        packets_diff = 0

	tableKey = "%s:%s:%s:%s" % (src_ip_addr, dst_ip_addr, src_port, dst_port)
	tableValue = '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n' % (priority, in_port, src_mac_addr, dst_mac_addr, eth_type, src_ip_addr, dst_ip_addr, proto_no, type_of_service, time_to_live, frag_offset, src_port, dst_port, packets, bytes, used_time, flags, actions, currTime, appId, packets_diff, bandwidth)
	flow_stats_dict[tableKey] =  tableValue

    #print "dictionary is", flow_stats_dict
    if not firstTime:
	#print "not first time"
        new_dict = compareDicts(prev_flow_stats, flow_stats_dict) 
	prev_flow_stats = flow_stats_dict
        createFlowStatsCsv(new_dict, fileName)
    
    else:
	#print "this is first time"
        firstTime = False
        createFlowStatsCsv(flow_stats_dict, fileName)
    

def compareDicts(prev_table, curr_table):

    #print "i m inside compare dict"
    for key in curr_table.keys():
	if key in prev_table.keys():
	    #print "curr table value", curr_table[key]
	    #print "prev table value", prev_table[key]
            diff_bytes = int(curr_table[key].split(',')[14]) - int(prev_table[key].split(',')[14])
            packets_diff = int(curr_table[key].split(',')[13]) - int(prev_table[key].split(',')[13])
	    #print "bytes diff is", diff_bytes
            bandwidth = (diff_bytes * 8) / 10
	    #print "bandwidth is", bandwidth

            #print "before changing the dict", curr_table[key]
            value_list = curr_table[key].split(',')
            value_list[-1] = bandwidth
            value_list[20] = packets_diff
	    valueList = ""
	    listLen = len(value_list)
	    for i in range(0, listLen):
    	        if (i == listLen - 1):
                    valueList = valueList + str(value_list[i])
                else:
        	    valueList = valueList + str(value_list[i]) + ","
            #print "value list before adding in dict", valueList
            #valueList = valueList + "\n"
    	    curr_table[key] = valueList + "\n"
            #print "current table key is", curr_table[key]
    return curr_table

def createFlowStatsCsv(flowTable, fileName):
 
    #table_column_header = "skb_priority, in_port, src_mac, dst_mac, eth_type, src_ip, dst_ip, proto, tos, ttl, frag, src_port, dst_port, packets, bytes, used_time, flags, actions, time\n"

    fd = open(fileName, "a")
    #fd.write(table_column_header)    
    for key, value in flowTable.iteritems():
	fd.write(value)
    fd.close()
    loadFile("tera", fileName)


def getSwitchId():

    print "get the switch id"
    buffer = StringIO()
    url_id = 'http://10.6.0.190:8080/stats/switches'
    c = pycurl.Curl()
    c.setopt(c.URL, url_id)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()
    body = buffer.getvalue()
    #value = json.loads(body)
    return json.loads(body)[1]

def getPortStats(switch_id):

    buffer = StringIO()
    port_url= 'http://10.6.0.190:8080/stats/port/%s' % switch_id
    c = pycurl.Curl()
    c.setopt(c.URL, port_url)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()
    body = buffer.getvalue()
    #print "type of stats out is", type(body), body
    portStat_dict = json.loads(body)
    #print "switch id", switch_id
    value = portStat_dict['%s' % switch_id]
    #print len(value)
    createPortStatsCsv(value)

def getPortDescr(switch_id):

    buffer = StringIO()
    port_url= 'http://10.6.0.190:8080/stats/portdesc/%s' % switch_id
    c = pycurl.Curl()
    c.setopt(c.URL, port_url)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()
    body = buffer.getvalue()
    #print "type of stats out is", type(body), body
    portDescr_dict = json.loads(body)
    #print "switch id", switch_id
    value = portDescr_dict['%s' % switch_id]
    #print len(value)
    createPortDescrCsv(value)


def createPortStatsCsv(dict_portStats):

    #table_header = "tx_dropped, rx_packets, rx_crc_err, tx_bytes, rx_dropped, port_no, rx_over_err, rx_frame_err, rx_bytes, tx_errors, duration_nsec, collisions, duration_sec, rx_errors, tx_packets, time\n"
     
    currTime = datetime.datetime.now()
    #fileName = "portStat_%s.csv" % currTime
    fileName = "portStats.csv"
    fd = open("%s" % fileName, "a")
    #fd.write(table_header)
    for dict_port in dict_portStats:
        #print dict_port.values()
        table_data = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (
    dict_port['tx_dropped'], dict_port['rx_packets'], dict_port['rx_crc_err'], dict_port['tx_bytes'],  dict_port['rx_dropped'], dict_port['port_no'], dict_port['rx_over_err'],  dict_port['rx_frame_err'], dict_port['rx_bytes'], dict_port['tx_errors'], dict_port['duration_nsec'], dict_port['collisions'], dict_port['duration_sec'],dict_port['rx_errors'], dict_port['tx_packets'], currTime)
        fd.write(table_data)
    fd.close()
    loadFile("tera", fileName)

def createPortDescrCsv(portDescr_tablevalue):

    currTime = datetime.datetime.now()
    #fileName = "portDescr_%s" % currTime
    fileName = "portDescr.csv"
    #table_header = "hw_addr, curr, supported, max_speed, advertised, peer, port_no, curr_speed, name, state, config, time\n"
    fd = open("%s" % fileName, "a")
    #fd.write(table_header)
    for dict_port in portDescr_tablevalue:
        table_data  = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (
            dict_port['hw_addr'], dict_port['curr'], dict_port['supported'],
dict_port['max_speed'], dict_port['advertised'], dict_port['peer'],
dict_port['port_no'], dict_port['curr_speed'], dict_port['name'],
dict_port['state'], dict_port['config'], currTime)
        fd.write(table_data)
    fd.close()

    # Load the CSV file into database table
    loadFile("tera", fileName)

def loadFile(dbName, fileName):

   mysql_path = "/home/mravi/mysql-5.5.32/target/usr/local/mysql/bin"

   query = "%s/mysqlimport --socket=/tmp/mysql.sock --user=root --compress --fields-terminated-by=',' --lines-terminated-by='\n' --local --lock-tables --verbose -h 10.6.0.190 %s %s" % (mysql_path, dbName, fileName)

   status, output =  commands.getstatusoutput(query)
   os.system('rm "%s"' % fileName)
   #status, output =  commands.getstatusoutput('rm %s' % fileName)
   #print output
   #print status
    
####################### MAIN PROGRAM #####################


if __name__ == '__main__':

    protoTable("protoFile.txt")
    appTable("app_ids.txt")
   
    while True:
    
     
    	# Get the flow stats and create table
    	flowTable()
    	# Get Switch ID
    	switch_id = getSwitchId()

    	# Get port statistics
    	getPortStats(switch_id) 
   
   	# Get port description
    	getPortDescr(switch_id)
	
    	# Sleep for 10 secs before polling for the statistics 
    	time.sleep(10)
    #flowTable()
