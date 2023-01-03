# domain-enum.py
This script is designed to perform a subdomain enumeration on a list of domains using Amass and Subfinder called from the subscan.py script. It then performs DNS record enumeration on a list of subdomains using the dns_info.py script, a WAF scan on the list of subdomains using wafw00f, and, if specified, an nmap scan on the list of subdomains.
    
## Requirements

* Python 3
* Amass
* Subfinder
* wafw00f
* nmap (optional)

## Usage

To use this script, run the following command:

    ./subdomain_enumeration.py input_file subdomain_output dns_output wafw00f_output [-k] [-v] [-n]

Where <input_file> is the file containing the list of domains to scan, <subdomain_output> is the desired output file name for the Subdomain Enumeration script (*Currently does not support file extensions*), dns_output is the desired output file name for the DNS record enumeration, wafw00f_output is the desired output file name for the WAF scan, and the optional flags -k, -v, and -n specify to keep the Amass and Subfinder output files, show the output of the Amass and Subfinder commands in real time, and perform an nmap scan, respectively.

## Example

Here is an example of how to use this script:

    ./subdomain_enumeration.py domains.txt subdomains dns_results.txt wafw00f_results.txt -k -v -n

This will scan the list of domains in domains.txt for subdomains, saving the output to a file named subdomains.txt. It will then perform DNS record enumeration on the list of subdomains and save the output to a file named dns_results.txt. It will also perform a WAF scan on the list of subdomains and save the output to a file named wafw00f_results.txt. The -k flag specifies to keep the Amass and Subfinder output files, the -v flag specifies to show the output of the Amass and Subfinder commands in real time, and the -n flag specifies to perform an nmap scan on the list of subdomains.

*Additional note: Specifying subdomains.txt instead of subdomains would result in the output file name being subdomains.txt.txt*
