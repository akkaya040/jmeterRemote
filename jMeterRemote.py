import paramiko
import config
from scp import SCPClient

servers = config.servers
passwords = config.passwords


def print_result(stdout_str, stderr_str ):
    print('------------------------------------------------------------------------------------')
    if stdout_str != None :
        print(stdout_str)
    if stderr_str != None :
        print(stderr_str)
    print('------------------------------------------------------------------------------------')


def run_sudo_command(connection,sudo_password,command):

    command = "sudo -S -p '' " + command

    stdin, stdout, stderr = connection.exec_command(command)
    print('---command: '+command)
    stdin.write(sudo_password+"\n")
    stdin.flush()
    stdout_str = stdout.read().decode()
    stderr_str = stderr.read().decode()
    print_result(stdout_str, stderr_str)
    return stdout_str, stderr_str


def run_command(connection,command):
    stdin, stdout, stderr = connection.exec_command(command)
    print('---command: '+command)
    stdout_str = stdout.read().decode()
    stderr_str = stderr.read().decode()
    stdin.close()
    stdout.close()
    stderr.close()
    #print_result(stdout_str, stderr_str)
    return stdout_str, stderr_str


def prepare_users(connection,i,userHead,userTail,fileName):
    #Clear Users If Exist 
    run_command(connection,"rm -rf Test/Users/*.csv")
    
    print("User will be prepared...")
    total_user = config.user_count #total users will be seperated for each remote machine.
    server_count = len(servers)
    j=total_user/server_count
    print('i=',i)
    start=str(int(1+i*j))
    stop=str(int((1+i)*j))
    print('start= ',start,' stop= ',stop)

    cmd1="counter="+start+";end="+stop+"; while [[ $counter -le $end ]]; do echo '"+userHead+"'$counter'"+userTail+"'>>"+"Test/Users/"+fileName+".csv; counter=$((counter+1)); done"
    run_command(connection,cmd1)

    print("User preparation was done...")


def connect_to_server(server,passw):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=server, port=config.port, username=config.username, password=passw)
    print("Server connection is open: "+server)
    return ssh_client


def copy_file_from_windows(connection,localPath,remotePath):
    print(localPath+" ---------Transfer Started-------> "+remotePath)
    with SCPClient(connection.get_transport()) as scp:
        scp.put(files=localPath,remote_path=remotePath)
    print(localPath+" ---------Transfer Done-------> "+remotePath)


def control_installation():
    print( "Controls Started...")
    control_java=[]
    control_apache=[]
    control_test=[]
    control_users=[]
    for i in range(len(servers)):
        connection = connect_to_server(server=servers[i],passw=passwords[i])
        
        stdout_str, stderr_str = run_command(connection,"~/apache-jmeter-5.4.1/bin/jmeter --version")
        if "5.4.1" in stdout_str:
            control_apache.append(servers[i]+' Jmeter exist: TRUE')
        else:
            control_apache.append(servers[i]+' Jmeter exist: FALSE')
            
        stdout_str, stderr_str = run_command(connection,"ls ~/Test/")
        if "currencySet.csv" in stdout_str and "Test.jmx" in stdout_str and "TestSmoke.jmx" in stdout_str:
            control_test.append(servers[i]+' Test files exist: TRUE')
        else:
            control_test.append(servers[i]+' Test files exist: FALSE')

        stdout_str, stderr_str = run_command(connection,"java --version")
        if "OpenJDK Runtime Environment" in stdout_str:
            control_java.append(servers[i]+' Java exist: TRUE')
        else:
            control_java.append(servers[i]+' Java exist: FALSE')
        
        stdout_str, stderr_str = run_command(connection,"ls Test/Users/")
        if "User_Market_Buyer.csv" in stdout_str and "User_Limit_Seller.csv" in stdout_str and "User_Limit_Buyer.csv" in stdout_str and "User_Market_Seller.csv" in stdout_str :
            control_users.append(servers[i]+' Users exist: TRUE')
        else:
            control_users.append(servers[i]+' Users exist: FALSE')
        

        connection.close()
    print("---------------------------------")
    print(*control_java, sep = "\n")
    print("---------------------------------")
    print(*control_apache, sep = "\n")
    print("---------------------------------")
    print(*control_test, sep = "\n")
    print("---------------------------------")
    print(*control_users, sep = "\n")
    print("---------------------------------")


def run_test():
    test_name=input("Please enter which test would you like to run ? (TestSmoke | Test): ")
    if test_name == "TestSmoke":
        testcmd="~/apache-jmeter-5.4.1/bin/jmeter -n -t Test/" +test_name + ".jmx"
    elif test_name == "Test":
        testcmd="~/apache-jmeter-5.4.1/bin/jmeter -n -t Test/" +test_name + ".jmx"
    else:
        print("The file is not exist which is entered.")
        return

    print("Test will have been started...")
    for i in range(len(servers)):
        connection = connect_to_server(server=servers[i],passw=passwords[i])
        #run_command(connection,testcmd)
    print("Tests were started...")


def prep_users():
    for i in range(len(servers)):
        connection = connect_to_server(server=servers[i],passw=passwords[i])
        prepare_users(connection,i)


def install():
    print("Installation has just started...")
    for i in range(len(servers)):
        connection = connect_to_server(server=servers[i],passw=passwords[i])
        
        ###Jmeter To Remote Machine
        copy_file_from_windows(connection,config.local_jmeter_path,config.remote_working_path) 
        
        ###Untar Jmeter
        run_command(connection,"tar -xvf *.tar") 
        
        ###Install Java Dependecies Jdk,Jre For Jmeter---
        run_sudo_command(connection,passwords[i],"apt install -y openjdk-11-jdk-headless")
        run_sudo_command(connection,passwords[i],"apt install -y openjdk-11-jre-headless")

        ###Control Jmeter
        run_command(connection,"~/apache-jmeter-5.4.1/bin/jmeter --version")

        ###Create Test/ and Test/Users directories
        run_command(connection,"mkdir Test;cd Test;mkdir Users;cd ..;")
        

        connection.close()
        print("Server connection was closed...")
    print("Installation was done.")

def transfer_test_files():
    print("Test files transfer has just started...")
    for i in range(len(servers)):
        connection = connect_to_server(server=servers[i],passw=passwords[i])
        ###Get Test Scripts
        copy_file_from_windows(connection,config.local_csv_path,config.remote_tests_path)
        copy_file_from_windows(connection,config.local_test_path,config.remote_tests_path)
        copy_file_from_windows(connection,config.local_smoketest_path,config.remote_tests_path)
        connection.close()
    print("Test files transfer was done.")


def task_runner(task_name):
    if task_name == "Install":
        install()
    elif task_name == "Transfer Test Files":
        transfer_test_files()
    elif task_name == "Control Installation":
        control_installation()
    elif task_name == "Prepare Users":
        prep_users()
    elif task_name == "Start Tests":
        run_test()


def main():
    
    taskList = {
        "1":"Install",
        "2":"Transfer Test Files",
        "3":"Control Installation",
        "4":"Prepare Users",
        "5":"Start Tests",
        "0":"Exit",
    }
    
    print("Please select a task ?")
    for taskNum in taskList:
        print(taskNum+"- "+taskList[taskNum])
    
    while 1:
        i = input("Task ================> ")
        if i=="0":
            print("Succesfully exit !!!")
            break
        elif i in taskList:
            task_runner(taskList[i])
        else:
            print("Unhandled Selection!")
            
        print("\nPlease select a task ?")
        for taskNum in taskList:
            print(taskNum+"- "+taskList[taskNum])


main()
