#!/usr/bin/python

import netaddr
import csv

class PolicyUser:
    def __init__(self,file=None):
        self.users = {}
        if file is not None:
            self.loadConfig(file)
	    #self.dump_config()

    def loadConfig(self, file):
        with open(file,mode='r') as fd:
            networkips= csv.reader(fd)
            #ip/mask,applications
            for networkip in networkips:
               #self.ip,self.mask=networkip[0].split('/');
               #remove the key from the list
               self.users[networkip[0]] = networkip

    def isIpValidSub(self, ip):
        for key in self.users.keys():
            keyIp, mask= key.split('/')

            zeroMaskLen = 32 - int(mask)
            bitMask = (0xffffffff >> zeroMaskLen) << zeroMaskLen
            checkIpMask= int(netaddr.IPAddress(ip)) & bitMask
            origIpMask= int(netaddr.IPAddress(keyIp)) & bitMask
            #print "checkIpMask, origIpMask :", checkIpMask, origIpMask

            if origIpMask == checkIpMask:
		return True

    def dump_config(self):
	    for k,v in self.users.iteritems():
		    print k,v

    def get_name(self,ip):
        if ip in self.users.keys():
            return self.users[ip][1]
        else:
            return None
    

#if __name__ == "__main__":
#    policy=PolicyUser('myusers.csv')


