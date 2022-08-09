from netmiko import ConnectHandler
import getpass
import colorama
from colorama import init
init()
from colorama import Fore,Back,Style


ipHandle=open("ipfile.txt")
iplist=ipHandle.readlines()

configList="config_file.txt"

user = input("Enter your ssh username : ")
password = getpass.getpass()

for line in  iplist:
    HOST=line.strip("\n")
    
    if HOST:
    
        print ("Config on switch %s ... " %HOST)
        session = ConnectHandler(device_type='cisco_ios',host=HOST, username=user, password=password )
        session.send_config_from_file(configList)
        print (Fore.GREEN + "Config on switch %s was succesfully" %HOST + Style.RESET_ALL)
        session.disconnect()
    else:
        ipHandle.close()
        print (Fore.GREEN + "ipfile.txt has ended" + Style.RESET_ALL)
        
    
ipHandle.close()

    
