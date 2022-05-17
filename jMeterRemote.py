import paramiko
import config
from scp import SCPClient

servers = config.servers
passwords = config.passwords

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
    pass


def run_test():
    pass


def prep_users():
    pass


def install():
    pass


def main():
    
    print("Please select a task ?\n1- Install\n2- Control Installation\n3- Prepare Users\n4- Start Tests\n5- Exit")
    while 1:
        i = int(input("Task: "))
        if i == 1:
            install()
        elif i==2:
            control_installation()
        elif i==3:
            prep_users()
        elif i==4:
            run_test()
        elif i==5:
            print("Succesfully exit !!!")
            break
        else:
            print("Unhandled Selection!")
        print("\nPlease select a task ?\n1- Install | 2- Control Installation | 3- Prepare Users | 4- Start Tests | 5- Exit")

    



main()
