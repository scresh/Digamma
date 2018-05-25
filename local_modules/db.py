import sqlite3

pages_query = '''
  CREATE TABLE `Pages` (
    `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    `url`	TEXT NOT NULL UNIQUE,
    `title`	TEXT NOT NULL,
    `html`	TEXT NOT NULL
  );
'''
words_query = '''
  CREATE TABLE `Words` (
    `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    `word`	TEXT NOT NULL UNIQUE
  );
'''

sentences_query = '''
  CREATE TABLE `Sentences` (
    `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    `sentence`	TEXT NOT NULL UNIQUE
  );
'''

pairs_query = '''CREATE TABLE Pairs (
  word_id int NOT NULL,
  page_id int NOT NULL,
  sentence_id int NOT NULL,
  FOREIGN KEY (word_id) REFERENCES Words(id),
  FOREIGN KEY (page_id) REFERENCES Pages(id),
  FOREIGN KEY (sentence_id) REFERENCES Sentences(id)
);
'''

check_page_query = 'SELECT EXISTS(SELECT 1 FROM Pages WHERE url=?);'
insert_page_query = 'INSERT INTO Pages (url, title, html) VALUES (?, ?, ?);'
select_page_query = 'SELECT id FROM Pages WHERE url=?;'

check_word_query = 'SELECT EXISTS(SELECT 1 FROM Words WHERE word=?);'
insert_word_query = 'INSERT INTO Words (word) VALUES (?);'
select_word_query = 'SELECT id FROM Words WHERE word=?;'

check_sentence_query = 'SELECT EXISTS(SELECT 1 FROM Sentences WHERE sentence=?);'
insert_sentence_query = 'INSERT INTO Sentences (sentence) VALUES (?);'
select_sentence_query = 'SELECT id FROM Sentences WHERE sentence=?;'

insert_pair_query = 'INSERT INTO Pairs (word_id, page_id, sentence_id) VALUES (?, ?, ?);'


class Database:
    def __init__(self, filename):
        self.con = sqlite3.connect(filename, check_same_thread=False)
        self.cur = self.con.cursor()

        self.cur.execute(pages_query)
        self.cur.execute(words_query)
        self.cur.execute(sentences_query)
        self.cur.execute(pairs_query)

    def insert(self, url, words, html, title, sentences):
        self.cur.execute(check_page_query, (url,))
        if self.cur.fetchone()[0] != 0:
            return

        self.cur.execute(insert_page_query, (url, title, html))
        self.cur.execute(select_page_query, (url,))
        url_id = self.cur.fetchone()[0]

        for sentence in sentences:
            self.cur.execute(check_sentence_query, (sentence,))
            if self.cur.fetchone()[0] == 0:
                self.cur.execute(insert_sentence_query, (sentence,))

        for word in words:
            self.cur.execute(check_word_query, (word,))
            if self.cur.fetchone()[0] == 0:
                self.cur.execute(insert_word_query, (word,))

            self.cur.execute(select_word_query, (word,))
            word_id = self.cur.fetchone()[0]

            for sentence in sentences:
                if word in sentence.lower():
                    self.cur.execute(select_sentence_query, (sentence,))
                    sentence_id = self.cur.fetchone()[0]
                    self.cur.execute(insert_pair_query, (word_id, url_id, sentence_id))

        self.con.commit()
