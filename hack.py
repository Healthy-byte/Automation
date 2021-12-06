import subprocess
import os
import threading
import socket
import nmap
import yaml
import json
import netifaces
from ipaddress import IPv4Network
from ipaddress import IPv4Address


port_list = []
port_str = ""
ip_list = []
ip_str = ""


def private_ip():
    '''
    Denne funktion gør brug af modulet netifaces.
    Dette bliver brugt til at finde hvilke interfaces
    der bliver brugt og hvilken IP adresse der er blevet 
    tildelt til enheden der kører koden. Hvis enheden
    er på 2 forskellige addresser på WiFi og LAN 
    bliver begge interfaces gemt i ip_private_list.
    Dette bliver returneret sammen med netmaske
    '''
    net_private_list = []
    ip_private_list = []
    try:
        interface = netifaces.ifaddresses('eth0')
        if len(interface) > 2:
            net_private_list.append([interface[2][0]['addr'], interface[2][0]['netmask']])
            ip_private_list.append(interface[2][0]['addr'])
    
        interface = netifaces.ifaddresses('wlan0')
        if len(interface) > 2:
            net_private_list.append([interface[2][0]['addr'], interface[2][0]['netmask']])
            ip_private_list.append(interface[2][0]['addr'])
    except:
        pass
    return net_private_list, ip_private_list


def net_id_finder(ip_private_list):
    '''
    Denne funktion gør brug af ipadress modulet.
    Dette bliver brugt til at finde den lavest mulige
    IP-adresse (netID) i netværket samt hvor mange hosts der
    skal scannes (subnet mask). Funktionen tager et 
    argument som er interfaces der skal scannes. 
    Der kan scannes klasse A, B, C og classless netværk.
    IPv4Network funktionen fra ipadress modulet giver
    netID og omdanner subnet maske til CIDR notation,
    hvilket bliver returneret
    '''
    ip_antal = 0
    threads = []
    threads.clear()
    ip_split = ip_private_list[0].split('.')
    netmask_split = ip_private_list[1].split('.')
    if int(netmask_split[1]) != 255:
        for i in range(int(ip_split[1]) + 1):
            try:
                net = IPv4Network(f"{ip_split[0]}.{ip_split[1]}.0.0/{ip_private_list[1]}")
                return net
            except:
                ip_split[1] = str(int(ip_split[1]) - 1)
    elif int(netmask_split[2]) != 255:
        for i in range(int(ip_split[2]) + 1):
            try:
                net = IPv4Network(f"{ip_split[0]}.{ip_split[1]}.{ip_split[2]}.0/{ip_private_list[1]}")
                return net
            except:
                ip_split[2] = str(int(ip_split[2]) - 1)
    elif int(netmask_split[3]) != 255:
        for i in range(int(ip_split[3])):
            ip_split[3] = str(int(ip_split[3]) - 1)
            try:
                net = IPv4Network(f"{ip_split[0]}.{ip_split[1]}.{ip_split[2]}.{ip_split[3]}/{ip_private_list[1]}")
                return net
            except:
                pass


def ping_test(ip_scan, ip_private_list):
    '''
    Denne funktion gør brug subprocess modulet til at 
    køre vores ping kommando på de forskellige hosts. 
    funktionen tager 2 argurmenter. Det første argument
    er den IP adresse der skal scannes. Det andet argument
    er de interfaces der skal scannes. Denne funktion 
    bliver kaldt af host_scanner() og returnere derfor ikke
    men tilføjer til lister/streng der bliver returneret af 
    host_scanner()
    '''
    global ip_list
    global ip_str
    DEVNULL = open(os.devnull, "w")
    svar = subprocess.run(["ping", "-c", "1", ip_scan], stdout=DEVNULL, stderr=DEVNULL)
    if svar.returncode == 0:
        if len(ip_private_list) == 1:
            ip = ip_private_list[0]
            if ip != ip_scan:
                ip_list.append(ip_scan)
                ip_str += "Host: " + ip_scan + " er aktiv\n"
            else:
                ip_str += "Host: " + ip_scan + " er aktiv (mig selv)\n"
        if len(ip_private_list) == 2:
            ip1 = ip_private_list[0]
            ip2 = ip_private_list[1]
            if ip_scan == ip1 or ip_scan == ip2:
                ip_str += "Host: " + ip_scan + " er aktiv (mig selv)\n"
            else:
                ip_list.append(ip_scan)
                ip_str += "Host: " + ip_scan + " er aktiv\n"


