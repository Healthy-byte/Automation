import Scan_methods
import art
import socket
import time
import sys
import yaml


def main():
    art.tprint("AutoScan", font="random")
    system = sys.platform
    if system == "win32":
        my_ip = socket.gethostbyname(socket.gethostname())
        print(my_ip)
    else:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            my_ip =  s.getsockname()[0] # Giver både IP og port. Skal bruge indeks 0
            #print (my_ip)
        except:
            print("Not able to connect to the internet, waiting 30 seconds and trying again")
            time.sleep(30)
            main()

    #hostname = socket.gethostname()
    #my_ip = socket.gethostbyname(hostname)

    if my_ip != "127.0.0.1":
        print (f"My ip address is {my_ip}")
        #Scanning live hosts on network
        host_list = Scan_methods.hostthreading(str(my_ip))
        print("SCANNING NETWORK...\n")
        if host_list =="":
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
            
            #nice_print = open_ports.append(Scan_methods.port_scanner(index))
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

        Scan_methods.service_on_port()
        with open("output_file.yml", "w") as outfile:
            yaml.dump(Scan_methods.service_on_port(), outfile, default_flow_style=False)
        #for ip_adresses in host_list:
            #Scan_methods.service_on_port(ip_adresses)
    else:
        print("Not connected to the internet, waiting 1 minute and trying again")
        time.sleep(60)
        main()
if __name__ == "__main__":
    main()