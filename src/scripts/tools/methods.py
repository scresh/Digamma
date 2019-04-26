import socket
import struct
from datetime import datetime

from re import sub
import os
from bs4 import BeautifulSoup
from os.path import expanduser
from subprocess import call, DEVNULL

excluded_ips = [
    [167772160, 184549375],
    [2130706432, 2147483647],
    [2886729728, 2887778303],
    [3232235520, 3232301055],
]

SUCCESS = '\033[92m'
WARNING = '\033[93m'
NORMAL = '\033[0m'


def execute(command):
    return call(command, stderr=DEVNULL, stdout=DEVNULL, shell=True)


def is_html_possible(url):
    supposed_extension = url.split('.')[-1]
    if len(supposed_extension) > 4:
        return True
    if supposed_extension == 'html':
        return True
    return False


def get_onion_domain(url):
    if is_onion_domain(url):
        return '/'.join(url.split('/')[:3])
    else:
        return None


def is_onion_domain(url):
    try:
        if (url.startswith('http://') or url.startswith('https://')) and url.split('/')[2][-6:] == '.onion':
            return True

    except IndexError:
        pass

    return False


def get_values(html, url):
    soup = BeautifulSoup(html, features="html.parser")

    title = soup.title.string
    hrefs = set()

    for tag in soup.findAll(["script", "style", "table", "a", "img", "button", "header", "footer", "nav"]):
        if tag.name == 'a' and tag.string:
            div = soup.new_tag('div')
            div.string = tag.string
            tag.insert_after(div)

        if tag.get('href'):
            href = tag['href']

            if href[0] == '/':
                href = get_onion_domain(url) + href

            if is_onion_domain(href) and is_html_possible(url):
                hrefs.add(href)

        tag.extract()

    content = ' '.join(filter(lambda x: 1 <= len(x) <= 16, sub(r'\s+', ' ', soup.get_text()).split()))
    words = set(sub(r'([^\s\w]|_)+', '', content).lower().split())

    return title, content, list(words), list(hrefs)


def int_to_ip(no):
    return socket.inet_ntoa(struct.pack("!I", no))


def socket_to_int(ip, port):
    socket_int = port
    ip_split = ip.split('.')

    for i in range(len(ip_split)):
        socket_int += int(ip_split[i]) * 256**(3-i) * 2**16

    return socket_int


def get_default_path():
    slash = ['/', '\\'][os.name == 'nt']

    return expanduser("~") + slash + datetime.now().strftime("%Y-%m-%d %H_%M_%S") + '.db'


def is_ip_permitted(ip_int):
    return not any(
        [
            ip_range[0] <= ip_int <= ip_range[1]
            for ip_range in excluded_ips
        ]
    )


def generate_location_str(lat, lon):
    lat_str = ['N', 'S'][lat < 0]
    lon_str = ['E', 'W'][lon < 0]
    lat = abs(lat)
    lon = abs(lon)

    lat_deg = int(lat)
    lon_deg = int(lon)
    lat -= lat_deg
    lat *= 60
    lon -= lon_deg
    lon *= 60

    lat_min = int(lat)
    lon_min = int(lon)
    lat -= lat_min
    lon -= lon_min

    lat_sec = round(lat * 60, 1)
    lon_sec = round(lon * 60, 1)

    return f'{lat_deg}°{lat_min}\'{lat_sec}\"{lat_str} {lon_deg}°{lon_min}\'{lon_sec}\"{lon_str}'