def host_scanner():
    '''
    Denne funktion gør brug af threading modulet til at gøre
    host scanneren mere effiktiv. Threading kalder ping_test funktionen.
    Her gør vi også brug af private_ip()
    funktionen til at finde interfaces samt net_id_finder() til 
    at finde alle de mulige hosts på et interface. Funktionen 
    itererer igennem de mulige hosts, hvoraf 510 threads er 
    maksimalt antal der bliver startet af gangen. Funktionen 
    returnerer en streng og en liste med hosts der svare tilbage
    på ping kommandoen.
    '''
    global ip_list
    global ip_str
    ip_list = []
    ip_str = ""
    threads = []
    net_private_list, ip_private_list = private_ip()
    if len(net_private_list) > 0:
        antal_thread = 0
        max_thread = 510
        thread_sent = 0

        if len(net_private_list) == 1:
            net = net_id_finder(net_private_list[0])
            ip_str = f"Starter scanning af hele IPv4 network: {str(net)}\nFinder alle aktive enheder.\nScanner Well knowns Ports(1-1024) hos aktive enheder.\nAktive porte bliver Nmap scannet.\nNmap info gives til Searchsploit\n\n"
            for host in net:
                t = threading.Thread(target=ping_test, args=(str(host), ip_private_list))
                threads.append(t)
                antal_thread += 1

                if antal_thread == max_thread:
                    for i in range(510):
                        threads[i].start()
                    for i in range(510):
                        threads[i].join
                        thread_sent += 1
                    max_thread += antal_thread

            for i in range(net.num_addresses - 2 - thread_sent):
                threads[i].start()
            for i in range(net.num_addresses - 2 - thread_sent):
                threads[i].join

        elif len(net_private_list) == 2:
            net = net_id_finder(net_private_list[0])
            ip_str = f"Starter scanning af hele IPv4 network: {str(net)}\nFinder alle aktive enheder.\nScanner Well knowns Ports(1-1024) hos aktive enheder.\nAktive porte bliver Nmap scannet.\nNmap info gives til Searchsploit\n\n"
            for host in net:
                t = threading.Thread(target=ping_test, args=(str(host), ip_private_list))
                threads.append(t)
                antal_thread += 1

                if antal_thread == max_thread:
                    for i in range(510):
                        threads[i].start()
                    for i in range(510):
                        threads[i].join
                        thread_sent += 1
                    max_thread += antal_thread

            for i in range(net.num_addresses - 2 - thread_sent):
                threads[i].start()
            for i in range(net.num_addresses - 2 - thread_sent):
                threads[i].join

            if IPv4Address(net_private_list[1][0]) not in net:
                net = net_id_finder(net_private_list[1])
                ip_str += f"\nStarter scanning af IPv4 network: {str(net)}\n\n"
                thread_sent = 0
                max_thread = 510
                for host in net:
                    t = threading.Thread(target=ping_test, args=(str(host), ip_private_list))
                    threads.append(t)
                    antal_thread += 1

                    if antal_thread == max_thread:
                        for i in range(510):
                            threads[i].start()
                        for i in range(510):
                            threads[i].join
                            thread_sent += 1
                        max_thread += antal_thread

                for i in range(net.num_addresses - 2 - thread_sent):
                    threads[i].start()
                for i in range(net.num_addresses - 2 - thread_sent):
                    threads[i].join
            else:
                ip_str += "\nInterface: wlan0, er i sammet network som eth0 interfacet.\n"
    else:
        ip_str += "Interface: eth0 og wlan0, er ikke på noget netværk"
    return ip_str, ip_list


def tcp_connnecter(ip, port):
    '''
    Denne funktion gør brug af socket modulet. Dette bliver
    brugt til at oprette forbindelse til en IP-adresse og port
    Denne funtion tager imod 2 argumenter. Funktionen returnerer
    ikke noget da den bliver kaldt af port_scanner funktionen.
    Der bliver derfor kun tilføjet åben port til en liste og streng.
    '''
    global port_list
    global port_str
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.settimeout(1)
    try:
        opret_socket = TCPsock.connect_ex((ip, port))
        if opret_socket == 0:
            port_str += "Port " + str(port) + ": Aktiv\n"
            port_list.append(port)
    except:
        print(f"Kunne ikke oprette TCP socket til {ip}:{port}")


def port_scanner(ip):
    '''
    Denne funktion gør brug af threading modulet til at gøre
    port scanning mere effektiv. Den tager imod 1 argument i
    form af den IP-adresse der skal scannes. Der bliver scannet
    efter alle velkendte porte. Ved hjælp af threading modulet bliver
    tcp_connecter funktionen kaldt mange gange på samme tid.
    Der bliver returneret en liste og en streng med åbne porte 
    '''
    global port_list
    global port_str
    port_str = ""
    port_list.clear()
    thread_list = []
    for port in range(1025):
        thread = threading.Thread(target=tcp_connnecter, args=(ip, port))
        thread_list.append(thread)
    for port in range(512):
        thread_list[port].start()
    for port in range(512):
        thread_list[port].join()
    for port in range(512, 1025):
        thread_list[port].start()
    for port in range(512, 1025):
        thread_list[port].join()
    return port_str, port_list


