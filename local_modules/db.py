import sqlite3

pages_query = '''
  CREATE TABLE `Urls` (
    `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    `url`	TEXT NOT NULL UNIQUE
  );
'''
words_query = '''
  CREATE TABLE `Words` (
    `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    `word`	TEXT NOT NULL UNIQUE
  );
'''

pairs_query = '''CREATE TABLE Pairs (
  word_id int NOT NULL,
  url_id int NOT NULL,
  FOREIGN KEY (word_id) REFERENCES Words(id),
  FOREIGN KEY (url_id) REFERENCES Urls(id)
);
'''

check_url_query = 'SELECT EXISTS(SELECT 1 FROM Urls WHERE url=?);'
insert_url_query = 'INSERT INTO Urls (url) VALUES (?);'
select_url_query = 'SELECT id FROM Urls WHERE url=?;'

check_word_query = 'SELECT EXISTS(SELECT 1 FROM Words WHERE word=?);'
insert_word_query = 'INSERT INTO Words (word) VALUES (?);'
select_word_query = 'SELECT id FROM Words WHERE word=?;'


insert_pair_query = 'INSERT INTO Pairs (word_id, url_id) VALUES (?, ?);'


class Database:
    def __init__(self, filename):
        self.con = sqlite3.connect(filename, check_same_thread=False)
        self.cur = self.con.cursor()

        self.cur.execute(pages_query)
        self.cur.execute(words_query)
        self.cur.execute(pairs_query)

    def insert(self, url, words):
        self.cur.execute(check_url_query, (url,))
        if self.cur.fetchone()[0] != 0:
            return

        self.cur.execute(insert_url_query, (url,))
        self.cur.execute(select_url_query, (url,))
        url_id = self.cur.fetchone()[0]

        for word in words:
            self.cur.execute(check_word_query, (word,))
            if self.cur.fetchone()[0] == 0:
                self.cur.execute(insert_word_query, (word,))

            self.cur.execute(select_word_query, (word,))
            word_id = self.cur.fetchone()[0]
            self.cur.execute(insert_pair_query, (word_id, url_id))
        self.con.commit()

