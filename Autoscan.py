import Scan_methods
import art
import socket
import time

def main():
    art.tprint("AutoScan", font="random")
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    if local_ip != "127.0.0.1":
        print (f"My ip address is {local_ip}")
        #Scanning live hosts on network
        host_list = Scan_methods.hostthreading(str(local_ip))
        print("SCANNING NETWORK...\n")
        if list =="":
            print("NO HOSTS FOUND")
        else:
            #print(host_list)
            for i in host_list:
                print(f"HOST: ----> {i} <---- IS LIVE", end="\n")
        print ("\n")
        #out_file = open("Test_Output.txt", "w")
        open_ports = []
        list_til_scan = {}
        #print (host_list)
        for index in host_list:
            print (f"Scanning IP: {index}\n")
            open_ports.append(Scan_methods.port_scanner(index))
            nice_print = open_ports.append(Scan_methods.port_scanner(index))
            #pprint.pprint(nice_print)


        open_ports = open_ports[0]
        print('''
  _      ___  _     __  _           
 / \ | |  |  /  |/ (_  /   /\  |\ | 
 \_X |_| _|_ \_ |\ __) \_ /--\ | \| 
                                    ''')
        for i in open_ports:
            print (i)
        print('''
  _      ___  _     __  _           
 / \ | |  |  /  |/ (_  /   /\  |\ | 
 \_X |_| _|_ \_ |\ __) \_ /--\ | \| 
                                    ''')

        print("\n Doing extensive scanning of open ports using NMAP: \n")
        
        Scan_methods.service_on_port()
        #for ip_adresses in host_list:
            #Scan_methods.service_on_port(ip_adresses)
        
    else:
        print("Not connected to the internet, waiting 1 minute and trying again")
        time.sleep(60)
        main()
if __name__ == "__main__":
    main()