def service_on_port(ip, port):
    '''
    Denne funktion gør brug af nmap modluet til at lave fulde scanninger.
    Funktionen tager 2 argumenter, en IP-adresse og en port til søgning.
    Nmap scanningen giver rigtig meget output  men for os er det "name", 
    "product" og "version" der har relevans. Funktionen returnerer 
    en liste og streng. 
    '''
    nmscan = nmap.PortScanner()
    service_str = ""
    service_list = []
    try:
        nmscan.scan(ip, str(port), "-A")
        if nmscan[ip].has_tcp(port):
            result = nmscan[ip].tcp(port)
            service_str += f"Name:  {result['name']}\nProduct: {result['product']}\nVersion: {result['version']}\n"
            service_list.append([port, result["name"], result["product"], result["version"]])
    except:
        pass
    return service_str, service_list


def run_subprocess(name, product, version):
    '''
    Denne funktion gør brug af subprocess modulet til at simplificere
    vores Searchsploit søgninger. Funktionen gør også brug af json
    modulet til at gøre det let læseligt. Funktionen tager 3 argumenter
    til søgning i Seachsploit. Funktionen returnere en dictionary med 
    resultat af søgning.
    '''
    process = subprocess.Popen(["/opt/exploitdb/searchsploit", "-j", name, product, version], stdout=subprocess.PIPE)
    output = process.stdout.read()
    json_output = json.loads(output.decode())
    return json_output


def search_exploit(service_list):
    '''
    Denne funktion gør brug af yaml modulet til at printe vores
    json dictionaries i læseligt format. Funktionen gør også brug af
    run_subprocess funktionen. Funktionen tager et argument i form af
    en liste der indeholder port, name, product og version. Denne funktion
    returnerer en streng til udprint. 
    '''
    cve_str = ""
    for port, name, product, version in service_list:
        if len(product) > 1:
            cve_str += f"Kommando: searchsploit -j {product} {version}\n"
            searchsploit = run_subprocess("", product, version)
            try:
                if len(searchsploit['RESULTS_EXPLOIT']) > 0:
                    cve_str += "\n"
                    for i in range(len(searchsploit['RESULTS_EXPLOIT'])):
                        if i < 16:
                            cve_str += f"{yaml.dump(searchsploit['RESULTS_EXPLOIT'][i])}\n"
                elif len(searchsploit['RESULTS_EXPLOIT']) == 0 and version != "":
                    cve_str += f"Kommando: searchsploit -j {product}\n"
                    searchsploit = run_subprocess("", product, "")
                    if len(searchsploit['RESULTS_EXPLOIT']) > 0:
                        cve_str += "\n"
                        for i in range(len(searchsploit['RESULTS_EXPLOIT'])):
                            if i < 16:
                                cve_str += f"{yaml.dump(searchsploit['RESULTS_EXPLOIT'][i])}\n"
                    else:
                        cve_str += f"Searchsploit gav ingen resultater.\n"
                else:
                    cve_str += f"Searchsploit gav ingen resultater.\n"
            except:
                pass
        elif len(name) > 1 and version != "":
            cve_str += f"Kommando: searchsploit -j {name} {version}\n"
            searchsploit = run_subprocess(name, "", version)
            try:
                if len(searchsploit['RESULTS_EXPLOIT']) > 0:
                    cve_str += "\n"
                    for i in range(len(searchsploit['RESULTS_EXPLOIT'])):
                        if i < 16:
                            cve_str += f"{yaml.dump(searchsploit['RESULTS_EXPLOIT'][i])}\n"
                else:
                    cve_str += f"Searchsploit gav ingen resultater.\n"
            except:
                pass
        else:
            cve_str += f"Nmap scan gav ikke et product eller et navn samt version nummer.\n"
    return cve_str


def searchsploit_update():
    '''
    Denne funktion gør brug af subprocess modulet til at 
    opdatere Searchsploit værktøjet. Funktionen returnerer
    en streng.
    '''
    sploit_str = ""
    try:
        svar = subprocess.run(["/opt/exploitdb/searchsploit", "-u"])
        if svar.returncode == 6:
            sploit_str += "Searchsploit er blevet opdateret."
        else:
            sploit_str += f"Noget gik galt under opdatering.\nReturn code: {svar.returncode}"
    except:
        sploit_str += "Subprocess gik ned, kommando: searchsploit -u"
    return sploit_str
