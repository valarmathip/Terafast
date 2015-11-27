import os, sys, time
import commands, re
import datetime
import pycurl
import json
import pika
import logging
import configparser
import threading
import pika
from StringIO import StringIO
from netaddr import *

#config = configparser.ConfigParser()
logging.basicConfig()

prev_flow_stats_table = {}
curr_flow_stats_table = {}
prev_ports_stats_table = {}
curr_ports_stats_table = {}
curr_ports_descr_table = {}
subscr_ip_table = {}
topDstIPTable = {}
new_dict = {}
firstTime = True
firstTimePort = True
first_time_topDstIP = True
appIdTable = {}
proto_table = {}
switchList = []
block_list_ip = []
threshold_data = 1000000

def ProcessDpiMsgFromRMQ(ch, method, properties, body):
    global prev_flow_stats_table
    print " [x] Received %r" % (body,)
    #print "properties", properties.headers
    key = properties.headers.keys()[0]
    appIdFromDpi = properties.headers[key]
    #print "app id is", appIdFromDpi
    prev_flow_stats_value = prev_flow_stats_table.get(key, None)
    if prev_flow_stats_value is not None:
	prev_flow_stats_table[key][19] = appIdFromDpi	

def receive_rabbitmq_msg():
    channel.basic_consume(callback, queue='dpi')

    channel.start_consuming()


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
    #currTime = time.strftime("%H:%M:%S", time.localtime())
   
    table_column_header = "skb_priority, src_mac, dst_mac, eth_type, src_ip, dst_ip, proto, tos, ttl, frag, src_port, dst_port, packets, bytes, used_time, flags, bandwidht, appId\n"
    global curr_flow_stats_table
    global prev_flow_stats_table
    global firstTime
    currTime = datetime.datetime.now()
    fileName = "flowStats.csv"
    print "Get the flow stats at time: %s" % currTime
    status, output = commands.getstatusoutput("ovs-dpctl dump-flows")
    for line in output.splitlines():
        #print "line is", line
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
            used_bytes = remat.group(1)
	else:
	    used_bytes = ' '
        #print "used bytes are", used_bytes
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
        else:
            in_port = ' '
        

        appId = getAppId(proto_no, src_port, dst_port, line)
        bandwidth = 0
        packets_diff = 0

        my_subnet = IPNetwork('10.6.0.0/16')
        local_ip_list = list(my_subnet)
        #print "len of total hosts", len(local_ip_list)
        #print "first IP is", local_ip_list[0]
        #print "src ip address is", src_ip_addr
        #print "dst ip address is", dst_ip_addr
        #print "src ip address is", src_port
        #print "dst ip address is", dst_port
        if (src_ip_addr != ' ') and (dst_ip_addr != ' ') and (src_port != ' ') and (dst_port != ' '):
            src_ip = IPAddress(src_ip_addr)
            dst_ip = IPAddress(dst_ip_addr)

            if (src_ip in local_ip_list) and (int(src_port) > int(dst_port)):
                flow_direction = 'Forward'
            elif (dst_ip in local_ip_list) and (int(dst_port) > int(src_port)):
                flow_direction = 'Reverse'
                #print "dst_ip", dst_ip
                #print "dst_port", dst_port
                #print "src_port", src_port
            else:
                flow_direction = 'Reverse'
            #print "current flow direction is", flow_direction
        else:
            flow_direction = 'None'
            #print "flow direction in else part", flow_direction

	tableKey = "%s:%s:%s:%s" % (src_ip_addr, dst_ip_addr, src_port, dst_port)
	tableValue = [priority, in_port, src_mac_addr, dst_mac_addr, eth_type, src_ip_addr, dst_ip_addr, proto_no, type_of_service, time_to_live, frag_offset, src_port, dst_port, packets, used_bytes, used_time, flags, actions, appId, packets_diff, bandwidth, flow_direction, currTime]
	curr_flow_stats_table[tableKey] =  tableValue

    #print "current flow stat table is", curr_flow_stats_table	
    #print "dictionary is", flow_stats_dict
    if not firstTime:
	#print "not first time"
        new_flow_stats_table = compareDicts(prev_flow_stats_table, curr_flow_stats_table) 
        processTopTalkers(new_flow_stats_table)
         
        #createFlowStatsCsv(new_flow_stats_table, fileName)
        createCsvAndWriteDb(new_flow_stats_table, fileName)
	prev_flow_stats_table = curr_flow_stats_table
	curr_flow_stats_table = {}
    
    else:
	#print "this is first time"
        firstTime = False
        #createFlowStatsCsv(curr_flow_stats_table, fileName)
        createCsvAndWriteDb(curr_flow_stats_table, fileName)
	prev_flow_stats_table = curr_flow_stats_table
        curr_flow_stats_table = {}

