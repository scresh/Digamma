import argparse
from time import sleep

from tools.methods import *
import threading
import socket

from tools.shared_memory import IoTSharedMemory


class IoTThread(threading.Thread):
    def __init__(self, thread_id, shared_memory):
        super().__init__()
        self.thread_id = thread_id
        self.shared_memory = shared_memory
        self.batch_size = int(256 ** 4 / shared_memory.threads_no)

    def run(self):
        batch_sqrt = int(self.batch_size ** 0.5)
        ip_int_base = self.thread_id * self.batch_size
        for i in range(self.batch_size):

            if not self.shared_memory.run_threads:
                break

            ip = int_to_ip(ip_int_base + batch_sqrt * (i % batch_sqrt) + int(i / batch_sqrt))
            for port in self.shared_memory.ports:
                if not self.shared_memory.run_threads:
                    break

                try:
                    target_socket = socket.socket()
                    target_socket.settimeout(self.shared_memory.timeout)
                    target_socket.connect((ip, port))

                    data = "GET / HTTP/1.1\r\n\r\n"
                    target_socket.send(data.encode())
                    banner = target_socket.recv(128)
                    target_socket.close()

                    self.shared_memory.save_banner(ip, port, banner)
                    self.print(f'[+] Connection to {ip}:{port} succeeded!\nBanner:{banner}', SUCCESS)

                except Exception as e:
                    self.print(f'[-] Connection to {ip}:{port} failed: {type(e).__name__}', WARNING)

    def print(self, text, color):
        if self.shared_memory.run_threads:
            print(f'Thread #{self.thread_id}:\t{color}{text}{NORMAL}')


def main():
    parser = argparse.ArgumentParser(description='Run IoT scanner')
    parser.add_argument('--threads', default=4, choices=[1, 4, 16, 64, 256, 1024], help='The number of threads')
    parser.add_argument('--ports', nargs='+', type=int, default=[21, 22, 23, 80])
    args = parser.parse_args()

    thread_list = []
    shared_memory = IoTSharedMemory(threads_no=args.threads, ports=args.ports, timeout=0.5)

    for thread_id in range(args.threads):
        thread_list.append(IoTThread(thread_id, shared_memory))
        thread_list[thread_id].start()

    try:
        while shared_memory.run_threads:
            sleep(0.25)
    except KeyboardInterrupt:
        print(f'\nStopping {args.threads} threads...')
        shared_memory.run_threads = False
        for thread in thread_list:
            thread.join()


if __name__ == '__main__':
    main()
