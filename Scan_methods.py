import subprocess
import os
import threading
import sys
import socket
import nmap
import yaml
import paramiko

# Disse varibaler skal være globale da data fra flere funktioner skal gemmes
port_list_til_print = []
ip_and_port_for_scan = []
host_list = []


def hostscanner(IP):
    global host_list
    system = sys.platform
    DEVNULL = open(os.devnull, "w")
# Skraldespand vaiabel

    if system == 'win32':
        svar = subprocess.run(["ping", "-n", "1", "-w", "20", IP], stdout=DEVNULL)
    else:
        svar = subprocess.run(["ping", "-c", "1", IP], stdout=DEVNULL)
    if svar.returncode == 0:
        host_list.append(IP)


def hostthreading(ip_input):
    threads = []
    global host_list
    ip_sidste_octet = ip_input.split(".")

# Dette tager data fra arrayets 3 indeksering dvs. 4 plads
# Lav om i range, dette er ændret fordi det tage FUCKING lang tid
# At køre scriptet og fejlfinde kode.
    for ip_sidste_octet[3] in range(0, 255):
        ip_til_scan = ".".join(map(str, ip_sidste_octet))
        t = threading.Thread(target=hostscanner, args=(ip_til_scan,))
        threads.append(t)
    for i in range(10, 255):
        threads[i].start()
    for i in range(10, 255):
        threads[i].join
    return host_list


def tcp_connnecter(ip_input, port_number):
    global port_list_til_print
    global ip_and_port_for_scan
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.settimeout(1)
    try:
        a = TCPsock.connect_ex((ip_input, port_number))
        if a == 0:
            port_list_til_print.append(f"IP: {ip_input} PORT: {port_number}: OPEN")
            ip_and_port_for_scan.append([ip_input, port_number])
    except:
        print("Error occured")
    #return port_list, "SHIT AINT WORKING"

def port_scanner(ip_input):
    global port_list_til_print
    threads = [] # tom liste
    for ports in range(500):
        t = threading.Thread(target=tcp_connnecter, args=(ip_input, ports))
        threads.append(t)

# Her tilføjer alle de tråde der skal startes til ip'en
# Dette bliver tilføjet til vores threads liste som vi kører alle sammen på samme tid senere hen 

    for i in range(500):
        threads[i].start()

# Her starter vi alle de threads vi har gjort klart før
# Disse threads bliver kaldt ved hjælp af indekseringen [i]

    for i in range(500):
        threads[i].join()
    return port_list_til_print

CVE_search_list = []
# Prøver med normal liste, dette kan give problemer når jeg skal hente data ud igen til søgning, overvejer en dict til at holde styr på IP

def service_on_port():
    global ip_and_port_for_scan
    global CVE_search_list
    #print(ip_and_port_for_scan)
    nmscan = nmap.PortScanner()

# Bliver nok nød til at læse lidt igennem source for at fatte hvordan ting bliver printet pænt
# https://bitbucket.org/xael/python-nmap/src/master/nmap/nmap.py

    for i, j in ip_and_port_for_scan:
        print(f"Service Scanning {i} : {j}")
        #nmscan.scan(i, str(j), "-sC -sV") 
        nmscan.scan(i, str(j), "-A")
        var_for_print = nmscan.analyse_nmap_xml_scan()
        #print(var_for_print)
        #print(yaml.dump(var_for_print, default_flow_style=False))

# Bliver nok nød til at greppe script, cpe, product og version direkte inde i min forloop
# Da jeg har brug for (i), (j) da jeg ikke kan regne med disse værdier er de samme (IP og port).
# Min tanke er at bygge en liste op med de ting jeg skal hive ud fra nmap scan og bruge til CVE søgning

        til_print = nmscan[i].tcp(j)
        #print(til_print)
        #print (til_print["state"])
        print("Port " + str(j) + ": " + til_print["state"] + " " + til_print["cpe"] + "\n")
        splittet_cpe = til_print["cpe"].split(":")
        for i in splittet_cpe[-3:]:
            print (i)

        try:
            name = var_for_print['scan'][i]['tcp'][j]['name']
            product = var_for_print['scan'][i]['tcp'][j]['product']
            version = var_for_print['scan'][i]['tcp'][j]['version']
            if len(name) or len(product) or len(version) > 2:
                CVE_search_list.append([i, name, product, version])
            else:
                print(f"Can't fetch data for {i}")
        except:
            pass
#Bliver nød til at sætte try except ind da den ellers får typeerror fejl, da der nogle gange ikke er værdier i de keys jeg efterspørger.


def search_exploit():
    global CVE_search_list
    #print (CVE_search_list)

# Specifik søgning af exploiot-db databasen. Kan laves til online søgning, lige nu søger den kun lokalt.
# Overvejer om man skal have "searchsploit -u" med i koden så biblioteket bliver opdateret hver gang man køre koden

    for ip, name, product, version in CVE_search_list:
        print(f"\nScanning for known CVE: {ip} {name} {product} {version}")
        if len(product) > 1:
            subprocess.run(["searchsploit", product])
            command = f"searchsploit {product} | grep {version}"
        elif len(name) > 1:
            subprocess.run(["searchsploit", name])
        else:
            print("Not able to fetch data")
# Skal have snakket lidt med Ole om hvor specifik søgningen skal være, om man vil have en quick win eller man vil finde overordnede exploits
# Lige nu kan jeg ikke få grep til at fungere. PIPE med subproccess er fundet her: https://stackoverflow.com/questions/13332268/how-to-use-subprocess-command-with-pipes

def bruteforce():
    global ip_and_port_for_scan
    #print (ip_and_port_for_scan)
    ip_and_port_for_bruteforce = []
    for i, j in ip_and_port_for_scan:
        if j == 22:
            ip_and_port_for_bruteforce.append([i, j])
            print (f"SSH running on IP: {i}\nStarting Bruteforce")
    #print (ip_and_port_for_bruteforce)
# Kode fra paramiko https://docs.paramiko.org/en/stable/api/client.html
    ssh_connection = paramiko.SSHClient()
    ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
