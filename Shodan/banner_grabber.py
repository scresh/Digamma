import socket

list_of_ports_to_scan = [21, 22, 25, 80, 110, 443]
#ip_list = ['140.120.51.160', '178.159.11.162']

def grab_banner(target_ip, target_port):
	try:
		s = socket.socket()
		s.connect((target_ip, target_port))
		print '[+] Connection to ' + target_ip + ' port ' + str(target_port) + ' succeeded!'
		try:
			name = socket.gethostbyaddr(target_ip)
			#print name
			get = 'GET / HTTP/1.1\r\n' + 'Host: ' + name[0] + '\r\n\r\n'
			#print get
			s.send(get)
			ret = s.recv(1024)
			print '[+]' + str(ret)
		except Exception, e:
			print '[-] Unable to grab any information: ' + str(e)
			
	except Exception, e:
		print '[-] Connection to ' + target_ip + ' port ' + str(target_port) + ' failed: ' + str(e)
	finally:
		s.close()

def main():
	
	socket.setdefaulttimeout(2)
	for i in range(178, 255):
		for j in range(159, 255):
			for k in range(11, 255):
				for l in range(162, 255):
					ip_adr = str(i) + '.' + str(j) + '.' + str(k) + '.' + str(l)
					for port in list_of_ports_to_scan:
						grab_banner(ip_adr, port)

if __name__ == '__main__':
	main()
