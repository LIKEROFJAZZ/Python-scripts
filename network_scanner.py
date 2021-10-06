#!/usr/bin/env python

# to access fields/help menu of scapy classes, type scapy.ls(scapy.class)

import optparse
import scapy.all as scapy

# scans the network or whatever IP and MAC you set to scan. ARP = IP ether = MAC

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--Target", dest="ip", help="specify the targeted IP address ")
    (options, arguments) = parser.parse_args()
    if not options.ip:
        parser.error("[-] Please specify an IP address, use --help for more info.")

    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients_list = []

    for element in answered_list:
        client_dict = {"IP": element[1].psrc, "MAC": element[1].hwsrc}
        clients_list.append(client_dict)
    return(clients_list)


def print_result(results_list):
    print("IP\t\t\tMAC ADDRESS\n-------------------------------------")

    for client in results_list:
        print(client["IP"] + "\t\t" + client["MAC"])

# 10.0.2.1./24
options = get_arguments()
scan_result = scan(options.ip)
print_result(scan_result)