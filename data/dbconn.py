import psycopg2
import os

db_url = environ.get('DATABASE_URL')

def match(s1,s2):

    words1 = s1.split()
    words2 = []

    for w in s2.split(','):
        for x in w.split():
            words2.append(x)

    for w1 in words1:
        for w2 in words2:
            if(w1.lower()==w2.lower()):
                return True
    return False


class DbConn:
    def __init__(self):
        self.conn = psycopg2.connect(db_url)
        self.make_tables()

    def reset(self):
        cur = self.conn.cursor()
        cur.execute("DROP TABLE IF EXISTS book")
        self.make_tables()
        cur.close()
        self.conn.commit()

    def make_tables(self):

        cmd = '''
            CREATE TABLE IF NOT EXISTS book(
                id serial PRIMARY KEY,
                name TEXT,
                short_name TEXT,
                download_link TEXT,
                year INTEGER,
                semister INTEGER
            );
            '''

        try: 
            cur = self.conn.cursor()
            cur.execute(cmd)
            cur.close()
            self.conn.commit()
        except Exception:
            print('Error while making tables')

    def add_book(self, name, short_name, download_link, year, sem):
        cur = self.conn.cursor()
        cur.execute('''INSERT INTO book(name, short_name, download_link, year, semister) VALUES( %s, %s, %s, %s, %s )
            ''', (name.lower(), short_name.lower(), download_link, year, sem))

        cur.close()
        self.conn.commit()

    def find_book(self, book_name):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM book''')
        
        books = cur.fetchall()
        result = []

        for book in books:
            if match(book[1], book_name) or match(book_name, book[2]):
                result.append(book)

        cur.close()        
        return result

    def find_sem(self, q_year, q_sem):
        cur = self.conn.cursor()
        ret = []
        cur.execute("SELECT * FROM book WHERE year=%s AND semister=%s", (q_year,q_sem))
        books = cur.fetchall()

        for book in books:
            id, name, short_name, link, year, sem = book
            if q_year==year and q_sem==sem:
                ret.append([name,link])

        cur.close()
        return ret


    def del_book(self, id):
        cur = self.conn.cursor()
        cur.execute('''DELETE FROM book WHERE id=%s''',(id,))

        cur.close()
        self.conn.commit()

    def show_all(self):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM book')
        a = cur.fetchall()
        cur.close()
        return a


