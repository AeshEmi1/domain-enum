#!/usr/bin/env python3

import argparse
import subprocess

# Parse the command-line arguments
parser = argparse.ArgumentParser(description="Scan a list of domains for subdomains using Amass and Subfinder")
parser.add_argument("input_file", help="The file containing the list of domains to scan")
parser.add_argument("subdomain_output", help="The output file name for the subscan.py script. Do not specify file extension") #This needs fixing on the subscan.py end
parser.add_argument("dns_output", help="The output file name for the dns_info.py script")
parser.add_argument("wafw00f_output", help="The output file name for wafw00f output")
parser.add_argument("-k", "--keep", action="store_true", help="Keeps the Amass and Subfinder output files separately (For Subdomain Enumeration)")
parser.add_argument("-v", "--verbose", action="store_true", help="Show the output of the Amass and Subfinder commands in real time (For Subdomain Enumeration)")
parser.add_argument("-n", action="store_true", help="Perform an extensive nmap scan on the subdomains. (Will not perform UDP port scans)")
parser.add_argument("-l", "--logging", action="store_true", help="Enable logging for amass")
parser.add_argument("-w", "--wordlist", help="Specify a wordlist for brute forcing", default=None)
args = parser.parse_args()

# This needs to be made more efficient by editing subscan.py
subdomain_final_name = "{}.txt".format(args.subdomain_output)

# Commands
subdomain_enumeration_command = ["subscan.py", args.input_file, args.subdomain_output]
dns_enumeration_command = ["dns_info.py", subdomain_final_name, args.dns_output]
wafw00f_enumeration_command = ["wafw00f", "-i", subdomain_final_name, "-o", args.wafw00f_output, "-a"]

#Check for subdomain enumeration flags
if args.keep:
	subdomain_enumeration_command.append("-k")
if args.verbose:
	subdomain_enumeration_command.append("-v")
	wafw00f_enumeration_command.append("-vv")
if args.logging:
	subdomain_enumeration_command.append("-l")
if args.wordlist is not None:
	subdomain_enumeration_command.append("-w")
	subdomain_enumeration_command.append(args.wordlist)

# Perform Subdomain Enumeration
subprocess.run(subdomain_enumeration_command)

# Perform DNS record enumeration
subprocess.run(dns_enumeration_command)

# Perform WAF scan
subprocess.run(wafw00f_enumeration_command)

# Perform a dnmasscan
if args.n:
	masscan_output_name = "{}-masscan".format(args.subdomain_output)
	nmap_command = ["sudo", "dnmasscan", subdomain_file_name, masscan_output_name, "-p-", "--max-rate", "18000"]
	if args.verbose:
		nmap_command.append("-v")
	subprocess.run(nmap_command)

print("-------------------------------------------")
print("ENUMERATION COMPLETE")
print("-------------------------------------------")
