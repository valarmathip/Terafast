#!/usr/bin/python

import time
from pysqllib import MySqlAccess
from policyuser import PolicyUser
from collections import OrderedDict
from operator import itemgetter


#Every 5 mins, check the bandwidth  hogger  and isolate from the  network

sub_value = {}
sub_dict = {}

conn_dict = {}
conn_value = {}

server_dict = {}
server_value = {}

app_dict = {}
app_value = {}

FWD=1
REV=2


def get_field(record,field):
    record_map = { 'in_port':0, 'out_port':1, 'src_mac':2, 'dst_mac':3, 'src_ip':4, 'dst_ip':5, 'src_port':6, 'dst_port':7, 'proto':8, 'total_pkts':9, 'total_bytes':10, 'delta_pkts':11, 'delta_bytes':12, 'create_time':13, 'last_seen':14, 'app_id':15,'tos':16 }

    index = record_map[field]
    return record[index]

def update_dict_table(dictKey, dictTable, dir, startTime):

    #check if its a new key?
    if dictKey not in dictTable.keys():
        dictTable[dictKey] = {}
        #new user, so lets create an entry
        dictTable[dictKey]['tx_bytes'] = dictTable[dictKey]['rx_bytes'] = dictTable[dictKey]['tx_pkts'] = dictTable[dictKey]['rx_pkts'] = 0
        if dir == FWD:
            dictTable[dictKey]['tx_bytes'] = get_field(record,'delta_bytes')
            dictTable[dictKey]['tx_pkts'] = get_field(record,'delta_pkts')
        else:
            dictTable[dictKey]['rx_bytes'] = get_field(record,'delta_bytes')
            dictTable[dictKey]['rx_pkts'] = get_field(record,'delta_pkts')

        create_time = get_field(record,'create_time')
        # let worry about our start window to calculate his bandwidth
        if (create_time < startTime):
            create_time = startTime
        dictTable[dictKey]['create_time'] = create_time
        dictTable[dictKey]['last_seen'] = get_field(record,'last_seen')
        dictTable[dictKey]['record_cnt'] =1
    else:
        #user exists

        if dir == FWD:
            dictTable[dictKey]['tx_bytes'] += get_field(record,'delta_bytes')
            dictTable[dictKey]['tx_pkts'] += get_field(record,'delta_pkts')
        else:
            dictTable[dictKey]['rx_bytes'] += get_field(record,'delta_bytes')
            dictTable[dictKey]['rx_pkts'] += get_field(record,'delta_pkts')
        dictTable[dictKey]['record_cnt'] +=1
        create_time = get_field(record,'create_time')
        # let worry about our start window to calculate his bandwidth
        if (create_time <= startTime):
            create_time = startTime
        elif dictTable[dictKey]['create_time'] > create_time :
            dictTable[dictKey]['create_time'] = create_time;

        if get_field(record,'last_seen') < dictTable[dictKey]['last_seen']:
            dictTable[dictKey]['last_seen'] = get_field(record, 'last_seen')


def update_app_dict_table(app_port, dir, startTime):

    update_dict_table(app_port, app_dict, dir, startTime)

def update_server_dict_table(server_ip, dir, startTime):

    update_dict_table(server_ip, server_dict,  dir, startTime)

def update_connection_dict_table(sub_ip, server_ip, dir, startTime):

    conn_key = sub_ip + '-' + server_ip;
    update_dict_table(conn_key,conn_dict,  dir, startTime)


def update_sub_dict_table(sub_ip, dir, startTime):
    #check if its a new key?

    update_dict_table(sub_ip,sub_dict, dir, startTime)


def Process_Sub_record(policy,record, startTime):

    #find sub ip and direction
    sub_ip = get_field(record,'src_ip')
    dir = FWD
    net_port = get_field(record, 'dst_port')

    if not policy.isIpValidSub(sub_ip):
        sub_ip = get_field(record,'dst_ip')
        dir = REV 
        net_port = get_field(record, 'src_port')
        if not policy.isIpValidSub(sub_ip):
            #print "both ipis belongs to valid range. how did we get here!!!!", record
            return
        else:
            server_ip = get_field(record,'src_ip')
    else:
        server_ip = get_field(record,'dst_ip')

    update_sub_dict_table(sub_ip,dir, startTime);
    update_connection_dict_table(sub_ip, server_ip, dir, startTime)
    update_server_dict_table(server_ip, dir, startTime)
    update_app_dict_table(net_port,dir, startTime)
    

