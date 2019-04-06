import argparse
from time import sleep

from tools.db import Database
from tools.methods import *
import threading
import socket
import requests

from tools.shared_memory import IoTSharedMemory


class IoTThread(threading.Thread):
    def __init__(self, thread_id, shared_memory):
        super().__init__()
        self.thread_id = thread_id
        self.batch_size = int(256 ** 4 / shared_memory.threads_no)

        self.shared_memory = shared_memory
        self.thread_memory = []

    def run(self):
        if self.shared_memory.socket_list:
            socket_list = self.shared_memory.socket_list
        else:
            socket_list = self.socket_generator()

        for ip, port in socket_list:
                if not self.shared_memory.run_threads:
                    break
                self.get_banner(ip, port)

        self.shared_memory.run_threads = False

    def print(self, text, color):
        if self.shared_memory.run_threads:
            print(f'Thread #{self.thread_id}:\t{color}{text}{NORMAL}')

    def get_banner(self, ip, port):
        try:
            target_socket = socket.socket()
            target_socket.settimeout(self.shared_memory.timeout)

            target_socket.connect((ip, port))

            data = "HEAD / HTTP/1.1\r\n\r\n"
            target_socket.send(data.encode())
            banner = ''

            recv_data = ' '
            while len(recv_data) > 0:
                recv_data = target_socket.recv(256)
                banner += recv_data.decode("utf-8")

            target_socket.close()

            if len(banner.strip()) > 0:

                ip_info = requests.get(f'https://extreme-ip-lookup.com/json/{ip}').json()
                latitude = float(ip_info.get('lat'))
                longitude = float(ip_info.get('lon'))
                location = generate_location_str(longitude, latitude)

                organization = ip_info.get('org')
                county = ip_info.get('country')
                county_code = ip_info.get('countryCode')

                self.thread_memory.append(
                    (socket_to_int(ip, port), banner.strip(), location, organization, county, county_code)
                )
                self.print(f'[+] Connection to {ip}:{port} succeeded!', SUCCESS)
        except:
            pass

    def socket_generator(self):
        batch_sqrt = int(self.batch_size ** 0.5)
        ip_min_int = self.thread_id * self.batch_size
        ip_max_int = ip_min_int + self.batch_size

        for i in range(batch_sqrt):
            ip_int = ip_min_int + i

            while ip_int < ip_max_int:
                for port in self.shared_memory.ports:
                    yield int_to_ip((ip_int + self.shared_memory.seed) % 256**4), port
                ip_int += batch_sqrt


def main():
    parser = argparse.ArgumentParser(description='Run IoT scanner')
    parser.add_argument('--threads', type=int, default=32, help='The number of threads')
    parser.add_argument('--ports', nargs='+', type=int, default=[21, 22, 23, 80])
    parser.add_argument('--file', type=argparse.FileType('r'))
    args = parser.parse_args()

    db_file = Database()
    thread_list = []
    shared_memory = IoTSharedMemory(threads_no=args.threads, ports=args.ports, file=args.file, timeout=0.5)

    for thread_id in range(args.threads):
        thread_list.append(IoTThread(thread_id, shared_memory))
        thread_list[thread_id].start()

    try:
        while shared_memory.run_threads:
            sleep(0.25)
    except KeyboardInterrupt:
        shared_memory.run_threads = False
        print(f'\nStopping {args.threads} threads...')

    for thread in thread_list:
        thread_id_str = str(thread.thread_id).zfill(3)
        print(f'[ Thread #{thread_id_str} ]\t Saving banners...')
        db_file.insert_devices(thread.thread_memory)
        thread.join()


if __name__ == '__main__':
    main()
