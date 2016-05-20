

Test_Dict = eval(open('snmp_config.txt').read())

Test_Dict_out_eval = open('snmp_config.txt').read()



print Test_Dict
print Test_Dict_out_eval


print Test_Dict['cpmy_name']

print Test_Dict_out_eval['cpmy_name']