def processTopTalkers(flow_table):
    """ To process the top5 sourceIP, destination IP and applications from the current flow table"""

    print "flowTable in process table function"
    global subscr_ip_table

    for key,value in flow_table.iteritems():
        #print "current value is", value
        subscrIPTable(value)
        #subscrIPTable1(value)
        #top5DstIPTable(value)
        #top5AppTable(value)
        #top5ConnTable(value)

    #for key,value in flow_table.iteritems():
    #    subscrIPTable1(value)

    print "subscriber ip table is", subscr_ip_table
    writeSubscrIPTableIntoDB(subscr_ip_table, 'subscriberIpTable.csv')

def subscrIPTable(value):

    global subscr_ip_table   

    if value[21] == 'Forward':
        print "value in forward flow", value
        print "bandwidth is subsrc ip table is", value[20]
        up_stream_bytes = (value[20] * 10) / 8
        #down_stream_bytes = 0
        print "diiff bytes in subsrc ip table is", up_stream_bytes
        if value[5] in subscr_ip_table.keys():
            subscr_ip_table[value[5]][1] = subscr_ip_table[value[5]][1] + up_stream_bytes
            last_update_time = time.time()
            subscr_ip_table[value[5]][3] = last_update_time
        else:
            down_stream_bytes = 0
            start_time =  time.time()
            last_update_time = start_time
            subscr_ip_table[value[5]] = [start_time, up_stream_bytes, down_stream_bytes, last_update_time]
    elif value[21] == 'Reverse':
        print "value in reverse flow", value
        down_stream_bytes = (value[20] * 10) / 8
        if value[6] in subscr_ip_table.keys():
            subscr_ip_table[value[6]][2] = subscr_ip_table[value[6]][2] + down_stream_bytes
            last_update_time = time.time()
            subscr_ip_table[value[6]][3] = last_update_time
        else:
            up_stream_bytes = 0
            start_time =  time.time()
            last_update_time = time.time()
            subscr_ip_table[value[6]] = [start_time, up_stream_bytes, down_stream_bytes, last_update_time]


def getTop5SubsrcIP():
    global subscr_ip_table
    global threshold_data
    global block_list_ip

    print "current subscriber_ip_table is", subscr_ip_table
    curr_time = time.time()
    for key, value in subscr_ip_table.iteritems():
        #print value[0]
        #print value[1]
        #print value[2]
        entry_time = value[0]
        last_updated_time = value[3]
        if (curr_time - last_updated_time) < 120:
            print "found subscriber in the last 5mins", key
            #print "data consumed %s is: %s" % (key, value[1])
            print "value for %s is: %s" % (key, value)
            if int(last_updated_time - entry_time) != 0:
                
                upStream_data = int(value[1]) / (last_updated_time - entry_time)
                downStream_data = int(value[2]) / (last_updated_time - entry_time)
                #print "total consumed upstream data is", upStream_data
                #print "total consumed upstream data is", upStream_data
                if upStream_data > threshold_data:
                    print "total consumed upstream data is", upStream_data
                    block_list_ip.append(key)
                elif downStream_data > threshold_data:
                    print "total consumed down stream data is", downStream_data
                    block_list_ip.append(key) 


    print "ip's available in the block list is:", block_list_ip
    dropFlows()

    threading.Timer(120, getTop5SubsrcIP).start()

