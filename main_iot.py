import socket
import sys
from local_modules.tools import *
from local_modules.db import *
from random import randint

'''
Forbidden ranges:
    0.0.0.0 to 0.255.255.255
    10.0.0.0 to 10.255.255.255
    127.0.0.0 to 127.255.255.255
    172.16.0.0 to 172.31.255.255
    192.168.0.0 to 192.168.255.255
'''

excluded_ips = [
    [167772160, 184549375],
    [2130706432, 2147483647],
    [2886729728, 2887778303],
    [3232235520, 3232301055],
]
ports = [21, 22, 25, 80, 110, 443]
google_ip = "212.182.64.91"

# ip_list = ['140.120.51.160', '178.159.11.162']

def grab_banner(target_ip, target_port):
    try:
        target_ip = google_ip
        s = socket.socket()
        s.connect((target_ip, target_port))
        print '[+] Connection to ' + target_ip + ' port ' + str(target_port) + ' succeeded!'
        try:
            name = socket.gethostbyaddr(target_ip)
            get = 'GET / HTTP/1.1\r\n' + 'Host: ' + name[0] + '\r\n\r\n'
            s.send(get)
            ret = s.recv(128)
            print '[+]' + str(ret)
            return str(ret)
        except Exception, e:
            print '[-] Unable to grab any information: ' + str(e)
            return None
    except Exception, e:
        print '[-] Connection to ' + target_ip + ' port ' + str(target_port) + ' failed: ' + str(e)
        return None
    finally:
        s.close()


def main():
    iot_db = IoTDatabase("iot_database.db")
    socket.setdefaulttimeout(0.5)

    visited_ips = tuple()

    while True:
        ip = randint(2 ** 24, 2 ** 32)

        if excluded_ips[0][0] <= ip <= excluded_ips[0][1]:
            continue
        elif excluded_ips[1][0] <= ip <= excluded_ips[1][1]:
            continue
        elif excluded_ips[2][0] <= ip <= excluded_ips[2][1]:
            continue
        elif excluded_ips[3][0] <= ip <= excluded_ips[3][1]:
            continue
        elif ip in visited_ips:
            continue
        else:
            visited_ips += (ip,)

        try:
            ip_adr = no_to_ip(ip)
            for port in ports:
                banner = grab_banner(ip_adr, port)
                if banner is not None:
                    banner = ''.join([line.strip() for line in banner.strip().splitlines()])
                    banner = ip_adr + ':' + str(port) + ' - ' + banner
                    print banner
                    iot_db.insert(ip_adr, port, banner)

        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
