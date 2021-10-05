import subprocess
import os
import threading 
import sys
import socket
import nmap
import yaml


host_list = []
#host_list_print = ""
def hostscanner(IP):
    global host_list
    global host_list_print
    system = sys.platform
    DEVNULL = open(os.devnull, "w") #Skraldespand vaiabel
    
    if system == 'win32':
        cmd_kommando = "ping -n 1 -w 20 " + IP # -n er antal gange -w er ms
    else:
        cmd_kommando = "ping -c 1 " + IP
    svar = subprocess.call(cmd_kommando, stdout=DEVNULL)
    if svar == 0:
        host_list.append(IP)
        #host_list_print += "HOST: " + IP + " IS LIVE!\n"      

def hostthreading(ip_input):
    threads = []
    global host_list
    #global host_list_print
    ip_sidste_octet = ip_input.split(".")
    for ip_sidste_octet[3] in range(0,255): #Dette tager data fra arrayets 3 indeksering dvs. 4 plads
        ip_til_scan = ".".join(map(str, ip_sidste_octet))
        t = threading.Thread(target=hostscanner, args=(ip_til_scan,))
        threads.append(t)
    for i in range (0,255):
        threads[i].start()
    for i in range (0,255):
        threads[i].join
    #print(host_list) #Til debug 
    return host_list

port_list_til_print = [] #Brugte en del tid på at finde ud af at dene variabel skal være global da der skal gemmes data fra flere funktioner.
#raw_ports = [[]]
ip_and_port_for_scan = []
def tcp_connnecter(ip_input, port_number):
    global port_list_til_print
    global raw_ports
    global ip_and_port_for_scan
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.settimeout(1)
    #succes = []
    try:
        a = TCPsock.connect_ex((ip_input, port_number))
        if a == 0:
            #succes.append(a) 
            #port_liste.append(port_number)
            port_list_til_print.append(f"IP: {ip_input} PORT: {port_number}: OPEN")

            ip_and_port_for_scan.append([ip_input, port_number])

            #ip_and_port_for_scan.update({ip_input : port_number}) dictionaries kan ikke indeholde samme key til flere forskellige values.
            #Detter bliver bare overskrevet. 
            #print(f"IP: {ip_input} PORT: {port_number}: OPEN")
            #print("Port " + str(port_number) + ": OPEN")   
            #print(port_list) Den bliver taget en ad gange fordi threading funktionen har denne fukntion som targer
            # Så kan ikke fylde en liste op her, da der bliver startet en ny "instans" af funktionen hele tiden    
    except:
        print("Error occured")
    #return port_list, "SHIT AINT WORKING"

def port_scanner(ip_input):
    global port_list_til_print
    global raw_ports
    threads = [] # tom liste
    for ports in range(10000):
        t = threading.Thread(target=tcp_connnecter, args=(ip_input, ports))
        threads.append(t) 
        #Her tilføjer alle de tråde der skal startes til ip'en
        #Dette bliver tilføjet til vores threads liste som vi kører alle sammen på samme tid senere hen
    
    for i in range(10000):
        threads[i].start()
        #Her starter vi alle de threads vi har gjort klart før
        #Disse threads bliver kaldt ved hjælp af indekseringen [i]

    for i in range(10000):
        threads[i].join()
    return port_list_til_print

def service_on_port():
    global raw_ports
    global ip_and_port_for_scan
    nmscan = nmap.PortScanner()
    '''
    nmscan.scan("192.168.0.1", "443", "-v -sC -sV")
    print(nmscan.scaninfo())
    print("IP status: ", nmscan["192.168.0.1"].state())
    print(nmscan["192.168.0.85"].all_protocols())
    '''
    #print(nmscan.command_line())
    #Bliver nok nød til at læse lidt igennem source for at fatte hvordan ting bliver printet pænt
    # https://bitbucket.org/xael/python-nmap/src/master/nmap/nmap.py
    for i, j in ip_and_port_for_scan:
        print(f"Service / Script Scanning {i} : {j}")
        nmscan.scan(i, str(j), "-sC -sV") #Den rigtige variabel (tager meget lang tid)
        print(nmscan.command_line())
        print(nmscan.csv())
        var_for_print = nmscan.analyse_nmap_xml_scan()
        print (yaml.dump(var_for_print, default_flow_style=False))
        #dom = xml.dom.minidom.parseString(var_for_print)
        #print(dom)
        
        #for i, j in var_for_print.items:
         #   print (f"Dette er en test: {i}")
          #  for key in j:
           #     print(key + " : " , j[key])
        #pprint.pprint(nmscan.analyse_nmap_xml_scan)
        #print(nmscan.scaninfo())
        #print(nmscan.get_nmap_last_output())
        #var_for_print = nmscan.csv()
        #df = pandas.read_csv(var_for_print)
        #print(df)
        #print(nmscan[scan])
        #print("IP status: ", nmscan[i].state())


    #return var_for_print
#service_on_port()