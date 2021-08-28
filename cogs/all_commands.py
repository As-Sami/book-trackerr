import discord
import asyncio
from discord.ext import commands
from data import dbconn

RESPOND_TIME = 30
SUPER_USERS = list( map(int , environ.get('SUPER_USERS').split(',')) )

async def get_info(bot, ctx, msz, time):
	await ctx.send(msz)

	def check(msz):
		return msz.author == ctx.message.author

	try: 
		msz = await bot.wait_for('message', check=check, timeout=time)
		return msz.content
	except asyncio.TimeoutError:
		return ''

def cap(s):
    x = s.split()
    s = ''
    for word in x:
        s += word.capitalize() + ' ' 
    return s


def get_help(s):
	if s=='help':
		return '''
Hello, I am Book Tracker.
I track your books and arrange it for you.

Here is all the basic commands.
```>search
>library
>add
>delete```
Type `>help <command name>` to know more specificly about the command.
		'''
	elif s=='search':
		return '''
The search command searches the book for you. It takes the name of the book to search.
Example : 

`>search dm`
`>search discrete math`
		'''
	elif s=='library':
		return '''
Library command provides you the books of specific semester.
>library year semester

Example:

```>library 1 2
>library 2 1```

		'''
	elif s=='add':
		return '''
The add command is admin only command. This command is for 
adding book in the database.
Type `>add <book name>` and it will ask some more info(aliases, download link, year, semester) from you and then it will add the book to database.

		'''
	elif s=='delete':
		return '''
The delete command is admin only command. Used for deleting book from
database

Type `>delete book_name` and it will ask you to confirm the book deletion.
		'''


