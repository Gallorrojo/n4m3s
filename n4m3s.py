import ssl
import socket
import argparse
import sys
import os
import re
import logging
import ipaddress
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def logger(level):
    if level:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def banner():
    print("Por @gallorrojo")

def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -d google.com")
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-d', '--domain', help="Domain name to enumerate it's CN and Subjects Alt Name")
    parser.add_argument('-f', '--file', help="File contains a list with domains name to enumerate it's CN and Subjects Alt Name")
    parser.add_argument('-o', '--output', help="Save the results to text file")
    parser.add_argument('-v', '--verbose', help='Enable verbosity and display results in realtime', nargs='?', default=False)
    return parser.parse_args()

def parser_error(errmsg):
    logging.ERROR("Usage: python " + sys.argv[0] + " [Options] use -h for help")
    sys.exit()

def write_file(filename, names):
    logging.INFO("Saving results to file: ", filename)
    with open(str(filename), 'wt') as f:
        for key, value in names.items():
            f.write(f"{key},{value}" + os.linesep)
   
def get_cn_sans(url):
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=url)
        conn.connect((url, 443))
        cert_bin = conn.getpeercert(True)
        cert = x509.load_der_x509_certificate(cert_bin, default_backend())

        # Obtener el Common Name (CN)
        subject = cert.subject
        cn = subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value

        # Obtener los Subject Alternative Names (SANs)
        san_extension = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        sans = san_extension.value.get_values_for_type(x509.DNSName)

        return cn, sans
    except Exception as e:
        logging.debug(f"No se pudo conectar a {url} - {e}")
        return None, []

def read_domains_list(inputFile):
    try:
        with open(inputFile, 'r') as file:
            subdominios = file.readlines()
            subdominios = [subdominio.strip() for subdominio in subdominios]
        return subdominios
    except Exception as e:
        logging.debug(f"Can't read the file: {inputFile} - {e}")
        return []

def isIpAddress(ip_address):
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return None

def isDomain(domain):
    pattern = r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'
    return re.match(pattern, domain) is not None

def main(domain, inputFile, outputFile, verbose):
    logger(verbose)
    n4m3s = {}
    if domain:
        if isDomain(domain) or isIpAddress(domain):
            cn, sans = get_cn_sans(domain)
            if cn is not None:
                n4m3s[cn] = [sans]
                logging.info(f"input:{domain}, CN:{cn}, SANS:{sans}")
        else:
            logging.error(f"{domain} is not a domain or ip address")
    if inputFile:
        domains = read_domains_list(inputFile)
        for d in domains:
            if isDomain(d) or isIpAddress(domain):
                cn, sans = get_cn_sans(d)
                if cn is not None:
                    n4m3s[cn] = [sans]
                    logging.info(f"input:{d}, CN:{cn}, SANS:{sans}")
            else:
                logging.error(f"{domain} is not a domain or ip address")
    if outputFile:
        write_file(outputFile, n4m3s)

def interactive():
    banner()
    args = parse_args()
    domain = args.domain
    inputFile = args.file
    outputFile = args.output
    verbose = args.verbose
    if verbose or verbose is None:
        verbose = True
    main(domain, inputFile, outputFile, verbose)

if __name__ == "__main__":
    interactive()
