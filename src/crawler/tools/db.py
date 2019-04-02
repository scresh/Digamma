from sqlite3 import connect, IntegrityError
from datetime import datetime


class Database:
    def __init__(self):
        self.con = connect('../db-api/digamma.db', check_same_thread=False)
        # self.con.text_factory = str

        self.cur = self.con.cursor()

    def insert_page(self, url, title, content, words):
        try:
            now = datetime.now()
            self.cur.execute(
                'INSERT INTO Pages (url, title, content, updated_at) VALUES (?, ?, ?, ?);', (url, title, content, now)
            )
            self.con.commit()

            self.cur.execute('SELECT id FROM Pages WHERE url=?;', (url,))
            page_id = self.cur.fetchone()[0]

        except IntegrityError:
            return

        else:
            for word in words:
                try:
                    self.cur.execute('INSERT INTO Words (word) VALUES (?);', (word, ))
                    self.con.commit()

                except IntegrityError:
                    pass

                self.cur.execute('SELECT id FROM Words WHERE word=?;', (word, ))
                word_id = self.cur.fetchone()[0]

                self.cur.execute('INSERT INTO WordsPages (page_id, word_id) VALUES (?, ?);', (page_id, word_id))
                self.con.commit()

    def insert_device(self, socket, banner):
        try:
            now = datetime.now()
            self.cur.execute(
                'INSERT INTO Devices (socket, banner, updated_at) VALUES (?, ?, ?);', (socket, banner, now)
            )
            self.con.commit()
        except IntegrityError:
            pass