class Cmds(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.db = dbconn.DbConn()

	@commands.command()
	async def help(self, ctx):
		s = discord.Embed(description='', color=0x008000)
		name = str(ctx.message.content.strip()[5:]).strip()

		if name=='':
			s.set_author(name="Book-TrackeR", icon_url=ctx.me.avatar_url)
			s.add_field(name=get_help('help'), value=':grin:', inline=False)

		elif name=='search':
			s.set_author(name="Search Command Guide", icon_url=ctx.me.avatar_url)
			s.add_field(name=get_help('search'), value=':grin:', inline=False)
		elif name=='library':
			s.set_author(name="Library Command Guide", icon_url=ctx.me.avatar_url)
			s.add_field(name=get_help('library'), value=':grin:', inline=False)
		elif name=='add':
			s.set_author(name="Add Command Guide", icon_url=ctx.me.avatar_url)
			s.add_field(name=get_help('add'), value=':grin:', inline=False)
		elif name=='delete':
			s.set_author(name="Delete Command Guide", icon_url=ctx.me.avatar_url)
			s.add_field(name=get_help('delete'), value=':grin:', inline=False)

		await ctx.send(embed=s)


	@commands.command()
	async def search(self, ctx):
		s = discord.Embed(description='', color=0x008000)
		name = str(ctx.message.content.strip()[7:]).strip()

		if name=='':
			s.set_author(name="Search Command Guide", icon_url=ctx.me.avatar_url)
			s.add_field(name=get_help('search'), value=':grin:', inline=False)

			await ctx.channel.send(embed=s)
			return

		s.set_author(name="Your searched results ", icon_url=ctx.me.avatar_url)

		info = self.db.find_book(name)

		if(info==[]):
			s.add_field(name="Sorry..... I couldn't find the book", value=':worried:', inline=False)

		for id, name, short_name, link, year, sem in info:
			s.add_field(name = f'{cap(name)} - {year}/{sem}', value = f"[Download]({link})", inline=False)

		await ctx.send(embed=s)

	@commands.command()
	async def library(self, ctx, year=None, sem=None):
		
		if year==None and sem==None:
		    s = discord.Embed(description='', color=0x008000)
		    s.set_author(name="Library Command Guide", icon_url=ctx.me.avatar_url)
		    s.add_field(name=get_help('library'), value=':grin:', inline=False)

		    await ctx.channel.send(embed=s)
		    return
		
		if year==None or sem==None:
			await ctx.channel.send("You must provide year and semester")
			return


		try:
			y = int(year)
			if y<1 and y>4:
				await ctx.send("Year should be between 1-4")
				return
		except:
			await ctx.send("Year should be a number")
			return


		try:
			sm = int(sem)
			if sm<1 and sm>4:
				await ctx.send("Semester should be between 1-4")
				return
		except:
			await ctx.send("Semester should be a number")
			return


		info = self.db.find_sem(int(year),int(sem))

		yr=''
		if(year=='1'):yr='1st'
		elif(year=='2'):yr='2nd'
		elif(year=='3'):yr='3rd'
		elif(year=='4'):yr='4th'

		sm=''
		if(sem=='1'):sm='1st'
		elif(sem=='2'):sm='2nd'

		s = discord.Embed(description=f"", color=0x008000)
		s.set_author(name=f"The books for {yr}-year {sm}-library", icon_url=ctx.me.avatar_url)

		if(info==[]):
		    s.set_author(name='Books not published yet.....', icon_url=ctx.me.avatar_url)
		    s.add_field(name="Sorry.........", value=':confused:', inline=False)
		else:
		    for book_name, link in info:
		        s.add_field(name=f"{cap(book_name)}", value=f"[Download Link]({link})",inline=False)

		await ctx.channel.send(embed=s)


	@commands.command()
	async def add(self, ctx):

		book_name = str(ctx.message.content.strip()[4:]).strip()

		if(book_name==''):
			s = discord.Embed(description='', color=0x008000)
			s.set_author(name="Add Command Guide", icon_url=ctx.me.avatar_url)
			s.add_field(name=get_help('add'), value=':grin:', inline=False)
			await ctx.channel.send(embed=s)
			return

		if not (ctx.author.id in SUPER_USERS):
			await ctx.channel.send('This command is for admin only')
			return

		aliases = await get_info(self.client, ctx,"Enter aliace name for this book including commas(,) ", RESPOND_TIME)
		if aliases=='':
			await ctx.send("You didn't respond in time.... Operation stopped")
			return

		download_link = await get_info(self.client, ctx,"Enter download link ", RESPOND_TIME)
		if download_link=='':
			await ctx.send("You didn't respond in time.... Operation stopped")
			return
		

		year_n_sem = await get_info(self.client, ctx,"Enter year and semester ", RESPOND_TIME)
		if year_n_sem=='':
			await ctx.send("You didn't respond in time.... Operation stopped")
			return

		try:
			year , sem = year_n_sem.split()
		except:
			await ctx.send("Invalid input.... Operation stopped")
			return			

		try:
			y = int(year)
			if y<1 or y>4:
				await ctx.send("Year should be between 1-4.... Operation stopped")
				return
		except:
			await ctx.send("Year should be a number.... Operation stopped")
			return

		try:
			sm = int(sem)
			if sm<1 or sm>4:
				await ctx.send("library should be between 1-4.... Operation stopped")
				return
		except:
			await ctx.send("library should be a number.... Operation stopped")
			return


		self.db.add_book(book_name, aliases, download_link, year, sem)
		await ctx.send('Book added')


	@commands.command()
	async def delete(self, ctx):
		name = str(ctx.message.content.strip()[7:]).strip()
		if name=='':
			s = discord.Embed(description='', color=0x008000)
			s.set_author(name="Delete Command Guide", icon_url=ctx.me.avatar_url)
			s.add_field(name=get_help('delete'), value=':grin:', inline=False)

			await ctx.channel.send(embed=s)
			return			


		if not (ctx.author.id in SUPER_USERS):
			await ctx.channel.send('This command is for admin only')
			return

		s = discord.Embed(description=f"", color=0x008000)
		s.set_author(name='Found these following books', icon_url=ctx.me.avatar_url)
		
		books = self.db.find_book(name)
		if not books:
			s.set_author(name='Book was not found', icon_url=ctx.me.avatar_url)
			await ctx.send(embed=s)
			return
		
		ids=[]
		cnt = 0
		for id, name, name1, link, year, sem in books:
			s.add_field(name=f'{cnt+1}. {cap(name)} - {year}/{sem}', value=f"[Download]({link})" , inline=False)
			ids.append(id)
			cnt+=1
		await ctx.send(embed=s)

		num = await get_info(self.client, ctx, 'Which book do you want to delete??? Enter the serial number' , RESPOND_TIME)
		if num=='':
			await ctx.send("You didn't respond in time.... Deletion stopped")
			return

		try:
			id = int(num)-1
		except:
			await ctx.send('You should response with numbers.....Deletion stopped')
			return

		respond = await get_info(self.client, ctx, f'Are you sure you want to delete `{books[id][1]}`??[YES or NO]' , RESPOND_TIME)
		if respond=='':
			await ctx.send("You didn't respond in time.... Deletion stopped")
			return

		if respond.lower()=='yes' or respond.lower()=='yeah':
			self.db.del_book(books[id][0])
			await ctx.send('Book deleted')
		else:
			await ctx.send("Deletion stopped")

	@commands.command()
	async def addf(self, ctx, name, aliases, link, year, sem):
		if not (ctx.author.id in SUPER_USERS):
			await ctx.channel.send('This command is for admin only')
			return
			
		self.db.add_book(name, aliases, download_link, year, sem)
		await ctx.send('Book added')


def setup(client):
	client.add_cog(Cmds(client))