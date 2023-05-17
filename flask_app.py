import socket
import ssl
import time
import requests
from urllib.parse import urlparse
from flask import Flask, render_template
import datetime

app = Flask(__name__)

def get_urls():
    with open('url.txt', 'r') as f:
        urls = f.read().splitlines()
    return urls

def get_tls_info(domain):
    ctx = ssl.create_default_context()
    s = ctx.wrap_socket(socket.socket(), server_hostname=domain)
    s.connect((domain, 443))
    cert = s.getpeercert()
    not_after = cert['notAfter']
    expiration_date = datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y GMT")
    days_till_expiry = (expiration_date - datetime.datetime.now()).days
    is_valid = days_till_expiry > 0
    return is_valid, expiration_date.strftime("%Y-%m-%d %H:%M:%S"), days_till_expiry

def fetch_url_data(urls):
    url_data = []
    for url in urls:
        parsed_url = urlparse(url)
        start_time = time.time()
        try:
            response = requests.get(url)
            response_time = (time.time() - start_time) * 1000  # convert to milliseconds
            tls_valid, expiration_date, days_till_expiry = get_tls_info(parsed_url.hostname)
            url_data.append((url, response.status_code, response_time, tls_valid, expiration_date, days_till_expiry))
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    return url_data

@app.route('/')
def home():
    urls = get_urls()
    url_data = fetch_url_data(urls)
    return render_template('index.html', url_data=url_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