def dropFlows():
    """ Drop the flows for all the subscriber those are available in the block_list"""
    global block_list_ip
    if block_list_ip:
        for ip in block_list_ip:
            print "drop the flows for IP", ip
        block_list_ip = []
        print "block list after droping all", block_list_ip

def top5DstIPTable(value):
    """Process each flow and for a table based on the destination IPs(reverse flow)"""

    global topDstIPTable
    global first_time_topDstIP
    if value[21] == 'Reverse':
        if first_time_topDstIP:
            first_time_topDstIP = False
            start_time =  datetime.datetime.now()
            last_update_time = datetime.datetime.now()
            topDstIPTable[value[5]] = [value[20], start_time, last_update_time]
        else:
            if value[5] in topDstIPTable.keys():
                topDstIPTable[value[5]][0] = topDstIPTable[value[5]][0]  + value[20]
                last_update_time = datetime.datetime.now()
                topDstIPTable[value[5]][2] = last_update_time
            else:
                start_time =  datetime.datetime.now()
                last_update_time = datetime.datetime.now()
                topDstIPTable[value[5]] = [value[20], start_time, last_update_time]

def top5AppTable(value):
    """Process each flow and form a table with top applications"""

    global topAppTable
    global first_time_topApp
    if first_time_topApp:
        first_time_topApp = False
        start_time =  datetime.datetime.now()
        last_update_time = datetime.datetime.now()
        topAppTable[value[18]] = [value[20], start_time, last_update_time]
    else:
        if value[18] in topAppTable.keys():
            topAppTable[value[18]][0] = topAppTable[value[18]][0] + value[20]
            last_update_time = datetime.datetime.now()
            topAppTable[value[18]][2] = last_update_time
        else:
            start_time =  datetime.datetime.now()
            last_update_time = datetime.datetime.now()
            topAppTable[value[18]] = [value[20], start_time, last_update_time]

def compareDicts(prev_table, curr_table):

    for key in curr_table.keys():
	if key in prev_table.keys():
            diff_bytes = int(curr_table[key][14]) - int(prev_table[key][14])
            #print "bytes diff are", diff_bytes
            packets_diff = int(curr_table[key][13]) - int(prev_table[key][13])
            if (packets_diff < 0):
                print "curr Table bytes : %s, prev_table_bytes: %s" %(curr_table[key][14], prev_table[key][14])
            bandwidth = (abs(diff_bytes) * 8) / 10
            #print "bandwidth is",bandwidth
            #print "absolute value for bandwidth is", abs(bandwidth)
            appId = prev_table[key][18]
	    curr_table[key][18] = appId
	    curr_table[key][19] = packets_diff
	    curr_table[key][20] = bandwidth
            #print "type of bandwidth is", type(curr_table[key][20])

    return curr_table

def writeSubscrIPTableIntoDB(tableName, fileName):

    fd = open(fileName, "w+")
    for key, value in tableName.iteritems():
        line = "%s,%s,%s,%s,%s\n" %(key,value[0],value[1],value[2],value[3])
        fd.write(line)
    fd.close()
    loadFile("fileName")

def createCsvAndWriteDb(tableName, fileName):
 
    #table_column_header = "skb_priority, in_port, src_mac, dst_mac, eth_type, src_ip, dst_ip, proto, tos, ttl, frag, src_port, dst_port, packets, bytes, used_time, flags, actions, time\n"

    fd = open("%s" % fileName, "w+")
    #fd.write(table_column_header)    
    for key, value in tableName.iteritems():
	#fd.write(value)
	listLen = len(value)
        strList = ""
	for i in range(0, listLen):
	    if (i == listLen - 1):
		strList = strList + str(value[i])
	    else:
		strList = strList + str(value[i]) + ","
	strList = strList + "\n"
	fd.write(strList)
    fd.close()
    loadFile(fileName)


def getSwitchId(sdnIp, sdnPort):

    print "get the switch id"
    buffer = StringIO()
    url_id = 'http://%s:%s/stats/switches' % (sdnIp, sdnPort)
    c = pycurl.Curl()
    c.setopt(c.URL, url_id)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()
    body = buffer.getvalue()
    #value = json.loads(body)
    return json.loads(body)

