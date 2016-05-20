import re

dict1 = {'polatis:1':'1', 'terafast:2':'2'}

for i,j in dict1.iteritems():
    key = i[:-2]
    print key


line = '2015-09-16T03:13:16.858894-00:00'

match = re.match('(\d+-\d+-\d+)T(\d+:\d+):\d+.\d+-\d+:\d+', line)


print match.group()
#print match.group(1).split('-')
p = match.group(1).split('-')
print match.group(2)
q = match.group(2).split(':')


for j in range(0, 2):
    q[j] = int(q[j])+1
    print q[j]
    print q

for i in range(0, 3):
    p[i] = int(p[i])+1
    print p[i]
    print p






import sys
import datetime

 
from lxml import etree as etree
from ncclient import manager
from ncclient.xml_ import *

from xml.etree.ElementTree import *


now = datetime.datetime.now()

 
def connect(host, port, user, password, source):
 

    global now
    try:
        show_command = sys.argv[1]
    except IndexError:
        print "please specify show command as first argument."
        sys.exit(1)
 
    try:
        xpath_expr = sys.argv[2]
    except IndexError:
        xpath_expr=''
 
    conn = manager.connect(host=host,
            port=port,
            username=user,
            password=password,
            timeout=3,
            device_params = {'name':'junos'},
            hostkey_verify=False)

    curr_time = now.isoformat()
 
    #t = """<system-restart xmlns="http://www.polatis.com/yang/optical-switch"/>""" 
    #t = """<set-current-datetime xmlns="http://www.polatis.com/yang/optical-switch"><current-datetime>2015-02-18T09:08:15.949336</current-datetime></set-current-datetime>"""
    t = """<set-current-datetime xmlns="http://www.polatis.com/yang/optical-switch"><current-datetime>%s</current-datetime></set-current-datetime>""" % curr_time
    try:
        #result = conn.command(command=show_command, format='xml')
        result = conn.rpc(t)
        print "result is : %s" % result
    except Exception, e:
        print "ncclient_demo.py: Encountered critical error"
        print e
        #sys.exit(1)





    set_cur_dt = Element('set-current-datetime', {'xmlns':"http://www.polatis.com/yang/optical-switch"})
    current_dt = SubElement(set_cur_dt, 'current-datetime')
    current_dt.text = '2015-02-18T09:08:15.949336'


    result = """<set-current-datetime xmlns="http://www.polatis.com/yang/optical-switch"><current-datetime>2015-02-18T09:08:15.949336</current-datetime></set-current-datetime>"""

    print "result is : %s" % result
    xmlstr = tostring(set_cur_dt)
    #tree = etree.XML(result.tostring)
    tree = etree.XML(xmlstr)
    print " tree is : %s\n\n" % tree
 
    if xpath_expr:
        print "insdie if loop\n\n"
        filtered_tree_list = tree.xpath(xpath_expr)
        print "filtered_tree_list is : %s\n\n" % filtered_tree_list
        for element in filtered_tree_list:
            print " inside foe loop"
            print etree.tostring(element)
    else:
        print "else loop"
        print etree.tostring(tree)
 
if __name__ == '__main__':
    connect('10.99.99.227', 830, 'admin', 'root', 'running')


"""



#!/usr/bin/env python
from datetime import date
from lxml.html import tostring
from lxml.html.builder import E


datestr = date(2013, 11, 30).strftime('%Y-%m-%d')

page = E.html(
    E.title("date demo"),
    E('time', "some value", datetime=datestr))

with open('somefile.html', 'wb') as file:
    file.write(tostring(page, doctype='<!doctype html>', pretty_print=True))



import datetime

format = "%a %b %d+'T'+ %H:%M:%S %Y"
#format = "%A %B %D+'T'+ %H:%M:%S %Y"

today = datetime.datetime.today()
print 'ISO     :', today

s = today.strftime(format)
print 'strftime:', s

d = datetime.datetime.strptime(s, format)
print 'strptime:', d.strftime(format)



from config import get_config_arg

c  = get_config_arg('cross_connects', 'ingress_ports_range')

print "c i s: %s" % c



list1 = ['1','2','3']

list3 = []
list4 = []
list2 = [17,18,19]

b = ''
r = ''

w = str(list1)
x = str(list2)

for i in range(2,13, 5):
  
    a = ''.join(w[i])
    #print a
    if i == 12:
        b = b+a
        #list3.append(a)
    else:
        b = b+a+','
    #print a
    list3.append(a)
    #print list3



print len(x)
print x[5]
print x[6]
for i in range(1, 10, 4):
    print i

    p = ''.join(x[i])+''.join(x[i+1])
    print p
    if i == 7:
        r = r+p
    else:
        r = r+p+','
    list4.append(p)


print "list3 is %s" % list3
print "list4 is %s" % list4

print "b is %s" % b
print "r is %s" % r


print list3 == list4

"""
