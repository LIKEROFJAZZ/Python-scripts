#subprocess.call allows us to execute commands from pyth. script
import subprocess
import optparse
import re  

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="select which interface to change the MAC address on")
    parser.add_option("-m", "--mac", dest="new_MAC", help="new MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_MAC:
        parser.error("[-] Please specify a MAC address, use --help for more info.")
    return options
def change_mac(interface, new_MAC):
    print("[+] changing Mac address for " + interface + " to " + new_MAC)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_MAC])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_Search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_Search_result:
        return (mac_address_Search_result.group(0))
    else:
        print("could not read MAC address")

options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC:" + str(current_mac))

change_mac(options.interface, options.new_MAC)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_MAC:
    print("MAC address was successfuly changed to " + current_mac)
else:
    print("MAC address did not change")

