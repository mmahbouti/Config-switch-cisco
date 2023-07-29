from netmiko import ConnectHandler
import getpass
from colorama import init
init()
from colorama import Fore,Back,Style
import pandas as pd

def create_excel_from_text(input_text, output_file, header):
    # Split the input text into lines and then split each line by spaces to get the data
    rows = [line.split() for line in input_text.strip().split('\n')]

    # Create a pandas DataFrame from the rows and use the provided header
    df = pd.DataFrame(rows, columns=header)

    # Export the DataFrame to an Excel file
    df.to_excel(output_file, index=False)



ipHandle=open("ipfile.txt")
iplist=ipHandle.readlines()

user = input("Enter your ssh username : ")
password = getpass.getpass()

text_for_excel=''

for line in  iplist:
    HOST=line.strip("\n")
    
    if HOST:
    
        print (Fore.CYAN + "Show CDP On Device %s ... " %HOST + Style.RESET_ALL)
        
        session = ConnectHandler(device_type='cisco_ios',host=HOST, username=user, password=password,port='2222')
        cdp_neighbor_result = session.send_command('show cdp neighbor',use_textfsm=True)
        interface_status_result = session.send_command('show interface status',use_textfsm=True)
        
        for entity in interface_status_result:
            if entity["vlan"] == "trunk":
                port_from_interface_status = entity["port"]

                for x in cdp_neighbor_result:
                    local_intf = x['local_interface']
                    neighbor_name = x['neighbor']
                    neighbor_port = x['neighbor_interface']
                    
                    port_from_cdp = x["local_interface"]
                    if port_from_cdp.find("Gig ")==0:
                        port_from_cdp = port_from_cdp.replace("Gig ","Gi")
                    elif port_from_cdp.find("Fas ")==0:
                        port_from_cdp = port_from_cdp.replace("Fas ","Fa")
                    elif port_from_cdp.find("Ten ")==0:
                        port_from_cdp = port_from_cdp.replace("Ten ","Te")

                    if port_from_interface_status == port_from_cdp:
                        temp_text = str(HOST) + " " +str(local_intf.split()[0]+ local_intf.split()[1]) + " " + str(neighbor_name) + " " + str(neighbor_port.split()[0]+ neighbor_port.split()[1]) + " " + str(entity["vlan"]) + "\n"
                        text_for_excel = text_for_excel + temp_text
                        print (str(HOST) + " " +str(local_intf) + " is  connected to " + str(neighbor_name) + " " + str(neighbor_port) + " and mode is Trunk")

ipHandle.close()

header = ["Src-IP", "Src-Port", "Dst-Hostname", "Dst-Port", "Mode"]
create_excel_from_text(text_for_excel, "cShowUplinkOnAccessSwitch.xlsx", header)
print (Fore.GREEN + "Excel file created successfully." + Style.RESET_ALL)
