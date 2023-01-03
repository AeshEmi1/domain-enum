#!/usr/bin/env python3

import subprocess
import sys

# Check if the required number of arguments was provided
if len(sys.argv) != 3:
  print("Usage: dns_lookup.py <input_file> <output_file>")
  sys.exit(1)

# Get the input and output file names from the arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# Open the input file for reading
with open(input_file, "r") as f:
  # Read the list of domain names from the file
  domains = f.read().splitlines()

# Open the output file for writing
with open(output_file, "w") as f:
  # Iterate over the list of domain names
  for domain in domains:
    # Define a list of DNS record types to query
    f.write("DNS RECORDS FOR DOMAIN: " + domain + "\n\n")
    record_types = ["NS", "A", "AAAA", "CNAME", "MX", "SOA", "TXT", "PTR"]

    # Iterate over the list of record types
    for record_type in record_types:
      # Use subprocess.run to run the dig command and get the DNS record of the specified type for the domain
      result = subprocess.run(["dig", "+noall", "+answer", domain, record_type], capture_output=True)

      # Get the output from the command
      record = result.stdout.decode()

      # Write the record to the output file
      if record != "":
        f.write(record)

    f.write("_______________________\n\n")
