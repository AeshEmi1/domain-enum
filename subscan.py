#!/usr/bin/env python3

import argparse
import subprocess
import os
import threading

# Parse the command-line arguments
parser = argparse.ArgumentParser(description="Scan a list of domains for subdomains using Amass and Subfinder")
parser.add_argument("input_file", help="the file containing the list of domains to scan")
parser.add_argument("output_file", help="the file to write the unique subdomains to")
parser.add_argument("-w", "--wordlist", help="Specify a wordlist for brute forcing", default=None)
parser.add_argument("-k", "--keep", action="store_true", help="Keeps the Amass and Subfinder output files separately")
parser.add_argument("-v", "--verbose", action="store_true", help="Show the output of the Amass and Subfinder commands in real time")
parser.add_argument("-l", "--logging", action="store_true", help="Enable logging for amass")
args = parser.parse_args()

amass_file = "{}-amass.txt".format(args.output_file)
subfinder_file = "{}-subfinder.txt".format(args.output_file)
output_file = "{}.txt".format(args.output_file)

# Define a function to run Amass
def run_amass():
	amass_command = ["amass", "enum", "-brute", "-df",  args.input_file, "-o", amass_file, "-config", os.path.expanduser("~/.config/amass/config.ini")]
	if args.verbose:
		amass_command.append("-v")
	if args.logging:
		amass_command.append("-log")
		amass_command.append("{}.log".format(amass_file))
	if args.wordlist is not None:
		amass_command.append("-w")
		amass_command.append(args.wordlist)

	subprocess.run(amass_command)

# Define a function to run Subfinder
def run_subfinder():
	subfinder_command = ["subfinder", "-dL", args.input_file, "-all", "-o", subfinder_file, "-silent"]
	subfinder_command_verbose = ["subfinder", "-dL", args.input_file, "-all", "-o", subfinder_file]

	if args.verbose:
		subprocess.run(subfinder_command_verbose)
	else:
		subprocess.run(subfinder_command)

#Create threads
amass_thread = threading.Thread(target=run_amass)
subfinder_thread = threading.Thread(target=run_subfinder)

#Start threads
amass_thread.start()
subfinder_thread.start()

#Wait for threads to finish
amass_thread.join()
subfinder_thread.join()

# Open the output file for writing
with open(output_file, "w") as f:

    # Combine the amass and subfinder output
	with open(amass_file, "r") as am, open(subfinder_file, "r") as su, open(output_file, "w") as out:
		out.write(am.read())
		out.write(su.read())

    # Remove duplicate subdomains
	with open(output_file, "r") as f:
		lines = f.readlines()

	lines_set = set(lines)
	
	# Extract the root domain from each subdomain
	root_domains = []
	for subdomain in lines_set:
		domain = urlparse(subdomain).netloc
		root_domain = ".".join(domain.split(".")[-2:])
		root_domains.append(root_domain)

	# Zip the subdomains and root domains together and sort them by root domain
	sorted_subdomains = [subdomain for _, subdomain in sorted(zip(root_domains, lines_set))]

	# Write the sorted subdomains to the output file
	with open(output_file, "w") as f:
		for line in sorted_subdomains:
			f.write(line)

if os.path.exists(amass_file) and not args.keep:
    os.remove(amass_file)

if os.path.exists(subfinder_file) and not args.keep:
    os.remove(subfinder_file)