def getPortStats(switch_id):

    global prev_ports_stats_table
    global curr_ports_stats_table
    global firstTimePort

    buffer = StringIO()

    port_url= 'http://%s:%s/stats/port/%s' % (sdnIp, sdnPort, switch_id)
    c = pycurl.Curl()
    c.setopt(c.URL, port_url)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    currTime = datetime.datetime.now()
    #print "curr time is", currTime
    c.perform()
    c.close()
    body = buffer.getvalue()
    #print "body is", body
    #print "type of stats out is", type(body), body
    portStat_dict = json.loads(body)
    #print "switch id", switch_id
    port_stats_list = portStat_dict['%s' % switch_id]
    #print "port table list is", port_stats_list
    for dict_port in port_stats_list:
	port_table_key = dict_port['port_no']
        port_table_value = [switch_id, dict_port['tx_dropped'], dict_port['rx_packets'], dict_port['rx_crc_err'], dict_port['tx_bytes'], dict_port['rx_dropped'], dict_port['port_no'], dict_port['rx_over_err'], dict_port['rx_frame_err'], dict_port['rx_bytes'], dict_port['tx_errors'], dict_port['duration_nsec'], dict_port['collisions'], dict_port['duration_sec'], dict_port['rx_errors'], dict_port['tx_packets'], currTime]

	curr_ports_stats_table[port_table_key] = port_table_value
    #print "current ports stats ", curr_ports_stats_table
    #print len(value)
	
    if not firstTimePort:
	for key in curr_ports_stats_table.keys():
	    if key in prev_ports_stats_table.keys():
		tx_bytes = int(curr_ports_stats_table[key][3]) - int(prev_ports_stats_table[key][3])
		tx_bandwidth = (tx_bytes * 8) / 10
		rx_bytes = int(curr_ports_stats_table[key][8]) - int(prev_ports_stats_table[key][8])
		rx_bandwidth = (rx_bytes * 8) / 10
		tx_dropped_count = int(curr_ports_stats_table[key][0]) - int(prev_ports_stats_table[key][0])
		rx_dropped_count = int(curr_ports_stats_table[key][4]) - int(prev_ports_stats_table[key][4])					
		tx_packets_count = int(curr_ports_stats_table[key][14]) - int(prev_ports_stats_table[key][14])					
		rx_packets_count = int(curr_ports_stats_table[key][2]) - int(prev_ports_stats_table[key][2])					
		tx_errors_count = int(curr_ports_stats_table[key][9]) - int(prev_ports_stats_table[key][9])					
		rx_errors_count = int(curr_ports_stats_table[key][13]) - int(prev_ports_stats_table[key][13])					
		counts_list = [tx_bandwidth, rx_bandwidth, tx_dropped_count, rx_dropped_count, tx_packets_count, rx_packets_count, tx_errors_count, rx_errors_count]
	  	curr_ports_stats_table[key] = curr_ports_stats_table[key] + counts_list
	#print "curr table at the second time", curr_ports_stats_table
        createPortStatsCsv(curr_ports_stats_table)
        prev_ports_stats_table = curr_ports_stats_table
	curr_ports_stats_table = {}
    else:
	#print "inside if as this is first time"
        firstTimePort = False 
        # Counts_list elemets are tx_bandwidth, rx_bandwidth, tx_dropped_count, rx_dropped_count, tx_packets_count,
	# rx_packets_count, tx_errors_count, rx_errors_count
	counts_list = [0, 0, 0, 0, 0, 0, 0, 0]
	for key,value in curr_ports_stats_table.iteritems():
	   curr_ports_stats_table[key] = value + counts_list
        #print "cuur ports at first time", curr_ports_stats_table
        createPortStatsCsv(curr_ports_stats_table)
        prev_ports_stats_table = curr_ports_stats_table
	curr_ports_stats_table = {}

