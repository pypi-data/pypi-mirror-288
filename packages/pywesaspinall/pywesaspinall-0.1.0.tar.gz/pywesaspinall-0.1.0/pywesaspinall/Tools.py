import requests
import json

def get_ip():
    response = requests.get('https://icanhazip.com')
    ip = dict()
    ip['ip_address'] = response.text
    return json.dumps(ip)

ip = get_ip()