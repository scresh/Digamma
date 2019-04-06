from http.server import BaseHTTPRequestHandler, HTTPServer
from snippet import generate_snippet
from urllib.parse import urlparse, parse_qs
from sqlite3 import connect
import json
import time


def get_words(params):
    try:
        words = set(params['query'][0].lower().split())
    except (KeyError, IndexError):
        words = []

    return words


def get_page_id(params):
    try:
        page_id = int(params['page_id'][0])
    except (KeyError, IndexError, ValueError):
        page_id = -1

    return page_id


def socket_to_str(socket):
    port = socket % 2 ** 16
    socket = int(socket / 2 ** 16)

    ip_segments = []
    for i in range(4):
        ip_segments.append(socket % 256)
        socket = int(socket / 256)

    ip = '.'.join(map(str, ip_segments))

    return f'{ip}:{port}'


class Handler(BaseHTTPRequestHandler):
    con = connect('digamma.db', check_same_thread=False)
    cur = con.cursor()

    def do_GET(self):
        path = urlparse(self.path).path
        params = parse_qs(urlparse(self.path).query)

        if path == '/searchTor':
            self.send_tor_search_response(params)

        elif path == '/previewTor':
            self.send_tor_preview_response(params)

        elif path == '/searchIoT':
            self.send_iot_search_response(params)

        else:
            self.send_get_response({'error': 'Page not found'}, 404)

    def send_get_response(self, content, status_code):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', f'http://localhost:4200')
        self.end_headers()
        self.wfile.write(
            bytes(json.dumps(content, ensure_ascii=False), 'UTF-8')
        )

    def send_tor_search_response(self, params):
        words = get_words(params)

        if not (0 < len(words) < 12):
            self.send_get_response({'error': 'Incorrect number of words in query'}, 400)

        elif not all(map(lambda x: 0 < len(x) < 16, words)):
            self.send_get_response({'error': 'Incorrect word length'}, 400)

        else:
            pages_dict = self.get_page_dict(words)

            sorted_pages = [
                (page_id, pages_dict[page_id]) for page_id in
                sorted(pages_dict, key=lambda x: len(pages_dict[x]), reverse=True)
            ]

            response = self.create_tor_search_response_dict(sorted_pages)
            self.send_get_response(response, 200)

    def send_tor_preview_response(self, params):
        page_id = get_page_id(params)

        self.cur.execute('SELECT title, content, updated_at FROM Pages WHERE id == ?;', (page_id,))
        page_info = self.cur.fetchone()

        if not page_info:
            self.send_get_response({'error': 'Page ID does not exist'}, 400)
        else:
            title, content, updated_at = page_info
            updated_at = updated_at.split('.')[0]
            response = {'result': {'title': title, 'content': content, 'updated_at': updated_at}}
            self.send_get_response(response, 200)

    def send_iot_search_response(self, params):
        words = get_words(params)

        if not (0 < len(words) < 20):
            self.send_get_response({'error': 'Incorrect number of words in query'}, 400)

        elif not all(map(lambda x: 0 < len(x) < 64, words)):
            self.send_get_response({'error': 'Incorrect word length'}, 400)

        else:
            device_dict = self.get_device_dict(words)

            sorted_devices = [
                (device_id, device_dict[device_id]) for device_id in
                sorted(device_dict, key=lambda x: len(device_dict[x]), reverse=True)
            ]

            response = self.create_iot_search_response_dict(sorted_devices)

            self.send_get_response(response, 200)

    def get_page_dict(self, words):
        pages_dict = {}

        for word in words:
            self.cur.execute('SELECT id FROM Words WHERE word == ?;', (word,))
            word_id = self.cur.fetchone()

            if word_id:
                word_id = word_id[0]

            else:
                continue

            self.cur.execute('SELECT page_id FROM WordsPages WHERE word_id == ?;', (word_id,))
            page_ids = map(lambda x: x[0], self.cur.fetchall())
            for page_id in page_ids:
                if page_id not in pages_dict:
                    pages_dict[page_id] = []

                pages_dict[page_id].append(word)

        return pages_dict

    def get_device_dict(self, words):
        device_dict = {}

        for word in words:
            self.cur.execute('SELECT id FROM Devices WHERE banner LIKE ? COLLATE NOCASE;', (f'%{word}%',))
            device_ids = self.cur.fetchall()

            if device_ids:
                device_ids = [*map(lambda x: x[0], device_ids)]
            else:
                continue

            for device_id in device_ids:
                if device_id not in device_dict:
                    device_dict[device_id] = []

                device_dict[device_id].append(word)

        return device_dict

    def create_tor_search_response_dict(self, sorted_pages):
        response = {'results': []}
        for page in sorted_pages:
            page_id = page[0]
            words = page[1]

            self.cur.execute('SELECT id, url, title, content FROM Pages WHERE id == ?;', (page_id,))
            page_id, url, title, content = self.cur.fetchone()
            snippet = generate_snippet(content, words)
            response['results'].append({'id': page_id, 'url': url, 'title': title, 'snippet': snippet})

        return response

    def create_iot_search_response_dict(self, sorted_devices):
        response = {'results': []}
        for device in sorted_devices:
            device_id = device[0]
            words = device[1]

            self.cur.execute('SELECT socket, banner FROM Devices WHERE id == ?;', (device_id,))
            socket, banner = self.cur.fetchone()

            socket_str = socket_to_str(socket)

            response['results'].append({'socket': socket_str, 'banner': banner})

        return response


def main():
    host_name = 'localhost'
    port_number = 9000

    httpd = HTTPServer((host_name, port_number), Handler)
    print(time.asctime(), 'Server Starts - %s:%s' % (host_name, port_number))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (host_name, port_number))


if __name__ == '__main__':
    main()
