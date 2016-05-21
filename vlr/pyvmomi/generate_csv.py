import sys
import os
import re
import commands


def get_vm_details(vm_server, output):

    for line in output.splitlines():
        if "Name" in line:
            remat = re.match(r'Name\s+\:\s+(\S+)', line)
            if remat:
                #print "name is", remat.group(1)
                #all_vms.append(remat.group(1))
                vm_name = remat.group(1)
                line_to_write = '%s, %s\n' % (vm_server, vm_name)
                print "line to write is", line_to_write
                with open(output_csv_file, 'a') as fp:
                    print "inside file with"
                    fp.write(line_to_write)

    #print "list of vms connected in the vsphere client is", all_vms
    #return all_vms


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print ("%s <vm server list fileName> <csv file name>" % sys.argv[0])
        sys.exit(0)
    
    vm_server_list_file = sys.argv[1]
    output_csv_file = sys.argv[2]
    status, output = commands.getstatusoutput("rm -rf %s" % output_csv_file)
    with open(vm_server_list_file, 'r') as fp:
        for line in fp:
            out = line.split(" ")
            print "out is", out
            host = line.split(" ")[0]
            username = line.split(" ")[1]
            password = line.split(" ")[2].split("\n")[0]
            print "vm server name is", host
            command = "python getallvms.py --host %s --user %s --password %s" % (host, username, password)
	    #command = "python control_local_vmhost.py %s %s %s vms_%s.txt" % (host, username, password, host)
            print "command to run is: '%s'" % command
            status, output = commands.getstatusoutput(command)
            get_vm_details(host, output)
            #print "Status code is: '%s'" % status
            #print output
