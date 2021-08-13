import psycopg2
import discord
from os import environ
from discord.ext.commands import Bot, when_mentioned_or

# CONSTANTS
token = environ.get('BOT_TOKEN')
db_url = environ.get('DATABASE_URL')

SUPER_USERS=[759026765976567810]

bot = Bot(description="Pdf Library", command_prefix=when_mentioned_or(">"), help_command=None )
conn = psycopg2.connect(db_url)
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
    cur.execute("SELECT * FROM book WHERE name=%s OR short_name=%s", (name.lower(),name.lower()))
    if cur.fetchall()==[]:
        return "book not found"
    
    cur.execute("DELETE FROM book WHERE name=%s OR short_name=%s", (name.lower(),name.lower()))
    conn.commit()
    return "book deleted"

#---------------------------------------------------------------------------------------------|

def help_search(s): #---------------------
    disc = '''
The search command searches the book for you.
It takes the name of the book to search. 

`>search book_name`

Example:

```>search dm
>search "Discrete Math"```
    
    '''
    s.add_field(name=disc , value='\nFarewell', inline=False)
    return s

def help_semister(s): #---------------------
    disc = '''
The semister command provides you all the book for the semister.
Your have to tell him which year and which semister's book do you want.

`>semister year semister`

Example:

```>semister 1 2
>semister 2 1```
    '''
    s.add_field(name=disc , value='\nFarewell', inline=False)
    return s

def help_add(s): #---------------------
    disc = '''
The add command is admin only command. This command is for 
adding book in the database.

```>add   book_name     short_name      download_link  year semister```
    
Example:
   
```>addBook "Thomas Calculus" Calculus https://t.me/sustcse2019/10 1 2```

    '''

    s.add_field(name=disc , value='\nFarewell', inline=False)
    return s

def help_delete(s): #---------------------
    disc = '''
The delete command is admin only command. Used for deleting book from
database

`>delete book_name`

Example:

```>delete Matrix```

    '''

    s.add_field(name=disc , value='\nFarewell', inline=False)
    return s

#--------------------------------------------------

@bot.event
async def on_ready():
	print('I am ready')



@bot.command()
async def help(ctx, name=''):
    s = discord.Embed(title='All Command Guide', color=0x008000)
    s.set_author(name="Book-Trackerr\n", icon_url=ctx.me.avatar_url)

    if name=='search':
        s = discord.Embed(title='Search Command Guide', color=0x008000)
        help_search(s)
    elif name=='semister':
        s = discord.Embed(title='Semister Command Guide', color=0x008000)
        help_semister(s)
    elif name=='add':
        s = discord.Embed(title='Add Command Guide', color=0x008000)
        help_add(s)
    elif name=='delete':
        s = discord.Embed(title='Delete Command Guide', color=0x008000)
        help_delete(s)
    else:
        disc = '''
There are 4 basic command 

`search`
`semister`
`add`
`delete`

The last 2 are admin only command. That mean only the admin can use these command.
To know specific command details, type `>help command_name` 
            '''

        s.add_field(name=disc , value='\nFarewell', inline=False)

    await ctx.channel.send(embed=s)


@bot.command()
async def search(ctx, name=''):

    if name=='':
        s = discord.Embed(title='Search Command Guide', color=0x008000)
        s.set_author(name="Book-Trackerr\n", icon_url=ctx.me.avatar_url)
        await ctx.channel.send(embed=help_search(s))
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
        s = discord.Embed(title='Semister Command Guide', color=0x008000)
        s.set_author(name="Book-Trackerr\n", icon_url=ctx.me.avatar_url)
        await ctx.channel.send(embed=help_semister(s))
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

    s = discord.Embed(title=f"\n\nThe books for {yr}-year {sm}-semister\n", color=0x008000)
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

    if name=='' or short_name=='' or tel_link=='' or year==0 or sem==0:
        s = discord.Embed(title='Add Command Guide', color=0x008000)
        s.set_author(name="Book-Trackerr\n", icon_url=ctx.me.avatar_url)
        await ctx.channel.send( embed=help_add(s) )

    elif ctx.author.id in SUPER_USERS:
        add_book(name,short_name,tel_link,year,sem)
        await ctx.channel.send('Book added')
    else:
        await ctx.channel.send('This command is for admin only')

@bot.command()
async def delete(ctx, name=''):

    if name=='':
        s = discord.Embed(title='Delete Command Guide', color=0x008000)
        s.set_author(name="Book-Trackerr\n", icon_url=ctx.me.avatar_url)
        await ctx.channel.send(embed=help_delete(s))

    elif ctx.author.id in SUPER_USERS:
        await ctx.channel.send(del_book(name))

    else:
        await ctx.channel.send('This command is for admin only')

conn.commit()

bot.run(token)
