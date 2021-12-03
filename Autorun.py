import hack
import socket
import time
import telepot
import os
from datetime import datetime
from requests import get
from secrets import token, chat_id

internet = False
first_boot = True
file_path = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(file_path, "myscan.txt")


def telebot_msg_rcv(msg):
    '''
    Denne funktion står for behandling af beskeder
    der bliver modtaget fra Telegram applikationen.
    Funktionen tager et argument "msg" i form af et 
    dictionary. Dette argument bliver givet af en 
    API og er noget der er lavet af Telegram.
    '''

    command = msg['text']
    print("Har modtaget kommandoen: %s" % command)
    if command == "Scan":
        scan()
    elif command == "Searchsploit update":
        telebot_cli_print(hack.searchsploit_update())


def telebot_cli_print(msg):
    '''
    Denne funktion behandler output. Den printer
    først i terminalen med print() statement.
    herefter sender den beskeden via telepot
    modulet. Tilsidst bliver output gemte til 
    en fil og sendt til Telegram applikationen
    som en rapport til senere brug. Denne funktion
    tager et argument "msg" hvilket er en streng.
    '''
    print (msg)
    global file_name
    global first_boot
    global internet
    if internet and msg != "":
        bot.sendMessage(chat_id, msg)
    if first_boot:
        first_boot = False
        tal = 1
        while os.path.isfile(file_name):
            file_name = f"myscan{tal}.txt"
            tal += 1
    file = open(file_name, "a")
    file.write(f"{msg} \n")
    file.close()
    if msg == "Scanning afsluttet.":
        file = open(file_name, "rb")
        bot.sendDocument(chat_id, file)


def scan():
    '''
    Denne funktion står for at køre alle vores
    scan funktioner fra "hack.py" filen samt
    vores telebot_cli_print funktion. Dette er
    vores hovedfunktion.
    '''
    dato = datetime.now()
    dato_list = (dato.strftime("%d/%m/%Y"), dato.strftime("%H:%M:%S"))
    telebot_cli_print(f"Dato: {dato_list[0]}\nTid: {dato_list[1]}")
    ip_str, ip_list = hack.host_scanner()
    if ip_list == []:
        telebot_cli_print("Ingen aktive ip'er fundet\n")
    else:
        telebot_cli_print(ip_str)
        for host in ip_list:
            telebot_cli_print(f"starter portscan mod {host}")
            port_str, port_list = hack.port_scanner(host)
            telebot_cli_print(port_str)
            if port_list == []:
                telebot_cli_print("Ingen aktive porte fundet\n")
            else:
                for port in port_list:
                    telebot_cli_print(f"Starter service scan: {host}:{port}")
                    service_str, service_list = hack.service_on_port(host, port)
                    if service_list == []:
                        telebot_cli_print(f"Nmap scan gav ikke et navn, product eller version\n")
                    else:
                        telebot_cli_print(service_str)
                        cve_str = hack.search_exploit(service_list)
                        telebot_cli_print(cve_str)
    telebot_cli_print("Scanning afsluttet.")


'''
Den sidste del af koden består i opsætning. 
Det er her vi sætter vores telepot bot op med
"bot.message_loop(telebot_msg_rcv)".
Det er også her vi lokale og offentlige IP
ved hjælp af private_ip() funktionen fra
hack biblioteket.
'''
net_private_list, ip_private_list = hack.private_ip()
try:
    public_ip = get('https://api.ipify.org').text
    bot = telepot.Bot(token)
    bot.message_loop(telebot_msg_rcv)
    internet = True
    print("Telebot is up and running")
    if len(net_private_list) == 1:
        telebot_cli_print(f"Local IP: {net_private_list[0][0]} / {net_private_list[0][1]}\nPublic IP: {public_ip}\n")
    else:
        telebot_cli_print(f"Local IP: {net_private_list[0][0]} / {net_private_list[0][1]}\n          {net_private_list[1][0]} / {net_private_list[1][1]}\nPublic IP: {public_ip}\n")
except Exception:
    internet = False
    if len(net_private_list) == 1:
        telebot_cli_print(f"Local IP: {net_private_list[0][0]} / {net_private_list[0][1]}\n")
        scan()
    elif len(net_private_list) == 2:
        telebot_cli_print(f"Local IP: {net_private_list[0][0]} / {net_private_list[0][1]}\n          {net_private_list[1][0]} / {net_private_list[1][1]}\n")
        scan()
    else:
        telebot_cli_print("Interface: eht0 og wlan0 er ikke tilsluttet et network")
while 1:
    time.sleep(3600)
    scan()
