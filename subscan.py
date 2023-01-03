#!/usr/bin/env python3

import argparse
import subprocess
import os

# Parse the command-line arguments
parser = argparse.ArgumentParser(description="Scan a list of domains for subdomains using Amass and Subfinder")
parser.add_argument("input_file", help="the file containing the list of domains to scan")
parser.add_argument("output_file", help="the file to write the unique subdomains to")
parser.add_argument("-k", "--keep", action="store_true", help="Keeps the Amass and Subfinder output files separately")
parser.add_argument("-v", "--verbose", action="store_true", help="Show the output of the Amass and Subfinder commands in real time")
parser.add_argument("-l", "--logging", action="store_true", help="Enable logging for amass")
args = parser.parse_args()

amass_file = "{}-amass.txt".format(args.output_file)
subfinder_file = "{}-subfinder.txt".format(args.output_file)
output_file = "{}.txt".format(args.output_file)

# Open the output file for writing
with open(output_file, "w") as f:
	# Iterate over the list of domains
	amass_command = ["amass", "enum", "-dns-qps", "3000", "-brute", "-df",  args.input_file, "-o", amass_file, "-config", "~/.config/amass/config.ini"]
	if args.verbose:
		amass_command.append("-v")
		amass_command.append("-src")
	if args.logging:
		amass_command.append("-log")
		amass_command.append("{}.log".format(amass_file))

	subprocess.run(amass_command)

	subfinder_command = ["subfinder", "-dL", args.input_file, "-all", "-o", subfinder_file, "-silent"]
	subfinder_command_verbose = ["subfinder", "-dL", args.input_file, "-all", "-o", subfinder_file]

	if args.verbose:
		subprocess.run(subfinder_command_verbose)
	else:
		subprocess.run(subfinder_command)

    # Combine the amass and subfinder output
	with open(amass_file, "r") as am, open(subfinder_file, "r") as su, open(output_file, "w") as out:
		out.write(am.read())
		out.write(su.read())

    # Remove duplicate subdomains
	with open(output_file, "r") as f:
		lines = f.readlines()

	lines_set = set(lines)

    # Write the unique subdomains to the output file
	with open(output_file, "w") as f:
		for line in lines_set:
			f.write(line)

if os.path.exists(amass_file) and not args.keep:
    os.remove(amass_file)

if os.path.exists(subfinder_file) and not args.keep:
    os.remove(subfinder_file)
