import socket
import sys
import json
from local_modules.tools import *
from local_modules.db import *
from datetime import datetime
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


# ip_list = ['140.120.51.160', '178.159.11.162']

def grab_banner(target_ip, target_port):
    try:
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
    filename = datetime.now().strftime("%Y-%m-%d %H_%M_%S.db")
    iot_db = IoTDatabase(filename)
    socket_list = json.loads(open("list.txt", 'r').read())
    socket.setdefaulttimeout(1.0)

    visited_ips = tuple()
    for socket_object in socket_list:

        ip = socket_object["ip"]
        port = socket_object["ports"][0]["port"]

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

            banner = grab_banner(ip, port)
            if banner is not None:
                print ip, port, banner
                iot_db.insert(ip, port, banner)

        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
