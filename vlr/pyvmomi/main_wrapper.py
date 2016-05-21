import sys
import os
import commands

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print ("%s <vm server list fileName>" % sys.argv[0])
        sys.exit(0)
    
    vm_server_list_file = sys.argv[1]
    #username = sys.argv[2]
    #password = sys.argv[3]
    with open(vm_server_list_file, 'r') as fp:
        for line in fp:
            out = line.split(" ")
            print "out is", out
            host = line.split(" ")[0]
            username = line.split(" ")[1]
            password = line.split(" ")[2].split("\n")[0]
            print "vm server name is", host
            command = "python control_local_vmhost.py %s %s %s vms_%s.txt" % (host, username, password, host)
            print "command to run is: '%s'" % command
            status, output = commands.getstatusoutput(command)
            print "Status code is: '%s'" % status
            print output
