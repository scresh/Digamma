import socket
import sys

list_of_ports_to_scan = [21, 22, 25, 80, 110, 443]


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
            ret = s.recv(1024)
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
    saved_banners = open('saved_banners', 'a')

    # zmienna pomocniczna do "testow"
    b = 0

    socket.setdefaulttimeout(2)
    for i in range(178, 255):
        for j in range(159, 255):
            for k in range(11, 255):
                for l in range(162, 255):
                    ip_adr = str(i) + '.' + str(j) + '.' + str(k) + '.' + str(l)
                    for port in list_of_ports_to_scan:
                        banner = grab_banner(ip_adr, port)
                        if banner is not None:
                            banner = ''.join([line.strip() for line in banner.strip().splitlines()])
                            banner = ip_adr + ':' + str(port) + ' - ' + banner
                            saved_banners.write(banner + '\n')
                            b = b + 1
                            # zakonczy po 10 bannerach
                            if b > 10:
                                saved_banners.close()
                                sys.exit()


if __name__ == '__main__':
    main()
