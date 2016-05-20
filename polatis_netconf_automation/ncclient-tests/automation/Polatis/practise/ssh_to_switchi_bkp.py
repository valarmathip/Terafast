import paramiko
import re



class test:


    def test_again(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('10.99.99.227', username='root', password='P0lat1s')
        stdin, stdout, stderr = ssh.exec_command("date -u +'%Y-%m-%dT%H:%M:%S.%s%z'")
        sys_reboot = ssh.exec_command("reboot")
        type(stdin)
        r = stdout.readlines()
        e = stderr.readlines()
                
        print "err : " , e
                
        print type(r)
                
                
        output = str(r).split('\'')
                
        reg = re.search(r'(\d+-\d+-\d+T\d+:\d+)', output[1])
                
        print "reg : ", reg.group(1)
                
        
        print "output is :", output[1]



#obj = ssh_to_remote()
#obj.ssh_to_switch()
