from sqlite3 import connect, IntegrityError
from datetime import datetime


class Database:
    def __init__(self):
        self.con = connect('../db-api/digamma.db', check_same_thread=False)

        self.cur = self.con.cursor()

    def insert_pages(self, pages):
        now = datetime.now()

        for page in pages:
            title, content, words, url = page

            try:
                self.cur.execute(
                    'INSERT INTO Pages (url, title, content, updated_at) VALUES (?, ?, ?, ?);',
                    (url, title, content, now),
                )
            except IntegrityError:
                pass
        self.con.commit()

        for page in pages:
            words = page[2]

            for word in words:
                try:
                    self.cur.execute(
                        'INSERT INTO Words (word) VALUES (?);',
                        (word, ),
                    )

                except IntegrityError:
                    pass
        self.con.commit()

        for page in pages:
            title, content, words, url = page

            self.cur.execute(
                'SELECT id FROM Pages WHERE url=?;',
                (url,),
            )
            page_id = self.cur.fetchone()[0]

            for word in words:
                self.cur.execute(
                    'SELECT id FROM Words WHERE word=?;',
                    (word, )
                )
                word_id = self.cur.fetchone()[0]
            try:
                self.cur.execute(
                    'INSERT INTO WordsPages (page_id, word_id) VALUES (?, ?);',
                    (page_id, word_id),
                )
            except IntegrityError:
                    pass

            self.con.commit()

    def insert_devices(self, devices):
        now = datetime.now()
        for device in devices:
            socket, banner, location, organization, county, county_code = device
            try:
                self.cur.execute(
                    'INSERT INTO Devices (socket, banner, updated_at, location, organization, county, county_code) '
                    'VALUES (?, ?, ?, ?, ?, ?, ?);',
                    (socket, banner, now, location, organization, county, county_code),
                )
            except IntegrityError:
                pass
        self.con.commit()
