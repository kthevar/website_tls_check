import requests
import time
import ssl
import OpenSSL
from urllib.parse import urlparse
import datetime

def get_tls_info(domain):
    cert = ssl.get_server_certificate((domain, 443))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    cert_info = {}
    cert_info['issuer'] = x509.get_issuer()
    cert_info['expiration_date'] = x509.get_notAfter().decode('utf-8')
    expiration_date = datetime.datetime.strptime(cert_info['expiration_date'], "%Y%m%d%H%M%SZ")
    cert_info['valid'] = expiration_date > datetime.datetime.utcnow()
    return cert_info

def fetch_url_data(urls):
    url_data = []
    for url in urls:
        parsed_url = urlparse(url)
        start_time = time.time()
        try:
            response = requests.get(url)
            response_time = time.time() - start_time
            tls_info = get_tls_info(parsed_url.hostname)
            url_data.append((url, response.status_code, response_time, tls_info['valid']))
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    return url_data

def get_urls_from_file(filename):
    with open(filename, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls

def main():
    urls = get_urls_from_file("url.txt")
    url_data = fetch_url_data(urls)
    print(url_data)

if __name__ == "__main__":
    main()
