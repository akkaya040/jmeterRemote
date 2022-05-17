import os

# Get the current working directory
cwd = os.getcwd()

#Configuration variables
username = 'remoteServerUserName'
port=22
servers = ["192.168.2.20","192.168.2.21","192.168.2.22"]
passwords = ["p4ssw0rd!","p4ssw0rd!","@p4ssw0rd!"]

#Local Path Data For Copying To Remote Machines
local_jmeter_path = cwd+'\\apache-jmeter-5.4.1.tar'
local_csv_path = cwd+'\\Tests\\currencySet.csv'
local_test_path = cwd+'\\Tests\\Test.jmx'
local_smoketest_path = cwd+'\\Tests\\TestSmoke.jmx'

#Remote Path Data For Store Test Script In Remote Machines
remote_working_path = '/home/akkaya/'
remote_tests_path = '/home/akkaya/Test'

print("-------------------------------------------------------------------------------------------------------")
print("Current directory:    {0}".format(cwd))
print("username:             {0}".format(username))
print("port:                 {0}".format(port))
print("servers:              {0}".format(servers))
print("passwords:            {0}".format(passwords))
print("local_jmeter_path:    {0}".format(local_jmeter_path))
print("local_test_path:      {0}".format(local_test_path))
print("local_smoketest_path: {0}".format(local_smoketest_path))
print("remote_working_path:  {0}".format(remote_working_path))
print("remote_tests_path:    {0}".format(remote_tests_path))
print("-------------------------------------------------------------------------------------------------------")