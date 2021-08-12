import psycopg2
import discord
from discord.ext.commands import Bot, when_mentioned_or



bot = Bot(description="Pdf Library", command_prefix=when_mentioned_or(">"), help_command=None )
conn = psycopg2.connect(dbname="postgres" , user="postgres" , password="p@ssword")
cur = conn.cursor()

#---------------------------------------------------------------------------------------------|

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

    conn.commit()


def find_book(book_name):
    cur.execute('''SELECT * FROM book WHERE name=%s OR short_name=%s''', (book_name.lower(),book_name.lower()))
    
    books = cur.fetchall()
    a = []
    for book in books:
        a.append( [cap(book[0]) , book[2]] )
    
    return a 

def find_sem(q_year, q_sem):

    ret = []
    cur.execute("SELECT * FROM book WHERE year=%s AND semister=%s", (q_year,q_sem))
    books = cur.fetchall()

    for book in books:
        name, short_name, link, year, sem = book
        if q_year==year and q_sem==sem:
            ret.append([cap(name),link])

    # ret = f"The books for {yr}-year and {sm}-semister\n\n" + ret

    return ret


def del_book(name):
    cur.execute("SELECT FROM book WHERE name=%s OR short_name=%s", (name.lower(),name.lower()))
    if cur.fetchall()=='':
        return "book not found"
    cur.execute("DELETE FROM book WHERE name=%s OR short_name=%s", (name.lower(),name.lower()))
    conn.commit()
    return "book deleted"

#---------------------------------------------------------------------------------------------|

@bot.event
async def on_ready():
	print('I am ready')



@bot.command()
async def help(ctx, name=''):
    if name=='':
        await ctx.channel.send('''```
    Hello I'm Book Tracker. 
    I track book for u ^_^.

    Here are the command Lists

    >search  
    >semister
    >add
    >delete

    The search command command search the book for you. 
    Syntax : >search book_name
    
        >search DS
        >search Ds
        >search "Data Structure"

    The semister command provides you all the book for the semister.
    Syntax : >semister year semister

        >semister 1 2
        >semister 2 1

    The add command is admin only command.
    Syntax : >add book_name short_name telegram_link year semister

        >addBook "Thomas Calculus" Calculus https://t.me/sustcse2019/10 1 2

    The delete command is also admin only command.
    Syntax : >delete book_name

        >delete Matrix

    Enjoy....................................
        ```''')


@bot.command()
async def search(ctx, name=''):

    if name=='':
        await ctx.channel.send('Help msz for search command')
        return

    s = discord.Embed(description='', color=0x008000)
    s.set_author(name="Book-Trackerr\n", icon_url=ctx.me.avatar_url)

    info = find_book(name)

    if(info==[]):
        s.add_field(name="Sorry,,,, I couldn't find the book", value=':worried:', inline=False)

    for book_name, link in info:
        s.add_field(name=f"\n\nBook name : {book_name}", value=f"[Download Link]({link})\n",
                            inline=False)

    await ctx.channel.send(embed=s)

@bot.command()
async def semister(ctx, year='0', sem='0'):
    if year=='0' or (year<'0' or year>'4') or(sem<'0' or sem>'2'):
        await ctx.channel.send('wrong search')
        return

    info = find_sem(int(year),int(sem))

    yr=''

    if(year=='1'):yr='1st'
    elif(year=='2'):yr='2nd'
    elif(year=='3'):yr='3rd'
    elif(year=='4'):yr='4th'

    sm=''
    if(sem=='1'):sm='1st'
    elif(sem=='2'):sm='2nd'

    s = discord.Embed(description=f"\n\n```The books for {yr}-year {sm}-semister```\n", color=0x008000)
    s.set_author(name="Book-Trackerr\n", icon_url=ctx.me.avatar_url)

    if(info==[]):
        s.description = 'Books not published yet.....'
        s.add_field(name="----------", value=':confused:', inline=False)
    else:
        for book_name, link in info:
            s.add_field(name=f"\n\n{book_name}", value=f"[Download Link]({link})\n",
                        inline=False)

    await ctx.channel.send(embed=s)



@bot.command()
async def add(ctx, name='',short_name='', tel_link='', year=0,sem=0):
	if name==''or short_name==''or  tel_link=='' or  year==0 or sem==0:
		await ctx.channel.send('insufficient information')
	elif ctx.author.id == 759026765976567810:
		add_book(name,short_name,tel_link,year,sem)
		await ctx.channel.send('Book added')
	else:
		await ctx.channel.send('This command is for admin only')

@bot.command()
async def delete(ctx, name=''):
	if name=='':
		await ctx.channel.send('insufficient information')
	elif ctx.author.id == 759026765976567810:
		await ctx.channel.send(del_book(name))

	else:
		await ctx.channel.send('This command is for admin only')

conn.commit()

bot.run('ODM1OTQyNjY5MzkzMDY4MDMy.YIWyRw.gnGP2BCfJ9xjUJ-iPXw6IVyNJ8A')
