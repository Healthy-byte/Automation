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
            my_ip = s.getsockname()[0]
# Giver både IP og port. Skal bruge indeks 0

        except:
            print("Not able to connect to the internet, waiting 60 seconds and trying again")
            time.sleep(60)
            main()

    if my_ip != "127.0.0.1" or "127.0.1.1":
        print(f"My ip address is {my_ip}")
        host_list = Scan_methods.hostthreading(str(my_ip))
# Scanning live hosts on network
        print("SCANNING NETWORK...\n")

        if host_list == "":
            print("NO HOSTS FOUND")
        else:
            for i in host_list:
                print(f"HOST: ----> {i} <---- IS LIVE", end="\n")
                print (f"Scanning: {i}...", end="\n")
                print ("\n")
                open_ports = Scan_methods.port_scanner(i)
        Scan_methods.service_on_port()
# Gem metoden i en variabel og smid den i fil til print som senere kan sendes
        Scan_methods.bruteforce()

        
    else:
        print("Not connected to the internet, waiting 1 minute and trying again")
        time.sleep(60)
        main()
if __name__ == "__main__":
    main()