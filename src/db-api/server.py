from http.server import BaseHTTPRequestHandler, HTTPServer
from snippet_generator import generate_snippet
from urllib.parse import urlparse, parse_qs
from sqlite3 import connect
import json
import time


class Handler(BaseHTTPRequestHandler):
    con = connect('digamma.db', check_same_thread=False)
    cur = con.cursor()

    def do_GET(self):
        path = urlparse(self.path).path
        params = parse_qs(urlparse(self.path).query)

        try:
            words = set(params['query'][0].lower().split())
        except (KeyError, IndexError):
            words = []

        if path == '/searchTor':
            if not (0 < len(words) < 12):
                self.send_get_response({'error': 'Incorrect number of words in query'}, 400)

            elif not all(map(lambda x: 0 < len(x) < 16, words)):
                self.send_get_response({'error': 'Incorrect word length'}, 400)

            else:
                pages_dict = {}

                for word in words:
                    self.cur.execute('SELECT id FROM Words WHERE word == ?;', (word, ))
                    word_id = self.cur.fetchone()

                    if word_id:
                        word_id = word_id[0]

                    else:
                        continue

                    self.cur.execute('SELECT page_id FROM WordsPages WHERE word_id == ?;', (word_id, ))
                    page_ids = map(lambda x: x[0], self.cur.fetchall())
                    for page_id in page_ids:
                        if page_id not in pages_dict:
                            pages_dict[page_id] = []

                        pages_dict[page_id].append(word)

                sorted_pages = [
                    (page_id, pages_dict[page_id]) for page_id in
                    sorted(pages_dict, key=lambda x: len(pages_dict[x]), reverse=True)
                ]

                response = {'results': []}
                for page in sorted_pages:
                    page_id = page[0]
                    words = page[1]

                    self.cur.execute('SELECT url, title, content FROM Pages WHERE id == ?;', (page_id,))
                    url, title, content = self.cur.fetchone()
                    snippet = generate_snippet(content, words)
                    response['results'].append({'url': url, 'title': title, 'snippet': snippet})

                self.send_get_response(response, 200)

        # elif path == '/searchIoT':
        #     pass
        else:
            self.send_get_response({'error': 'Page not found'}, 404)

    def send_get_response(self, content, status_code):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1:4200')
        self.end_headers()
        self.wfile.write(
            bytes(json.dumps(content, ensure_ascii=False), 'UTF-8')
        )


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
