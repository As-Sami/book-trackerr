import psycopg2

conn = psycopg2.connect(dbname="postgres" , user="postgres" , password="p@ssword")
cur = conn.cursor()

def reset():
	cur.execute('DROP TABLE book')

	cur.execute('''CREATE TABLE book(
	name TEXT,
	short_name TEXT,
	tel_link TEXT,
	year INTEGER,
	semister INTEGER
	);''')



def cap(s):
	x = s.split()
	s = ''
	for word in x:
		s += word.capitalize() + ' ' 
	return s


def add_book( name, short_name, tel_link, year, sem):
    cur.execute(f"""
    	INSERT INTO book VALUES( %s, %s, %s, %s, %s )
    	""", (name.lower(), short_name.lower(), tel_link, year, sem))

def find_book(book_name):
	cur.execute('''SELECT * FROM book WHERE name=%s OR short_name=%s''', (book_name.lower(),book_name.lower()))
	
	books = cur.fetchall()
	a = ""
	for book in books:
		a += "Book name : " + cap(book[0]) + "\nTelegram Link: " + cap(book[2]) + '\n'

	if a=='':
		return 'Book not found :(\n'
	
	return a 

def show_sem(q_year, q_sem):

    if (q_sem<0 and q_sem>2) or (q_year<0 and q_year>4):
        return 'invalid search'

    yr=''
    sm=''

    if(q_year==1):yr='1st'
    elif(q_year==2):yr='2nd'
    elif(q_year==3):yr='3rd'
    elif(q_year==4):yr='4th'

    if(q_sem==1):sm='1st'
    elif(q_sem==2):sm='2nd'

    ret = ''
    cur.execute("SELECT * FROM book WHERE year=%s AND semister=%s", (q_year,q_sem))
    books = cur.fetchall()

    for book in books:
        name, short_name, link, year, sem = book
        if q_year==year and q_sem==sem:
            ret += f"Book Name : {cap(name)} \nTelegram Link: {link}\n\n"

    if ret=='':
        ret = 'Books not published yet'
    else:
        ret = f"The books for {yr}-year and {sm}-semister\n\n" + ret

    return ret


def del_book(name):
	cur.execute("DELETE FROM book WHERE name=%s OR short_name=%s", (name.lower(),name.lower()))

# reset()

# add_book("Programing with C"               , "C programing", "https://t.me/sustcse2019/7", 1, 1)
# add_book("Discrete Math"                   , "DM"          , "https://t.me/sustcse2019/2", 1, 1)
# add_book("Fundamentals of Eletric Circuits", "EEE-1//1"    , "https://t.me/sustcse2019/3", 1, 1)
# add_book("Matrix"                          , "Marix"       , "https://t.me/sustcse2019/6", 1, 1)
# add_book("Linear Algebra"                  , "LA"          , "https://t.me/sustcse2019/5", 1, 1)


# add_book("Data Structure"                       , "DS"                    , "https://t.me/sustcse2019/9" , 1, 2)
# add_book("Electronic Devices and Circuit Theory", "EEE-1//2"              , "https://t.me/sustcse2019/13", 1, 2)
# add_book("Thomas Calculus"                      , "Calculus"       		, "https://t.me/sustcse2019/10", 1, 2)
# add_book("Das Mukherjee Calculus"               , "Calculus"				, "https://t.me/sustcse2019/11", 1, 2)
# add_book("Fundamentals of Physics"              , "Physics"               , "https://t.me/sustcse2019/14", 1, 2)


cur.execute('''SELECT * FROM book''')
a = cur.fetchall()

for x in a:
	print(x)

print(find_book('C programing'))

del_book('Calculus')
print(show_sem(1,2))



conn.commit()

cur.close()
conn.close()

# from os import environ

# environ['BOT_TOKEN'] = 'BOt token here'
# environ['Some other config VAR'] = 'Its value'

# bot_token = environ.get('BOT_TOKEN') or 'andu'

# print(bot_token)