def getPortDescr(switch_id):

    global curr_ports_descr_table    
    buffer = StringIO()
    port_url= 'http://%s:%s/stats/portdesc/%s' % (sdnIp, sdnPort, switch_id)
    c = pycurl.Curl()
    c.setopt(c.URL, port_url)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    currTime = datetime.datetime.now()
    c.perform()
    c.close()
    body = buffer.getvalue()
    #print "type of stats out is", type(body), body
    portDescr_dict = json.loads(body)
    #print "switch id", switch_id
    value = portDescr_dict['%s' % switch_id]
    for dict_port in value:
	table_key = dict_port['port_no']
	table_value = [switch_id, dict_port['hw_addr'], dict_port['curr'], dict_port['supported'], dict_port['max_speed'], dict_port['advertised'], dict_port['peer'], dict_port['port_no'], dict_port['curr_speed'], dict_port['name'], dict_port['state'], dict_port['config'], currTime]
    	curr_ports_descr_table[table_key] = table_value
    #print "curr ports descr table is ",  curr_ports_descr_table
    #print len(value)
    createPortDescrCsv(curr_ports_descr_table)


def createPortStatsCsv(ports_stats_table):

    fileName = "portStats.csv"
    fd = open(fileName, "w+")
    for key, value in ports_stats_table.iteritems():
	listLen = len(value)
	strList = ""
	for i in range(0, listLen):
	    if (i == listLen - 1):
		strList = strList + str(value[i])
	    else:
		strList = strList + str(value[i]) + ","	
	strList = strList + "\n"
	fd.write(strList)

    fd.close()
    # Load the ports stats table into database 
    loadFile(fileName)

def createPortDescrCsv(ports_descr_table):

    fileName = "portDescr.csv"
    fd = open("%s" % fileName, "w+")
    for key, value in ports_descr_table.iteritems():
	listLen = len(value)
        strList = ""
	for i in range(0, listLen):
	    if (i == listLen - 1):
		strList = strList + str(value[i])
	    else:
		strList = strList + str(value[i]) + ","
	strList = strList + "\n"
	fd.write(strList)
    fd.close()
    # Load the CSV file into database table
    loadFile(fileName)

def loadFile(fileName):
    
   mysql_server = config['GENERIC']['db_server_name'] 
   dbName = config['GENERIC']['database_name'] 
   mysql_path = "/home/mravi/mysql-5.5.32/target/usr/local/mysql/bin"

   query = "%s/mysqlimport --socket=/tmp/mysql.sock --user=root --compress --fields-terminated-by=\",\" --lines-terminated-by=\"\n\" --local --lock-tables --verbose -h %s %s %s" % (mysql_path, mysql_server, dbName, fileName)

   status, output =  commands.getstatusoutput(query)
   #os.system('rm "%s"' % fileName)
    
####################### MAIN PROGRAM #####################

def FetchAndProcessStats():

    global switchList
    pollingInterval = config.get('GENERIC', 'pollinterval')
    flowTable()
    for switch_id in switchList:
        getPortStats(switch_id)
	getPortDescr(switch_id)
    threading.Timer(int(pollingInterval), FetchAndProcessStats).start()

if __name__ == '__main__':

    protoTable("protoFile.txt")
    appTable("app_ids.txt")

    # arguments/config file- sdn ip, ovs-ip, pollinterval
    #print "before reading conf file"
    # do all the initializations
    # Get Switch ID
    config = configparser.ConfigParser()
    config.read("config.cfg")
    sdnIp = config['GENERIC']['sdn_controller_ip']
    sdnPort = config['GENERIC']['sdn_controller_port']
    rabbitMQ_server = config['GENERIC']['rabbimq_server']
    rabbitMQ_port = config['GENERIC']['rabbimq_server_port']
    #print "sdn ip is", sdnIp
    

    # Block the RabbitMQ connection to receive
    credentials = pika.PlainCredentials('testuser', 'testuser')
    #credentials = pika.PlainCredentials('test', 'test')
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitMQ_server, int(rabbitMQ_port), '/', credentials))
    channel = connection.channel()

    switchList= getSwitchId(sdnIp, sdnPort)
    # initializer timer for  poll interval
    
    FetchAndProcessStats()

    # Process top5 subscriber ip
    getTop5SubsrcIP()

    channel.basic_consume(ProcessDpiMsgFromRMQ, queue='dpi')

    channel.start_consuming()   

