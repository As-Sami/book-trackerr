import discord
from discord.ext.commands import Bot, when_mentioned_or


bot = Bot(description="Pdf Library", command_prefix=when_mentioned_or(">"))

#---------------------------------------------------------------------------------------------|

def add_book( name, short_name, tel_link, year, sem):
    f = open("book.txt", "a")
    f.write( name + '|' + short_name + '|' + tel_link + '|' + str(year) + '|' + str(sem) )
    f.write('\n')
    f.close()

def find_book(book_name):
    f = open('book.txt')
    books = f.read().split('\n')
    books.pop()

    for book in books:
        name, short_name, link, year, sem= book.split('|')
        if(name.lower()==book_name.lower() or book_name.lower()==short_name.lower()):
            return f"Book Name : {name} \nTelegram Link: {link}\n"

    f.close()
    return 'Book not found'

def find_sem(q_year, q_sem):

    if (int(q_sem)<0 and int(q_sem)>2) or (int(q_year)<0 and int(q_year)>4):
        return 'invalid search'

    f = open('book.txt')
    books = f.read().split('\n')
    books.pop()

    yr=''
    sm=''

    if(q_year=='1'):yr='1st'
    elif(q_year=='2'):yr='2nd'
    elif(q_year=='3'):yr='3rd'
    elif(q_year=='4'):yr='4th'

    if(q_sem=='1'):sm='1st'
    elif(q_sem=='2'):sm='2nd'

    ret = ''
    for book in books:
        name, short_name, link, year, sem= book.split('|')
        if q_year==year and q_sem==sem:
            ret += f"Book Name : {name} \nTelegram Link: {link}\n\n"

    if ret=='':
        ret = 'Books not published yet'
    else:
        ret = f"The books for {yr}-year and {sm}-semister\n\n" + ret

    f.close()
    return ret


def del_book(book_name):
    f = open('book.txt')
    books = f.read().split('\n')
    books.pop()
    f.close()

    i = 0
    for book in books:
        name, short_name, link, year, sem= book.split('|')
        if(name.lower()==book_name.lower() or book_name.lower()==short_name.lower()):
            books.pop(i)
            break
        i+=1    

    f = open('book.txt','w')
    for book in books:
        f.write(book+'\n')
    
    return 'Work done'

#---------------------------------------------------------------------------------------------|

@bot.event
async def on_ready():
	print('I am ready')


@bot.command()
async def show_book(ctx, name=''):
	if name=='':
		await ctx.channel.send('wrong number')
	else:
		info = find_book(name)
		await ctx.channel.send(f"{info}")

@bot.command()
async def show_sem(ctx, year='0', sem='0'):
	if year==0:
		await ctx.channel.send('wrong number')
	else:
		info = find_sem(str(year),str(sem))
		await ctx.channel.send(f"```\n{info}\n```")


@bot.command()
async def addBook(ctx, name='',short_name='', tel_link='', year=0,sem=0):
	if name==''or short_name==''or  tel_link=='' or  year==0 or sem==0:
		await ctx.channel.send('insufficient information')
	elif ctx.author.id == 759026765976567810:
		add_book(name,short_name,tel_link,year,sem)
		await ctx.channel.send('Book added')
	else:
		await ctx.channel.send('This command is for admin only')

@bot.command()
async def delBook(ctx, name=''):
	if name=='':
		await ctx.channel.send('insufficient information')
	elif ctx.author.id == 759026765976567810:
		await ctx.channel.send(del_book(name))
	else:
		await ctx.channel.send('This command is for admin only')

bot.run('ODM1OTQyNjY5MzkzMDY4MDMy.YIWyRw.tqAsZqR1RetpX12SvNiHqljA22M')