def sort_dict(dictTable):
    sorted_table = sorted(dictTable.items(), key = lambda x: x[1]['rx_bytes'], reverse=True)
    return sorted_table
    
    
def dump_sub_records(dictTable):
    
    sorted_dict_rxbytes = sorted(dictTable.items(), key = lambda x: x[1]['rx_bytes'], reverse=True)
    sorted_dict_txbytes = sorted(dictTable.items(), key = lambda x: x[1]['tx_bytes'], reverse=True)

#        print "avg_tx_rate=%u bps, avg_rx_rate=%u bps\n" % (value['tx_bytes']*8/timeInterval, value['rx_bytes']*8/timeInterval)
#        print "avg_tx_pkt_rate=%u, avg_rx_pkt_rate=%u\n" % (value['tx_pkts']/timeInterval, value['rx_pkts']/timeInterval)

if __name__ == "__main__":
    
    # read the records of all subscribers in the last 300 secs
    # aggregate the records based on subscriber ( 2 dictionaries one for tx and another of rx
    # sort the subscriber list based on tx and rx bytes usage
    # take the last 10 top subs
    print "loading the users config"
    policy = PolicyUser('/home/mravi/dbloader/tf_users.csv')
    pollInterval = 300; # 120 secs
    print "connecting to database"
    mySqlHandler = MySqlAccess('10.6.3.5', 'root','','flowmon')
    print "connected to database"
    currTimeStamp = time.time()

    startWindow = currTimeStamp - pollInterval
    sqlFetch = "select * from flow_table where LastSeen > %s" 
    args = (startWindow)


    print "fetch records from database"
    records = mySqlHandler.get_records(sqlFetch,args)
    
    print "Processing all records...., pl wait", len(records)
    time1 = time.time()
    currCnt = 0
    for record in records:
        # if the last seen field in this record is not  within our window, lets ignore it
        last_seen_time = get_field(record,'last_seen');
        if last_seen_time < startWindow:
            print "noticed idle record here..\n"
            continue;
        Process_Sub_record(policy,record, startWindow)
        currCnt +=1
        if not (currCnt % 1000):
            print "Processed %u records" % currCnt


    
    print "all records processed in %u secs" % (time.time() - time1)
    #let sort the sub  table and find out the top user
    sqlFetch = "select * from total_stats_table where timestamp > %s" 
    args = (currTimeStamp - pollInterval)


    print "fetch records from database"
    total_rx_bytes=total_tx_bytes=0
    records = mySqlHandler.get_records(sqlFetch,args)
    for record in records:
        total_rx_bytes += record[2]
        total_tx_bytes += record[1]
 
    total_rx_rate = total_rx_bytes*8/pollInterval;
    total_tx_rate = total_tx_bytes*8/pollInterval;

    print "Total rx_rate=%u, Total_tx_rate=%u" % (total_rx_rate, total_tx_rate)
    currEntryCnt =0;
    sort_sub_list_rx = []
    sort_sub_list_rx = sort_dict(sub_dict)
    for entry in sort_sub_list_rx :
        userName = policy.get_name(entry[0]+'/32')
        if userName is None:
            continue
        txRate= entry[1]['rx_bytes']*8/pollInterval

        print "Hogger: ip=%s, %s, rxRate = %u bps" % (entry[0],userName, txRate)
        currEntryCnt += 1
        if currEntryCnt == 5:
            break;

    currEntryCnt =0;
    sort_conn_list_rx = []
    sort_conn_list_rx = sort_dict(conn_dict)
    for entry in sort_conn_list_rx:
        rxRate= entry[1]['rx_bytes']*8/pollInterval
        print "Hogger: %s, rxRate = %u bps" % (entry[0],rxRate)
        currEntryCnt += 1
        if currEntryCnt == 5:
            break;



    
    #dump_sub_records(sub_dict)
    #dump_sub_records(server_dict)
    #dump_sub_records(conn_dict)
    #dump_sub_records(app_dict)

   

    
