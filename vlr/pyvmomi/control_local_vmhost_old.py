import sys
import os
import commands
import re

def getAllVms():
    command = "python getallvms.py --host %s --user %s --password %s" % (host, user, password)
    status, output = commands.getstatusoutput(command)

    all_vms = []

    for line in output.splitlines():
        if "Name" in line:
            remat = re.match(r'Name\s+\:\s+(\S+)', line)
            if remat:
                #print "name is", remat.group(1)
                all_vms.append(remat.group(1))
    #print "list of vms connected in the vsphere client is", all_vms
    return all_vms 


def powerOnVm(vm_name):

    command = "python poweronvm.py --host '%s' --user '%s' --password '%s' --vmname '%s'" % (host, user, password, vm_name)
    status, output = commands.getstatusoutput(command)
    if 'Virtual Machine(s) have been powered on successfully' in output:
        print 'vm machine "%s" is successfully powered on' % vm_name
    elif 'Caught vmodl fault' in output:
        remat = re.search(r'.*Caught vmodl fault\s+:\s+(.*)', output)
        if remat:
            print 'Error while trying to power on vm machine "%s" is: %s' % (vm_name, remat.group(1))
        else:
            print "reg ex failed"        
    else:
         print 'Error while trying to power on vm machine "%s" is: %s' % (vm_name, output)
       
     
def powerOffVm(vm_name):
  
    command = "python poweroffvm.py --host '%s' --user '%s' --password '%s' --vmname '%s'" % (host, user, password, vm_name)
    status, output = commands.getstatusoutput(command)
    if 'Virtual Machine(s) have been powered off successfully' in output:
        print 'vm machine "%s" is successfully powered off' % vm_name
    elif 'Caught vmodl fault' in output:
        remat = re.search(r'.*Caught vmodl fault\s+:\s+(.*)', output)
        if remat:
            print 'Error while trying to power off vm machine "%s" is: %s' % (vm_name, remat.group(1))
        else:
            print "reg ex failed"
    else:
        print 'Error while trying to power on vm machine "%s" is: %s' % (vm_name, output)


def vm_power_on_off(file_name, all_vms):
    
    """ Power on/off the vm machines based on the user requirment"""

    with open(file_name, 'r') as fp:
        for line in fp:
            out_list = line.split(' ')
            vm_name = out_list[0]
            operation = out_list[-1].split('\n')[0]
            if vm_name in all_vms:
                if operation == 'ON':
                    powerOnVm(vm_name)
                elif operation == 'OFF':
                    powerOffVm(vm_name)
                else:
                    print "Invalid operation"
            else:
                print 'The vm machine "%s" is not connected with the vm host %s' % (vm_name, host)

 
if __name__ == "__main__":

    if len(sys.argv) != 5:
        print ("%s <vshpere IP : 10.6.0.196> <username: administrator> <password: r@und103cl@cQ> <vms_list_filename>" % sys.argv[0])
        sys.exit(0)

    host = str(sys.argv[1])
    user = str(sys.argv[2])
    password = str(sys.argv[3])
    vms_list_filename = str(sys.argv[4])
    all_vms = getAllVms()    
    print "All the connected vm instance in host '%s' is : %s" % (host, all_vms)
    vm_power_on_off(vms_list_filename, all_vms)
